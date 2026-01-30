| variable             | definition                                                                                                           | notes                                 |
|:---------------------|:---------------------------------------------------------------------------------------------------------------------|:--------------------------------------|
| valor_total          | Sum of crop value components (P220_1_VAL, P220_2_VAL, P220_3A_VAL, P220_3B_VAL).                                     | Output for SFA.                       |
| area_total_ha        | ¿CUÁL FUE LA SUPERFICIE COSECHADA DE ……….? (Hectáreas)                                                               | Sum of harvested area across crops.   |
| diversificacion_area | 1 - HHI based on harvested area shares.                                                                              | Main diversification index.           |
| hhi_area             | Sum of squared harvested area shares.                                                                                | HHI concentration index.              |
| shannon_area         | Shannon entropy using harvested area shares.                                                                         | Alternative diversification index.    |
| num_crops_area       | Count of distinct crops (P204_COD).                                                                                  | Alternative diversification measure.  |
| labor_total          | Sum of permanent and seasonal workers (P1001A_2A_*C, P1001A_2B_*C).                                                  | Labor input.                          |
| input_costs          | Sum of expenditures on abono, fertilizantes, plaguicidas (P237_VAL, P239, P241).                                     | Intermediate input proxy.             |
| practice_any         | 1 if any of P301A_1, P301A_2, P301A_3, P301A_4, P301A_4A, P301A_4B, P301A_4C, P301A_11, P301A_16, P301A_17 equals 1. | Sustainable practices outcome.        |
| size_cat             | Producer size categories based on area_total_ha.                                                                     | Small <2ha, Medium 2-5ha, Large >5ha. |
| weight               | FACTOR DE EXPANSIÓN DE PRODUCTOR AGROPECUARIO                                                                        | Survey expansion weight.              |
| psu                  | NÚMERO CORRELATIVO EN SECUENCIA SERPENTIN POR REGIÓN                                                                 | Primary sampling unit.                |
| estrato              | ESTRATO MUESTRAL                                                                                                     | Sampling stratum.                     |