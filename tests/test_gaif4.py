"""
GAIF-4 Calculator Tests

Every test case is traceable to a specific section or formula in the
GAIF-4 Working Specification v1.5.
"""

import pytest
from gaif4.calculator import (
    normalize_emr,
    normalize_t1pr,
    normalize_cfr,
    normalize_gdr,
    classify_dimension,
    compute_grade,
    assess,
    EMR_PASS,
    EMR_FAIL,
    T1PR_PASS,
    T1PR_FAIL,
    CFR_PASS,
    CFR_FAIL,
    GDR_PASS,
)


# -----------------------------------------------------------------------
# Section 4.2: FAIL Boundary Alignment Verification
# "All four FAIL boundaries produce the same normalized value [0.50]"
# -----------------------------------------------------------------------

class TestFailBoundaryAlignment:
    """GAIF-4 v1.5, Section 4.2: FAIL Boundary Alignment Verification."""

    def test_emr_fail_at_050(self):
        assert normalize_emr(0.25) == pytest.approx(0.50)

    def test_t1pr_fail_at_050(self):
        assert normalize_t1pr(0.30) == pytest.approx(0.50)

    def test_cfr_fail_at_050(self):
        assert normalize_cfr(0.85) == pytest.approx(0.50)

    def test_gdr_fail_at_050_high(self):
        # High coverage target = 4.0
        assert normalize_gdr(4.0, 4.0) == pytest.approx(0.50)

    def test_gdr_fail_at_050_critical(self):
        # Critical coverage target = 2.0
        assert normalize_gdr(2.0, 2.0) == pytest.approx(0.50)

    def test_gdr_fail_at_050_medium(self):
        assert normalize_gdr(8.0, 8.0) == pytest.approx(0.50)

    def test_gdr_fail_at_050_low(self):
        assert normalize_gdr(12.0, 12.0) == pytest.approx(0.50)


# -----------------------------------------------------------------------
# Section 4.2: EMR Normalization
# -----------------------------------------------------------------------

class TestEMRNormalization:
    """GAIF-4 v1.5, Section 4.2: ES_score = max(0, 1.0 - EMR/0.50)."""

    def test_zero_emergence(self):
        assert normalize_emr(0.00) == pytest.approx(1.0)

    def test_pass_threshold(self):
        # EMR = 0.10 (PASS boundary)
        assert normalize_emr(0.10) == pytest.approx(0.80)

    def test_fail_threshold(self):
        assert normalize_emr(0.25) == pytest.approx(0.50)

    def test_ceiling(self):
        assert normalize_emr(0.50) == pytest.approx(0.0)

    def test_above_ceiling_clamps(self):
        assert normalize_emr(0.80) == pytest.approx(0.0)

    def test_worked_example(self):
        # Section 4.4: EMR = 0.08 -> ES_score = 0.84
        assert normalize_emr(0.08) == pytest.approx(0.84)

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            normalize_emr(-0.01)


# -----------------------------------------------------------------------
# Section 4.2: T1PR Normalization
# -----------------------------------------------------------------------

class TestT1PRNormalization:
    """GAIF-4 v1.5, Section 4.2: CR_score = max(0, 1.0 - T1PR/0.60)."""

    def test_zero_contamination(self):
        assert normalize_t1pr(0.00) == pytest.approx(1.0)

    def test_pass_threshold(self):
        # T1PR = 0.10 -> 0.833
        assert normalize_t1pr(0.10) == pytest.approx(0.8333, rel=1e-3)

    def test_fail_threshold(self):
        assert normalize_t1pr(0.30) == pytest.approx(0.50)

    def test_ceiling(self):
        assert normalize_t1pr(0.60) == pytest.approx(0.0)

    def test_above_ceiling_clamps(self):
        assert normalize_t1pr(0.96) == pytest.approx(0.0)

    def test_worked_example(self):
        # Section 4.4: T1PR = 0.24 -> CR_score = 0.60
        assert normalize_t1pr(0.24) == pytest.approx(0.60)


# -----------------------------------------------------------------------
# Section 4.2: CFR Normalization
# -----------------------------------------------------------------------

