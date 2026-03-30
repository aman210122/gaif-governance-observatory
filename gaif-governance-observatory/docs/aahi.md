# AI Architecture Health Index (AAHI)

## The Problem

When someone asks "How healthy is our AI governance?" the answer today is a qualitative narrative. AAHI provides a continuously computed number.

## The Formula

```
AAHI(t) = Sum(w_i * H(S_i, t)) / Sum(w_i)
```

Where H(S_i, t) is the per-system health score and w_i is the risk-based weight.

## Six Health Dimensions

| Dimension | Source | Formula |
|---|---|---|
| Governance Velocity | FF-1 | h_gov = max(0, 1 - GDR/GDR_max) |
| Behavioral Compliance | FF-2 | 1.0 when all contracts satisfied, decreases with drift |
| Composition Safety | FF-3 | h_comp = S_actual / S_required (Tier C only) |
| Trust Integrity | FF-4 | Binary: 1 if all invariants hold, 0 if violated (Tier C only) |
| Supply Chain | AI-BOM | Proportion of AI-BOM elements that are current |
| Cost Compliance | FF-6 | h_cost = max(0, 1 - C_actual/C_max) |

## Operational Zones

| Zone | AAHI Range | Status | Action |
|---|---|---|---|
| Green | >= 0.8 | Healthy | Routine monitoring |
| Yellow | 0.6 - 0.8 | Degrading | Increase monitoring, governance attention report |
| Orange | 0.4 - 0.6 | Intervention needed | Escalation, freeze deployments, emergency review |
| Red | < 0.4 | Crisis | Executive escalation, suspend Tier C, incident response |

## Floor Constraint

If any dimension scores below 0.3 for a Critical or High tier system, AAHI is capped at Yellow (max 0.79) regardless of the weighted average. This prevents masking critical failures.

## Using the Tool

```bash
python tools/aahi_calculator.py
```

## Reference

GAIF v1.0, Section 6.7. https://doi.org/10.5281/zenodo.19341015
