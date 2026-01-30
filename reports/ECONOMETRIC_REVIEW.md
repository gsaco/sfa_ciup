# MIT Econometric Review of `sfa_ciup` Pipeline
Date: 2026-01-26

## Executive Summary (Brutal, but fair)
- **Core pipeline is coherent and mostly correct**, but a few methodological choices materially affect inference. The main remaining issues are (i) endogeneity of diversification, (ii) sensitivity of SFA to cost proxies and Z specification, and (iii) unweighted SFA (package limitation).
- **Recent fixes improved SFA reliability**: moving region dummies to the inefficiency equation and using total cost for inputs reduced gamma from ~0.999 to ~0.93 and eliminated singular covariance matrices. This makes inference *possible* (though still fragile).
- **Remaining risks are economic, not just technical**: endogeneity of diversification, measurement error in inputs, climate/topography point sampling, and high practice prevalence in logit models.
- **Documentation alignment is now improved**, but any future changes to specs/controls should be mirrored in `docs/MODELS.md`, `docs/ENA_CONTROLS_MAPPING.md`, and `docs/SFA_INTERPRETATION_AUDIT.md`.

---

## 1) Full Process Map (End-to-End)
This is the effective pipeline executed by `scripts/run_all.sh`:
1. **Repo scan + profiling**
   - `src/ena/scan_repo.py`
   - `src/ena/01_load_and_profile.py` → module profile + key diagnostics
2. **Schema creation and application**
   - `src/ena/02_build_schema_from_dictionary.py`
   - `src/ena/03_apply_schema.py`
3. **Diversification indices**
   - `src/ena/04_compute_diversification.py`
4. **Model dataset assembly**
   - `src/ena/05_build_model_data.py`
   - `src/ena/06_build_model_data_plus_controls.py`
5. **External data ingestion**
   - UBIGEO: `src/external/ubigeo/*`
   - CHIRPS: `src/external/chirps/*`
   - Temperature (TerraClimate): `src/external/temperature/*`
   - Topography (Copernicus DEM): `src/external/topography/*`
6. **Feature merges**
   - `src/features/merge_geo_features.py`
   - `src/features/merge_temperature_features.py`
   - `src/features/merge_geo2_features.py`
7. **Sample loss QA**
   - `src/qa/sample_loss_analysis.py`
8. **Econometric estimation**
   - SFA: `R/01_sfa_main.R`
   - Logit: `R/02_logit_practices.R`
9. **Report build**
   - `src/report/build_report.py`

**Assessment**: Process coverage is solid and modular. Key steps are sequenced correctly, with diagnostics and tables produced at each stage. The missingness policy is now enforced in core sums and aggregations (see Section 4).

---

## 2) Data Sources (Primary and External)
### Primary (ENA 2024)
- Raw modules under `data/raw/ENA_2024/`
- Dictionary: `DICCIONARIO DE DATOS ENA-2024.pdf`
- Keys: `ANIO, CCDD, CCPP, CCDI, NSEGM, ID_PROD, UA`
- Survey design: `FACTOR_PRODUCTOR` (weights), `ESTRATO` (strata), `NSEGM` (PSU)

### External (geo/climate/topo)
Sources are documented in repo. URLs listed here in code block per repo policy:
```
UBIGEO fallback: https://raw.githubusercontent.com/jmcastagnetto/ubigeo-peru-aumentado/master/ubigeo_distrito.csv
CHIRPS v2 monthly: https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/
TerraClimate THREDDS: http://thredds.northwestknowledge.net:8080/thredds/catalog/TERRACLIMATE_ALL/data/catalog.html
Copernicus DEM 90m: https://copernicus-dem-90m.s3.amazonaws.com/
```

**Assessment**: Sources are credible and standard for Peru. Climate/topography data are gridded and sampled at district capitals, which is a **known representativeness risk** for heterogeneous districts.

---

## 3) Key Variable Construction (with provenance)
### Core production variables
- **Output**: `valor_total`
  - Source: CAP200AB crop module (value components)
  - In `src/ena/04_compute_diversification.py`, crop-level `valor_total_cultivo` = sum of value components.
- **Land**: `area_total_ha`
  - Source: CAP200AB harvested area (aggregated)
- **Labor**: `labor_total`
  - Source: CAP1000 (`P1001A_2A_*C` and `P1001A_2B_*C`)
  - Constructed in `src/ena/05_build_model_data.py`