class TestCFRNormalization:
    """GAIF-4 v1.5, Section 4.2: CF_score = max(0, (CFR-0.70)/0.30)."""

    def test_perfect_compliance(self):
        assert normalize_cfr(1.00) == pytest.approx(1.0)

    def test_pass_threshold(self):
        # CFR = 0.95 -> 0.833
        assert normalize_cfr(0.95) == pytest.approx(0.8333, rel=1e-3)

    def test_fail_threshold(self):
        assert normalize_cfr(0.85) == pytest.approx(0.50)

    def test_floor(self):
        assert normalize_cfr(0.70) == pytest.approx(0.0)

    def test_below_floor_clamps(self):
        assert normalize_cfr(0.50) == pytest.approx(0.0)

    def test_worked_example(self):
        # Section 4.4: CFR = 0.97 -> CF_score = 0.90
        assert normalize_cfr(0.97) == pytest.approx(0.90)

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError):
            normalize_cfr(1.01)


# -----------------------------------------------------------------------
# Section 4.2: GDR Normalization
# -----------------------------------------------------------------------

class TestGDRNormalization:
    """GAIF-4 v1.5, Section 4.2: Adapted h_gov with FAIL at 0.50."""

    def test_fully_governed(self):
        assert normalize_gdr(1.0, 4.0) == pytest.approx(1.0)

    def test_below_fully_governed(self):
        assert normalize_gdr(0.5, 4.0) == pytest.approx(1.0)

    def test_worked_example(self):
        # Section 4.2: GDR=2.5, target=4.0 -> GC_score = 0.75
        assert normalize_gdr(2.5, 4.0) == pytest.approx(0.75)

    def test_fail_boundary(self):
        assert normalize_gdr(4.0, 4.0) == pytest.approx(0.50)

    def test_zero_point(self):
        # Zero at 2*target - 1 = 7.0 for target=4.0
        assert normalize_gdr(7.0, 4.0) == pytest.approx(0.0)

    def test_above_zero_clamps(self):
        assert normalize_gdr(10.0, 4.0) == pytest.approx(0.0)

    def test_critical_target(self):
        # Critical target = 2.0, zero at 2*2-1 = 3.0
        assert normalize_gdr(2.0, 2.0) == pytest.approx(0.50)
        assert normalize_gdr(3.0, 2.0) == pytest.approx(0.0)

    def test_h_gov_paper_difference(self):
        # GDR paper: h_gov(2.5, target=4.0) = 0.50
        # GAIF-4:   GC_score(2.5, target=4.0) = 0.75
        # This test documents the intentional adaptation.
        gc_score = normalize_gdr(2.5, 4.0)
        h_gov_paper = 1.0 - ((2.5 - 1.0) / (4.0 - 1.0))  # = 0.50
        assert gc_score == pytest.approx(0.75)
        assert h_gov_paper == pytest.approx(0.50)
        assert gc_score != h_gov_paper  # intentional difference


# -----------------------------------------------------------------------
# Section 4.3: Grade Classification
# -----------------------------------------------------------------------

class TestGradeClassification:

    def test_grade_a(self):
        assert compute_grade(["PASS", "PASS", "PASS", "PASS"]) == "A"

    def test_grade_b(self):
        assert compute_grade(["PASS", "WARN", "PASS", "PASS"]) == "B"

    def test_grade_c(self):
        assert compute_grade(["PASS", "WARN", "WARN", "PASS"]) == "C"

    def test_grade_d(self):
        assert compute_grade(["PASS", "FAIL", "PASS", "PASS"]) == "D"

    def test_grade_f(self):
        assert compute_grade(["FAIL", "FAIL", "PASS", "PASS"]) == "F"

    def test_grade_f_three_fail(self):
        assert compute_grade(["FAIL", "FAIL", "FAIL", "PASS"]) == "F"

    def test_fail_overrides_warn(self):
        assert compute_grade(["WARN", "FAIL", "WARN", "PASS"]) == "D"

    def test_two_fail_overrides_warn(self):
        assert compute_grade(["WARN", "FAIL", "FAIL", "WARN"]) == "F"


