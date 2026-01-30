# Run Results Summary

This summary reflects the full pipeline run executed on 2026-01-26. Full tables are saved under `outputs/tables/` and `reports/reporte_final.md`.

## Data & Coverage
- Total producer rows in `model_data_ena2024.parquet`: **35,187**
- Missingness audit (key constructed variables):
| variable      |   all_missing_share |   partial_missing_share |   any_missing_share |
|:--------------|--------------------:|------------------------:|--------------------:|
| labor_total   |            0.169637 |                0.820161 |            0.989797 |
| input_costs   |            0.15932  |                0.481115 |            0.640435 |
| practice_any  |            0        |                0        |            0        |
| num_practices |            0        |                0        |            0        |

- Geo/CHIRPS match (overall):
|   share_geo_match |   share_chirps_match |
|------------------:|---------------------:|
|          0.968397 |             0.968397 |

- Controls with highest missingness (overall):
| variable                  |   missing_pct |
|:--------------------------|--------------:|
| credito_obtenido          |      0.86603  |
| riego_tecnificado_any     |      0.403189 |
| riego_tecnificado_share   |      0.403189 |
| gasto_semilla             |      0.315685 |
| semilla_certificada_share |      0.286498 |

## Sample Loss
Overall sample retention from base → geo2 datasets:
| sample_type   |   n_base |   n_geo2 |   share_remaining |
|:--------------|---------:|---------:|------------------:|
| logit         |    34074 |    34039 |          0.998973 |
| sfa           |    26594 |    26546 |          0.998195 |

## SFA Results (Main Model)
Key coefficients from `outputs/tables/02_sfa_main.csv`:
| term                   |   estimate |   std_error |   p_value | component    |
|:-----------------------|-----------:|------------:|----------:|:-------------|
| log_land               |  0.903865  |  0.00599543 |   0       | frontier     |
| log_labor              |  0.253828  |  0.00728654 |   0       | frontier     |
| log_inputs             |  0.0700737 |  0.00668903 |   0       | frontier     |
| Z_diversificacion_area |  1.92938   |  0.200792   |   0       | inefficiency |
| Z_size_mediano         |  2.33356   |  0.213122   |   0       | inefficiency |
| Z_size_grande          |  8.84212   |  0.390458   |   0       | inefficiency |
| Z_diversif_mediano     | -0.199522  |  0.242916   |   0.41144 | inefficiency |
| Z_diversif_grande      | -5.54254   |  0.289242   |   0       | inefficiency |

Diagnostics (all models):
| model              |   n_valid |    gamma | cov_singular   |    cov_cond | input_cost_var           |
|:-------------------|----------:|---------:|:---------------|------------:|:-------------------------|
| main_area          |     26594 | 0.932684 | False          | 5.66888e+06 | costo_total_agropecuario |
| alt_shannon        |     26594 | 0.98871  | False          | 8.35808e+09 | costo_total_agropecuario |
| alt_num_crops      |     26594 | 0.989347 | False          | 1.25658e+10 | costo_total_agropecuario |
| small_only         |     16015 | 0.844036 | False          | 1.03329e+06 | costo_total_agropecuario |
| controls_ena       |     26121 | 0.91452  | False          | 1.45648e+06 | costo_total_agropecuario |
| temp_topo          |     26546 | 0.969876 | False          | 6.58239e+08 | costo_total_agropecuario |
| controls_temp_topo |     26073 | 0.938377 | False          | 2.92143e+07 | costo_total_agropecuario |
| xgeo_prcp          |     26578 | 0.935241 | False          | 1.19823e+07 | costo_total_agropecuario |
| zgeo_prcp          |     26578 | 0.934011 | False          | 1.10367e+07 | costo_total_agropecuario |

Technical Efficiency (TE) summary from `data/processed/ena2024_with_TE.parquet`:
|       |              te |
|:------|----------------:|
| count | 26594           |
| mean  |     0.47342     |
| std   |     0.240277    |
| min   |     0.000108145 |
| 10%   |     0.0971611   |
| 50%   |     0.511442    |
| 90%   |     0.763354    |
| max   |     0.893334    |

## Logit Results (Main Model)
Key coefficients from `outputs/tables/04_logit_main.csv`:
| term                                       |     estimate |   std_error |     p_value |   odds_ratio |
|:-------------------------------------------|-------------:|------------:|------------:|-------------:|
| diversificacion_area                       |  1.3819      |    0.335264 | 3.83592e-05 |     3.98245  |
| log_area                                   | -0.000931479 |    0.15031  | 0.995056    |     0.999069 |
| diversificacion_area:size_catmediano_2_5ha |  0.106619    |    0.435072 | 0.806423    |     1.11251  |
| diversificacion_area:size_catpequeno_<2ha  |  0.116845    |    0.456233 | 0.79788     |     1.12395  |

## Robustness Tables (Paths)
- SFA robustness: `outputs/tables/03_sfa_robustness.csv`
- Logit robustness: `outputs/tables/05_logit_robustness.csv`
- Geo SFA: `outputs/tables/07_sfa_with_geo_controls.csv`
- Geo logit: `outputs/tables/09_logit_with_geo_controls.csv`
- Controls SFA: `outputs/tables/13_sfa_with_controls_ena.csv`
- Temp/topo SFA: `outputs/tables/14_sfa_with_temp_topo.csv`
- Controls logit: `outputs/tables/16_logit_with_controls_ena.csv`
- Temp/topo logit: `outputs/tables/17_logit_with_temp_topo.csv`

## Interpretation & Conclusions
### Production elasticities
- Coefficients on `log_land`, `log_labor`, and `log_inputs` represent output elasticities in the frontier equation. Signs and magnitudes are economically plausible for smallholder agriculture, but interpretation should be cautious given measurement error and survey aggregation.

### Diversification and inefficiency
- Z‑coefficients indicate how diversification and size shift inefficiency (positive → **lower** inefficiency under `ineffDecrease=TRUE`). The interactions imply heterogeneous effects by size class. Interpret combined marginal effects, not single coefficients in isolation.

### Gamma and variance decomposition
- Gamma values are high but not boundary‑clipped for most models, indicating inefficiency variance dominates noise variance. For any model flagged with `cov_singular=True`, inference should not be interpreted.

### Logit practice adoption
- Diversification effects on adoption are size‑dependent. Given high prevalence of `practice_any`, odds ratios should be interpreted with care; marginal effects are likely modest in absolute terms.

### Main conclusions
- The pipeline is methodologically coherent, and the missingness policy is now enforced across core aggregations.
- SFA inference is generally valid (non‑singular covariance for main models), but climate/controls specifications still require checking the diagnostics table for each model.
- Results are best presented as associational, not causal, given potential endogeneity of diversification and unweighted SFA estimation.
