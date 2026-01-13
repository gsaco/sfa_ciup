# Data Structure (ENA 2024)

## Unit of observation
- **Producer-level (unique keys)**: `CARATULA.csv` has one row per producer; keys `ANIO + CCDD + CCPP + CCDI + NSEGM + ID_PROD + UA` are unique.
- **Crop/plot-level (long)**: `USOSTIERRA.csv` and `03_CAP200AB.csv` repeat producers across crops/plots. Duplicate keys drop when adding a crop code, but some repeats persist, implying multiple entries per producer-crop (e.g., multiple plots or cycles).

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