# -----------------------------------------------------------------------
# Section 4.4: Worked Example (complete end-to-end)
# -----------------------------------------------------------------------

class TestWorkedExample:
    """GAIF-4 v1.5, Section 4.4: Complete worked example."""

    def test_worked_example_full(self):
        sc = assess(
            emr_interaction=0.08,
            t1pr=0.24,
            cfr=0.97,
            gdr=2.5,
            gdr_risk_level="high",
        )

        # Normalized scores
        assert sc.emr.normalized_score == pytest.approx(0.84)
        assert sc.t1pr.normalized_score == pytest.approx(0.60)
        assert sc.cfr.normalized_score == pytest.approx(0.90)
        assert sc.gdr.normalized_score == pytest.approx(0.75)

        # Statuses
        assert sc.emr.status == "PASS"
        assert sc.t1pr.status == "WARN"
        assert sc.cfr.status == "PASS"
        assert sc.gdr.status == "WARN"

        # Composite and grade
        assert sc.composite == pytest.approx(0.60)
        assert sc.grade == "C"


# -----------------------------------------------------------------------
# Dimension classification edge cases
# -----------------------------------------------------------------------

class TestDimensionClassification:

    def test_emr_boundary_pass(self):
        assert classify_dimension("emr", 0.099) == "PASS"

    def test_emr_boundary_warn(self):
        assert classify_dimension("emr", 0.10) == "WARN"

    def test_emr_boundary_fail(self):
        assert classify_dimension("emr", 0.251) == "FAIL"

    def test_cfr_boundary_pass(self):
        assert classify_dimension("cfr", 0.951) == "PASS"

    def test_cfr_boundary_warn(self):
        assert classify_dimension("cfr", 0.95) == "WARN"

    def test_cfr_boundary_fail(self):
        assert classify_dimension("cfr", 0.849) == "FAIL"

    def test_gdr_pass(self):
        assert classify_dimension("gdr", 1.0, 4.0) == "PASS"

    def test_gdr_warn(self):
        assert classify_dimension("gdr", 3.9, 4.0) == "WARN"

    def test_gdr_fail(self):
        assert classify_dimension("gdr", 4.0, 4.0) == "FAIL"

    def test_gdr_missing_target_raises(self):
        with pytest.raises(ValueError):
            classify_dimension("gdr", 2.0)


# -----------------------------------------------------------------------
# Scenario tests: real-world pipeline configurations
# -----------------------------------------------------------------------

class TestScenarios:

    def test_catastrophic_pipeline(self):
        """Pipeline with multiple failures."""
        sc = assess(emr_interaction=0.40, t1pr=0.50, cfr=0.80, gdr=6.0)
        assert sc.grade == "F"
        assert sc.composite < 0.50

    def test_near_perfect_pipeline(self):
        """Pipeline that passes everything."""
        sc = assess(emr_interaction=0.02, t1pr=0.05, cfr=0.99, gdr=0.5)
        assert sc.grade == "A"
        assert sc.composite > 0.80

    def test_single_fail_is_grade_d(self):
        """One failing dimension produces Grade D."""
        sc = assess(emr_interaction=0.30, t1pr=0.05, cfr=0.99, gdr=0.5)
        assert sc.grade == "D"
        assert sc.emr.status == "FAIL"

    def test_composite_below_050_means_fail(self):
        """Composite < 0.50 guarantees at least one FAIL."""
        sc = assess(emr_interaction=0.30, t1pr=0.05, cfr=0.99, gdr=0.5)
        assert sc.composite < 0.50
        fail_count = sum(
            1 for d in sc.dimensions if d.status == "FAIL"
        )
        assert fail_count >= 1


# -----------------------------------------------------------------------
# Report generation (smoke test)
# -----------------------------------------------------------------------

class TestReport:

    def test_report_generates(self):
        from gaif4.report import generate_markdown
        sc = assess(emr_interaction=0.08, t1pr=0.24, cfr=0.97, gdr=2.5)
        report = generate_markdown(sc)
        assert "GAIF-4 Safety Assessment Scorecard" in report
        assert "Grade: C" in report
        assert "0.60" in report
        assert "WARN" in report