- **Input costs (component sum)**: `input_costs`
  - Source: CAP200E `P237_VAL` (abono), `P239` (fertilizantes), `P241` (plaguicidas)
  - Constructed in `src/ena/05_build_model_data.py`
- **Input costs (SFA proxy)**: `input_costs_sfa`
  - Source: CAP1000 `costo_total_agropecuario` (preferred) or `gasto_agricola_total` fallback
  - Used in `R/01_sfa_main.R`

### Diversification
- `diversificacion_area`, `hhi_area`, `shannon_area`, `num_crops_area`
- `diversificacion_valor`, `hhi_valor`, `shannon_valor`, `num_crops_valor`
- Method: HHI and Shannon on crop shares (see `docs/DIVERSIFICATION_INDEX.md`)

### Practices (logit outcome)
- `practice_any`: any of `P301A_1, 2, 3, 4, 4A, 4B, 4C, 11, 16, 17` equals 1
- `num_practices`: count of those == 1

### Size category
- `size_cat`: based on `area_total_ha` cut at 2 and 5 hectares

### Controls (ENA modules)
Derived via `src/features/ena_controls.py` and merged in `src/ena/06_build_model_data_plus_controls.py`. Examples:
- Irrigation: `riego_any`, `riego_share` (and `riego_tecnificado_*` computed but high missingness)
- Machinery: `uso_maquinaria`, `gasto_compra_*`, `gasto_alquiler_mant_equipos` (counts `num_maquinaria_equipo` are high-missing)
- Seeds/fertilizer: `usa_abono`, `usa_fertilizantes`, `semilla_semillero_any`, `semilla_comercial_any`
- Extension/credit/education: `capacitacion_recibida`, `asistencia_tecnica_recibida`, `nivel_educacion`, `asociacion_miembro` (credit is high-missing)

**Assessment**: The variable logic is economically plausible and mostly correct. Missingness handling has been standardized (see Section 4), and the main controls set now excludes high‑missing variables to preserve sample size.

---

## 4) Missingness Policy (Correctness Assessment)
### Current policy (as implemented)
- **Sums of components** use `min_count=1` so all-missing → NA (fixed in `src/ena/05_build_model_data.py`).
- **Yes/no indicators**: standardized mapping (`1→1`, `2/0→0`, others → NA), with explicit `*_missing` flags.
- **Zero fill** only when a “no” indicator logically implies zero (e.g., no irrigation → zero irrigation spending).
- Diagnostic output: `outputs/tables/19_missingness_audit.csv`.

### Status
- Crop‑level `valor_total_cultivo` now uses `min_count=1`, so all‑missing components remain NA and value‑based diversification does not silently impute zeros.

**Assessment**: The missingness policy is now consistent across core sums and aggregations.

---

## 5) Model Specifications (As Implemented)
### SFA (R/01_sfa_main.R)
- **Package**: `frontier`
- **Assumptions**:
  - `ineffDecrease = TRUE`
  - `truncNorm = FALSE` (half‑normal inefficiency)
  - `timeEffect = FALSE`
- **Frontier equation (X)**:
  - Main: `log_y ~ log_land + log_labor + log_inputs`
  - `log_inputs` uses `input_costs_sfa = costo_total_agropecuario` (fallback to `gasto_agricola_total` or `input_costs` if absent)
- **Inefficiency equation (Z)**:
  - `diversificacion_area`, size dummies, interactions
  - **Region dummies moved to Z** (important for identification and gamma stability)
- **Geo/Climate**:
  - `xgeo_prcp`: adds `prcp_total_z` to X
  - `zgeo_prcp`: adds `prcp_total_z` to Z
  - `temp_topo`: adds climate/topo variables to X (currently excludes `elev_m` to avoid rank deficiency)
- **Outputs**: `outputs/tables/02_sfa_main.csv`, `outputs/tables/02_sfa_diagnostics.csv`, `outputs/tables/03_sfa_robustness.csv`, `outputs/tables/03_sfa_te.parquet`

### Logit (R/02_logit_practices.R)
- **Package**: `survey`
- **Outcome**: `practice_any`
- **Spec**: `practice_any ~ diversificacion_area * size_cat + log(area_total_ha + 1) + region_natural`
- **Survey design**:
  - `ids = ~psu`, `strata = ~estrato`, `weights = ~weight`
  - `survey.lonely.psu = "adjust"`

