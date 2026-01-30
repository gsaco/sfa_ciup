# SFA Interpretation Audit

## Model Setup
- Frontier: `log(valor_total)` on `log_land`, `log_labor`, `log_inputs` (where `log_inputs` uses `input_costs_sfa`).
- Inefficiency (`zNames`): diversification, size dummies, interactions **and region dummies** (regions live in Z, not X).
- Assumptions: `ineffDecrease=TRUE`, half‑normal inefficiency (`truncNorm=FALSE`), no time effects.
- Estimation: unweighted (package limitation).

## Coefficient Interpretation
- With `ineffDecrease=TRUE`, **positive Z coefficients reduce inefficiency** (raise TE) and **negative Z coefficients increase inefficiency** (lower TE).
- Main SFA estimates (`outputs/tables/02_sfa_main.csv`, model `main_area`):
  - `Z_diversificacion_area` = **1.93** (p < 1e-15): diversification improves efficiency for the baseline size group.
  - `Z_diversif_mediano` = **-0.20** (p = 0.41): no statistically clear difference from the baseline effect.
  - `Z_diversif_grande` = **-5.54** (p < 1e-15): diversification **worsens** efficiency for large farms (net effect flips sign).
  - Region Z terms are large and positive, implying higher efficiency in regions 2–3 relative to region 1, conditional on inputs.

## Efficiency (TE) Diagnostics
- TE range: **0.0001–0.89**; mean **~0.47**, median **~0.51** (see `data/processed/ena2024_with_TE.parquet` and `reports/run_results_summary.md`).
- TE by size/region: see `outputs/tables/03_sfa_te.parquet` summary tables in `reports/reporte_final.md` for current group means.

## Convergence / Reliability Concerns
- `gamma` (main) ≈ **0.933**; range across models **0.844–0.989** (see `outputs/tables/02_sfa_diagnostics.csv`).
- Covariance matrices are **not singular** in the current run; however, some geo/climate specs still have large condition numbers → interpret SEs with caution.

## Interpretation Guidance
- Emphasize **combined marginal effects**: diversification’s net effect depends on size because of interactions.
- Use TE summaries to ground coefficient interpretation; avoid reading single Z coefficients in isolation.
- Present results as **associational**, not causal, given unweighted SFA and potential endogeneity of diversification.
