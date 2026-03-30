"""
Tests for GAIF core library.
Run with: python -m pytest tests/ -v
"""

import sys
import pytest
sys.path.insert(0, "tools")

from gaif_core import (
    classify_tier,
    GovernanceTier,
    compute_gdr,
    compute_composition_safety,
    compute_composition_cost,
    compute_aahi,
    SystemHealth,
    classify_risk_tier,
)


# ---------------------------------------------------------------------------
# Tier Classification Tests
# ---------------------------------------------------------------------------

class TestTierClassification:
    def test_autonomous_always_tier_c(self):
        """A=2 should always produce Tier C regardless of D and T."""
        for d in (0, 1, 2):
            for t in (0, 1, 2):
                assert classify_tier(d, t, 2) == GovernanceTier.TIER_C

    def test_full_control_non_autonomous_tier_a(self):
        """A=0 and D=0 should produce Tier A."""
        for t in (0, 1, 2):
            assert classify_tier(0, t, 0) == GovernanceTier.TIER_A

    def test_transparency_does_not_affect_tier(self):
        """T should not change the tier assignment."""
        for d in (0, 1, 2):
            for a in (0, 1):
                tiers = {classify_tier(d, t, a) for t in (0, 1, 2)}
                assert len(tiers) == 1, f"T affected tier for D={d}, A={a}"

    def test_vendor_api_tier_b(self):
        """D=1, T=1, A=1 (typical vendor API) should be Tier B."""
        assert classify_tier(1, 1, 1) == GovernanceTier.TIER_B

    def test_invalid_values_raise(self):
        """Values outside 0-2 should raise ValueError."""
        with pytest.raises(ValueError):
            classify_tier(3, 0, 0)
        with pytest.raises(ValueError):
            classify_tier(0, -1, 0)

    def test_all_27_combinations(self):
        """All 27 possible D,T,A combinations should produce a valid tier."""
        for d in (0, 1, 2):
            for t in (0, 1, 2):
                for a in (0, 1, 2):
                    result = classify_tier(d, t, a)
                    assert isinstance(result, GovernanceTier)


# ---------------------------------------------------------------------------
# GDR Tests
# ---------------------------------------------------------------------------

class TestGDR:
    def test_healthy_system(self):
        result = compute_gdr("test", 4, 4, "critical")
        assert result.gdr == 1.0
        assert result.status == "healthy"

    def test_stage1_escalation(self):
        result = compute_gdr("test", 6, 2, "critical")
        assert result.gdr == 3.0
        assert result.status == "stage1_escalation"

    def test_stage2_escalation(self):
        result = compute_gdr("test", 18, 2, "high")
        assert result.gdr == 9.0
        assert result.status == "stage2_escalation"

    def test_zero_reviews(self):
        """Zero reviews should not cause division by zero."""
        result = compute_gdr("test", 10, 0, "high")
        assert result.gdr == 10.0

    def test_paper_example_system_a(self):
        """Verify System A from GAIF v1.0 Section 4.5.7 worked example."""
        result = compute_gdr("System A", 6, 4, "critical")
        assert result.gdr == 1.5
        assert result.status == "healthy"

    def test_paper_example_system_b(self):
        """Verify System B from worked example."""
        result = compute_gdr("System B", 18, 2, "high")
        assert result.gdr == 9.0
        assert result.status == "stage2_escalation"


# ---------------------------------------------------------------------------
# Composition Safety Tests
# ---------------------------------------------------------------------------

class TestCompositionSafety:
    def test_independent_mode(self):
        result = compute_composition_safety(0.90, 0.95, "independent")
        assert result.max_hops == 2  # log(0.90)/log(0.95) = 2.05

    def test_amplified_mode(self):
        result = compute_composition_safety(0.90, 0.97, "amplified", alpha=0.2)
        assert result.max_hops == 0  # s_eff = 0.776, n_max = 0.41

    def test_paper_healthcare_example(self):
        """Verify n_max from GAIF v1.0 Section 6.2."""
        result = compute_composition_safety(0.90, 0.97, "independent")
        assert abs(result.n_max - 3.46) < 0.1

    def test_safety_degrades_with_hops(self):
        r1 = compute_composition_safety(0.90, 0.95, "independent", num_components=2)
        r2 = compute_composition_safety(0.90, 0.95, "independent", num_components=5)
        assert r2.end_to_end_safety < r1.end_to_end_safety


# ---------------------------------------------------------------------------
# Composition Cost Tests
# ---------------------------------------------------------------------------

class TestCompositionCost:
    def test_basic_cost(self):
        result = compute_composition_cost(0.50, 0.10, 0.05)
        assert result.max_hops == 4  # (0.50 - 0.05) / 0.10 = 4.5

    def test_with_amplification(self):
        result = compute_composition_cost(0.50, 0.10, 0.05, beta=1.3)
        assert result.max_hops == 3  # (0.50 - 0.05) / 0.13 = 3.46


# ---------------------------------------------------------------------------
# AAHI Tests
# ---------------------------------------------------------------------------

class TestAAHI:
    def test_healthy_system(self):
        systems = [SystemHealth("test", GovernanceTier.TIER_A, 1.0)]
        result = compute_aahi(systems)
        assert result.zone == "green"

    def test_floor_constraint(self):
        """Critical system with dimension below 0.3 should cap AAHI at Yellow."""
        systems = [
            SystemHealth("critical", GovernanceTier.TIER_A, 3.0,
                         h_gov=0.2, h_behav=1.0, h_supply=1.0, h_cost=1.0),
        ]
        result = compute_aahi(systems)
        assert result.floor_triggered
        assert result.aahi <= 0.79

    def test_paper_worked_example(self):
        """Verify AAHI from GAIF v1.0 Section 6.7 worked example."""
        systems = [
            SystemHealth("S1", GovernanceTier.TIER_A, 3.0,
                         h_gov=0.90, h_behav=0.85, h_supply=1.0, h_cost=0.95),
            SystemHealth("S2", GovernanceTier.TIER_B, 2.0,
                         h_gov=0.40, h_behav=0.60, h_supply=0.50, h_cost=0.80),
            SystemHealth("S3", GovernanceTier.TIER_C, 1.5,
                         h_gov=0.85, h_behav=0.90, h_comp=0.75, h_trust=1.0,
                         h_supply=0.80, h_cost=0.70),
        ]
        result = compute_aahi(systems)
        assert result.zone == "yellow"
        assert abs(result.aahi - 0.786) < 0.01


# ---------------------------------------------------------------------------
# Risk Tier Tests
# ---------------------------------------------------------------------------

class TestRiskTier:
    def test_critical(self):
        assert classify_risk_tier(85)["tier"] == "critical"

    def test_high(self):
        assert classify_risk_tier(65)["tier"] == "high"

    def test_medium(self):
        assert classify_risk_tier(50)["tier"] == "medium"

    def test_low(self):
        assert classify_risk_tier(20)["tier"] == "low"
