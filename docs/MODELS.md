# Models

## Stochastic Frontier (SFA)
- **Package**: `frontier` (R).
- **Output (Y)**: `log(valor_total)` with `valor_total` = sum of crop value components (S/).
- **Inputs (X)**: `log(area_total_ha)`, `log(labor_total + 1)`, `log(input_costs + 1)`.
- **Controls**: Region fixed effects (`region_natural` dummies).
- **Inefficiency (u) specification**:
  - Diversification: `diversificacion_area` (1 − HHI based on harvested area).
  - Size categories: `size_mediano`, `size_grande` (small as baseline).
  - Interaction: `diversificacion_area × size_mediano`, `diversificacion_area × size_grande`.
- **Weights**: `frontier` does not accept survey weights; results are unweighted and noted as a limitation.
- **Outputs**: `outputs/tables/02_sfa_main.*`, `outputs/tables/03_sfa_robustness.*`, and `data/processed/ena2024_with_TE.parquet`.

## Logit (survey-weighted)
- **Package**: `survey` (R).
- **Outcome**: `practice_any` = 1 if producer reports ≥1 agricultural practice (`P301A_*`).
- **Specification**:
  - Main: `practice_any ~ diversificacion_area * size_cat + log(area_total_ha + 1) + region_natural`.
  - Robustness: alternative diversification indices (`shannon_area`, `num_crops_area`), stricter outcome (`num_practices >= 2`), and small-producer subsample.
- **Survey design**: `weights = FACTOR_PRODUCTOR`, `strata = ESTRATO`, `PSU = NSEGM` (with lonely PSU adjustment).
- **Outputs**: `outputs/tables/04_logit_main.*`, `outputs/tables/05_logit_robustness.*`.
