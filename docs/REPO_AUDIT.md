# Repo Audit

- Generated: 2026-01-13T12:23:21

## Tree (depth <= 3)

```
./
  DICCIONARIO DE DATOS ENA-2024.pdf
  Ficha.pdf
  README.md
  requirements.txt
  R/
    01_sfa_main.R
    02_logit_practices.R
    install_packages.R
  data/
    README.md
    external/
      processed/
      raw/
    intermediate/
      ena2024_dictionary.csv
      ena2024_raw.parquet
      ena2024_schema.parquet
      module_profile.csv
      raw_manifest.csv
      variable_map.json
    processed/
      ena2024_features.parquet
      ena2024_with_TE.csv
      ena2024_with_TE.parquet
      ena2024_with_TE_geo.csv
      ena2024_with_TE_geo.parquet
      model_data_ena2024.csv
      model_data_ena2024.parquet
      model_data_ena2024_plus_geo.csv
      model_data_ena2024_plus_geo.parquet
    raw/
      ENA_2024/
  docs/
    CHANGELOG.md
    CHIRPS_FEATURES.md
    DATA_GAPS.md
    DATA_STRUCTURE.md
    DIVERSIFICATION_INDEX.md
    ENA2024_VARIABLE_DICTIONARY.md
    EXTERNAL_DATA.md
    GEO_MERGE.md
    MODELS.md
    REPO_AUDIT.md
    REPO_INVENTORY.md
    REPRODUCIBILITY.md
    RESULTS_INTERPRETATION.md
    ROBUSTNESS_WITH_GEO.md
  logs/
    baseline_run.log
    geo_keys_profile_20260113_112438.log
    geo_keys_profile_20260113_112450.log
    geo_keys_profile_20260113_112518.log
    load_and_profile_20260113_082944.log
    load_and_profile_20260113_085420.log
    load_and_profile_20260113_092901.log
    load_and_profile_20260113_112210.log
    run_all_20260113_085420.log
    run_all_20260113_092850.log
    run_all_20260113_112209.log
  outputs/
    baseline_manifest.json
    manifest.json
    baseline_tables/
      00_sample_overview.csv
      00_sample_overview.md
      01_diversification_descriptives.csv
      01_diversification_descriptives.md
      02_sfa_main.csv
      02_sfa_main.md
      03_sfa_robustness.csv
      03_sfa_robustness.md
      04_logit_main.csv
      04_logit_main.md
      05_logit_robustness.csv
      05_logit_robustness.md
      99_variable_definitions_table.csv
      99_variable_definitions_table.md
    tables/
      00_sample_overview.csv
      00_sample_overview.md
      01_diversification_descriptives.csv
      01_diversification_descriptives.md
      02_sfa_main.csv
      02_sfa_main.md
      03_sfa_robustness.csv
      03_sfa_robustness.md
      04_logit_main.csv
      04_logit_main.md
      05_logit_robustness.csv
      05_logit_robustness.md
      06_geo_feature_coverage.csv
      06_geo_feature_coverage.md
      07_sfa_with_geo_controls.csv
      07_sfa_with_geo_controls.md
      08_sfa_compare_main_effects.csv
      08_sfa_compare_main_effects.md
      09_logit_with_geo_controls.csv
      09_logit_with_geo_controls.md
      10_logit_compare_main_effects.csv
      10_logit_compare_main_effects.md
      99_variable_definitions_table.csv
      99_variable_definitions_table.md
  reports/
    reporte_final.md
  scripts/
    run_all.sh
    setup.sh
  src/
    ena/
      01_load_and_profile.py
      02_build_schema_from_dictionary.py
      03_apply_schema.py
      04_compute_diversification.py
      05_build_model_data.py
      __init__.py
      io.py
      scan_repo.py
      __pycache__/
    external/
      __init__.py
      __pycache__/
      chirps/
      ubigeo/
    features/
      __init__.py
      diversification.py
      merge_geo_features.py
      __pycache__/
    qa/
      geo_keys_profile.py
    report/
      build_report.py
    tests/
      conftest.py
      test_chirps_features.py
      test_diversification.py
      test_ubigeo_capitals.py
      __pycache__/
  venv/
    pyvenv.cfg
    bin/
      Activate.ps1
      activate
      activate.csh
      activate.fish
      dumppdf.py
      f2py
      normalizer
      numpy-config
      pdf2txt.py
      pdfplumber
      pip
      pip3
      pip3.13
      py.test
      pygmentize
      pypdfium2
      pytest
      python
      python3
      python3.13
      tabulate
      __pycache__/
    include/
      python3.13/
    lib/
      python3.13/
```

## ENA 2024 and dictionary locations

- ENA 2024 raw data: `data/raw/ENA_2024/`
- ENA 2024 zip: `data/ENA_2024.zip`
- Dictionary: `DICCIONARIO DE DATOS ENA-2024.pdf`

## Scripts building diversification and model data

- Diversification: `src/features/diversification.py`, `src/ena/04_compute_diversification.py`
- Model data: `src/ena/05_build_model_data.py`
- Geo merge: `src/features/merge_geo_features.py`
- Schema mapping: `src/ena/02_build_schema_from_dictionary.py`, `src/ena/03_apply_schema.py`

## External data scripts

- UBIGEO: `src/external/ubigeo/download_ubigeo_capitals.py`, `src/external/ubigeo/download_ubigeo_fallback.py`, `src/external/ubigeo/parse_ubigeo_capitals.py`
- CHIRPS: `src/external/chirps/download_chirps_monthly.py`, `src/external/chirps/extract_chirps_points.py`

## Variables used in SFA (R/01_sfa_main.R)

- Output: `log(valor_total)` (sum of crop value components)
- Inputs: `log_land`, `log_labor`, `log_inputs`
- Controls: `region_natural` dummies; geo model adds `prcp_total_z` and `log_surface_km2`
- Inefficiency (Z): `diversificacion_area`, `size_mediano`, `size_grande`, interactions; geo model adds `prcp_total_z`

## Variables used in logit (R/02_logit_practices.R)

- Outcome: `practice_any`
- Covariates: `diversificacion_area * size_cat`, `log_area`, `region_natural`
- Geo logit adds: `prcp_total_z`
- Survey design: `weight`, `estrato`, `psu`
