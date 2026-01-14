# Repo Inventory

- Generated: 2026-01-13T19:23:18
- Repo root: `/Users/gabrielsaco/Documents/GitHub/sfa_ciup`

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
      ena2024_with_TE_controls.csv
      ena2024_with_TE_controls.parquet
      ena2024_with_TE_geo.csv
      ena2024_with_TE_geo.parquet
      ena2024_with_TE_geo2.csv
      ena2024_with_TE_geo2.parquet
      model_data_ena2024.csv
      model_data_ena2024.parquet
      model_data_ena2024_plus_controls.csv
      model_data_ena2024_plus_controls.parquet
      model_data_ena2024_plus_controls_temp.csv
      model_data_ena2024_plus_controls_temp.parquet
      model_data_ena2024_plus_geo.csv
      model_data_ena2024_plus_geo.parquet
      model_data_ena2024_plus_geo2.csv
      model_data_ena2024_plus_geo2.parquet
    raw/
      ENA_2024/
  docs/
    CHANGELOG.md
    CHIRPS_FEATURES.md
    DATA_GAPS.md
    DATA_STRUCTURE.md
    DIVERSIFICATION_INDEX.md
    ECONOMIC_VIABILITY.md
    ENA2024_VARIABLE_DICTIONARY.md
    ENA_CONTROLS_MAPPING.md
    EXTERNAL_DATA.md
    GEO_MERGE.md
    MODELS.md
    REPO_AUDIT.md
    REPO_INVENTORY.md
    REPRODUCIBILITY.md
    RESULTS_INTERPRETATION.md
    ROBUSTNESS_SUMMARY.md
    ROBUSTNESS_WITH_GEO.md
    TEMPERATURE_FEATURES.md
    TOPOGRAPHY_FEATURES.md
  logs/
    baseline_run.log
    geo_keys_profile_20260113_112438.log
    geo_keys_profile_20260113_112450.log
    geo_keys_profile_20260113_112518.log
    load_and_profile_20260113_082944.log
    load_and_profile_20260113_085420.log
    load_and_profile_20260113_092901.log
    load_and_profile_20260113_112210.log
    load_and_profile_20260113_173759.log
    load_and_profile_20260113_174005.log
    load_and_profile_20260113_180802.log
    load_and_profile_20260113_192106.log
    run_all_20260113_085420.log
    run_all_20260113_092850.log
    run_all_20260113_112209.log
    run_all_20260113_173758.log
    run_all_20260113_174004.log
    run_all_20260113_180802.log
    run_all_20260113_192105.log
    run_all_20260113_192318.log
  outputs/
    baseline_manifest.json
    manifest.json
    manifest_baseline.json
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
      11_controls_ena_coverage.csv
      11_controls_ena_coverage.md
      12_temp_topo_coverage.csv
      12_temp_topo_coverage.md
      13_sfa_with_controls_ena.csv
      13_sfa_with_controls_ena.md
      14_sfa_with_temp_topo.csv
      14_sfa_with_temp_topo.md
      15_sfa_compare_effects_all.csv
      15_sfa_compare_effects_all.md
      16_logit_with_controls_ena.csv
      16_logit_with_controls_ena.md
      17_logit_with_temp_topo.csv
      17_logit_with_temp_topo.md
      18_logit_compare_effects_all.csv
      18_logit_compare_effects_all.md
      99_variable_definitions_table.csv
      99_variable_definitions_table.md
      sample_loss_analysis.csv
      sample_loss_analysis.md
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
      06_build_model_data_plus_controls.py
      __init__.py
      io.py
      scan_repo.py
      __pycache__/
    external/
      __init__.py
      __pycache__/
      chirps/
      temperature/
      topography/
      ubigeo/
    features/
      __init__.py
      diversification.py
      ena_controls.py
      merge_geo2_features.py
      merge_geo_features.py
      merge_temperature_features.py
      __pycache__/
    qa/
      geo_keys_profile.py
      sample_loss_analysis.py
    report/
      build_report.py
    tests/
      conftest.py
      test_chirps_features.py
      test_diversification.py
      test_ena_controls.py
      test_temperature_features.py
      test_topography_features.py
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
      rio
      tabulate
      __pycache__/
    include/
      python3.13/
    lib/
      python3.13/
```

## ENA 2024 data locations

- Raw ENA 2024 folder: `/Users/gabrielsaco/Documents/GitHub/sfa_ciup/data/raw/ENA_2024` (exists: True)
- Raw ENA 2024 zip: `/Users/gabrielsaco/Documents/GitHub/sfa_ciup/data/ENA_2024.zip` (exists: False, size: NA)
- Data README: `/Users/gabrielsaco/Documents/GitHub/sfa_ciup/data/README.md` (exists: True)

## Variable dictionary

- Dictionary file: `/Users/gabrielsaco/Documents/GitHub/sfa_ciup/DICCIONARIO DE DATOS ENA-2024.pdf` (exists: True, size: 1.51 MB)

## Existing scripts that read ENA

- None found in repo at scan time.

## Data formats and approximate sizes

| Extension | Count | Total size |
|---|---:|---:|
| .csv | 31 | 394.91 MB |
| .gz | 205 | 2.78 GB |
| .json | 7 | 89.95 KB |
| .md | 1 | 20.45 KB |
| .nc | 4 | 1.28 MB |
| .parquet | 4 | 280.33 KB |
| .pdf | 42 | 105.04 MB |
| .tif | 126 | 954.23 MB |
| .xlsx | 1 | 10.98 KB |

