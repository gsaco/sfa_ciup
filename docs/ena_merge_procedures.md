# ENA Merge Procedures (Forensic + Reproducibility Audit)

## Scope and source of truth
This document enumerates every ENA CSV merge performed by the repository pipeline, from raw ENA modules to final merged outputs. Source of truth is the current repository contents, including scripts, logs, and docs. Any step not explicitly present is marked **UNKNOWN** with minimal verification guidance.

## Entry points (pipeline orchestration)
- **Primary pipeline**: `scripts/run_all.sh` (calls ENA scripts in order and writes `logs/run_all_YYYYMMDD_HHMMSS.log`).
- **ENA-only steps (subsequence)**:
  1) `src/ena/scan_repo.py`
  2) `src/ena/01_load_and_profile.py`
  3) `src/ena/02_build_schema_from_dictionary.py`
  4) `src/ena/03_apply_schema.py`
  5) `src/ena/04_compute_diversification.py`
  6) `src/ena/05_build_model_data.py`
  7) `src/ena/06_build_model_data_plus_controls.py`

## Data contract (canonical keys and invariants)

### Canonical keys
- **Raw ENA key columns (uppercase)**: `ANIO`, `CCDD`, `CCPP`, `CCDI`, `NSEGM`, `ID_PROD`, `UA`.
  - Defined in `src/ena/01_load_and_profile.py` as `KEY_COLS`.
- **Standardized key columns (lowercase)**: `anio`, `ccdd`, `ccpp`, `ccdi`, `psu`, `id_prod`, `ua`.
  - Used throughout `src/ena/03_apply_schema.py`, `src/ena/04_compute_diversification.py`, `src/ena/05_build_model_data.py`, and `src/ena/06_build_model_data_plus_controls.py`.

### Key invariants and uniqueness expectations
- `CARATULA.csv` is expected to be **unique on** `(ANIO, CCDD, CCPP, CCDI, NSEGM, ID_PROD, UA)`.
  - Checked in `src/ena/01_load_and_profile.py` using `.duplicated(subset=KEY_COLS)` and logged.
- `03_apply_schema.py` enforces **many-to-one** merge constraint when joining crop records to CARATULA:
  - `crop.merge(caratula, on=KEY_COLS, how="left", validate="many_to_one")`.
  - This asserts **right side (CARATULA)** is unique per key.
- Other merges generally **do not validate** key uniqueness; duplicate keys on the right may inflate rows.

### Column naming standardization
- Column names are normalized by stripping whitespace via `ena.io.normalize_columns`.
- Standardized variable names are derived from `data/intermediate/variable_map.json` (built from `DICCIONARIO DE DATOS ENA-2024.pdf`).
  - Mapping built in `src/ena/02_build_schema_from_dictionary.py`.
  - Applied in `src/ena/03_apply_schema.py` (rename after merge).

### Encoding, delimiter, and NA tokens
- **Encoding**: `ena.io.read_csv` tries `utf-8`, then `latin-1`, then `cp1252`. If all fail, raises UnicodeDecodeError. No fallback beyond those encodings.
- **Delimiter**: Pandas default (comma). **UNKNOWN** if any ENA CSV uses a non-comma delimiter.
  - Minimal verification: `python - <<'PY'
import pandas as pd
print(pd.read_csv('data/raw/ENA_2024/973-Modulo1893/CARATULA.csv', nrows=1).head())
PY` and check column counts; if single column appears, delimiter mismatch.
- **NA tokens**: Pandas defaults only; no custom `na_values` are set. **UNKNOWN** whether ENA uses custom NA tokens.
  - Minimal verification: scan CSVs for common codes (`-99`, `99`, `.`) and add `na_values` if needed.

### Type expectations and coercions
- All key columns are coerced to string in most steps via `coerce_keys()`.
- Numeric fields are coerced with `pd.to_numeric(..., errors="coerce")` (missing becomes `NaN`).
- Binary indicators are standardized using `yes_no_dummy()`:
  - `1 -> 1`, `0 or 2 -> 0`, else `NA`.

