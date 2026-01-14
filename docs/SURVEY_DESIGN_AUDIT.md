# Survey Design Audit

## Design Implementation
- **Logit models:** `R/02_logit_practices.R` uses `svydesign(ids=~psu, strata=~estrato, weights=~weight, nest=TRUE)` with `survey.lonely.psu="adjust"`.
- **PSU / strata coverage:** No missing `psu` or `estrato` in the logit estimation sample. PSUs are unique within strata; no PSU spans multiple strata.
- **Cluster sizes:** Mean PSU cluster size approx 3.85 (max 20). Many strata have only one PSU (lonely PSU handling is enabled).
- **Weights:** `FACTOR_PRODUCTOR` used directly; distribution is highly right-skewed (max ~20,703).

## Risks / Limitations
- **Small clusters:** Many single-PSU strata can inflate variance estimates; the "adjust" option mitigates but does not eliminate sensitivity.
- **Outcome prevalence:** With `practice_any` approx 95%, effective information for binary models is limited; separation-like behavior is possible.

## SFA Note
- **Weights not used:** SFA is unweighted due to package limitations (as stated in the report). This should be emphasized as a limitation for population-level inference.

## Recommendation
- If a more appropriate PSU variable exists in ENA metadata (e.g., cluster/conglomerate ID), re-estimate logit models with that PSU and compare SEs. No alternative PSU variable was found in the parsed dictionary; NSEGM appears to be the intended PSU.

