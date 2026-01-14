# Variable Definitions Audit

## Practice Variables
- **Source:** `08_CAP300AB.csv` (P301A_*).
- **Coding check:** Raw values are `{1,2}` for all P301A_* checked; dictionary examples (e.g., P240) show `1=Si`, `2=No`, consistent with the current `==1` coding.
- **Construction:** `num_practices = sum(P301A_* == 1)` and `practice_any = num_practices > 0` (`src/ena/05_build_model_data.py`).
- **Prevalence:** `practice_any` mean approx 0.953; `num_practices` mean approx 7.06, max 21. High prevalence likely reflects broad inclusion of routine practices (plowing, fertilizers, pesticides) rather than only "sustainable" practices.
- **Risk:** Interpretation as "sustainable practices" is likely overstated unless a narrower subset is used.

## PSU / Strata / Weights
- **PSU:** `NSEGM` mapped to `psu` in `src/ena/02_build_schema_from_dictionary.py`; dictionary description: "Numero correlativo en secuencia serpentin por region."
- **PSU diagnostics:** 9,962 unique PSUs; mean cluster size approx 3.5 (max 20). PSU is unique within strata (no PSU spans >1 stratum).
- **Strata:** `ESTRATO` mapped to `estrato`; used in logit survey design.
- **Weights:** `FACTOR_PRODUCTOR` mapped to `weight`.

## Size Categories
- **Definition:** `size_cat` from `area_total_ha` bins: `<2`, `2-5`, `>5` ha.
- **Missingness:** 3.16% overall; concentrated in region 1 (~9.4%). Missing size implies missing `area_total_ha`.

## Monetary and Input Variables
- **Output:** `valor_total` = sum of P220_* value components (S/). Range: min 2, max 7,077,408; missing approx 9.6%.
- **Inputs:** `input_costs` = P237_VAL + P239 + P241 (S/). Max approx 33,612,372; share zero approx 15.9%; heavy tails.
- **Other costs (controls):** `gasto_agua_riego`, `gasto_semilla`, `capital_total` show large zero mass and extreme upper tails; log1p transforms used in models.

## Irrigation / Seed Controls
- **Irrigation:** `riego_crop` coded as `water_source != 1` (assumes code 1 indicates rainfed/none); `riego_tecnificado_crop` uses `irrigation_system` in {1..6}. Value codes need confirmation in the dictionary (not explicit in parsed tables).
- **Seed certification:** `seed_certified` codes 1/2 mapped to yes/no; consistent with other yes/no variables.

