"""
GAIF Core Library
=================
Implements the formal definitions from the GAIF v1.0 specification.

Reference: Sharma, A. (2026). GAIF: Governed AI Architecture Framework v1.0.
Zenodo. https://doi.org/10.5281/zenodo.19341015
"""

import json
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Governance Tier Classification (Section 5.1.1)
# ---------------------------------------------------------------------------

class GovernanceTier(Enum):
    TIER_A = "Tier A: Governed AI Platform"
    TIER_B = "Tier B: Managed SaaS AI"
    TIER_C = "Tier C: Agent Platform"


class DataControl(Enum):
    """D attribute: level of organizational control over data."""
    FULL = 0           # Full control over training and inference data
    THIRD_PARTY = 1    # Data passes through third-party with contractual controls
    VARIABLE = 2       # Variable access across multiple sources with mixed control


class ModelTransparency(Enum):
    """T attribute: visibility into model internals."""
    FULL = 0       # Full visibility into architecture, weights, training
    API_ONLY = 1   # API-level observation only with vendor documentation
    PARTIAL = 2    # Agent logic visible but underlying model behavior opaque


class AutonomyLevel(Enum):
    """A attribute: degree of autonomous operation."""
    INVOKED = 0       # Produces outputs only when explicitly invoked
    VENDOR_API = 1    # Invoked through vendor API with predefined behavior
    AUTONOMOUS = 2    # Autonomously plans, executes multi-step workflows


def classify_tier(data_control: int, transparency: int, autonomy: int) -> GovernanceTier:
    """
    Formal tier classification function f(D, T, A) from Section 5.1.1.

    Rules:
        - Tier C if A = 2 (autonomous agents always require Tier C)
        - Tier A if A = 0 AND D = 0 (non-autonomous + full data control)
        - Tier B otherwise

    Note: T does not directly affect tier assignment by design.
    T determines governance intensity within the assigned tier,
    not the tier itself. Lower T increases Model Risk scores
    (questions M3, M4 in the risk assessment), which raises
    governance intensity.

    Args:
        data_control: D in {0, 1, 2}
        transparency: T in {0, 1, 2}
        autonomy: A in {0, 1, 2}

    Returns:
        GovernanceTier classification
    """
    if not all(v in (0, 1, 2) for v in (data_control, transparency, autonomy)):
        raise ValueError("All attributes must be 0, 1, or 2")

    if autonomy == 2:
        return GovernanceTier.TIER_C
    elif autonomy == 0 and data_control == 0:
        return GovernanceTier.TIER_A
    else:
        return GovernanceTier.TIER_B


TIER_GOVERNANCE_REQUIREMENTS = {
    GovernanceTier.TIER_A: {
        "description": "Governed AI Platform",
        "governance_approach": "Direct governance through model registry, CI/CD gates, internal review boards",
        "requirements": [
            "Model registry with mandatory metadata before production deployment",
            "Automated CI/CD pipeline with safety validation gates",
            "Data provenance tracking from source through training to inference",
            "Model performance monitoring with automated drift detection",
            "Retraining pipeline with defined triggers",
            "Model retirement workflow with dependency analysis",
            "Full AI-BOM generated from internal pipelines",
        ],
        "primary_risks": [
            "Training data quality",
            "Model drift",
            "Overfitting",
            "Internal misuse",
        ],
    },
    GovernanceTier.TIER_B: {
        "description": "Managed SaaS AI",
        "governance_approach": "Contractual governance through vendor agreements, SLAs, API usage policies",
        "requirements": [
            "API gateway with compliance-aware routing",
            "Input/output logging for all vendor API calls",
            "Vendor model behavior monitoring for silent updates",
            "Fallback architecture for vendor API failures",
            "Contractual governance register",
            "Cost monitoring and budget controls at API call level",
            "Vendor-attested AI-BOM through contractual governance",
        ],
        "primary_risks": [
            "Vendor lock-in",
            "Data leakage",
            "API behavior changes",
            "Compliance gaps in vendor policies",
        ],
    },
    GovernanceTier.TIER_C: {
        "description": "Agent Platform",
        "governance_approach": "Compositional governance through agent-level safety constraints, tool permissions, human oversight",
        "requirements": [
            "Agent permission model following least privilege",
            "Human-in-the-loop checkpoints at defined decision points",
            "Inter-agent communication monitoring",
            "Agent execution trace logging",
            "Safety constraint enforcement layer",
            "Circuit breaker patterns for anomalous behavior",
            "Trust Inheritance Protocol enforcement",
            "Composed AI-BOM aggregating all agents in pipeline",
        ],
        "primary_risks": [
            "Emergent behavior",
            "Unintended tool use",
            "Hallucination propagation",
            "Loss of human oversight",
            "Trust inheritance violations",
        ],
    },
}


