# Data Gaps and Fallbacks

## Output (Y) for SFA
- **Plan A (used)**: `valor_total` from crop module `03_CAP200AB.csv`, sum of value components (`P220_1_VAL`, `P220_2_VAL`, `P220_3A_VAL`, `P220_3B_VAL`).
- **Plan B**: use total production quantities (`P219_*`) with regional prices (not available in repo).
- **Plan C**: proxy output with total agricultural expenses (`P1001A_TOTAL`) if value data are missing.

## Land input
- **Plan A (used)**: harvested area `P217_SUP_ha` aggregated by producer.
- **Plan B**: total parcel area from `P104_*` or `P105_SUP_ha`.
- **Plan C**: use `USOSTIERRA` area if CAP200AB missing.

## Labor input
- **Plan A (used)**: counts of permanent + seasonal workers (`P1001A_2A_*C`, `P1001A_2B_*C`).
- **Plan B**: labor cost variables (`P1001A_2A_*`, `P1001A_2B_*`) as proxy.
- **Plan C**: omit labor and document limitation.

## Input costs
- **Plan A (used)**: sum of `P237_VAL` (abono), `P239` (fertilizantes), `P241` (plaguicidas).
- **Plan B**: total agricultural expenses `P1001A_TOTAL`.
- **Plan C**: omit input costs and document limitation.

## Sustainable practices outcome
- **Plan A (used)**: `practice_any` = 1 if any `P301A_*` practice equals 1.
- **Plan B**: stricter outcome `num_practices >= 2`.
- **Plan C**: use training variables `P701*` as proxy for sustainability (not used).

## Survey design
- **Weights**: `FACTOR_PRODUCTOR` available; used in logit.
- **SFA weights**: not supported by `frontier`; unweighted SFA is documented as a limitation.

## Coverage issues
- Some geographic codes (`CCDD/CCPP/CCDI`) are missing for ~2.6–4.3% of records; handled as missing in joins/filters.
- `valor_total` and `diversificacion_area` have non-trivial missingness (~9.6% and ~3.2% respectively); models drop missing rows.
- CHIRPS baseline window uses 2015–2020 as a fallback; 1991–2020 was not used due to download size/time constraints.
