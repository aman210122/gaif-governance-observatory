#!/usr/bin/env python3
"""
GAIF AI Risk Assessment Tool
=============================
Interactive 25-question risk assessment for AI systems.

Reference: GAIF v1.0, Section 9.1, Appendix B
https://doi.org/10.5281/zenodo.19341015
"""

import json
from gaif_core import RISK_DOMAINS, classify_risk_tier


def print_header():
    print("\n" + "=" * 60)
    print("  GAIF AI Risk Assessment Tool v0.1.0")
    print("  Based on GAIF v1.0, Section 9.1")
    print("=" * 60)
    print("\n  25 questions across 5 risk domains.")
    print("  Score each question 0-4:")
    print("    0 = Not addressed at all")
    print("    1 = Minimally addressed")
    print("    2 = Partially addressed")
    print("    3 = Mostly addressed")
    print("    4 = Fully addressed")


def run_interactive():
    print_header()

    system_name = input("\nSystem name: ").strip() or "Unnamed System"

    scores = {}
    domain_scores = {}

    for domain_key, domain in RISK_DOMAINS.items():
        print(f"\n{'=' * 60}")
        print(f"  {domain['label'].upper()}")
        print(f"{'=' * 60}")

        domain_total = 0
        for q in domain["questions"]:
            print(f"\n  {q['id']}: {q['text']}")
            while True:
                try:
                    score = int(input(f"    Score (0-4): "))
                    if 0 <= score <= 4:
                        scores[q["id"]] = score
                        domain_total += score
                        break
                except (ValueError, EOFError):
                    pass
                print("    Please enter 0, 1, 2, 3, or 4")

        domain_scores[domain_key] = {
            "label": domain["label"],
            "score": domain_total,
            "max": 20,
            "percentage": f"{domain_total / 20 * 100:.0f}%",
        }

    total = sum(scores.values())
    tier_result = classify_risk_tier(total)

    print("\n" + "=" * 60)
    print(f"  RISK ASSESSMENT RESULT")
    print("=" * 60)
    print(f"\n  System: {system_name}")
    print(f"\n  Domain Scores:")

    for dk, ds in domain_scores.items():
        bar = "#" * ds["score"] + "." * (20 - ds["score"])
        print(f"    {ds['label']:20s} {ds['score']:2d}/20  [{bar}]  {ds['percentage']}")

    print(f"\n  Total Score:    {total}/100")
    print(f"  Risk Tier:      {tier_result['tier'].upper()}")
    print(f"  Review Cadence: {tier_result['review_cadence']}")

    # Risk-specific guidance
    weakest = min(domain_scores.items(), key=lambda x: x[1]["score"])
    print(f"\n  Weakest Domain: {weakest[1]['label']} ({weakest[1]['score']}/20)")
    print(f"  Priority: Address {weakest[1]['label'].lower()} gaps first.")

    # Mapping to GAIF governance requirements
    print(f"\n  GAIF Governance Requirements for {tier_result['tier'].upper()} tier:")
    if tier_result["tier"] == "critical":
        print("    - Full AI Architecture Board review")
        print("    - Mandatory safety architecture patterns")
        print("    - Continuous monitoring + external audit")
    elif tier_result["tier"] == "high":
        print("    - Senior architect review")
        print("    - Required safety patterns")
        print("    - Automated monitoring with alerting")
    elif tier_result["tier"] == "medium":
        print("    - Architect review")
        print("    - Recommended safety patterns")
        print("    - Standard monitoring")
    else:
        print("    - Self-certification with spot audits")
        print("    - Basic monitoring")

    print()

    save = input("Save assessment to JSON? (y/n): ").strip().lower()
    if save == "y":
        filename = f"{system_name.lower().replace(' ', '_')}_risk_assessment.json"
        output = {
            "system_name": system_name,
            "total_score": total,
            "risk_tier": tier_result["tier"],
            "review_cadence": tier_result["review_cadence"],
            "domain_scores": domain_scores,
            "question_scores": scores,
        }
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    run_interactive()
