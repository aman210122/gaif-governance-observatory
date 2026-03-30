# GAIF Governance Tiers

## The Three-Tier Model

GAIF classifies every AI deployment into one of three governance tiers based on three measurable attributes.

### Attributes

| Attribute | Values | What It Measures |
|---|---|---|
| **D (Data Control)** | 0 = Full control, 1 = Third-party with contracts, 2 = Variable/mixed | How much control your organization has over the data |
| **T (Model Transparency)** | 0 = Full visibility, 1 = API-only, 2 = Partial | How much you can see into the model |
| **A (Autonomy Level)** | 0 = Invoked only, 1 = Vendor API, 2 = Autonomous | How independently the system operates |

### Classification Rules

```
if A == 2:  -> Tier C (autonomous agents always require Tier C)
if A == 0 and D == 0:  -> Tier A (non-autonomous + full control = internal platform)
otherwise:  -> Tier B (everything else)
```

### Why T Does Not Affect Tier Assignment

T determines governance intensity within a tier, not the tier itself. A Tier B system with T=0 (open-source model on vendor infrastructure) and T=1 (black-box vendor API) both need Tier B governance patterns. But the T=0 system allows deeper behavioral contract verification. This is captured through the risk assessment (questions M3, M4), not through tier assignment.

### Quick Reference

| Tier | Description | Example | Governance Approach |
|---|---|---|---|
| **Tier A** | Governed AI Platform | Custom model on Databricks | Direct: model registry, CI/CD gates, internal review |
| **Tier B** | Managed SaaS AI | OpenAI API, Azure OpenAI | Contractual: vendor agreements, SLAs, output monitoring |
| **Tier C** | Agent Platform | LangGraph agents, Bedrock Agents | Compositional: agent permissions, human checkpoints, trust boundaries |

## Using the Tool

```bash
python tools/tier_classifier.py
```

See the [tier registry](../observatory/tier_registry/) for example classifications of well-known AI systems.

## Reference

GAIF v1.0, Section 5.1.1. https://doi.org/10.5281/zenodo.19341015
