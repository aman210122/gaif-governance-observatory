#!/usr/bin/env python3
"""
GAIF-4 Assessment CLI

Run a GAIF-4 safety assessment from the command line.

Usage:
    python -m gaif4.cli --emr 0.08 --t1pr 0.24 --cfr 0.97 --gdr 2.5
    python -m gaif4.cli --emr 0.08 --t1pr 0.24 --cfr 0.97 --gdr 2.5 --risk high --output report.md
    python -m gaif4.cli --demo
"""

import argparse
import sys

from .calculator import assess
from .report import generate_markdown


def run_demo():
    """Run the worked example from GAIF-4 v1.5 Section 4.4."""
    print("=" * 60)
    print("GAIF-4 WORKED EXAMPLE (Specification v1.5, Section 4.4)")
    print("=" * 60)
    print()
    print("Pipeline: Four-agent chain (triage, diagnosis, treatment,")
    print("          pharmacy) using GPT-4o-mini and Claude Sonnet 4.6")
    print("Topology: Chain")
    print("Review:   Semi-annual governance review")
    print()

    sc = assess(
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

    _print_scorecard(sc)
    print()
    print("Verification against specification:")
    print(f"  ES_score = {sc.emr.normalized_score:.2f}  (expected: 0.84)")
    print(f"  CR_score = {sc.t1pr.normalized_score:.2f}  (expected: 0.60)")
    print(f"  CF_score = {sc.cfr.normalized_score:.2f}  (expected: 0.90)")
    print(f"  GC_score = {sc.gdr.normalized_score:.2f}  (expected: 0.75)")
    print(f"  Composite = {sc.composite:.2f}  (expected: 0.60)")
    print(f"  Grade = {sc.grade}        (expected: C)")


def _print_scorecard(sc):
    """Print scorecard to terminal."""
    print("-" * 60)
    print(f"  GRADE: {sc.grade}     COMPOSITE: {sc.composite:.2f}")
    print("-" * 60)
    print()
    print(f"  {'Dimension':<25} {'Raw':>8} {'Norm':>8} {'Status':>8}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8}")

    for dim in sc.dimensions:
        if dim.metric_name == "T1PR":
            raw_str = f"{dim.raw_value:.0%}"
        elif dim.metric_name == "GDR":
            raw_str = f"{dim.raw_value:.1f}"
        else:
            raw_str = f"{dim.raw_value:.3f}"
        print(
            f"  {dim.metric_name:<25} {raw_str:>8} "
            f"{dim.normalized_score:>8.3f} {dim.status:>8}"
        )

    print()
    print(f"  GDR Risk Level: {sc.gdr_risk_level.capitalize()}")
    print(f"  GDR Coverage Target: {sc.gdr_coverage_target:.1f}")
    print()
    print(f"  Guidance: {sc.guidance}")


def main():
    parser = argparse.ArgumentParser(
        description="GAIF-4 Clinical AI Safety Assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m gaif4.cli --demo\n"
            "  python -m gaif4.cli --emr 0.08 --t1pr 0.24 "
            "--cfr 0.97 --gdr 2.5\n"
            "  python -m gaif4.cli --emr 0.30 --t1pr 0.45 "
            "--cfr 0.80 --gdr 5.0 --risk critical --output report.md\n"
        ),
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the worked example from GAIF-4 v1.5 Section 4.4",
    )
    parser.add_argument(
        "--emr", type=float,
        help="EMR_interaction value [0, 1]",
    )
    parser.add_argument(
        "--t1pr", type=float,
        help="Tier-1 Propagation Rate [0, 1]",
    )
    parser.add_argument(
        "--cfr", type=float,
        help="Compliance Fidelity Rate [0, 1]",
    )
    parser.add_argument(
        "--gdr", type=float,
        help="Governance Decay Rate (changes/reviews)",
    )
    parser.add_argument(
        "--risk", type=str, default="high",
        choices=["critical", "high", "medium", "low"],
        help="GDR risk level for coverage target (default: high)",
    )
    parser.add_argument(
        "--pipeline", type=str, default="",
        help="Pipeline description for the report",
    )
    parser.add_argument(
        "--topology", type=str, default="",
        help="Pipeline topology (chain, fc, star)",
    )
    parser.add_argument(
        "--passes", type=int, default=1,
        help="Number of assessment passes run (default: 1)",
    )
    parser.add_argument(
        "--output", type=str, default="",
        help="Output file path for markdown report (optional)",
    )

    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if any(v is None for v in [args.emr, args.t1pr, args.cfr, args.gdr]):
        print(
            "Error: All four metrics required (--emr, --t1pr, --cfr, --gdr)."
        )
        print("Use --demo to run the worked example.")
        parser.print_help()
        sys.exit(1)

    sc = assess(
        emr_interaction=args.emr,
        t1pr=args.t1pr,
        cfr=args.cfr,
        gdr=args.gdr,
        gdr_risk_level=args.risk,
        pipeline_description=args.pipeline,
        topology=args.topology,
        assessment_passes=args.passes,
    )

    _print_scorecard(sc)

    if args.output:
        report = generate_markdown(sc)
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\n  Report saved to: {args.output}")


if __name__ == "__main__":
    main()
