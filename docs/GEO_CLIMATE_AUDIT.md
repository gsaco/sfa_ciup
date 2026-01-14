# Geo/Climate Audit

## Data Sources and Merge Logic
- **UBIGEO district capitals:** `data/external/processed/ubigeo_district_capitals.parquet` merged on `ubigeo6` in `src/features/merge_geo_features.py` and `merge_geo2_features.py`.
- **CHIRPS precipitation:** `chirps_district_features_2024.parquet` merged on `ubigeo6`.
- **Temperature (TerraClimate):** `temperature_district_features_2023_2024.parquet` merged on `ubigeo6`.
- **Topography (Copernicus DEM):** `topography_district_features.parquet` merged on `ubigeo6`.

## Coverage
- **CHIRPS match rate:** 0.968.
- **Temperature match rate:** 0.968.
- **Topography match rate:** 0.968.
- Coverage gaps are limited but non-zero; see `outputs/tables/06_geo_feature_coverage.csv` and `outputs/tables/12_temp_topo_coverage.csv`.

## Plausibility Checks (Ranges)
- **Coordinates:** lat [-18.29, -0.97], lon [-81.27, -68.85] (consistent with Peru).
- **CHIRPS:** `prcp_total_z` [-4.92, 3.21], `prcp_2024_total` [4.23, 4839.30].
- **Temperature:** `tmean_2024` [6.85, 28.45], `delta_tmean_24_23` [-1.7, 1.2].
- **Topography:** `elev_m` [3.46, 4359.42], `slope_deg` [0.07, 25.87], `ruggedness` [0.14, 35.89].

## Collinearity
- Strong correlations detected:
  - `tmean_2024` vs `elev_m` approx -0.925.
  - `slope_deg` vs `ruggedness` approx 0.968.
- Interpretation of joint coefficients in SFA/logit should acknowledge collinearity and potential instability.

## Warnings and Risks
- Raster extraction warnings (`invalid value encountered in cast`) during CHIRPS and temperature processing; likely out-of-bounds points or masked pixels.
- CHIRPS z-score division warning when baseline std = 0 (handled by `np.where`, resulting in `NaN`).

## Overall Assessment
- Spatial ranges and match rates look plausible; merges appear consistent with expected Peru geography. The main risks are localized missingness and collinearity among climate/topo variables.

