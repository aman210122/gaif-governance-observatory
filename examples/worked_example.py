#!/usr/bin/env python3
"""
GAIF-4 Worked Example
From: GAIF-4 Working Specification v1.5, Section 4.4

Pipeline: Four-agent chain (triage, diagnosis, treatment, pharmacy)
          using GPT-4o-mini and Claude Sonnet 4.6
Topology: Chain
Review:   Semi-annual governance review

Expected results:
  ES_score  = 0.84  (EMR = 0.08, PASS)
  CR_score  = 0.60  (T1PR = 0.24, WARN)
  CF_score  = 0.90  (CFR = 0.97, PASS)
  GC_score  = 0.75  (GDR = 2.5 vs target 4.0, WARN)
  Composite = 0.60
  Grade     = C (two WARN, zero FAIL)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gaif4.calculator import assess
from gaif4.report import generate_markdown


def main():
    scorecard = assess(
        emr_interaction=0.08,
        t1pr=0.24,
        cfr=0.97,
        gdr=2.5,
        gdr_risk_level="high",
        pipeline_description=(
            "Four-agent chain (triage, diagnosis, treatment, pharmacy) "
            "using GPT-4o-mini and Claude Sonnet 4.6"
        ),
        topology="chain",
        assessment_passes=3,
    )

    # Print summary
    print("GAIF-4 Worked Example (Specification v1.5, Section 4.4)")
    print("=" * 55)
    print()
    for dim in scorecard.dimensions:
        print(
            f"  {dim.metric_name:<6} raw={dim.raw_value:<8} "
            f"normalized={dim.normalized_score:.2f}  {dim.status}"
        )
    print()
    print(f"  Composite: {scorecard.composite:.2f}")
    print(f"  Grade:     {scorecard.grade}")
    print(f"  Guidance:  {scorecard.guidance}")

    # Verify against specification
    print()
    print("Verification:")
    checks = [
        ("ES_score", scorecard.emr.normalized_score, 0.84),
        ("CR_score", scorecard.t1pr.normalized_score, 0.60),
        ("CF_score", scorecard.cfr.normalized_score, 0.90),
        ("GC_score", scorecard.gdr.normalized_score, 0.75),
        ("Composite", scorecard.composite, 0.60),
    ]
    all_pass = True
    for name, actual, expected in checks:
        match = abs(actual - expected) < 0.005
        status = "OK" if match else "MISMATCH"
        if not match:
            all_pass = False
        print(f"  {name}: {actual:.4f} (expected {expected:.2f}) [{status}]")
    print(f"  Grade: {scorecard.grade} (expected C) "
          f"[{'OK' if scorecard.grade == 'C' else 'MISMATCH'}]")

    if all_pass and scorecard.grade == "C":
        print()
        print("All values match specification. Toolkit is correctly calibrated.")
    else:
        print()
        print("MISMATCH DETECTED. Check formulas.")
        sys.exit(1)

    # Generate report
    report = generate_markdown(scorecard)
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "worked_example_scorecard.md",
    )
    with open(output_path, "w") as f:
        f.write(report)
    print()
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