## Cleaning and harmonization rules
- **Column normalization**: `ena.io.normalize_columns()` strips whitespace from column names.
- **Key coercion**: `.astype("string")` for each key column; `normalize_key_series()` also strips trailing `.0` from keys (controls merge step).
- **Missing values**:
  - Numeric fields use `pd.to_numeric(errors="coerce")`.
  - `yes_no_dummy()` produces `NA` for anything outside expected codes.
  - `fill_zero_if_no()` sets expenditure fields to 0 when a "no" indicator is present.
- **Deduplication**:
  - `drop_duplicates(subset=ID_COLS)` in `src/ena/04_compute_diversification.py` for base features.
  - Multiple `drop_duplicates(subset=ID_COLS)` in `src/features/ena_controls.py` for module-level controls.
- **Aggregation**:
  - `groupby(ID_COLS, dropna=False)` with sums/means for aggregated controls and diversification metrics.

## Merge procedures (auditable checklist)

> **Notation**: M## = merge step ID. “Expected row-count change” indicates what should happen if keys are consistent; actual counts may differ if duplicates exist.

### M01 — Merge crop module with CARATULA (schema build)
- **Purpose**: Attach household/location/design fields (CARATULA) to crop-level records.
- **Inputs**:
  - `data/raw/ENA_2024/973-Modulo1895/03_CAP200AB.csv` (crop data)
  - `data/raw/ENA_2024/973-Modulo1893/CARATULA.csv` (household/location data)
- **Output**:
  - `data/intermediate/ena2024_schema.parquet`
- **Code pointer**:
  - `src/ena/03_apply_schema.py` → `main()`; merge block: `merged = crop.merge(caratula, on=KEY_COLS, how="left", validate="many_to_one")`.
- **Keys used**: `ANIO, CCDD, CCPP, CCDI, NSEGM, ID_PROD, UA`.
- **Join type / direction**: LEFT JOIN; **left table = crop module**, right = CARATULA.
- **Expected row-count change**: **No change** from crop rows if CARATULA is unique per key.
- **Assertions/validations**:
  - `validate="many_to_one"` enforces right-side uniqueness (CARATULA).
  - Missing key share printed to stdout.
- **Failure modes**:
  - Duplicate CARATULA keys → merge fails with `MergeError`.
  - Missing CARATULA file → `FileNotFoundError`.
  - Missing key columns → may reduce join matches (left join retains rows with nulls).

### M02 — Merge diversification metrics into base (features build)
- **Purpose**: Create a single row per `ID_COLS` with diversification metrics.
- **Inputs**:
  - `data/intermediate/ena2024_schema.parquet` (from M01)
- **Intermediate aggregates**:
  - `area_div`: from `compute_diversification(df, value_col="area_cosechada_ha")`
  - `value_div`: from `compute_diversification(df, value_col="valor_total_cultivo")`
  - `base`: `df[base_cols].drop_duplicates(subset=ID_COLS)`
- **Output**:
  - `data/processed/ena2024_features.parquet`
- **Code pointer**:
  - `src/ena/04_compute_diversification.py` → `main()`; `features = base.merge(area_div, on=ID_COLS, how="left").merge(value_div, on=ID_COLS, how="left")`.
- **Keys used**: `anio, ccdd, ccpp, ccdi, psu, id_prod, ua`.
- **Join type / direction**: LEFT JOINs; **left table = base**, right tables = aggregates.
- **Expected row-count change**: **No change** from `base` (one row per ID_COLS).
- **Assertions/validations**:
  - None on join uniqueness; relies on `groupby(ID_COLS)` in `compute_diversification`.
- **Failure modes**:
  - If `base` contains duplicate IDs (should not after `drop_duplicates`), row count may inflate.
  - If `compute_diversification` returns empty (all totals <= 0), merge yields missing metrics.

