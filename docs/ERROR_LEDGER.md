# Error Ledger

## Blockers
- None observed in baseline pipeline run (`logs/run_all_baseline.log`).

## Warnings / Modeling Risks
- **SFA convergence warnings (high severity for inference):** `gamma` near boundary and singular covariance reported multiple times during `R/01_sfa_main.R` (see `logs/run_all_baseline.log`). This can invalidate standard errors and hypothesis tests.
- **Raster extraction warnings (medium severity):** `rasterio` invalid cast warnings during CHIRPS and temperature extraction, and `prcp_total_z` division warnings when baseline std is zero (`src/external/chirps/extract_chirps_points.py:91`). These likely correspond to out-of-bounds or zero-variance baseline pixels; the outputs are set to `NaN` but should be tracked.
- **Outcome near-determinism (medium severity):** `practice_any` is ~95% overall, and `usuario_agua=1` almost always implies `practice_any=1` (row share ~99.9%). This can cause quasi-separation and unstable logit inference.

## Pipeline / Reproducibility Risks
- **R-to-Python parquet conversion dependency:** `R/01_sfa_main.R` uses `system2("python", ...)` (not the venv) to write parquet. If system Python lacks `pandas/pyarrow`, TE parquet outputs will fail. Consider pinning the venv python path or adding a fallback.
- **Pandas FutureWarnings:** Groupby `observed=False` warnings in QA and plot scripts indicate future behavior changes; not blocking but should be tracked.

## Data Gaps / Sample Loss Notes
- **Missing `area_total_ha` and `valor_total`:** `area_total_ha` missing share ~3.16% (region 1 ~9.4%), `valor_total` missing share ~9.6%; these drive sample loss in SFA/logit and may bias results.

