#!/usr/bin/env python3
"""
AAHI Worked Example
====================
Reproduces the worked example from GAIF v1.0, Section 6.7.

Three systems: Critical clinical NLP (Tier A), High vendor API (Tier B),
Medium multi-agent pipeline (Tier C).
"""

import sys
sys.path.insert(0, "../tools")

from gaif_core import compute_aahi, SystemHealth, GovernanceTier

# Define three systems matching the paper's worked example
systems = [
    SystemHealth(
        name="Clinical NLP Model",
        tier=GovernanceTier.TIER_A,
        risk_weight=3.0,       # Critical tier
        h_gov=0.90,            # GDR = 1.5, below threshold 2.0
        h_behav=0.85,          # Behavioral drift approaching contract limit
        h_comp=None,           # N/A: not a composed system
        h_trust=None,          # N/A: not an agent
        h_supply=1.0,          # AI-BOM current
        h_cost=0.95,           # Within budget
    ),
    SystemHealth(
        name="Vendor Summarization API",
        tier=GovernanceTier.TIER_B,
        risk_weight=2.0,       # High tier
        h_gov=0.40,            # GDR = 9.0, well above threshold 4.0
        h_behav=0.60,          # Vendor model update changed distribution
        h_comp=None,           # N/A
        h_trust=None,          # N/A
        h_supply=0.50,         # Vendor AI-BOM partially stale
        h_cost=0.80,           # Approaching budget
    ),
    SystemHealth(
        name="Clinical Agent Pipeline",
        tier=GovernanceTier.TIER_C,
        risk_weight=1.5,       # Medium tier
        h_gov=0.85,
        h_behav=0.90,
        h_comp=0.75,           # End-to-end safety at 75% of budget
        h_trust=1.0,           # All invariants hold
        h_supply=0.80,
        h_cost=0.70,
    ),
]

result = compute_aahi(systems)

print("GAIF AAHI Worked Example")
print("=" * 60)
print(f"\nEnterprise AAHI: {result.aahi:.3f}")
print(f"Zone: {result.zone.upper()} ({result.zone_label})")
print(f"Action: {result.zone_action}")

if result.floor_triggered:
    print(f"\nFloor constraint: {result.floor_details}")

print("\nPer-system breakdown:")
for name, info in result.per_system_scores.items():
    print(f"\n  {name}:")
    print(f"    H(S) = {info['score']:.3f}  |  Weight = {info['risk_weight']}")
    for dim, val in info["dimensions"].items():
        w = info["weights_used"].get(dim, 0)
        print(f"    {dim:25s}: {val:.2f}  (weight: {w:.3f})")

print(f"\nRecommendation: {result.recommendation}")