### M03 — Merge production/cost/practices modules into model dataset
- **Purpose**: Add costs, labor, and practices to ENA features for modeling.
- **Inputs**:
  - `data/processed/ena2024_features.parquet` (from M02)
  - `data/raw/ENA_2024/973-Modulo1910/18_CAP1000.csv` (production costs, labor)
  - `data/raw/ENA_2024/973-Modulo1899/07_CAP200E.csv` (inputs; aggregated)
  - `data/raw/ENA_2024/973-Modulo1900/08_CAP300AB.csv` (practices)
- **Output**:
  - `data/processed/model_data_ena2024.parquet`
  - `data/processed/model_data_ena2024.csv`
- **Code pointer**:
  - `src/ena/05_build_model_data.py` → `main()`; merge block:
    - `features.merge(cap1000, on=ID_COLS, how="left")`
    - `.merge(cap200e_agg, on=ID_COLS, how="left")`
    - `.merge(cap300, on=ID_COLS, how="left")`
- **Keys used**: `anio, ccdd, ccpp, ccdi, psu, id_prod, ua`.
- **Join type / direction**: LEFT JOINs; **left table = features**, right tables = module frames.
- **Expected row-count change**: **No change** from features if right tables are unique per ID.
- **Assertions/validations**:
  - Missing practice variables in CAP300 raise `ValueError`.
  - Missingness and range checks are printed after merge.
- **Failure modes**:
  - If CAP1000 or CAP300 contain duplicate keys, row counts can **inflate** (no `validate`).
  - Missing module files → `FileNotFoundError`.

### M04 — Merge irrigation controls (schema + CAP800 + CAP1000)
- **Purpose**: Build irrigation-related controls for each producer.
- **Inputs**:
  - `data/intermediate/ena2024_schema.parquet` (crop-level variables)
  - `data/raw/ENA_2024/973-Modulo1908/16_CAP800.csv`
  - `data/raw/ENA_2024/973-Modulo1910/18_CAP1000.csv`
- **Output**: In-memory DataFrame returned by `irrigation_features()`; later merged in M08.
- **Code pointer**:
  - `src/features/ena_controls.py` → `irrigation_features()`; merge block:
    - `crop_agg.merge(cap800, on=ID_COLS, how="left").merge(cap1000, on=ID_COLS, how="left")`
- **Keys used**: `anio, ccdd, ccpp, ccdi, psu, id_prod, ua`.
- **Join type / direction**: LEFT JOINs; **left table = crop_agg**, right tables = CAP800/CAP1000.
- **Expected row-count change**: **No change** from `crop_agg` if CAP800/CAP1000 unique per ID.
- **Assertions/validations**:
  - CAP800/CAP1000 are `drop_duplicates(subset=ID_COLS)` before merge.
- **Failure modes**:
  - If crop_agg is empty (e.g., no crop records), controls will be empty.

### M05 — Merge machinery/capital controls (CAP1000 + CAP1200)
- **Purpose**: Build machinery/asset controls.
- **Inputs**:
  - `data/raw/ENA_2024/973-Modulo1910/18_CAP1000.csv`
  - `data/raw/ENA_2024/973-Modulo1913/21_CAP1200B_ME.csv`
- **Output**: In-memory DataFrame returned by `machinery_capital_features()`; later merged in M08.
- **Code pointer**:
  - `src/features/ena_controls.py` → `machinery_capital_features()`; merge block:
    - `cap1000.merge(cap1200_agg, on=ID_COLS, how="left")`
- **Keys used**: `anio, ccdd, ccpp, ccdi, psu, id_prod, ua`.
- **Join type / direction**: LEFT JOIN; **left table = cap1000**, right table = cap1200_agg.
- **Expected row-count change**: **No change** if `cap1000` unique per ID.
- **Assertions/validations**:
  - None; relies on `cap1200_agg = groupby(ID_COLS)`.
- **Failure modes**:
  - Duplicate CAP1000 keys → row inflation.

