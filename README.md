# GAIF Governance Observatory

**Measure, monitor, and enforce governance in multi-agent LLM systems.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-59%20passing-brightgreen.svg)](#testing)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19378438-blue.svg)](https://doi.org/10.5281/zenodo.19378438)

---

## The Problem

You built a multi-agent LLM pipeline. Each agent passes safety checks individually. But when they work together, bad things happen: fabricated drug interactions, hallucinated clinical guidelines, compliance violations that no single agent caused.

**Per-agent governance does not compose into system-level governance.** This is not a theory. In experiments across 4,800+ clinical trials, we found 74 critical drug interaction events that emerged only at the pipeline level, invisible to any single-agent test.

GAIF (Governance AI Framework) gives you the tools to detect, measure, and prevent this.

---

## What GAIF Does

GAIF-4 defines four quantitative metrics that measure governance health across your multi-agent pipeline:

| Metric | What It Measures | Why It Matters |
|--------|-----------------|----------------|
| **EMR** (Emergent Misinformation Rate) | How often your pipeline generates clinically dangerous content that no single agent would produce alone | Catches "collective delusion" behavior |
| **T1PR** (Type-1 Pass Rate) | Rate at which contaminated outputs pass downstream safety filters | Reveals governance blind spots |
| **CFR** (Compliance Failure Rate) | Proportion of outputs violating regulatory or policy constraints | Maps directly to HIPAA/FDA risk |
| **GDR** (Governance Decay Rate) | How fast governance effectiveness degrades over time or across pipeline stages | Early warning system for governance rot |

---

## Quick Start

### Install

```bash
git clone https://github.com/aman210122/gaif-governance-observatory.git
cd gaif-governance-observatory
pip install -r requirements.txt
```

### Run Your First Governance Audit

```bash
# Score a pipeline output against GAIF-4 metrics
python tools/gaif_scorer.py --input data/sample_pipeline_output.json

# Check governance decay across pipeline stages
python tools/gdr_calculator.py --input data/sample_multi_stage.json

# Generate a full governance report
python tools/governance_report.py --input data/sample_pipeline_output.json --output report.json
```

### Example Output

```
GAIF-4 Governance Scorecard
============================
EMR:  0.0154  (74 events / 4,800 trials)
T1PR: 0.23    (23% contaminated outputs passed filters)
CFR:  0.0     (zero compliance violations detected)
GDR:  0.031   (3.1% governance decay per stage)

Overall Risk Level: MODERATE
Recommendation: Review T1PR threshold; pipeline filters are under-catching contaminated content.
```

---

## CLI Tools

The observatory ships with six command-line tools:

| Tool | Purpose |
|------|---------|
| `gaif_scorer.py` | Compute all four GAIF-4 metrics for a pipeline run |
| `gdr_calculator.py` | Measure governance decay across pipeline stages |
| `emr_detector.py` | Detect emergent misinformation events in multi-agent outputs |
| `t1pr_analyzer.py` | Analyze Type-1 pass rates and filter effectiveness |
| `compliance_checker.py` | Check outputs against configurable compliance rule sets |
| `governance_report.py` | Generate a full governance scorecard with recommendations |

---

## How It Maps to Standards

GAIF does not replace existing AI governance frameworks. It makes them measurable.

| Standard | GAIF Connection |
|----------|----------------|
| **NIST AI RMF** | GAIF metrics operationalize GOVERN and MEASURE functions with quantitative thresholds |
| **WHO AI Ethics** | CFR maps directly to WHO's transparency and accountability principles |
| **CHAI Blueprint** | EMR and T1PR address CHAI's requirements for clinical AI safety monitoring |
| **EU AI Act** | GDR provides the continuous monitoring required for high-risk AI systems |

See [`NIST-AI-RMF-Mapping.md`](NIST-AI-RMF-Mapping.md) for the full crosswalk.

---

## Research Behind This

GAIF grew out of independent research on multi-agent LLM safety in healthcare. Key findings that shaped these tools:

- **74 critical drug interaction events** emerged across 4,800 trials when LLM agents collaborated, even though each agent individually passed safety checks
- **The most safety-trained model produced the worst drug interactions** at the pipeline level, showing that single-agent alignment does not guarantee system-level safety
- **Governance effectiveness is model-dependent, not framework-dependent**, meaning the same governance rules work differently depending on which models are in your pipeline

### Related Papers (all solo-authored by Aman Sharma)

- **EMG**: "Emergent Misinformation Genesis in Multi-Agent LLM Clinical Pipelines" | [Zenodo](https://doi.org/10.5281/zenodo.19411743) | ~97K API calls, 4 model families, MIMIC-IV data
- **PHI-GUARD**: Compliance-aware LLM routing using CARES algorithm | [TechRxiv](https://doi.org/10.36227/techrxiv.177220388.80392106/v1) | Under review at IEEE JBHI
- **ContamPerc**: Contamination percolation in multi-agent LLM systems | Under review at IEEE Access | ~210K API calls
- **GDR**: "Continuous Architecture Assurance: Measuring Governance Decay" | Under review at IEEE Software
- **GNC**: Governance Non-Compositionality | Targeting NeurIPS 2026

---

## Data

The repository includes 14 JSON data files drawn from experiments on MIMIC-IV clinical data, covering multi-agent pipeline outputs, governance metric calculations, and compliance audit results.

---

## Testing

```bash
# Run the full test suite
python -m pytest tests/ -v

# 59 tests covering all CLI tools and metric calculations
```

---

## Use Cases

**If you are building multi-agent LLM systems** in healthcare, finance, legal, or any regulated industry, GAIF helps you answer:

- Are my agents safe individually but dangerous together?
- How fast is my governance decaying as my pipeline scales?
- Which model combinations create the highest compliance risk?
- Can contaminated content from one agent survive downstream safety filters?

**If you are a researcher** studying LLM safety, multi-agent coordination, or AI governance, GAIF gives you reproducible metrics to compare governance effectiveness across different architectures and model families.

**If you are a regulator or policy maker**, GAIF provides the quantitative bridge between high-level governance principles (NIST, WHO, EU AI Act) and measurable system behavior.

---

## Contributing

Contributions are welcome. If you are working on multi-agent LLM governance and want to extend GAIF metrics, add new compliance rule sets, or test against different model families, please open an issue or submit a pull request.

---

## Citation

If you use GAIF in your research or work, please cite:

```bibtex
@software{sharma2026gaif,
  author = {Sharma, Aman},
  title = {GAIF: Governance AI Framework for Multi-Agent LLM Systems},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.19378438},
  url = {https://github.com/aman210122/gaif-governance-observatory}
}
```

---

## Author

**Aman Sharma**
Principal Enterprise Architect, AI/ML | Blue Shield of California
[LinkedIn](https://linkedin.com/in/amansharmaarchitect) | [ORCID](https://orcid.org/0009-0005-5107-4485) | [Email](mailto:Aman_sharma007@yahoo.com)

---

## License

MIT License. See [LICENSE](LICENSE) for details.
