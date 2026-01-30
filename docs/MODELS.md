# Models

## Stochastic Frontier (SFA)
- **Package**: `frontier` (R).
- **Output (Y)**: `log(valor_total)` with `valor_total` = sum of crop value components (S/).
- **Inputs (X)**:
  - `log(area_total_ha)`
  - `log(labor_total + 1)`
  - `log(input_costs_sfa + 1)` where `input_costs_sfa` prefers `costo_total_agropecuario` (fallback `gasto_agricola_total`, then component-sum `input_costs`).
- **Inefficiency (u) specification**:
  - Diversification: `diversificacion_area` (1 − HHI based on harvested area).
  - Size categories: `size_mediano`, `size_grande` (small as baseline).
  - Interactions: `diversificacion_area × size_mediano`, `diversificacion_area × size_grande`.
  - **Region dummies** (`region_natural`) are included in the inefficiency equation (not in X).
- **Weights**: `frontier` does not accept survey weights; results are unweighted and noted as a limitation.
- **Diagnostics**: `outputs/tables/02_sfa_diagnostics.*` (gamma, covariance, sample used, input cost variable).
- **Outputs**: `outputs/tables/02_sfa_main.*`, `outputs/tables/03_sfa_robustness.*`, and `data/processed/ena2024_with_TE.parquet`.
- **Geo/climate robustness**:
  - XGEO: adds `prcp_total_z` (CHIRPS) and `log_surface_km2` to X.
  - ZGEO: adds `prcp_total_z` to inefficiency (Z).
  - Temp/topo: X adds `tmean_2024`, `delta_tmean_24_23`, `slope_deg`, `ruggedness`, `prcp_total_z` (elevation is excluded to avoid rank deficiency).
  - Outputs: `outputs/tables/07_sfa_with_geo_controls.*` and `outputs/tables/14_sfa_with_temp_topo.*`.

## Logit (survey-weighted)
- **Package**: `survey` (R).
- **Outcome**: `practice_any` = 1 if producer reports ≥1 practice among `P301A_1`, `P301A_2`, `P301A_3`, `P301A_4`, `P301A_4A`, `P301A_4B`, `P301A_4C`, `P301A_11`, `P301A_16`, `P301A_17`.
- **Specification**:
  - Main: `practice_any ~ diversificacion_area * size_cat + log(area_total_ha + 1) + region_natural`.
  - Robustness: alternative diversification indices (`shannon_area`, `num_crops_area`), stricter outcome (`num_practices >= 2`), and small-producer subsample.
- **Survey design**: `weights = FACTOR_PRODUCTOR`, `strata = ESTRATO`, `PSU = NSEGM` (with lonely PSU adjustment).
- **Outputs**: `outputs/tables/04_logit_main.*`, `outputs/tables/05_logit_robustness.*`.
- **Geo/climate robustness**:
  - Adds `prcp_total_z` to the main specification.
  - Outputs: `outputs/tables/09_logit_with_geo_controls.*` and `outputs/tables/10_logit_compare_main_effects.*`.

## Controls (ENA) used in models
- **Included (high completeness)**: `nivel_educacion`, `capacitacion_recibida`, `asistencia_tecnica_recibida`, `usuario_agua`, `asociacion_miembro`, `riego_any`, `uso_maquinaria`, `usa_abono`, `usa_fertilizantes`, `semilla_semillero_any`, `semilla_comercial_any`.
- **Excluded from main controls (high missingness)**: `credito_obtenido`, `riego_tecnificado_any/share`, `gasto_semilla`, `semilla_certificada_*`, `num_maquinaria_equipo`. These appear only in robustness or are omitted to preserve sample size.