# ---------------------------------------------------------------------------
# Governance Decay Rate (Section 4.5.7)
# ---------------------------------------------------------------------------

# Default GDR thresholds by risk tier
GDR_THRESHOLDS = {
    "critical": 2.0,
    "high": 4.0,
    "medium": 8.0,
    "low": 12.0,
}


@dataclass
class GDRResult:
    """Result of a Governance Decay Rate computation."""
    system_name: str
    change_events: int
    governance_reviews: int
    gdr: float
    risk_tier: str
    threshold: float
    status: str              # "healthy", "stage1_escalation", "stage2_escalation"
    automation_coverage: float
    recommendation: str


def compute_gdr(
    system_name: str,
    change_events: int,
    governance_reviews: int,
    risk_tier: str = "high",
    custom_threshold: Optional[float] = None,
) -> GDRResult:
    """
    Compute Governance Decay Rate per Section 4.5.7.

    GDR(S, t) = C(S, t) / max(G(S, t), 1)

    Args:
        system_name: Name of the AI system
        change_events: Number of change events in the period
        governance_reviews: Number of completed governance reviews
        risk_tier: One of "critical", "high", "medium", "low"
        custom_threshold: Override default threshold for this risk tier

    Returns:
        GDRResult with score, status, and recommendations
    """
    risk_tier = risk_tier.lower()
    if risk_tier not in GDR_THRESHOLDS:
        raise ValueError(f"risk_tier must be one of {list(GDR_THRESHOLDS.keys())}")

    threshold = custom_threshold or GDR_THRESHOLDS[risk_tier]
    gdr = change_events / max(governance_reviews, 1)

    if gdr <= threshold:
        status = "healthy"
        coverage = 0.0
        recommendation = "No escalation needed. GDR is within threshold."
    elif gdr <= 2 * threshold:
        status = "stage1_escalation"
        coverage = min(1.0, (gdr - threshold) / threshold)
        recommendation = (
            f"Stage 1: Activate automated governance controls covering "
            f"{coverage:.0%} of inference requests. Monitor drift, safety "
            f"metrics, and compliance checks."
        )
    else:
        status = "stage2_escalation"
        coverage = 1.0
        recommendation = (
            f"Stage 2: GDR exceeds 2x threshold. Accelerate governance "
            f"review cadence to next higher tier. Full automated monitoring "
            f"required."
        )

    return GDRResult(
        system_name=system_name,
        change_events=change_events,
        governance_reviews=governance_reviews,
        gdr=round(gdr, 2),
        risk_tier=risk_tier,
        threshold=threshold,
        status=status,
        automation_coverage=round(coverage, 2),
        recommendation=recommendation,
    )


# ---------------------------------------------------------------------------
# Composition Safety Degradation Model (Section 6.2)
# ---------------------------------------------------------------------------

class CompositionMode(Enum):
    INDEPENDENT = "independent"
    CORRELATED = "correlated"
    AMPLIFIED = "amplified"


@dataclass
class CompositionSafetyResult:
    """Result of a composition safety budget computation."""
    mode: CompositionMode
    per_component_safety: float
    end_to_end_safety: float
    n_max: float
    max_hops: int
    safety_required: float
    parameters: dict
    recommendation: str


