# Repo Inventory

- Generated: 2026-01-13T11:22:09
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
      model_data_ena2024.csv
      model_data_ena2024.parquet
    raw/
      ENA_2024/
  docs/
    CHANGELOG.md
    DATA_GAPS.md
    DATA_STRUCTURE.md
    DIVERSIFICATION_INDEX.md
    ENA2024_VARIABLE_DICTIONARY.md
    EXTERNAL_DATA.md
    MODELS.md
    REPO_INVENTORY.md
    REPRODUCIBILITY.md
    RESULTS_INTERPRETATION.md
  logs/
    baseline_run.log
    load_and_profile_20260113_082944.log
    load_and_profile_20260113_085420.log
    load_and_profile_20260113_092901.log
    run_all_20260113_085420.log
    run_all_20260113_092850.log
    run_all_20260113_112209.log
  outputs/
    manifest.json
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
    features/
      __init__.py
      diversification.py
      __pycache__/
    report/
      build_report.py
    tests/
      conftest.py
      test_diversification.py
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
| .csv | 30 | 394.52 MB |
| .md | 1 | 20.45 KB |
| .pdf | 42 | 105.04 MB |

