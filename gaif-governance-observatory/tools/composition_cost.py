#!/usr/bin/env python3
"""
GAIF Composition Cost Calculator
=================================
Computes maximum affordable composition depth for AI pipelines.

Reference: GAIF v1.0, Section 6.5
https://doi.org/10.5281/zenodo.19341015
"""

import json
from gaif_core import compute_composition_cost


def print_header():
    print("\n" + "=" * 60)
    print("  GAIF Composition Cost Calculator v0.1.0")
    print("  Based on GAIF v1.0, Section 6.5")
    print("=" * 60)


def run_interactive():
    print_header()

    print("\nThis tool computes the maximum number of pipeline hops")
    print("your multi-agent system can afford per query.")

    while True:
        try:
            c_max = float(input("\nMaximum acceptable cost per query ($): "))
            if c_max > 0:
                break
        except ValueError:
            pass

    while True:
        try:
            c_hop = float(input("Average cost per pipeline hop ($): "))
            if c_hop > 0:
                break
        except ValueError:
            pass

    while True:
        try:
            overhead = float(input("Orchestration overhead per query ($ , default 0.05): ") or "0.05")
            if overhead >= 0:
                break
        except ValueError:
            pass

    while True:
        try:
            beta = float(input("Cost amplification factor beta (1.0 = no amplification, default 1.0): ") or "1.0")
            if beta > 0:
                break
        except ValueError:
            pass

    result = compute_composition_cost(c_max, c_hop, overhead, beta)

    print("\n" + "=" * 60)
    print(f"  COMPOSITION COST RESULT")
    print("=" * 60)
    print(f"\n  Max cost/query:     ${result.cost_max:.2f}")
    print(f"  Per-hop cost:       ${c_hop:.4f}")
    print(f"  Amplification:      {beta}x")
    print(f"  Effective per-hop:  ${result.effective_per_hop:.4f}")
    print(f"  Overhead:           ${result.overhead:.4f}")
    print(f"\n  n_max_cost:         {result.n_max_cost}")
    print(f"  Maximum hops:       {result.max_hops}")
    print(f"  Projected cost:     ${result.total_cost:.4f}")

    print(f"\n  Recommendation:")
    print(f"    {result.recommendation}")
    print()


if __name__ == "__main__":
    run_interactive()