def compute_composition_safety(
    safety_required: float,
    per_component_safety: float,
    mode: str = "independent",
    rho: float = 0.0,
    alpha: float = 0.0,
    num_components: Optional[int] = None,
) -> CompositionSafetyResult:
    """
    Compute composition safety budget per Section 6.2.

    Three modes:
        Independent:  S = s^n
        Correlated:   S = S_A * S_B * (1 - rho) + min(S_A, S_B) * rho
        Amplified:    S = s^n * (1 - alpha)^n

    Args:
        safety_required: Minimum required end-to-end safety (e.g. 0.90)
        per_component_safety: Per-component safety (e.g. 0.95)
        mode: "independent", "correlated", or "amplified"
        rho: Error correlation factor (for correlated mode, 0-1)
        alpha: Amplification factor (for amplified mode, 0-1)
        num_components: If provided, compute actual end-to-end safety

    Returns:
        CompositionSafetyResult
    """
    mode_enum = CompositionMode(mode.lower())
    params = {}

    if mode_enum == CompositionMode.INDEPENDENT:
        n_max = math.log(safety_required) / math.log(per_component_safety)
        s_eff = per_component_safety
        params = {"per_component_safety": per_component_safety}

    elif mode_enum == CompositionMode.CORRELATED:
        n_max = math.log(safety_required) / math.log(per_component_safety)
        s_eff = per_component_safety
        params = {"rho": rho, "per_component_safety": per_component_safety}

    elif mode_enum == CompositionMode.AMPLIFIED:
        s_eff = per_component_safety * (1 - alpha)
        if s_eff <= 0 or s_eff >= 1:
            n_max = 0
        else:
            n_max = math.log(safety_required) / math.log(s_eff)
        params = {
            "alpha": alpha,
            "effective_per_hop_safety": round(s_eff, 4),
            "per_component_safety": per_component_safety,
        }

    max_hops = max(0, int(n_max))

    if num_components is not None:
        if mode_enum == CompositionMode.AMPLIFIED:
            e2e = (per_component_safety ** num_components) * ((1 - alpha) ** num_components)
        else:
            e2e = per_component_safety ** num_components
    else:
        e2e = per_component_safety ** max_hops if max_hops > 0 else per_component_safety

    if max_hops == 0:
        rec = (
            "WARNING: Even a single composition hop violates the safety budget "
            "under this degradation mode. Inter-component safety checkpoints "
            "are required at every hop."
        )
    elif max_hops <= 2:
        rec = (
            f"Maximum {max_hops} composition hops allowed. Pipeline depth is "
            f"severely constrained. Consider safety checkpoints between hops."
        )
    else:
        rec = f"Maximum {max_hops} composition hops allowed under {mode} degradation."

    return CompositionSafetyResult(
        mode=mode_enum,
        per_component_safety=per_component_safety,
        end_to_end_safety=round(e2e, 4),
        n_max=round(n_max, 2),
        max_hops=max_hops,
        safety_required=safety_required,
        parameters=params,
        recommendation=rec,
    )


# ---------------------------------------------------------------------------
# Composition Cost Model (Section 6.5)
# ---------------------------------------------------------------------------

@dataclass
class CompositionCostResult:
    """Result of a composition cost budget computation."""
    n_max_cost: float
    max_hops: int
    total_cost: float
    cost_max: float
    overhead: float
    effective_per_hop: float
    recommendation: str


def compute_composition_cost(
    cost_max: float,
    per_hop_cost: float,
    overhead: float = 0.0,
    beta: float = 1.0,
    num_hops: Optional[int] = None,
) -> CompositionCostResult:
    """
    Compute composition cost budget per Section 6.5.

    n_max_cost = (C_max - C_overhead) / (c * beta)

    Args:
        cost_max: Maximum acceptable per-query cost
        per_hop_cost: Cost per pipeline hop
        overhead: Orchestration and cross-cutting overhead
        beta: Cost amplification factor (1.0 = no amplification)
        num_hops: If provided, compute actual total cost

    Returns:
        CompositionCostResult
    """
    effective_cost = per_hop_cost * beta
    available = cost_max - overhead

    if effective_cost <= 0:
        raise ValueError("Effective per-hop cost must be positive")

    n_max = available / effective_cost
    max_hops = max(0, int(n_max))

    if num_hops is not None:
        total = overhead + (num_hops * effective_cost)
    else:
        total = overhead + (max_hops * effective_cost)

    if max_hops <= 1:
        rec = (
            f"Cost budget severely constrained. Maximum {max_hops} hop(s). "
            f"Consider cheaper models, caching, or reduced context windows."
        )
    else:
        rec = f"Maximum {max_hops} composition hops within cost budget of ${cost_max:.2f}."

    return CompositionCostResult(
        n_max_cost=round(n_max, 2),
        max_hops=max_hops,
        total_cost=round(total, 4),
        cost_max=cost_max,
        overhead=overhead,
        effective_per_hop=round(effective_cost, 4),
        recommendation=rec,
    )


