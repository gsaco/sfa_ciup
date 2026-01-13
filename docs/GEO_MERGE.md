# Geo Merge

## Keys
- Preferred key: `ubigeo6` built from `ccdd`, `ccpp`, `ccdi` (zero-padded).
- Source of coordinates/area: `data/external/processed/ubigeo_district_capitals.parquet`.

## Match rates
- Coverage and missingness are summarized in `outputs/tables/06_geo_feature_coverage.csv`.
- Merge uses district-level UBIGEO; records with missing `ccdd/ccpp/ccdi` remain unmatched.

## Assumptions
- District capital coordinates are used as representative point for CHIRPS sampling.
- The UBIGEO dataset is treated as authoritative for district names and areas.
