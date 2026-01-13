# External Data

## UBIGEO (district capitals + area)
- **Plan A (attempted)**: `DD_TB_UBIGEOS.xlsx` from the National Open Data portal.
  - URL: `https://www.datosabiertos.gob.pe/sites/default/files/DD_TB_UBIGEOS.xlsx`
  - Issue: file contains a data dictionary, not district coordinates or area.
- **Plan B (used)**: district-level dataset with coordinates and area.
  - URL: `https://raw.githubusercontent.com/jmcastagnetto/ubigeo-peru-aumentado/master/ubigeo_distrito.csv`
  - License: see repository LICENSE file.
  - Download script: `src/external/ubigeo/download_ubigeo_fallback.py`
  - Parser: `src/external/ubigeo/parse_ubigeo_capitals.py`
  - Output: `data/external/processed/ubigeo_district_capitals.parquet`
  - Metadata: `data/external/raw/ubigeo/metadata_fallback.json`

## CHIRPS precipitation (monthly)
- **Plan B (used)**: CHIRPS v2 monthly GeoTIFFs.
  - Base URL: `https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/`
  - File pattern: `chirps-v2.0.{YYYY}.{MM}.tif.gz`
  - Download script: `src/external/chirps/download_chirps_monthly.py`
  - Extract script: `src/external/chirps/extract_chirps_points.py`
  - Output: `data/external/processed/chirps_district_features_2024.parquet`
  - Metadata: `data/external/raw/chirps/metadata.json`
- **Baseline window**: 2015–2020 (fallback from 1991–2020 due to download size constraints).

## Notes
- All external data are cached under `data/external/raw/` with SHA256 hashes in metadata files.
- See `docs/CHIRPS_FEATURES.md` and `docs/GEO_MERGE.md` for processing details.
