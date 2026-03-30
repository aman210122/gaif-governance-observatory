#!/usr/bin/env python3
"""
Healthcare Case Study
======================
Demonstrates GAIF tools applied to a healthcare organization scenario
matching the case study in GAIF v1.0, Chapter 12.
"""

import sys
sys.path.insert(0, "../tools")

from gaif_core import classify_tier, compute_gdr, compute_composition_safety

print("GAIF Healthcare Case Study")
print("=" * 60)

# Step 1: Classify three systems
print("\n1. TIER CLASSIFICATION")
print("-" * 40)

systems = [
    {"name": "Databricks Mosaic AI Gateway", "D": 0, "T": 0, "A": 0},
    {"name": "Azure OpenAI (Summarization)", "D": 1, "T": 1, "A": 1},
    {"name": "Clinical Multi-Agent Pipeline", "D": 2, "T": 2, "A": 2},
]

for s in systems:
    tier = classify_tier(s["D"], s["T"], s["A"])
    print(f"  {s['name']:40s} -> {tier.value}")

# Step 2: Compute GDR for each
print("\n2. GOVERNANCE DECAY RATE (12-month period)")
print("-" * 40)

gdr_inputs = [
    {"name": "Clinical NLP (Tier A)", "changes": 6, "reviews": 4, "tier": "critical"},
    {"name": "Vendor Summarization (Tier B)", "changes": 18, "reviews": 2, "tier": "high"},
    {"name": "Internal Chatbot (Tier B)", "changes": 24, "reviews": 1, "tier": "medium"},
]

for g in gdr_inputs:
    result = compute_gdr(g["name"], g["changes"], g["reviews"], g["tier"])
    status_icon = {"healthy": "OK", "stage1_escalation": "WARN", "stage2_escalation": "CRIT"}
    print(f"  {g['name']:35s} GDR={result.gdr:5.1f}  [{status_icon[result.status]:4s}]  threshold={result.threshold}")

# Step 3: Composition safety for clinical pipeline
print("\n3. COMPOSITION SAFETY BUDGET")
print("-" * 40)

for mode, alpha in [("independent", 0), ("amplified", 0.2)]:
    result = compute_composition_safety(0.90, 0.97, mode, alpha=alpha)
    print(f"  {mode:15s}: n_max={result.n_max:5.2f} -> max {result.max_hops} hops")

print("\n  Healthcare implication: under amplified degradation,")
print("  even a single composition hop violates 90% safety budget.")
print("  Inter-component safety checkpoints are mandatory.")
