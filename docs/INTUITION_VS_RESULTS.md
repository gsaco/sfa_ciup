# Intuition vs Results

## Expected Economic Mechanisms
- **Diversification and efficiency:** Diversification can improve resilience and input smoothing (positive TE), but may reduce specialization/scale economies (negative TE), especially for larger farms.
- **Practices adoption:** Higher diversification could proxy for knowledge/capital and correlate with adopting more practices.
- **Inputs:** Land, labor, and inputs should have positive elasticities in the production frontier.

## Observed Results (Baseline)
- **SFA (main):** `Z_diversificacion_area` < 0 suggests diversification reduces inefficiency (higher TE), but interactions by size are large and mixed. TE-diversification correlation is slightly negative (-0.039).
- **Logit (practice_any):** Diversification is strongly positive (odds ratio ~15), but practice_any is ~95% overall.
- **Size:** TE declines with size category (small > medium > large), consistent with potential management constraints on larger units.
- **Region:** Region 3 has lower TE and lower practice_any prevalence.

## Mismatches / Tensions
- **Diversification vs TE:** Coefficients imply efficiency gains, but raw TE-diversification correlation is weak/negative; interactions dominate, suggesting heterogeneity that should be emphasized instead of a single "positive" effect.
- **Practice_any saturation:** With 95% prevalence, odds ratios are inflated and interpretation as "sustainable practice adoption" is fragile.
- **Size interactions:** The large magnitude of Z interactions implies strong heterogeneity; this may not align with a simple linear intuition.

## Reconciliation
- Interpret diversification effects as **heterogeneous and size-specific**, not uniform.
- Clarify that the outcome definition aggregates practices with varying sustainability; consider a stricter subset for sensitivity.
- Present regional differences as structural constraints rather than purely behavior-driven.

