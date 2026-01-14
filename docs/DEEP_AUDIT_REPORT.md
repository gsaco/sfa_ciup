# Deep Audit Report

## Pipeline Status
- Full pipeline executed successfully via `scripts/run_all.sh` (baseline log: `logs/run_all_baseline.log`).
- Non-blocking warnings:
  - Raster extraction warnings (CHIRPS/temperature) and CHIRPS z-score division by zero.
  - SFA `gamma` near boundary and occasional singular covariance warnings.
  - Pandas `observed=False` future warnings.

## Team Findings (Role-Specific)

### PI (Applied Micro / Ag Econ)
- Diversification effects are heterogeneous; interactions by size dominate the SFA inefficiency equation.
- `practice_any` is too broad to be interpreted as "sustainable" without qualification; several practices are standard production activities.
- The strong positive logit coefficient on diversification likely reflects saturation rather than meaningful adoption margins.
- "Bad control" risk: some ENA controls (e.g., capital, irrigation cost) may be simultaneously outcomes of diversification or correlated with unobservables.

### Econometrician (SFA + Discrete Choice)
- SFA warnings (gamma near 1, singular covariance) signal possible misspecification or weak separation of noise/inefficiency.
- TE distribution is plausible but TE-diversification correlation is weak/negative; interpret Z effects cautiously.
- Logit outcome near-deterministic (practice_any ~95%); potential quasi-separation and inflated ORs.

### Survey Statistician
- Survey design implemented with `psu=NSEGM`, `estrato=ESTRATO`, `weight=FACTOR_PRODUCTOR`, `nest=TRUE`.
- PSUs are unique within strata; many strata have only one PSU (lonely PSU adjustment used).
- Weights are highly skewed; for robustness, report weighted and unweighted descriptive stats.

### Data Engineer (Python)
- End-to-end pipeline runs; outputs and manifest written successfully.
- `R/01_sfa_main.R` uses system Python for parquet conversion; risk if system Python lacks `pyarrow/pandas`.
- Added `scripts/plot_pack.py` and requirements for plotting (matplotlib, seaborn).

### Geo/Climate Scientist
- External merges use UBIGEO district capitals and align with expected Peru coordinate ranges.
- Climate/topo ranges plausible; match rates ~96.8%.
- Strong collinearity: `tmean_2024` vs `elev_m` (-0.925), `slope_deg` vs `ruggedness` (0.968).

### Scientific Editor
- Report is data-table heavy; interpretation needs explicit caveats re: saturation and SFA convergence.
- Plots now provide diagnostic context (data quality, geo coverage, TE patterns).

## Key Diagnostics
- `practice_any` mean: 0.953; `usuario_agua=1` implies `practice_any=1` ~99.9%.
- `size_cat` missingness 3.16% overall (region 1 ~9.4%).
- Output/input heavy tails; log1p used in models; max values up to 10^7-10^8.
- TE mean approx 0.539; declines with size category.

## Artifacts Produced
- Plot pack generated in `outputs/plots/` with manifest at `outputs/plots/00_index/plot_manifest.md`.
- Audit docs created: variable definitions, survey design, SFA interpretation, geo/climate, intuition vs results.

## Experiments Run
- **X01_strict_practice_any:** Reduced outcome saturation (mean 0.953 -> 0.867) and lowered diversification OR (approx 15.5 -> 5.7), but near-determinism with `usuario_agua` persisted. Reverted (definition choice not confirmed).
- **X02_standardize_sfa_z:** Standardization rescaled coefficients but did not remove gamma boundary or singular covariance warnings. Reverted.

## Remaining Follow-ups
- Decide (PI) whether to adopt a stricter practices subset or report both definitions as robustness.
- Explore alternative SFA specifications (e.g., trimming extremes, alternative functional forms) if convergence warnings remain critical.
