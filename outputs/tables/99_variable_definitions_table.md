| variable             | definition                                                                       | notes                                 |
|:---------------------|:---------------------------------------------------------------------------------|:--------------------------------------|
| valor_total          | Sum of crop value components (P220_1_VAL, P220_2_VAL, P220_3A_VAL, P220_3B_VAL). | Output for SFA.                       |
| area_total_ha        | ¿CUÁL FUE LA SUPERFICIE COSECHADA DE ……….? (Hectáreas)                           | Sum of harvested area across crops.   |
| diversificacion_area | 1 - HHI based on harvested area shares.                                          | Main diversification index.           |
| hhi_area             | Sum of squared harvested area shares.                                            | HHI concentration index.              |
| shannon_area         | Shannon entropy using harvested area shares.                                     | Alternative diversification index.    |
| num_crops_area       | Count of distinct crops (P204_COD).                                              | Alternative diversification measure.  |
| labor_total          | Sum of permanent and seasonal workers (P1001A_2A_*C, P1001A_2B_*C).              | Labor input.                          |
| input_costs          | Sum of expenditures on abono, fertilizantes, plaguicidas (P237_VAL, P239, P241). | Intermediate input proxy.             |
| practice_any         | 1 if any agricultural practice P301A_* equals 1.                                 | Sustainable practices outcome.        |
| size_cat             | Producer size categories based on area_total_ha.                                 | Small <2ha, Medium 2-5ha, Large >5ha. |
| weight               | FACTOR DE EXPANSIÓN DE PRODUCTOR AGROPECUARIO                                    | Survey expansion weight.              |
| psu                  | NÚMERO CORRELATIVO EN SECUENCIA SERPENTIN POR REGIÓN                             | Primary sampling unit.                |
| estrato              | ESTRATO MUESTRAL                                                                 | Sampling stratum.                     |