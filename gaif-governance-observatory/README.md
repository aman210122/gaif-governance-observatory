# GAIF Governance Observatory

**An open-source toolkit and community-driven database for governing AI systems at enterprise scale.**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19341015.svg)](https://doi.org/10.5281/zenodo.19341015)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## The Problem

Every enterprise deploying AI today faces the same question: *How do we govern systems whose behavior is probabilistic, whose safety degrades through composition, and whose regulatory landscape changes faster than our review cycles?*

Existing frameworks were not built for this. TOGAF assumes deterministic systems. NIST AI RMF tells you what risks to manage but not how to architect for them. ISO 42001 defines a management system, not an architecture. Cloud well-architected frameworks are vendor-specific. None of them give you a computable metric that tells you whether your AI governance is healthy or decaying.

## What GAIF Provides

The **Governed AI Architecture Framework (GAIF)** introduces architectural primitives purpose-built for probabilistic AI systems. This repository provides computable tools that implement those primitives, plus a community-driven database that keeps them current.

### Computable Tools

| Tool | What It Does | Input | Output |
|---|---|---|---|
| **Tier Classifier** | Classifies AI systems by governance tier | Data control, transparency, autonomy scores | Tier A/B/C + governance requirements |
| **GDR Calculator** | Measures governance decay rate | Change events, review cycles, risk tier | GDR score + escalation triggers |
| **AAHI Calculator** | Computes AI Architecture Health Index | Health dimensions per system | AAHI score + operational zone |
| **Composition Safety** | Computes safety budget for multi-agent pipelines | Per-component safety, degradation mode | Max composition hops (n_max) |
| **Composition Cost** | Computes cost budget for AI pipelines | Per-hop costs, amplification factors | Max affordable hops (n_max_cost) |
| **Risk Assessment** | Interactive 25-question AI risk assessment | Answers to structured questions | Risk tier (Critical/High/Medium/Low) |

### Community-Driven Observatory

| Database | What It Contains | How to Contribute |
|---|---|---|
| **Regulatory Database** | Machine-readable AI regulations from 50+ jurisdictions | Encode your country's AI regulation as a JSON tuple |
| **Tier Registry** | GAIF tier classifications for well-known AI platforms | Classify a public AI system with justification |
| **AAHI Weight Profiles** | Industry-specific AAHI dimension weights | Propose weights for your industry with rationale |

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/gaif-governance-observatory.git
cd gaif-governance-observatory
pip install -r requirements.txt

# Classify an AI system
python tools/tier_classifier.py

# Calculate Governance Decay Rate
python tools/gdr_calculator.py

# Run the full AAHI health assessment
python tools/aahi_calculator.py

# Check composition safety budget
python tools/composition_safety.py

# Run the 25-question risk assessment
python tools/risk_assessment.py
```

## Why Contribute?

There is no standardized, machine-readable database of global AI regulations. Every enterprise governance team is manually tracking regulatory changes across dozens of jurisdictions. Every AI architect is making tier classification decisions without a shared reference. Every organization is defining governance health thresholds from scratch.

This repository changes that. Each contribution follows a formal schema derived from a published, DOI-stamped framework specification. Your encoded regulation or tier classification becomes part of a global reference that other practitioners can use immediately.

**Four ways to contribute:**

1. **Encode a regulation** -- Pick an AI regulation from your jurisdiction and encode it as a [Regulatory Policy JSON](docs/regulatory_policy_guide.md)
2. **Classify an AI system** -- Apply the tier classifier to a public AI platform and submit your classification with [justification](docs/tier_classification_guide.md)
3. **Propose industry weights** -- Submit AAHI dimension weights calibrated for your industry with a [rationale document](docs/aahi_weights_guide.md)
4. **Report edge cases** -- Applied a tool and got a surprising result? [Open an Issue](../../issues/new/choose) describing the edge case

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

## Framework Reference

This toolkit implements primitives from the GAIF v1.0 specification:

> Sharma, A. (2026). GAIF: Governed AI Architecture Framework v1.0 -- An AI-Native Enterprise Architecture Framework for Probabilistic, Learning, and Governed AI Systems. Zenodo. https://doi.org/10.5281/zenodo.19341015

Key concepts from the specification:

- [Governance Tiers](docs/governance_tiers.md) -- Three-tier model (Platform, SaaS, Agent) with formal classification
- [Governance Decay Rate](docs/governance_decay_rate.md) -- Quantifying the gap between system change velocity and governance review frequency
- [AI Architecture Health Index](docs/aahi.md) -- Continuously computed governance health score
- [Composition Safety](docs/composition_safety.md) -- Safety degradation modeling for multi-agent pipelines
- [Regulatory Adaptation](docs/regulatory_policy_guide.md) -- Machine-readable regulatory policy encoding

## Repository Structure

```
gaif-governance-observatory/
|-- tools/                          # Computable GAIF tools
|   |-- tier_classifier.py         # Governance tier classification
|   |-- gdr_calculator.py          # Governance Decay Rate computation
|   |-- aahi_calculator.py         # AI Architecture Health Index
|   |-- composition_safety.py      # Composition safety budget
|   |-- composition_cost.py        # Composition cost budget
|   |-- risk_assessment.py         # 25-question risk assessment
|   |-- gaif_core.py               # Shared library for all tools
|
|-- observatory/                    # Community-driven databases
|   |-- regulations/               # Machine-readable AI regulations
|   |   |-- eu/                    # European Union
|   |   |-- us/federal/            # US Federal
|   |   |-- us/states/             # US State-level
|   |   |-- uk/                    # United Kingdom
|   |   |-- india/                 # India
|   |   |-- brazil/                # Brazil
|   |   |-- china/                 # China
|   |-- tier_registry/             # Public AI system classifications
|   |   |-- classifications/       # Individual system classifications
|   |-- aahi_weights/              # Industry-specific AAHI weights
|
|-- dashboard/                      # AAHI visualization dashboard
|-- docs/                           # Documentation
|-- examples/                       # Worked examples
|-- tests/                          # Unit tests
```

## Current Status

| Component | Status | Contributors Needed |
|---|---|---|
| Core tools | v0.1.0 | Feedback and testing |
| EU regulations | 2 encoded | All EU member state implementations |
| US Federal regulations | 2 encoded | Agency-specific guidance (FDA, OCC, SEC) |
| US State regulations | 3 encoded | 47 more states |
| International regulations | 0 encoded | Every jurisdiction welcome |
| Tier classifications | 5 seed entries | All major AI platforms |
| AAHI weights | 1 profile (healthcare) | Financial services, government, manufacturing |
| Dashboard | v0.1.0 | UI/UX improvements |

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

The GAIF framework specification is available under Creative Commons Attribution 4.0 (CC BY 4.0) at [Zenodo](https://doi.org/10.5281/zenodo.19341015).

## Citation

If you use this toolkit or contribute to the observatory, please cite:

```bibtex
@misc{sharma2026gaif,
  author = {Sharma, Aman},
  title = {GAIF: Governed AI Architecture Framework v1.0},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.19341015},
  url = {https://doi.org/10.5281/zenodo.19341015}
}
```

## Contact

- **Author:** Aman Sharma
- **ORCID:** [0009-0005-5107-4485](https://orcid.org/0009-0005-5107-4485)
- **LinkedIn:** [amansharmaarchitect](https://linkedin.com/in/amansharmaarchitect)
