#!/usr/bin/env python3
"""
GAIF Governance Decay Rate Calculator
======================================
Computes GDR and escalation status for AI systems.

Reference: GAIF v1.0, Section 4.5.7
https://doi.org/10.5281/zenodo.19341015
"""

import json
import sys
from gaif_core import compute_gdr, GDR_THRESHOLDS


def print_header():
    print("\n" + "=" * 60)
    print("  GAIF Governance Decay Rate Calculator v0.1.0")
    print("  Based on GAIF v1.0, Section 4.5.7")
    print("=" * 60)


def run_interactive():
    print_header()

    name = input("\nSystem name: ").strip() or "Unnamed System"

    print(f"\nTime period for measurement (e.g., 'last 12 months'):")
    period = input("  Period: ").strip() or "measurement period"

    while True:
        try:
            changes = int(input("\nNumber of change events in this period: "))
            break
        except ValueError:
            print("Please enter a whole number.")

    print("\n  Change events include: model retraining, vendor API version")
    print("  updates, prompt modifications, data pipeline changes,")
    print("  configuration updates, feature store refreshes.")

    while True:
        try:
            reviews = int(input("\nNumber of completed governance reviews in this period: "))
            break
        except ValueError:
            print("Please enter a whole number.")

    print("\nRisk tier of this system:")
    for tier, threshold in GDR_THRESHOLDS.items():
        print(f"  [{tier}] GDR threshold = {threshold}")

    while True:
        risk_tier = input("\n  Enter risk tier: ").strip().lower()
        if risk_tier in GDR_THRESHOLDS:
            break
        print(f"  Please enter one of: {', '.join(GDR_THRESHOLDS.keys())}")

    result = compute_gdr(name, changes, reviews, risk_tier)

    status_icons = {
        "healthy": "OK",
        "stage1_escalation": "WARNING",
        "stage2_escalation": "CRITICAL",
    }

    print("\n" + "=" * 60)
    print(f"  GDR RESULT")
    print("=" * 60)
    print(f"\n  System:           {result.system_name}")
    print(f"  Period:           {period}")
    print(f"  Change events:    {result.change_events}")
    print(f"  Governance reviews: {result.governance_reviews}")
    print(f"\n  GDR:              {result.gdr}")
    print(f"  Threshold:        {result.threshold} ({result.risk_tier} tier)")
    print(f"  Status:           [{status_icons[result.status]}] {result.status}")

    if result.automation_coverage > 0:
        print(f"  Auto coverage:    {result.automation_coverage:.0%}")

    print(f"\n  Recommendation:")
    print(f"    {result.recommendation}")

    # Interpretation
    if result.gdr > 1:
        ungoverned = result.change_events - result.governance_reviews
        print(f"\n  Interpretation:")
        print(f"    {ungoverned} change events occurred without governance review.")
        print(f"    Each ungoverned change is a potential governance gap.")
    print()

    save = input("Save result to JSON? (y/n): ").strip().lower()
    if save == "y":
        filename = f"{name.lower().replace(' ', '_')}_gdr.json"
        output = {
            "system_name": result.system_name,
            "period": period,
            "change_events": result.change_events,
            "governance_reviews": result.governance_reviews,
            "gdr": result.gdr,
            "risk_tier": result.risk_tier,
            "threshold": result.threshold,
            "status": result.status,
            "automation_coverage": result.automation_coverage,
            "recommendation": result.recommendation,
        }
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    run_interactive()
