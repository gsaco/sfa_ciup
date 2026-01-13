# CHIRPS Features

## Source
- CHIRPS v2 monthly precipitation (GeoTIFFs): `https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/`
- File pattern: `chirps-v2.0.{YYYY}.{MM}.tif.gz`

## Methodology
- Points: district capital coordinates from `ubigeo_district_capitals.parquet`.
- Sampling: each monthly GeoTIFF is sampled at the nearest grid cell using `rasterio`.
- Annual totals:
  - `prcp_2024_total`: sum of monthly precipitation for 2024.
  - `prcp_2024_wet`: sum for Nov–Mar.
  - `prcp_2024_dry`: sum for May–Sep.
- Baseline:
  - Annual totals computed for each baseline year.
  - `prcp_baseline_mean` and `prcp_baseline_sd` computed across baseline years.
  - `prcp_total_anom` = `prcp_2024_total` − `prcp_baseline_mean`.
  - `prcp_total_z` = `prcp_total_anom` / `prcp_baseline_sd`.

## Baseline window
- **Fallback used**: 2015–2020 (Plan B), due to download size/time constraints for 1991–2020.
- The baseline window is recorded in `data/external/raw/chirps/metadata.json`.

## Outputs
- `data/external/processed/chirps_district_features_2024.parquet`
- `data/external/processed/chirps_metadata.json`

## QA
- Non-negative precipitation values.
- Coverage: >95% of districts with non-missing precipitation.
