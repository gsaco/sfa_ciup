# Changelog

## 2026-01-13
- Created repo inventory tooling and ran `python src/ena/scan_repo.py` to generate `docs/REPO_INVENTORY.md` and `data/intermediate/raw_manifest.csv`.
- Implemented ENA IO utilities and profiling script; ran `python src/ena/01_load_and_profile.py` to create `data/intermediate/ena2024_raw.parquet` and `data/intermediate/module_profile.csv`.
- Parsed the ENA 2024 dictionary and generated mapping artifacts via `python src/ena/02_build_schema_from_dictionary.py`.
- Normalized dictionary variable names (line breaks) and refreshed mapping outputs with `python src/ena/02_build_schema_from_dictionary.py`.
- Applied the schema mapping and merged CARATULA with CAP200AB via `python src/ena/03_apply_schema.py` to create `data/intermediate/ena2024_schema.parquet`.
- Documented data structure in `docs/DATA_STRUCTURE.md`.
- Built diversification features and descriptive tables with `python src/ena/04_compute_diversification.py`.
- Added diversification tests and ran `pytest -q`.
- Documented diversification index in `docs/DIVERSIFICATION_INDEX.md`.
- Built model-ready data with `python src/ena/05_build_model_data.py`.
- Installed R package dependencies for SFA (`frontier` and its dependencies).
- Ran SFA estimation and outputs via `Rscript R/01_sfa_main.R`.
- Ran survey logit models via `Rscript R/02_logit_practices.R`.
- Documented model specifications in `docs/MODELS.md`.
- Added fallback and data gap documentation in `docs/DATA_GAPS.md`.
- Documented external data status in `docs/EXTERNAL_DATA.md`.
- Generated report assets and manifest via `python src/report/build_report.py`.
- Added executable pipeline runner `scripts/run_all.sh`.
- Added reproducibility instructions in `docs/REPRODUCIBILITY.md`.
- Executed full pipeline via `./scripts/run_all.sh`.
- Added interpretation and improvement notes in `docs/RESULTS_INTERPRETATION.md`.
- Added `requirements.txt`, `R/install_packages.R`, and `scripts/setup.sh` for venv-based setup.
