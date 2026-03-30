#!/usr/bin/env python3
"""
GAIF Composition Safety Calculator
===================================
Computes maximum safe composition depth for multi-agent pipelines.

Reference: GAIF v1.0, Section 6.2
https://doi.org/10.5281/zenodo.19341015
"""

import json
from gaif_core import compute_composition_safety, CompositionMode


def print_header():
    print("\n" + "=" * 60)
    print("  GAIF Composition Safety Calculator v0.1.0")
    print("  Based on GAIF v1.0, Section 6.2")
    print("=" * 60)


def run_interactive():
    print_header()

    print("\nThis tool computes the maximum number of composition hops")
    print("your multi-agent pipeline can have while meeting a required")
    print("end-to-end safety level.")

    while True:
        try:
            s_req = float(input("\nRequired end-to-end safety (e.g. 0.90 for 90%): "))
            if 0 < s_req < 1:
                break
        except ValueError:
            pass
        print("Please enter a value between 0 and 1")

    while True:
        try:
            s_comp = float(input("Per-component safety (e.g. 0.95 for 95%): "))
            if 0 < s_comp < 1:
                break
        except ValueError:
            pass
        print("Please enter a value between 0 and 1")

    print("\nComposition degradation mode:")
    print("  [1] Independent - errors are statistically independent")
    print("  [2] Correlated  - errors in component A make errors in B more likely")
    print("  [3] Amplified   - downstream components amplify upstream errors")
    while True:
        choice = input("  Select mode (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            break

    rho = 0.0
    alpha = 0.0

    if choice == "1":
        mode = "independent"
    elif choice == "2":
        mode = "correlated"
        while True:
            try:
                rho = float(input("  Error correlation factor rho (0-1, e.g. 0.3): "))
                if 0 <= rho <= 1:
                    break
            except ValueError:
                pass
    else:
        mode = "amplified"
        while True:
            try:
                alpha = float(input("  Amplification factor alpha (0-1, e.g. 0.2): "))
                if 0 <= alpha < 1:
                    break
            except ValueError:
                pass
        print(f"  Effective per-hop safety: {s_comp * (1 - alpha):.4f}")

    result = compute_composition_safety(s_req, s_comp, mode, rho, alpha)

    print("\n" + "=" * 60)
    print(f"  COMPOSITION SAFETY RESULT")
    print("=" * 60)
    print(f"\n  Mode:              {result.mode.value}")
    print(f"  Safety required:   {result.safety_required}")
    print(f"  Per-component:     {result.per_component_safety}")

    if mode == "amplified":
        print(f"  Alpha:             {alpha}")
        print(f"  Effective safety:  {result.parameters['effective_per_hop_safety']}")

    print(f"\n  n_max:             {result.n_max}")
    print(f"  Maximum hops:      {result.max_hops}")
    print(f"  End-to-end safety: {result.end_to_end_safety}")

    print(f"\n  Recommendation:")
    print(f"    {result.recommendation}")

    # Compare all three modes
    print(f"\n  Comparison across all modes (for reference):")
    for m, a_val in [("independent", 0), ("correlated", 0), ("amplified", 0.2)]:
        r = compute_composition_safety(s_req, s_comp, m, alpha=a_val)
        print(f"    {m:15s}: n_max = {r.n_max:6.2f} -> max {r.max_hops} hops")

    print()


if __name__ == "__main__":
    run_interactive()