### M06 — Merge fertilizer/seed controls (CAP200E + schema seed cert)
- **Purpose**: Build seed and fertilizer controls.
- **Inputs**:
  - `data/raw/ENA_2024/973-Modulo1899/07_CAP200E.csv`
  - `data/intermediate/ena2024_schema.parquet`
- **Output**: In-memory DataFrame returned by `fertilizer_seed_features()`; later merged in M08.
- **Code pointer**:
  - `src/features/ena_controls.py` → `fertilizer_seed_features()`; merge block:
    - `cap200e_agg.merge(seed_agg, on=ID_COLS, how="left")`
- **Keys used**: `anio, ccdd, ccpp, ccdi, psu, id_prod, ua`.
- **Join type / direction**: LEFT JOIN; **left table = cap200e_agg**, right table = seed_agg.
- **Expected row-count change**: **No change** from cap200e_agg.
- **Assertions/validations**:
  - None; relies on `groupby(ID_COLS)` for both aggregates.
- **Failure modes**:
  - If `schema` missing `seed_certified`, seed_agg may be all NA.

### M07 — Merge extension/credit/education controls (CAP700 + CAP900 + CAP1100 + CAP800)
- **Purpose**: Build training/credit/education/association controls.
- **Inputs**:
  - `data/raw/ENA_2024/973-Modulo1907/15_CAP700.csv`
  - `data/raw/ENA_2024/973-Modulo1909/17_CAP900.csv`
  - `data/raw/ENA_2024/973-Modulo1911/19_CAP1100.csv`
  - `data/raw/ENA_2024/973-Modulo1908/16_CAP800.csv`
- **Output**: In-memory DataFrame returned by `extension_credit_education_features()`; later merged in M08.
- **Code pointer**:
  - `src/features/ena_controls.py` → `extension_credit_education_features()`; merge block:
    - `cap700.merge(cap900, on=ID_COLS, how="left")`
    - `.merge(cap1100, on=ID_COLS, how="left")`
    - `.merge(cap800, on=ID_COLS, how="left")`
- **Keys used**: `anio, ccdd, ccpp, ccdi, psu, id_prod, ua`.
- **Join type / direction**: LEFT JOINs; **left table = cap700**, right tables = cap900/cap1100/cap800.
- **Expected row-count change**: **No change** from cap700 if right tables unique per ID.
- **Assertions/validations**:
  - Each right table is `drop_duplicates(subset=ID_COLS)` before merge.
- **Failure modes**:
  - Duplicate cap700 keys → row inflation.

### M08 — Merge all ENA controls into base model data
- **Purpose**: Produce `model_data_ena2024_plus_controls` with all control variables.
- **Inputs**:
  - `data/processed/model_data_ena2024.parquet`
  - Output frames from M04–M07 (controls).
- **Output**:
  - `data/processed/model_data_ena2024_plus_controls.parquet`
  - `data/processed/model_data_ena2024_plus_controls.csv`
- **Code pointer**:
  - `src/ena/06_build_model_data_plus_controls.py` → `main()`; merge loop:
    - `merged = merged.merge(controls, on=ID_COLS, how="left")` for each controls frame.
- **Keys used**: `anio, ccdd, ccpp, ccdi, psu, id_prod, ua`.
- **Join type / direction**: LEFT JOINs; **left table = base model**, right tables = controls.
- **Expected row-count change**: **No change** from base if controls unique per ID.
- **Assertions/validations**:
  - Verifies expected control columns exist post-merge; raises if missing.
- **Failure modes**:
  - Duplicate keys in controls frames → row inflation.
  - Missing variable map → upstream controls creation fails.

### M09 — Merge ENA model data with geo/climate (non-ENA external, but part of pipeline)
- **Purpose**: Attach geographic and climate features to ENA model data.
- **Inputs**:
  - `data/processed/model_data_ena2024.parquet`
  - `data/external/processed/ubigeo_district_capitals.parquet`
  - `data/external/processed/chirps_district_features_2024.parquet`
- **Output**:
  - `data/processed/model_data_ena2024_plus_geo.parquet`
  - `data/processed/model_data_ena2024_plus_geo.csv`
