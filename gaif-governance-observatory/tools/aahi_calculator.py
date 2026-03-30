#!/usr/bin/env python3
"""
GAIF AI Architecture Health Index Calculator
=============================================
Computes enterprise-wide AAHI from per-system health dimensions.

Reference: GAIF v1.0, Section 6.7
https://doi.org/10.5281/zenodo.19341015
"""

import json
from gaif_core import (
    compute_aahi,
    SystemHealth,
    GovernanceTier,
    DEFAULT_WEIGHTS_REGULATED,
    AAHI_ZONES,
)


def print_header():
    print("\n" + "=" * 60)
    print("  GAIF AI Architecture Health Index Calculator v0.1.0")
    print("  Based on GAIF v1.0, Section 6.7")
    print("=" * 60)


def get_float(prompt, default=1.0):
    while True:
        raw = input(f"  {prompt} [{default}]: ").strip()
        if raw == "":
            return default
        try:
            val = float(raw)
            if 0.0 <= val <= 1.0:
                return val
            print("    Value must be between 0.0 and 1.0")
        except ValueError:
            print("    Please enter a number between 0.0 and 1.0")


def get_tier():
    print("  Governance Tier:")
    print("    [a] Tier A: Governed AI Platform")
    print("    [b] Tier B: Managed SaaS AI")
    print("    [c] Tier C: Agent Platform")
    while True:
        choice = input("  Enter tier (a/b/c): ").strip().lower()
        if choice == "a":
            return GovernanceTier.TIER_A
        elif choice == "b":
            return GovernanceTier.TIER_B
        elif choice == "c":
            return GovernanceTier.TIER_C
        print("  Please enter a, b, or c")


def run_interactive():
    print_header()

    print("\nDefault dimension weights (regulated industries):")
    for dim, weight in DEFAULT_WEIGHTS_REGULATED.items():
        print(f"  {dim}: {weight}")

    print("\nHow many AI systems to assess?")
    while True:
        try:
            n = int(input("  Number of systems: "))
            if n > 0:
                break
        except ValueError:
            pass
        print("  Please enter a positive number")

    systems = []
    for i in range(n):
        print(f"\n--- System {i + 1} of {n} ---")
        name = input(f"  System name: ").strip() or f"System {i + 1}"
        tier = get_tier()

        while True:
            try:
                weight = float(input("  Risk weight (e.g., 3.0=Critical, 2.0=High, 1.5=Medium, 1.0=Low): "))
                break
            except ValueError:
                print("  Please enter a number")

        print(f"\n  Health dimensions for {name} (0.0 = failed, 1.0 = healthy):")
        h_gov = get_float("Governance velocity health (h_gov)", 1.0)
        h_behav = get_float("Behavioral compliance (h_behav)", 1.0)

        h_comp = None
        h_trust = None
        if tier == GovernanceTier.TIER_C:
            h_comp = get_float("Composition safety (h_comp)", 1.0)
            h_trust = get_float("Trust integrity (h_trust)", 1.0)

        h_supply = get_float("Supply chain health (h_supply)", 1.0)
        h_cost = get_float("Cost compliance (h_cost)", 1.0)

        systems.append(SystemHealth(
            name=name,
            tier=tier,
            risk_weight=weight,
            h_gov=h_gov,
            h_behav=h_behav,
            h_comp=h_comp,
            h_trust=h_trust,
            h_supply=h_supply,
            h_cost=h_cost,
        ))

    result = compute_aahi(systems)

    zone_display = {
        "green": "GREEN",
        "yellow": "YELLOW",
        "orange": "ORANGE",
        "red": "RED",
    }

    print("\n" + "=" * 60)
    print(f"  AAHI RESULT")
    print("=" * 60)
    print(f"\n  Enterprise AAHI:  {result.aahi:.3f}")
    print(f"  Zone:             [{zone_display[result.zone]}] {result.zone_label}")
    print(f"  Action:           {result.zone_action}")

    if result.floor_triggered:
        print(f"\n  FLOOR CONSTRAINT: {result.floor_details}")

    print(f"\n  Per-System Breakdown:")
    for name, info in result.per_system_scores.items():
        print(f"\n    {name}:")
        print(f"      Score: {info['score']:.3f}  |  Tier: {info['tier']}  |  Weight: {info['risk_weight']}")
        print(f"      Dimensions: ", end="")
        dims = [f"{k}={v:.2f}" for k, v in info["dimensions"].items()]
        print(", ".join(dims))

    print(f"\n  Recommendation:")
    print(f"    {result.recommendation}")
    print()

    save = input("Save result to JSON? (y/n): ").strip().lower()
    if save == "y":
        filename = "aahi_result.json"
        output = {
            "aahi": result.aahi,
            "zone": result.zone,
            "zone_label": result.zone_label,
            "floor_triggered": result.floor_triggered,
            "floor_details": result.floor_details,
            "per_system_scores": result.per_system_scores,
            "recommendation": result.recommendation,
        }
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    run_interactive()