# ---------------------------------------------------------------------------
# AI Architecture Health Index (Section 6.7)
# ---------------------------------------------------------------------------

# Default AAHI dimension weights for regulated industries
DEFAULT_WEIGHTS_REGULATED = {
    "governance_velocity": 0.20,
    "behavioral_compliance": 0.25,
    "composition_safety": 0.20,
    "trust_integrity": 0.10,
    "supply_chain": 0.10,
    "cost_compliance": 0.15,
}

# AAHI operational zones
AAHI_ZONES = {
    "green": {"min": 0.8, "max": 1.0, "label": "Healthy", "action": "Routine monitoring"},
    "yellow": {"min": 0.6, "max": 0.8, "label": "Degrading", "action": "Increase monitoring, generate governance attention report"},
    "orange": {"min": 0.4, "max": 0.6, "label": "Intervention Required", "action": "Governance escalation, freeze new deployments, emergency review"},
    "red": {"min": 0.0, "max": 0.4, "label": "Crisis", "action": "Executive escalation, suspend Tier C operations, incident response"},
}


@dataclass
class SystemHealth:
    """Health dimensions for a single AI system."""
    name: str
    tier: GovernanceTier
    risk_weight: float
    h_gov: float = 1.0          # Governance velocity health (from FF-1)
    h_behav: float = 1.0        # Behavioral compliance (from FF-2)
    h_comp: Optional[float] = None   # Composition safety (Tier C only, from FF-3)
    h_trust: Optional[float] = None  # Trust integrity (Tier C only, from FF-4)
    h_supply: float = 1.0       # Supply chain health (AI-BOM)
    h_cost: float = 1.0         # Cost compliance (from FF-6)


@dataclass
class AAHIResult:
    """Result of an AAHI computation."""
    aahi: float
    zone: str
    zone_label: str
    zone_action: str
    per_system_scores: dict
    floor_triggered: bool
    floor_details: str
    recommendation: str