- **Code pointer**:
  - `src/features/merge_geo_features.py` → `main()`.
- **Keys used**: `ubigeo6` built from `ccdd/ccpp/ccdi`.
- **Join type / direction**: LEFT JOINs; **left table = model data**, right tables = external geo/climate.
- **Expected row-count change**: **No change** if `ubigeo6` is unique in right tables.
- **Assertions/validations**:
  - None; join coverage summarized to `outputs/tables/06_geo_feature_coverage.csv`.
- **Failure modes**:
  - Missing external feature files → `FileNotFoundError`.

### M10 — Merge ENA model data (plus controls) with temperature
- **Purpose**: Attach temperature features to ENA model data + controls.
- **Inputs**:
  - `data/processed/model_data_ena2024_plus_controls.parquet`
  - `data/external/processed/temperature_district_features_2023_2024.parquet`
- **Output**:
  - `data/processed/model_data_ena2024_plus_controls_temp.parquet`
  - `data/processed/model_data_ena2024_plus_controls_temp.csv`
- **Code pointer**:
  - `src/features/merge_temperature_features.py` → `main()`.
- **Keys used**: `ubigeo6` built from `ccdd/ccpp/ccdi`.
- **Join type / direction**: LEFT JOIN; **left table = model+controls**, right = temperature.
- **Expected row-count change**: **No change** if temperature features unique per `ubigeo6`.
- **Assertions/validations**:
  - None; coverage summarized to `outputs/tables/12_temp_topo_coverage.csv`.
- **Failure modes**:
  - Missing temperature file → `FileNotFoundError`.

### M11 — Merge ENA model data with geo+climate+topography (final geo2)
- **Purpose**: Attach full climate/topography features to ENA model data.
- **Inputs**:
  - `data/processed/model_data_ena2024_plus_controls_temp.parquet`
  - `data/external/processed/ubigeo_district_capitals.parquet`
  - `data/external/processed/chirps_district_features_2024.parquet`
  - `data/external/processed/topography_district_features.parquet`
- **Output**:
  - `data/processed/model_data_ena2024_plus_geo2.parquet`
  - `data/processed/model_data_ena2024_plus_geo2.csv`
- **Code pointer**:
  - `src/features/merge_geo2_features.py` → `main()`.
- **Keys used**: `ubigeo6` built from `ccdd/ccpp/ccdi`.
- **Join type / direction**: LEFT JOINs; **left table = model+controls+temp**, right = geo/climate/topo.
- **Expected row-count change**: **No change** if external features unique per `ubigeo6`.
- **Assertions/validations**:
  - None; coverage summarized to `outputs/tables/12_temp_topo_coverage.csv`.
- **Failure modes**:
  - Missing external files → `FileNotFoundError`.

## Merge map (nodes + edges)

### Table: Merge edges
| source_a | source_b | merged_output | keys | join type | code pointer |
|---|---|---|---|---|---|
| `03_CAP200AB.csv` | `CARATULA.csv` | `data/intermediate/ena2024_schema.parquet` | `ANIO, CCDD, CCPP, CCDI, NSEGM, ID_PROD, UA` | left (validate many_to_one) | `src/ena/03_apply_schema.py::main()` |
| `ena2024_schema.parquet (base)` | `area_div` | `ena2024_features.parquet` | `anio, ccdd, ccpp, ccdi, psu, id_prod, ua` | left | `src/ena/04_compute_diversification.py::main()` |
| `ena2024_features.parquet` | `18_CAP1000.csv` | `model_data_ena2024.parquet` | `anio, ccdd, ccpp, ccdi, psu, id_prod, ua` | left | `src/ena/05_build_model_data.py::main()` |
| `model_data_ena2024` | `07_CAP200E.csv (agg)` | `model_data_ena2024.parquet` | `anio, ccdd, ccpp, ccdi, psu, id_prod, ua` | left | `src/ena/05_build_model_data.py::main()` |
| `model_data_ena2024` | `08_CAP300AB.csv` | `model_data_ena2024.parquet` | `anio, ccdd, ccpp, ccdi, psu, id_prod, ua` | left | `src/ena/05_build_model_data.py::main()` |
| `model_data_ena2024` | `controls frames` | `model_data_ena2024_plus_controls` | `anio, ccdd, ccpp, ccdi, psu, id_prod, ua` | left | `src/ena/06_build_model_data_plus_controls.py::main()` |
| `model_data_ena2024` | `ubigeo + chirps` | `model_data_ena2024_plus_geo` | `ubigeo6` | left | `src/features/merge_geo_features.py::main()` |
| `model_data_ena2024_plus_controls` | `temperature` | `model_data_ena2024_plus_controls_temp` | `ubigeo6` | left | `src/features/merge_temperature_features.py::main()` |
| `model_data_ena2024_plus_controls_temp` | `ubigeo + chirps + topo` | `model_data_ena2024_plus_geo2` | `ubigeo6` | left | `src/features/merge_geo2_features.py::main()` |

