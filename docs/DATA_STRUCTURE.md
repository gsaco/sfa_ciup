# Data Structure (ENA 2024)

## Unit of observation
- **Producer-level (unique keys)**: `CARATULA.csv` has one row per producer; keys `ANIO + CCDD + CCPP + CCDI + NSEGM + ID_PROD + UA` are unique (40237 rows; 0 duplicates on keys).
- **Crop/plot-level (long)**: `USOSTIERRA.csv` and `03_CAP200AB.csv` repeat producers across crops/plots. Duplicate keys drop when adding a crop code, but some repeats persist, implying multiple entries per producer-crop (e.g., multiple plots or cycles).
  - `USOSTIERRA.csv`: 426505 rows; duplicates on producer keys = 424870; on keys+`P115_COD` = 259393; on keys+`P115_COD`+`P115_LOTE` = 102765.
  - `03_CAP200AB.csv`: 165711 rows; duplicates on producer keys = 160634; on keys+`P204_COD` = 71219; on keys+`P204_COD`+`P206_INI/FIN` = 54972; adding `P210_SUP_1/2` reduces to 35153.

## Keys and identifiers
- Primary keys used for joins: `ANIO`, `CCDD`, `CCPP`, `CCDI`, `NSEGM`, `ID_PROD`, `UA`.
- Crop identifiers (long modules): `P115_COD` in `USOSTIERRA.csv`; `P204_COD` in `03_CAP200AB.csv`.

## Survey design variables
- Weight: `FACTOR_PRODUCTOR` (producer expansion factor).
- Strata: `ESTRATO`.
- PSU/segment: `NSEGM`.

## Long vs wide notes
- Most CAP modules are wide at producer-level (no duplicate keys).
- Modules with crop/plot detail (`USOSTIERRA`, `CAP200*`) are long; aggregation to producer-level is required for modeling.
