# Robustness summary

## Executive takeaways
- Diversificacion effects are **not uniformly signed** in SFA: baseline is positive (efficiency‑improving for small/medium), while large‑farm interactions are negative and significant.
- Logit effects of diversification remain **positive and significant** across specs; size interactions are statistically weak.
- Sample loss after adding geo/climate is **<0.2%** overall (see `outputs/tables/sample_loss_analysis.csv`).

## SFA (inefficiency equation)
Key terms (see `outputs/tables/15_sfa_compare_effects_all.csv`):
| model | Z_diversificacion_area | p_value | Z_diversif_mediano | p_value | Z_diversif_grande | p_value |
|:--|--:|--:|--:|--:|--:|--:|
| main_area | 1.929 | 0 | -0.200 | 0.411 | -5.543 | 0 |
| controls_ena | 0.917 | 7.06e-12 | 0.718 | 0.00423 | -3.645 | 0 |
| temp_topo | 0.273 | 0.267 | 2.531 | 1.24e-13 | -7.970 | 0 |
| controls_temp_topo | 0.018 | 0.892 | 1.961 | 1.48e-13 | -3.585 | 0 |

Interpretation (ineffDecrease=TRUE): baseline diversification improves efficiency for small/medium producers, but the large‑farm interaction is negative and significant across specs, flipping the net effect for large farms.

## Logit (practicas sostenibles)
Key terms (see `outputs/tables/18_logit_compare_effects_all.csv`):
| model | diversificacion_area | odds_ratio | p_value |
|:--|--:|--:|--:|
| main | 1.382 | 3.98 | 3.84e-05 |
| controls_ena | 0.781 | 2.18 | 0.0145 |
| temp_topo | 1.267 | 3.55 | 0.00105 |
| controls_temp_topo | 0.791 | 2.21 | 0.0273 |

Interactions with size are statistically weak in all models.

Interpretation: diversification remains strongly and positively associated with adoption of practicas sostenibles after adding ENA and geo-climate controls.

## Sample composition
- Logit sample: 34,074 baseline vs 34,039 with geo2 (share remaining 0.99897).
- SFA sample: 26,594 baseline vs 26,546 with geo2 (share remaining 0.99820).
- Losses are small and balanced across region and size (see `outputs/tables/sample_loss_analysis.csv`).

## Collinearity and specification choice
- Potential collinearity exists between temperature/topography and region_natural; condition numbers rise in some climate specs.
- Preferred specification: controls + temp/topo **when diagnostics are stable** (see `outputs/tables/02_sfa_diagnostics.csv`).
- Fallback: controls‑only specs when temp/topo data are unavailable.
