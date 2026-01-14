# Plot Manifest

All plots are saved as both `.png` (300 dpi) and `.pdf` with the same base filename.

## 01_data_quality/hist_log_valor_total
- purpose: Check distribution of log output value and confirm scale.
- data used + filters: `data/processed/model_data_ena2024.parquet`; `valor_total > 0`; log applied.
- takeaway: Heavy right tail with log range ~0.69-15.77.
- validation checks performed: Verified log range from data; confirmed zeros excluded in log.

## 01_data_quality/diversification_distributions
- purpose: Compare distributions of diversification indices and crop counts.
- data used + filters: `data/processed/model_data_ena2024.parquet`; no filters beyond missing handling in plotting.
- takeaway: Diversification bounded within [0,1]; shannon and num_crops show right tails.
- validation checks performed: Verified min/max for `diversificacion_area` (0-0.977), `shannon_area` (0-3.97), `num_crops_area` (1-28).

## 01_data_quality/diversif_vs_num_crops
- purpose: Verify monotonic relationship between diversification and crop count.
- data used + filters: `data/processed/model_data_ena2024.parquet`; drop missing for both variables.
- takeaway: Positive association with dispersion at higher crop counts.
- validation checks performed: Checked ranges of both axes and absence of out-of-bounds values.

## 01_data_quality/cost_input_costs_log1p
- purpose: Diagnose heavy tails in `input_costs` and zero mass.
- data used + filters: `data/processed/model_data_ena2024.parquet`; log1p transform.
- takeaway: Large mass at zero with extreme outliers.
- validation checks performed: Computed share_zero=0.159, p99=270,283, max=33,612,372.

## 01_data_quality/cost_irrigation_cost_log1p
- purpose: Diagnose heavy tails in irrigation cost.
- data used + filters: `data/processed/model_data_ena2024_plus_controls.parquet`; log1p transform of `gasto_agua_riego`.
- takeaway: High zero mass and extreme max values.
- validation checks performed: Computed share_zero=0.528, p99=21,600, max=53,390,360.

## 01_data_quality/cost_seed_log1p
- purpose: Diagnose heavy tails in seed cost.
- data used + filters: `data/processed/model_data_ena2024_plus_controls.parquet`; log1p transform of `gasto_semilla`.
- takeaway: Moderate zero mass with long right tail.
- validation checks performed: Computed share_zero=0.316, p99=28,563, max=14,052,113.

## 01_data_quality/cost_capital_log1p
- purpose: Diagnose heavy tails in capital expenditures.
- data used + filters: `data/processed/model_data_ena2024_plus_controls.parquet`; log1p of `capital_total` (sum of machinery/equipment costs).
- takeaway: Strong zero mass and very large outliers.
- validation checks performed: Computed share_zero=0.709, p99=18,914, max=43,887,278.

## 01_data_quality/practice_any_by_region
- purpose: Check outcome prevalence by region.
- data used + filters: `data/processed/model_data_ena2024.parquet`; mean of `practice_any`.
- takeaway: Very high practice_any in regions 1-2; lower in region 3.
- validation checks performed: Verified mean by region against table 00 and summary stats.

## 01_data_quality/practice_any_by_size
- purpose: Check outcome prevalence by size category.
- data used + filters: `data/processed/model_data_ena2024.parquet`; mean of `practice_any`.
- takeaway: High prevalence across sizes, slightly lower for large farms.
- validation checks performed: Verified means vs computed group averages.

## 01_data_quality/num_practices_hist
- purpose: Examine distribution of practice counts.
- data used + filters: `data/processed/model_data_ena2024.parquet`; `num_practices`.
- takeaway: Mode around 6-8; right tail up to 21.
- validation checks performed: Verified min/max (0-21).

## 01_data_quality/usuario_agua_practice_any_heatmap
- purpose: Detect near-determinism between `usuario_agua` and `practice_any`.
- data used + filters: `data/processed/model_data_ena2024_plus_controls.parquet`; row-normalized crosstab.
- takeaway: `usuario_agua=1` almost always implies `practice_any=1`.
- validation checks performed: Verified crosstab row shares and counts.

## 02_geospatial/map_prcp_total_z
- purpose: Validate CHIRPS anomaly distribution and spatial orientation.
- data used + filters: `data/processed/model_data_ena2024_plus_geo.parquet`; drop missing coords and `prcp_total_z`.
- takeaway: Spatial gradient consistent with expected coast/sierra/selva patterns.
- validation checks performed: Checked lat/lon bounds (-18.3 to -1.0, -81.3 to -68.9) and `prcp_total_z` range (-4.92 to 3.21).

## 02_geospatial/map_tmean_2024
- purpose: Validate temperature surface and spatial orientation.
- data used + filters: `data/processed/model_data_ena2024_plus_geo2.parquet`; drop missing coords and `tmean_2024`.
- takeaway: Temperature varies plausibly with latitude/altitude.
- validation checks performed: Checked lat/lon bounds and `tmean_2024` range (6.85-28.45 C).

## 02_geospatial/map_elev_m
- purpose: Validate elevation surface and spatial orientation.
- data used + filters: `data/processed/model_data_ena2024_plus_geo2.parquet`; drop missing coords and `elev_m`.
- takeaway: Andes relief visible with high elevations inland.
- validation checks performed: Checked lat/lon bounds and `elev_m` range (3.5-4359 m).

## 02_geospatial/map_external_coverage
- purpose: Visualize spatial coverage for external layers (CHIRPS, temperature, topography).
- data used + filters: `data/processed/model_data_ena2024_plus_geo2.parquet`; drop missing coords.
- takeaway: Coverage gaps concentrated in a small subset of districts.
- validation checks performed: Verified match rates (CHIRPS 0.968, temperature 0.968, topo 0.968).

## 03_models/te_by_size_cat
- purpose: Compare TE distributions across size categories.
- data used + filters: `data/processed/ena2024_with_TE.parquet` merged to base data on ID keys.
- takeaway: TE declines with size category (large farms lower mean TE).
- validation checks performed: Verified merge keys and TE range (0.0001-0.89).

## 03_models/te_by_region
- purpose: Compare TE distributions across natural regions.
- data used + filters: `data/processed/ena2024_with_TE.parquet` merged to base data on ID keys.
- takeaway: Region 3 shows lower TE on average.
- validation checks performed: Verified merge keys and TE range.

## 03_models/te_vs_diversif_binned
- purpose: Inspect TE-diversification relationship by size.
- data used + filters: merged TE/base; bins of diversification_area (0-1).
- takeaway: Relationship is weak/non-monotonic with size-specific patterns.
- validation checks performed: Checked bin edges and counts per bin.

## 03_models/logit_pred_practice_any
- purpose: Plot predicted P(practice_any) vs diversification by size.
- data used + filters: `data/processed/model_data_ena2024.parquet`; predictions from `outputs/tables/04_logit_main.csv` coefficients; binned by diversification_area; weighted averages using `weight`.
- takeaway: Predicted probabilities are high across diversification levels; size interactions muted.
- validation checks performed: Confirmed coefficient mapping and prediction range (0-1).

## 03_models/logit_pred_practice_two_plus
- purpose: Plot predicted P(practice_two_plus) vs diversification by size.
- data used + filters: `data/processed/model_data_ena2024.parquet`; predictions from `outputs/tables/05_logit_robustness.csv` (model `alt_outcome_two_plus`); binned by diversification_area; weighted averages.
- takeaway: Predicted probability rises with diversification, but is high overall.
- validation checks performed: Confirmed coefficient mapping and prediction range (0-1).
