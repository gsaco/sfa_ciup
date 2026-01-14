# SFA Interpretation Audit

## Model Setup
- Frontier: log output (`log(valor_total)`) on log inputs (land, labor, inputs) + region dummies.
- Inefficiency (`zNames`): diversification, size dummies, and interactions.
- Estimation: unweighted (package limitation).

## Coefficient Interpretation
- In `frontier`, **positive Z coefficients increase inefficiency** (reduce TE), while negative Z coefficients decrease inefficiency (raise TE).
- Main SFA estimates (`outputs/tables/02_sfa_main.csv`):
  - `Z_diversificacion_area` is **negative** (approx -14.93), implying diversification reduces inefficiency (higher TE), **holding size interactions**.
  - Size and interaction terms are large and mixed in sign; interpretation depends on combined effects.

## Efficiency (TE) Diagnostics
- TE range: **0.0001-0.89** (mean approx 0.539).
- TE by size (mean): small approx 0.568, medium approx 0.524, large approx 0.442.
- TE by region (mean): region 1 approx 0.556, region 2 approx 0.542, region 3 approx 0.507.
- TE vs diversification correlation: **-0.039** (weak negative), suggesting that the raw TE-diversification relationship is not strongly positive despite the negative Z coefficient.

## Convergence / Reliability Concerns
- `gamma` approx 0.998 with repeated warnings and singular covariance in robustness models.
- Large Z coefficients and boundary gamma suggest possible misspecification or overfitting in the inefficiency equation.

## Interpretation Guidance
- Emphasize combined marginal effects: diversification effect depends on size category because of interactions.
- Report TE patterns (size/region) alongside coefficient signs to avoid over-interpreting raw Z values.
- Present results as associative, not causal, given unweighted SFA and potential misspecification.

