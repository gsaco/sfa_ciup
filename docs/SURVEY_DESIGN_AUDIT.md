# Survey Design Audit

Note: `practice_any` now uses P301A_1-4C, P301A_11, P301A_16, P301A_17. Current prevalence is ~0.776 (see `outputs/tables/00_sample_overview.*`).

## Design Implementation
- **Logit models:** `R/02_logit_practices.R` uses `svydesign(ids=~psu, strata=~estrato, weights=~weight, nest=TRUE)` with `survey.lonely.psu="adjust"`.
- **PSU / strata coverage:** No missing `psu` or `estrato` in the logit estimation sample. PSUs are unique within strata; no PSU spans multiple strata.
- **Cluster sizes:** Mean PSU cluster size approx 3.85 (max 20). Many strata have only one PSU (lonely PSU handling is enabled).
- **Weights:** `FACTOR_PRODUCTOR` used directly; distribution is highly right-skewed (max ~20,703).

## Risks / Limitations
- **Small clusters:** Many single-PSU strata can inflate variance estimates; the "adjust" option mitigates but does not eliminate sensitivity.
- **Outcome prevalence:** `practice_any` is common (~0.776), but not saturated. Separation risk is lower than before, yet ORs should be interpreted cautiously.

## SFA Note
- **Weights not used:** SFA is unweighted due to package limitations (as stated in the report). This should be emphasized as a limitation for population-level inference.

## Recommendation
- If a more appropriate PSU variable exists in ENA metadata (e.g., cluster/conglomerate ID), re-estimate logit models with that PSU and compare SEs. No alternative PSU variable was found in the parsed dictionary; NSEGM appears to be the intended PSU.