### Final lineage (raw → staged → final)
1. Raw ENA CSVs under `data/raw/ENA_2024/` (see `data/README.md`).
2. `data/intermediate/ena2024_schema.parquet` (crop + CARATULA merge).
3. `data/processed/ena2024_features.parquet` (diversification metrics merged).
4. `data/processed/model_data_ena2024.parquet` (costs/practices merged).
5. `data/processed/model_data_ena2024_plus_controls.parquet` (controls merged).
6. `data/processed/model_data_ena2024_plus_geo.parquet` and `..._plus_geo2.parquet` (geo/climate merged).

## Row-count and integrity audit

### Observed counts (from `logs/baseline_run.log`)
- `CARATULA.csv` rows: **40,237**.
- `ena2024_schema.parquet` rows: **165,711**.
- `model_data_ena2024.parquet` rows: **35,187**.

### Step-by-step audit (expected vs. observed)

| Step ID | Merge | Rows A (left) | Rows B (right) | Rows after | Matched rows | Left-only | Right-only | Duplicates introduced |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| M01 | CAP200AB ⟵ CARATULA | 165,711 | 40,237 | 165,711 | 165,711 | 0 | 5,050 | 0 |
| M02a | base ⟵ area_div | 35,187 | 34,075 | 35,187 | 34,075 | 1,112 | 0 | 0 |
| M02b | base+area ⟵ value_div | 35,187 | 31,824 | 35,187 | 31,824 | 3,363 | 0 | 0 |
| M03a | features ⟵ CAP1000 | 35,187 | 39,112 | 35,187 | 35,184 | 3 | 3,928 | 0 |
| M03b | (M03a) ⟵ CAP200E_agg | 35,187 | 35,185 | 35,187 | 35,185 | 2 | 0 | 0 |
| M03c | (M03b) ⟵ CAP300 | 35,187 | 38,733 | 35,187 | 35,185 | 2 | 3,548 | 0 |
| M04a | crop_agg ⟵ CAP800 | 35,187 | 39,112 | 35,187 | 35,184 | 3 | 3,928 | 0 |
| M04b | (M04a) ⟵ CAP1000 (gasto_agua) | 35,187 | 39,112 | 35,187 | 35,184 | 3 | 3,928 | 0 |
| M05 | CAP1000 ⟵ CAP1200B_agg | 39,112 | 26,200 | 39,112 | 26,200 | 12,912 | 0 | 0 |
| M06 | CAP200E_agg ⟵ seed_agg | 35,185 | 35,187 | 35,185 | 35,185 | 0 | 2 | 0 |
| M07a | CAP700 ⟵ CAP900 | 39,112 | 39,112 | 39,112 | 39,112 | 0 | 0 | 0 |
| M07b | (M07a) ⟵ CAP1100 | 39,112 | 37,514 | 39,112 | 37,514 | 1,598 | 0 | 0 |
| M07c | (M07b) ⟵ CAP800 (asociación) | 39,112 | 39,112 | 39,112 | 39,112 | 0 | 0 | 0 |
| M08a | base ⟵ controls (irrigation) | 35,187 | 35,187 | 35,187 | 35,187 | 0 | 0 | 0 |
| M08b | (M08a) ⟵ controls (machinery) | 35,187 | 39,112 | 35,187 | 35,184 | 3 | 3,928 | 0 |
| M08c | (M08b) ⟵ controls (fert/seed) | 35,187 | 35,185 | 35,187 | 35,185 | 2 | 0 | 0 |
| M08d | (M08c) ⟵ controls (extension/credit/edu) | 35,187 | 39,112 | 35,187 | 35,184 | 3 | 3,928 | 0 |
| M09a | model ⟵ ubigeo | 35,187 | 1,892 | 35,187 | 34,075 | 1,112 | 350 | 0 |
| M09b | (M09a) ⟵ chirps | 35,187 | 1,892 | 35,187 | 34,075 | 1,112 | 350 | 0 |
| M10 | model+controls ⟵ temperature | 35,187 | 1,892 | 35,187 | 34,075 | 1,112 | 350 | 0 |
| M11a | model+controls+temp ⟵ ubigeo | 35,187 | 1,892 | 35,187 | 34,075 | 1,112 | 350 | 0 |
| M11b | (M11a) ⟵ chirps | 35,187 | 1,892 | 35,187 | 34,075 | 1,112 | 350 | 0 |
| M11c | (M11b) ⟵ topography | 35,187 | 1,892 | 35,187 | 34,075 | 1,112 | 350 | 0 |