**Assessment**:
- The SFA spec is now **substantively improved**. Gamma is no longer boundary‑clipped, and covariance matrices are nonsingular across models.
- The logit spec is correctly survey‑weighted. Outcome prevalence is high but not saturated (see `docs/SURVEY_DESIGN_AUDIT.md`); separation risk is lower but ORs should still be interpreted cautiously.

---

## 6) Diagnostics and Correctness Checks
### SFA diagnostics (`outputs/tables/02_sfa_diagnostics.csv`)
- **Gamma** now ranges ~0.84–0.98 (main ≈ 0.93) instead of ~0.999.
- **Covariance**: nonsingular for all models after spec changes.
- **Condition numbers** are still large for some climate models → inference is possible but still fragile.

### Missingness audit (`outputs/tables/19_missingness_audit.csv`)
- Labor components: large partial missingness (~82%) → explains sample loss.
- Inputs (component sum): ~48% partial missingness.

**Assessment**: Diagnostics are now honest and actionable. The prior boundary gamma and singular covariance issues were real and are now addressed.

---

## 7) Economic Interpretation (Current Spec)
### SFA
- **Frontier coefficients** are *elasticities* of output with respect to inputs (land, labor, inputs).
- **Inefficiency (Z) coefficients**: with `ineffDecrease=TRUE`, positive values **reduce** inefficiency (raise TE); negative values **increase** inefficiency.
- **Diversification**: `Z_diversificacion_area` is positive in the main model, while the large‑farm interaction is strongly negative; the net effect depends on size category.
- **Region effects** now enter inefficiency rather than the frontier, implying structural heterogeneity is interpreted as *inefficiency heterogeneity* rather than technology shifts.
- **Gamma ≈ 0.93** implies most residual variance is attributed to inefficiency. This can be economically plausible for smallholder production but still signals that the noise component is small.

### Logit (practice adoption)
- Coefficients are in log‑odds; `exp(beta)` yields odds ratios.
- Interaction with size category implies **heterogeneous diversification effects** by farm size.
- Given relatively high prevalence of `practice_any`, marginal effects are likely modest in absolute terms even if statistically significant.

---

## 8) Assessment of Correctness (By Stage)
### ✅ Correct / defensible
- Key joins by producer ID (`ANIO+CCDD+CCPP+CCDI+NSEGM+ID_PROD+UA`).
- Diversification index formulas and aggregation logic.
- Survey‑weighted logit specification.
- New missingness policy for sums and indicators.
- SFA diagnostics with explicit gamma/singularity reporting.
- TE alignment with estimation sample.

### ⚠️ Potentially wrong / needs revision
- **External climate features** use point sampling; district heterogeneity is ignored, which can bias climate controls.
- **High‑missing controls** (credit, technified irrigation, seed certification) are excluded from the main specs; if included, sample loss is large and needs explicit reporting.

### Structural econometric risks (not “bugs,” but real)
- **Diversification endogeneity**: diversification is likely jointly determined with productivity; SFA “inefficiency equation” does not solve endogeneity.
- **Measurement error** in inputs (labor, costs) is likely high; with log transforms, this can bias elasticities and inflate inefficiency variance.
- **Unweighted SFA**: without survey weights, estimates are not strictly population‑representative.

---

## 9) Recommendations (Minimal but important)
1. **Document the current specs** in outputs and reports (especially Z vs X placement, input cost proxy, and missingness policy).
2. **Consider an IV strategy or panel extension** if causal statements about diversification are required.
3. **Report robustness** across alternative input cost measures (component sum vs total cost), since that materially affects gamma.
4. **Monitor condition numbers** and flag any models with unstable covariance in `outputs/tables/02_sfa_diagnostics.csv`.

---

## Appendix: Current Model Coefficients (Main SFA Z Terms)
From `outputs/tables/02_sfa_main.csv`:
- `Z_diversificacion_area` = 1.929
- `Z_diversif_mediano` = −0.200
- `Z_diversif_grande` = −5.543
- Region Z terms are positive (region 2, region 3)

Interpretation (ineffDecrease=TRUE): For small farms (baseline), diversification **reduces** inefficiency (higher TE). For large farms, the interaction reverses the effect, implying **higher** inefficiency with diversification. This is a nuanced, size‑dependent pattern, not a single monotone story.

---

## Bottom Line (MIT‑style): Are you doing something wrong?
Not fundamentally. The pipeline is rigorous and the fixes you implemented were necessary and correct. The remaining “wrongness” is mostly about **economic identification** and **documentation drift**, not code errors. If you present results as associative with robust diagnostics, you are on solid ground. If you present them as causal, you’re over‑claiming.
