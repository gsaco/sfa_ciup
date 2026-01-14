# Robustness summary

## Executive takeaways
- Diversificacion effects are stable across specifications: SFA inefficiency coefficients remain negative and significant, and logit odds ratios remain large and significant.
- Size interactions keep the same sign pattern in SFA (mediano positive, grande negative) and remain statistically weak in logit.
- Sample loss after adding temperature/topography is below 0.1% overall (see `outputs/tables/sample_loss_analysis.csv`).

## SFA (inefficiency equation)
- Baseline (M1): Z_diversificacion_area = -14.93 (p < 1e-15).
- + Controles ENA (M2): Z_diversificacion_area = -14.86 (p ~ 0).
- + Temp/topo (M3): Z_diversificacion_area = -35.06 (p = 3.7e-4).
- + Controles ENA + temp/topo (M4): Z_diversificacion_area = -102.12 (p ~ 0).
- Size interactions stay aligned across models: Z_diversif_mediano > 0 and Z_diversif_grande < 0 (see `outputs/tables/15_sfa_compare_effects_all.csv`).

Interpretation: higher diversification is associated with lower inefficiency in all SFA specifications; the sign pattern is unchanged with added controls.

## Logit (practicas sostenibles)
- Baseline (L1): diversificacion_area coef 2.74, OR 15.46 (p = 2e-6).
- + Controles ENA (L2): coef 2.65, OR 14.09 (p = 5e-6).
- + Temp/topo (L3): coef 2.49, OR 12.03 (p = 1.3e-4).
- + Controles ENA + temp/topo (L4): coef 2.38, OR 10.84 (p = 2.1e-4).
- Interactions with size are negative but not significant in any model (see `outputs/tables/18_logit_compare_effects_all.csv`).

Interpretation: diversification remains strongly and positively associated with adoption of practicas sostenibles after adding ENA and geo-climate controls.

## Sample composition
- Logit sample: 34,074 baseline vs 34,051 with geo2 (share remaining 0.9993).
- SFA sample: 31,824 baseline vs 31,804 with geo2 (share remaining 0.9994).
- Losses are small and balanced across region and size (see `outputs/tables/sample_loss_analysis.csv`).

## Collinearity and specification choice
- Potential collinearity exists between temperature/topography and region_natural, but coefficient signs and significance for diversification are stable across models.
- Preferred specification: M4/L4 (controls + temp/topo) when convergence is stable, because it adds key ENA controls and exogenous geo-climate factors with minimal sample loss.
- Fallback: M2/L2 when temperature/topography are unavailable.
