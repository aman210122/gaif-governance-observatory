# Governance Decay Rate (GDR)

## The Problem

AI systems change faster than governance reviews happen. A vendor API that updates its model weekly under annual vendor review has 51 ungoverned changes per year. GAIF calls this gap governance decay.

## The Formula

```
GDR(S, t) = C(S, t) / max(G(S, t), 1)
```

Where:
- C(S, t) = number of change events for system S in period t
- G(S, t) = number of governance reviews completed in the same period

A GDR of 1.0 means every change happens within a review cycle. A GDR of 9.0 means 9 changes per review, with 8 ungoverned.

## Change Events Include

- Model retraining or fine-tuning
- Vendor API model version updates
- Prompt template modifications
- Data pipeline changes
- Configuration updates
- Feature store refreshes

## Thresholds

| Risk Tier | GDR Threshold | Rationale |
|---|---|---|
| Critical | 2.0 | At most 2 changes per review cycle |
| High | 4.0 | At most 4 changes per review cycle |
| Medium | 8.0 | At most 8 changes per review cycle |
| Low | 12.0 | At most 12 changes per review cycle |

## Escalation

- **Stage 1** (GDR > threshold): Activate automated monitoring proportional to overshoot
- **Stage 2** (GDR > 2x threshold): Accelerate governance review cadence to next tier

## Using the Tool

```bash
python tools/gdr_calculator.py
```

## Reference

GAIF v1.0, Section 4.5.7. https://doi.org/10.5281/zenodo.19341015
