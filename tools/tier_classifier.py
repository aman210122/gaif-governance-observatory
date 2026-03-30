#!/usr/bin/env python3
"""
GAIF Tier Classifier
====================
Interactive tool to classify an AI system's governance tier.

Reference: GAIF v1.0, Section 5.1.1
https://doi.org/10.5281/zenodo.19341015
"""

import json
import sys
from gaif_core import (
    classify_tier,
    DataControl,
    ModelTransparency,
    AutonomyLevel,
    TIER_GOVERNANCE_REQUIREMENTS,
)


def print_header():
    print("\n" + "=" * 60)
    print("  GAIF Governance Tier Classifier v0.1.0")
    print("  Based on GAIF v1.0, Section 5.1.1")
    print("=" * 60)


def get_attribute(prompt, options):
    print(f"\n{prompt}")
    for val, desc in options:
        print(f"  [{val}] {desc}")
    while True:
        try:
            choice = int(input("\n  Enter value (0, 1, or 2): "))
            if choice in (0, 1, 2):
                return choice
            print("  Please enter 0, 1, or 2.")
        except (ValueError, EOFError):
            print("  Please enter 0, 1, or 2.")


def run_interactive():
    print_header()
    system_name = input("\nSystem name: ").strip() or "Unnamed System"

    d = get_attribute(
        "DATA CONTROL (D) - How much control does your organization have over the data?",
        [
            (0, "Full control over training and inference data"),
            (1, "Data passes through third-party infrastructure with contractual controls"),
            (2, "Variable data access across multiple sources with mixed control levels"),
        ],
    )

    t = get_attribute(
        "MODEL TRANSPARENCY (T) - How much visibility do you have into the model?",
        [
            (0, "Full visibility into model architecture, weights, and training process"),
            (1, "API-level observation only with vendor documentation"),
            (2, "Partial: agent logic visible but underlying model behavior opaque"),
        ],
    )

    a = get_attribute(
        "AUTONOMY LEVEL (A) - How autonomously does the system operate?",
        [
            (0, "Produces outputs only when explicitly invoked by application code"),
            (1, "Invoked through vendor API with predefined behavior"),
            (2, "Autonomously plans, executes multi-step workflows, uses tools"),
        ],
    )

    tier = classify_tier(d, t, a)
    reqs = TIER_GOVERNANCE_REQUIREMENTS[tier]

    print("\n" + "=" * 60)
    print(f"  CLASSIFICATION RESULT")
    print("=" * 60)
    print(f"\n  System:     {system_name}")
    print(f"  D={d}, T={t}, A={a}")
    print(f"\n  Tier:       {tier.value}")
    print(f"  Approach:   {reqs['governance_approach']}")

    print(f"\n  Governance Requirements:")
    for i, req in enumerate(reqs["requirements"], 1):
        print(f"    {i}. {req}")

    print(f"\n  Primary Risks:")
    for risk in reqs["primary_risks"]:
        print(f"    - {risk}")

    # Note about T
    if t > 0:
        print(f"\n  Note: T={t} does not change the tier assignment but increases")
        print(f"  Model Risk scores (M3, M4), raising governance intensity")
        print(f"  within {tier.value}.")

    print()

    # Output JSON
    result = {
        "system_name": system_name,
        "attributes": {"D": d, "T": t, "A": a},
        "tier": tier.value,
        "governance_requirements": reqs["requirements"],
        "primary_risks": reqs["primary_risks"],
    }

    save = input("Save classification to JSON? (y/n): ").strip().lower()
    if save == "y":
        filename = f"{system_name.lower().replace(' ', '_')}_classification.json"
        with open(filename, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved to {filename}")


def run_batch(input_file: str):
    """Run batch classification from a JSON file."""
    with open(input_file, "r") as f:
        systems = json.load(f)

    results = []
    for sys in systems:
        tier = classify_tier(sys["D"], sys["T"], sys["A"])
        results.append({
            "system_name": sys.get("name", "Unknown"),
            "D": sys["D"],
            "T": sys["T"],
            "A": sys["A"],
            "tier": tier.value,
        })

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_batch(sys.argv[1])
    else:
        run_interactive()