def compute_aahi(
    systems: list,
    weights: Optional[dict] = None,
) -> AAHIResult:
    """
    Compute AI Architecture Health Index per Section 6.7.

    AAHI(t) = Sum(w_i * H(S_i, t)) / Sum(w_i)

    Includes floor constraint: if any dimension scores below 0.3
    for a Critical or High risk tier system, AAHI is capped at
    Yellow zone (max 0.79).

    Args:
        systems: List of SystemHealth objects
        weights: Custom dimension weights (defaults to regulated industry weights)

    Returns:
        AAHIResult with composite score and zone classification
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS_REGULATED.copy()

    per_system = {}
    floor_triggered = False
    floor_details = ""

    for sys in systems:
        # Determine applicable dimensions based on tier
        is_tier_c = sys.tier == GovernanceTier.TIER_C

        if is_tier_c:
            w = weights.copy()
            dims = {
                "governance_velocity": sys.h_gov,
                "behavioral_compliance": sys.h_behav,
                "composition_safety": sys.h_comp if sys.h_comp is not None else 1.0,
                "trust_integrity": sys.h_trust if sys.h_trust is not None else 1.0,
                "supply_chain": sys.h_supply,
                "cost_compliance": sys.h_cost,
            }
        else:
            # Redistribute composition and trust weights proportionally
            non_ct_keys = ["governance_velocity", "behavioral_compliance", "supply_chain", "cost_compliance"]
            ct_weight = weights.get("composition_safety", 0) + weights.get("trust_integrity", 0)
            base_sum = sum(weights[k] for k in non_ct_keys)

            w = {}
            for k in non_ct_keys:
                w[k] = weights[k] + (weights[k] / base_sum) * ct_weight
            w["composition_safety"] = 0.0
            w["trust_integrity"] = 0.0

            dims = {
                "governance_velocity": sys.h_gov,
                "behavioral_compliance": sys.h_behav,
                "composition_safety": 0.0,
                "trust_integrity": 0.0,
                "supply_chain": sys.h_supply,
                "cost_compliance": sys.h_cost,
            }

        # Compute per-system health score
        h_score = sum(w[d] * dims[d] for d in dims)
        per_system[sys.name] = {
            "score": round(h_score, 3),
            "tier": sys.tier.value,
            "risk_weight": sys.risk_weight,
            "dimensions": {k: round(v, 3) for k, v in dims.items() if w.get(k, 0) > 0},
            "weights_used": {k: round(v, 3) for k, v in w.items() if v > 0},
        }

        # Floor constraint check for Critical/High systems
        if sys.risk_weight >= 2.0:  # Critical or High
            for dim_name, dim_val in dims.items():
                if w.get(dim_name, 0) > 0 and dim_val < 0.3:
                    floor_triggered = True
                    floor_details = (
                        f"System '{sys.name}' has {dim_name} = {dim_val:.2f} "
                        f"(below 0.3 floor for Critical/High tier). "
                        f"AAHI capped at Yellow zone (max 0.79)."
                    )

    # Compute enterprise AAHI
    total_weighted = sum(
        per_system[s.name]["score"] * s.risk_weight for s in systems
    )
    total_weights = sum(s.risk_weight for s in systems)
    aahi = total_weighted / total_weights if total_weights > 0 else 0.0

    # Apply floor constraint
    if floor_triggered and aahi > 0.79:
        aahi = 0.79

    aahi = round(aahi, 3)

    # Determine zone
    zone = "red"
    for z_name, z_def in AAHI_ZONES.items():
        if z_def["min"] <= aahi < z_def["max"] or (z_name == "green" and aahi >= z_def["min"]):
            zone = z_name
            break

    zone_info = AAHI_ZONES[zone]

    # Find primary contributor to degradation
    if zone != "green" and systems:
        worst = min(per_system.items(), key=lambda x: x[1]["score"])
        rec = (
            f"AAHI = {aahi:.3f} ({zone_info['label']}). "
            f"Primary contributor: {worst[0]} (score: {worst[1]['score']:.3f}). "
            f"Action: {zone_info['action']}."
        )
    else:
        rec = f"AAHI = {aahi:.3f} ({zone_info['label']}). {zone_info['action']}."

    return AAHIResult(
        aahi=aahi,
        zone=zone,
        zone_label=zone_info["label"],
        zone_action=zone_info["action"],
        per_system_scores=per_system,
        floor_triggered=floor_triggered,
        floor_details=floor_details,
        recommendation=rec,
    )


# ---------------------------------------------------------------------------
# Risk Assessment (Section 9.1, Appendix B)
# ---------------------------------------------------------------------------

RISK_DOMAINS = {
    "data_risk": {
        "label": "Data Risk",
        "questions": [
            {"id": "D1", "text": "Has the training data been profiled for quality, completeness, and bias?"},
            {"id": "D2", "text": "Is full data provenance tracked from source through feature engineering to model training?"},
            {"id": "D3", "text": "Has consent been obtained and documented for all data subjects whose data is used in training?"},
            {"id": "D4", "text": "Is the training data distribution representative of the production data distribution?"},
            {"id": "D5", "text": "Is there a process for detecting and responding to training data contamination?"},
        ],
    },
    "model_risk": {
        "label": "Model Risk",
        "questions": [
            {"id": "M1", "text": "Has the model been evaluated against defined accuracy, fairness, and safety benchmarks?"},
            {"id": "M2", "text": "Has adversarial testing been conducted to identify failure modes?"},
            {"id": "M3", "text": "Can the model's decisions be explained to the level required by applicable regulations?"},
            {"id": "M4", "text": "Is there automated monitoring for model drift, accuracy degradation, and behavioral changes?"},
            {"id": "M5", "text": "Are model failure modes documented with defined fallback procedures?"},
        ],
    },
    "deployment_risk": {
        "label": "Deployment Risk",
        "questions": [
            {"id": "P1", "text": "Is the deployment infrastructure resilient with defined failover and disaster recovery?"},
            {"id": "P2", "text": "Can the model be rolled back to a previous version within defined time constraints?"},
            {"id": "P3", "text": "Are vendor dependencies documented with contractual governance and exit strategies?"},
            {"id": "P4", "text": "Is there production monitoring covering performance, safety, cost, and business outcome metrics?"},
            {"id": "P5", "text": "Is the CI/CD pipeline for model deployment automated with safety validation gates?"},
        ],
    },
    "compliance_risk": {
        "label": "Compliance Risk",
        "questions": [
            {"id": "C1", "text": "Have all applicable regulations been identified and mapped to specific system components?"},
            {"id": "C2", "text": "Is data classification enforced with compliance-aware processing controls?"},
            {"id": "C3", "text": "Are audit trails generated automatically and retained per regulatory requirements?"},
            {"id": "C4", "text": "Are transparency and notification requirements met for AI-driven decisions?"},
            {"id": "C5", "text": "Are cross-border data transfer requirements addressed in the architecture?"},
        ],
    },
    "impact_risk": {
        "label": "Impact Risk",
        "questions": [
            {"id": "I1", "text": "What is the severity of harm if the AI system produces an incorrect output?"},
            {"id": "I2", "text": "Can decisions made by the AI system be reversed or corrected after the fact?"},
            {"id": "I3", "text": "Does the AI system interact with or affect vulnerable populations?"},
            {"id": "I4", "text": "What is the potential financial impact of AI system failure or misuse?"},
            {"id": "I5", "text": "What is the reputational risk to the organization from AI system failures?"},
        ],
    },
}

RISK_TIERS = {
    "critical": {"min": 80, "max": 100, "review_cadence": "Monthly + continuous automated"},
    "high": {"min": 60, "max": 79, "review_cadence": "Quarterly + continuous automated"},
    "medium": {"min": 40, "max": 59, "review_cadence": "Semi-annually"},
    "low": {"min": 0, "max": 39, "review_cadence": "Annually"},
}


def classify_risk_tier(total_score: int) -> dict:
    """Classify risk tier based on total assessment score (0-100)."""
    for tier_name, tier_def in RISK_TIERS.items():
        if tier_def["min"] <= total_score <= tier_def["max"]:
            return {
                "tier": tier_name,
                "score": total_score,
                "review_cadence": tier_def["review_cadence"],
            }
    return {"tier": "unknown", "score": total_score, "review_cadence": "N/A"}


# ---------------------------------------------------------------------------
# Regulatory Policy Schema (Section 6.6)
# ---------------------------------------------------------------------------

@dataclass
class RegulatoryPolicy:
    """
    Formal Regulatory Policy tuple RP from Section 6.6.

    RP = (Jurisdiction, Scope, Requirements, Effective_Date,
          AI_Risk_Tier, Mapping)
    """
    jurisdiction: str
    jurisdiction_type: str   # "supranational", "federal", "state", "sector"
    scope: dict              # Which AI systems are affected
    requirements: list       # Concrete obligations
    effective_date: str      # ISO date
    ai_risk_tier: str        # Mapping to GAIF risk tiers
    mapping: dict            # GAIF components that must be configured
    name: str = ""
    citation: str = ""
    url: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "jurisdiction": self.jurisdiction,
            "jurisdiction_type": self.jurisdiction_type,
            "scope": self.scope,
            "requirements": self.requirements,
            "effective_date": self.effective_date,
            "ai_risk_tier": self.ai_risk_tier,
            "mapping": self.mapping,
            "citation": self.citation,
            "url": self.url,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RegulatoryPolicy":
        return cls(**data)

    @classmethod
    def from_json(cls, path: str) -> "RegulatoryPolicy":
        with open(path, "r") as f:
            return cls.from_dict(json.load(f))