### Missing diagnostics (additions recommended)
If precise row-counts and match diagnostics are required for audit:

**Minimal code snippet to add per merge** (apply to each merge location):
```python
merged = left.merge(right, on=KEYS, how="left", indicator=True)
print("rows_left", len(left), "rows_right", len(right), "rows_merged", len(merged))
print(merged["_merge"].value_counts(dropna=False))
# detect inflation
if len(merged) > len(left):
    print("WARNING: row inflation detected")
```

**Where to add**:
- `src/ena/03_apply_schema.py` after `crop.merge(...)`.
- `src/ena/04_compute_diversification.py` after each merge.
- `src/ena/05_build_model_data.py` after each merge.
- `src/features/ena_controls.py` inside each control builder.
- `src/ena/06_build_model_data_plus_controls.py` in the merge loop.

## Reproduction commands (from scratch)

### Environment setup
```bash
./scripts/setup.sh
source venv/bin/activate
```

### Run the full pipeline
```bash
./scripts/run_all.sh
```

### Outputs to verify
- `data/intermediate/ena2024_schema.parquet`
- `data/processed/ena2024_features.parquet`
- `data/processed/model_data_ena2024.parquet`
- `data/processed/model_data_ena2024_plus_controls.parquet`
- `data/processed/model_data_ena2024_plus_geo.parquet`
- `data/processed/model_data_ena2024_plus_geo2.parquet`

Logs are written to `logs/run_all_YYYYMMDD_HHMMSS.log`.

## UNKNOWNs and minimal verification steps
- **Delimiter and NA tokens**: Not explicitly specified.
  - Verify by inspecting a raw CSV with `pd.read_csv(..., nrows=1)` and checking column counts; if a single column appears, delimiter mismatch.
  - Scan for special NA codes and, if found, add `na_values=` to `ena.io.read_csv`.
- **Right-side key uniqueness** (CAP1000, CAP300, CAP700, etc.): Not enforced by `validate`.
  - Verify by running `df.duplicated(subset=ID_COLS).sum()` for each module.
- **Row-count preservation** in control merges: Not logged.
  - Add merge indicator logging (snippet above) to each merge.
- **Exact matched/unmatched counts** for external geo/climate joins: Only coverage ratios are computed, not exact join diagnostics.
  - Add merge indicator logging to `src/features/merge_geo_features.py`, `src/features/merge_temperature_features.py`, `src/features/merge_geo2_features.py`.
