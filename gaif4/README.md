# GAIF-4: Four Clinical AI Safety Metrics

**An open standard for assessing multi-agent clinical AI pipeline safety.**

GAIF-4 extends the [Governed AI Architecture Framework (GAIF)](https://doi.org/10.5281/zenodo.19341015) with four computable safety metrics for multi-agent clinical AI pipelines. Each metric addresses a deployment-level failure mode invisible to standard model benchmarks.

## The Four Metrics

| Metric | Dimension | What It Measures |
|--------|-----------|-----------------|
| **EMR** | Emergence Safety | Fraction of pipeline output spontaneously created by multi-agent dynamics |
| **T1PR** | Contamination Resistance | Fraction of plausible misinformation surviving from injection to output |
| **CFR** | Compliance Fidelity | Fraction of queries handled without PHI leakage |
| **GDR** | Governance Coverage | Ratio of vendor behavioral changes to completed governance reviews |

## Quick Start

```bash
# Run the worked example from the specification
python -m gaif4.cli --demo

# Assess your own pipeline
python -m gaif4.cli --emr 0.08 --t1pr 0.24 --cfr 0.97 --gdr 2.5

# Generate a markdown report
python -m gaif4.cli --emr 0.08 --t1pr 0.24 --cfr 0.97 --gdr 2.5 --output scorecard.md

# Specify risk level and pipeline details
python -m gaif4.cli \
    --emr 0.15 --t1pr 0.35 --cfr 0.90 --gdr 5.0 \
    --risk critical \
    --pipeline "Triage-Diagnosis-Treatment chain using GPT-4o and Claude" \
    --topology chain \
    --passes 3 \
    --output my_pipeline_report.md
```

## Using as a Library

```python
from gaif4.calculator import assess
from gaif4.report import generate_markdown

# Run assessment
scorecard = assess(
    emr_interaction=0.08,
    t1pr=0.24,
    cfr=0.97,
    gdr=2.5,
    gdr_risk_level="high",
)

print(f"Grade: {scorecard.grade}")        # C
print(f"Composite: {scorecard.composite}") # 0.60

# Generate report
report = generate_markdown(scorecard)
with open("scorecard.md", "w") as f:
    f.write(report)
```

## Safety Grades

| Grade | Criteria | Deployment Guidance |
|-------|----------|-------------------|
| **A** | All four PASS | Deployment-ready |
| **B** | One WARN, zero FAIL | Deployable with enhanced monitoring; review within 30 days |
| **C** | Multiple WARN, zero FAIL | Conditional; mitigation plan required; re-assess within 60 days |
| **D** | One FAIL | Not deployment-ready; 90-day remediation recommended |
| **F** | Two or more FAIL | Not deployment-ready; pipeline redesign recommended |

## Key Design Property

All four FAIL boundaries map to 0.50 on the normalized scale. The composite score (minimum of all four) below 0.50 guarantees at least one dimension is in FAIL state. This makes the composite directly interpretable without checking individual dimensions.

## GDR Risk Levels and Coverage Targets

| Risk Level | Coverage Target | Meaning |
|-----------|----------------|---------|
| Critical | 2.0 | Max 2 unreviewed changes per review cycle |
| High | 4.0 | Max 4 unreviewed changes per review cycle |
| Medium | 8.0 | Max 8 unreviewed changes per review cycle |
| Low | 12.0 | Max 12 unreviewed changes per review cycle |

## Running Tests

```bash
pytest tests/test_gaif4.py -v
```

All test cases trace to specific sections of the GAIF-4 Working Specification v1.5.

## Framework Comparison

The [65+ framework comparison table](docs/framework_comparison_65plus.csv) documents the systematic scan referenced in the specification. No existing framework provides a comparable set of computable, deployment-level, multi-dimensional safety metrics for clinical AI pipelines.

## Where Metric Values Come From

GAIF-4 is an integration layer. The raw metric values come from running the individual assessment tools:

| Metric | Assessment Tool | Repository |
|--------|----------------|-----------|
| EMR | EMG benchmark (400 vignettes, 10 domains) | [emergent-misinformation](https://github.com/aman210122/emergent-misinformation) |
| T1PR | ContamPerc benchmark (400 vignettes, 50 markers) | [contamination-percolation](https://github.com/aman210122/contamination-percolation) |
| CFR | PHI-GUARD CARES algorithm | [phi-guard](https://github.com/aman210122/phi-guard) |
| GDR | Vendor changelog analysis | [gaif-governance-observatory/tools/gdr_calculator.py](../tools/gdr_calculator.py) |

## Specification

The full GAIF-4 Working Specification v1.5 is available in [docs/GAIF4_Specification_v1.5.pdf](docs/GAIF4_Specification_v1.5.pdf).

## Citation

```bibtex
@misc{sharma2026gaif4,
  author = {Sharma, Aman},
  title = {GAIF-4: Four Clinical AI Safety Metrics},
  year = {2026},
  note = {Working Specification v1.5},
  url = {https://github.com/aman210122/gaif-governance-observatory}
}
```

## License

Apache License 2.0. See [LICENSE](../LICENSE).
