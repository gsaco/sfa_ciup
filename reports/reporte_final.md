# El rol de la diversificacion de cultivos en la productividad agropecuaria: El caso del Peru

## Motivacion y preguntas

Se evalua la relacion entre diversificacion de cultivos y productividad/eficiencia (SFA), asi como su asociacion con practicas sostenibles (logit) usando ENA 2024.

## Datos ENA 2024 y diseno muestral

Fuente: ENA 2024 (INEI). Diseno muestral con pesos (FACTOR_PRODUCTOR), estratos y PSU.

### Tabla 00. Resumen muestral

| group_type   | group         |     n |       weight_sum |   mean_area_ha |   mean_valor_total |   mean_diversif |   mean_practice_any |
|:-------------|:--------------|------:|-----------------:|---------------:|-------------------:|----------------:|--------------------:|
| overall      | overall       | 35187 |      2.12001e+06 |       4.59897  |           28857.5  |        0.504382 |            0.952934 |
| region       | 1             |  8263 | 261788           |       4.29902  |           70773.2  |        0.422817 |            0.990922 |
| region       | 2             | 20601 |      1.54026e+06 |       1.85572  |            7172.15 |        0.567544 |            0.992476 |
| region       | 3             |  6323 | 317957           |      14.0166   |           46391    |        0.394723 |            0.774474 |
| size         | grande_>5ha   |  5840 | 232992           |      20.6877   |          119622    |        0.532199 |            0.89589  |
| size         | mediano_2_5ha |  6278 | 355684           |       3.20459  |           29777.7  |        0.541143 |            0.953011 |
| size         | pequeno_<2ha  | 21957 |      1.53022e+06 |       0.718452 |            5667.01 |        0.486473 |            0.966888 |
| size         | nan           |  1112 |   1112           |     nan        |             nan    |      nan        |            0.976598 |

## Indice de diversificacion (HHI)

| group_type   | group         |     n |   mean_diversificacion |   mean_hhi |   mean_num_crops |   mean_area_ha |
|:-------------|:--------------|------:|-----------------------:|-----------:|-----------------:|---------------:|
| overall      | overall       | 35187 |               0.504382 |   0.495618 |          3.5021  |       4.59897  |
| region       | 1             |  8263 |               0.422817 |   0.577183 |          3.30485 |       4.29902  |
| region       | 2             | 20601 |               0.567544 |   0.432456 |          3.64169 |       1.85572  |
| region       | 3             |  6323 |               0.394723 |   0.605277 |          3.28033 |      14.0166   |
| size         | grande_>5ha   |  5840 |               0.532199 |   0.467801 |          3.71336 |      20.6877   |
| size         | mediano_2_5ha |  6278 |               0.541143 |   0.458857 |          3.93883 |       3.20459  |
| size         | pequeno_<2ha  | 21957 |               0.486473 |   0.513527 |          3.32104 |       0.718452 |
| size         | nan           |  1112 |             nan        | nan        |        nan       |     nan        |

## Resultados SFA

| model | term | estimate | std_error | z_value | p_value | component | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main_area | (Intercept) |    8.7389376 | 2.136255e-02 |  409.077456 | 0.000000e+00 | frontier |
| main_area | log_land |    0.7321364 | 4.863750e-03 |  150.529207 | 0.000000e+00 | frontier |
| main_area | log_labor |    0.2396973 | 5.821649e-03 |   41.173440 | 0.000000e+00 | frontier |
| main_area | log_inputs |    0.1113705 | 2.407959e-03 |   46.250986 | 0.000000e+00 | frontier |
| main_area | region_natural2 |   -1.0062810 | 1.468704e-02 |  -68.514905 | 0.000000e+00 | frontier |
| main_area | region_natural3 |   -0.1579736 | 2.016540e-02 |   -7.833894 | 4.662937e-15 | frontier |
| main_area | Z_(Intercept) | -417.6695560 | 5.426450e+01 |   -7.696920 | 1.398881e-14 | inefficiency |
| main_area | Z_diversificacion_area |  -14.9304685 | 1.820617e+00 |   -8.200775 | 2.220446e-16 | inefficiency |
| main_area | Z_size_mediano |  -19.2780162 | 3.638200e+00 |   -5.298779 | 1.165796e-07 | inefficiency |
| main_area | Z_size_grande |  228.3013445 | 2.984120e+01 |    7.650543 | 1.998401e-14 | inefficiency |
| main_area | Z_diversif_mediano |  174.7929733 | 2.397926e+01 |    7.289341 | 3.115286e-13 | inefficiency |
| main_area | Z_diversif_grande |  -69.9012745 | 1.023423e+01 |   -6.830143 | 8.482992e-12 | inefficiency |
| main_area | sigmaSq |  323.0055372 | 4.225682e+01 |    7.643868 | 2.109424e-14 | variance |
| main_area | gamma |    0.9983073 | 2.389178e-04 | 4178.454385 | 0.000000e+00 | variance |


### Robustez SFA

| model | term | estimate | std_error | z_value | p_value | component | 
| --- | --- | --- | --- | --- | --- | --- | 
 | alt_shannon | (Intercept) |    8.73208342 | 2.170209e-02 |  402.3614024 | 0.000000e+00 | frontier |
| alt_shannon | log_land |    0.73449120 | 4.982121e-03 |  147.4253930 | 0.000000e+00 | frontier |
| alt_shannon | log_labor |    0.23855860 | 5.457640e-03 |   43.7109447 | 0.000000e+00 | frontier |
| alt_shannon | log_inputs |    0.11170024 | 2.380441e-03 |   46.9241860 | 0.000000e+00 | frontier |
| alt_shannon | region_natural2 |   -0.99585398 | 1.460241e-02 |  -68.1979122 | 0.000000e+00 | frontier |
| alt_shannon | region_natural3 |   -0.15771467 | 1.697409e-02 |   -9.2914941 | 0.000000e+00 | frontier |
| alt_shannon | Z_(Intercept) | -550.80037589 | 8.454616e+01 |   -6.5147885 | 7.279222e-11 | inefficiency |
| alt_shannon | Z_diversif_alt |    5.84565201 | 1.477524e+00 |    3.9563829 | 7.609316e-05 | inefficiency |
| alt_shannon | Z_size_mediano |  -10.55388864 | 2.666040e+00 |   -3.9586393 | 7.537799e-05 | inefficiency |
| alt_shannon | Z_size_grande |  277.12685226 | 4.181613e+01 |    6.6272713 | 3.419487e-11 | inefficiency |
| alt_shannon | Z_diversif_alt_med |   88.94439844 | 1.360415e+01 |    6.5380353 | 6.233214e-11 | inefficiency |
| alt_shannon | Z_diversif_alt_gra |  -29.26086292 | 4.398592e+00 |   -6.6523255 | 2.884981e-11 | inefficiency |
| alt_shannon | sigmaSq |  413.66648492 | 6.320315e+01 |    6.5450296 | 5.948353e-11 | variance |
| alt_shannon | gamma |    0.99867653 | 2.175634e-04 | 4590.2784955 | 0.000000e+00 | variance |
| alt_num_crops | (Intercept) |    8.73447555 | 2.186604e-02 |  399.4539777 | 0.000000e+00 | frontier |
| alt_num_crops | log_land |    0.73118912 | 4.882116e-03 |  149.7688810 | 0.000000e+00 | frontier |
| alt_num_crops | log_labor |    0.24012325 | 5.704234e-03 |   42.0956143 | 0.000000e+00 | frontier |
| alt_num_crops | log_inputs |    0.11176612 | 2.334938e-03 |   47.8668381 | 0.000000e+00 | frontier |
| alt_num_crops | region_natural2 |   -1.00731086 | 1.458153e-02 |  -69.0812656 | 0.000000e+00 | frontier |
| alt_num_crops | region_natural3 |   -0.16330941 | 1.990764e-02 |   -8.2033544 | 2.220446e-16 | frontier |
| alt_num_crops | Z_(Intercept) | -138.28060723 | 1.254125e+01 |  -11.0260664 | 0.000000e+00 | inefficiency |
| alt_num_crops | Z_diversif_alt2 |   -0.01591934 | 1.680842e-02 |   -0.9471049 | 3.435853e-01 | inefficiency |
| alt_num_crops | Z_size_mediano |   10.45352291 | 6.150321e-01 |   16.9967124 | 0.000000e+00 | inefficiency |
| alt_num_crops | Z_size_grande |   45.82898543 | 4.845374e+00 |    9.4582966 | 0.000000e+00 | inefficiency |
| alt_num_crops | Z_diversif_alt2_med |    3.83589023 | 4.295665e-01 |    8.9296766 | 0.000000e+00 | inefficiency |
| alt_num_crops | Z_diversif_alt2_gra |    3.85938611 | 1.293876e-01 |   29.8281083 | 0.000000e+00 | inefficiency |
| alt_num_crops | sigmaSq |  105.55980964 | 9.750960e+00 |   10.8255814 | 0.000000e+00 | variance |
| alt_num_crops | gamma |    0.99479080 | 5.338044e-04 | 1863.5867238 | 0.000000e+00 | variance |
| small_only | (Intercept) |    8.69261598 | 2.827201e-02 |  307.4636286 | 0.000000e+00 | frontier |
| small_only | log_land |    0.74018452 | 6.908090e-03 |  107.1474977 | 0.000000e+00 | frontier |
| small_only | log_labor |    0.21227448 | 7.250609e-03 |   29.2767807 | 0.000000e+00 | frontier |
| small_only | log_inputs |    0.10136816 | 3.125114e-03 |   32.4366269 | 0.000000e+00 | frontier |
| small_only | region_natural2 |   -0.88959983 | 1.733231e-02 |  -51.3260931 | 0.000000e+00 | frontier |
| small_only | region_natural3 |   -0.07516587 | 2.735723e-02 |   -2.7475681 | 6.003903e-03 | frontier |
| small_only | Z_(Intercept) | -125.92897218 | 3.269362e+01 |   -3.8517905 | 1.172573e-04 | inefficiency |
| small_only | Z_diversificacion_area |    6.03125518 | 9.066250e-01 |    6.6524255 | 2.883027e-11 | inefficiency |
| small_only | sigmaSq |   89.50415767 | 2.216741e+01 |    4.0376468 | 5.399006e-05 | variance |
| small_only | gamma |    0.99351725 | 1.625641e-03 |  611.1541455 | 0.000000e+00 | variance |


## Resultados logit (practicas sostenibles)

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main | (Intercept) |  2.46486908 | 0.5276047 |  4.6718100 | 3.084632e-06 | 11.7619422 |
| main | diversificacion_area |  2.73794586 | 0.5720020 |  4.7866017 | 1.758159e-06 | 15.4552053 |
| main | size_catmediano_2_5ha |  0.46187418 | 0.3743250 |  1.2338856 | 2.173187e-01 |  1.5870456 |
| main | size_catpequeno_<2ha |  0.32227160 | 0.4506583 |  0.7151130 | 4.745813e-01 |  1.3802596 |
| main | log_area |  0.02367428 | 0.1649711 |  0.1435056 | 8.858982e-01 |  1.0239567 |
| main | region_natural2 |  1.36863254 | 0.4756456 |  2.8774210 | 4.030836e-03 |  3.9299729 |
| main | region_natural3 | -2.18825347 | 0.3700672 | -5.9131241 | 3.640053e-09 |  0.1121124 |
| main | diversificacion_area:size_catmediano_2_5ha | -0.32400438 | 0.7803323 | -0.4152133 | 6.780082e-01 |  0.7232471 |
| main | diversificacion_area:size_catpequeno_<2ha | -0.88076139 | 0.8227013 | -1.0705725 | 2.844269e-01 |  0.4144672 |


### Robustez logit

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | alt_shannon | (Intercept) |  2.636871817 | 0.53551157 |  4.924023969 | 8.823690e-07 | 13.9694362 |
| alt_shannon | diversif_alt |  1.342079458 | 0.36116539 |  3.715969148 | 2.052187e-04 |  3.8269933 |
| alt_shannon | size_catmediano_2_5ha |  0.305467512 | 0.39186282 |  0.779526644 | 4.357161e-01 |  1.3572594 |
| alt_shannon | size_catpequeno_<2ha |  0.172378209 | 0.46132545 |  0.373658573 | 7.086783e-01 |  1.1881271 |
| alt_shannon | log_area |  0.001594283 | 0.16273653 |  0.009796715 | 9.921840e-01 |  1.0015956 |
| alt_shannon | region_natural2 |  1.322915679 | 0.47621568 |  2.777975896 | 5.495612e-03 |  3.7543519 |
| alt_shannon | region_natural3 | -2.184579525 | 0.37075233 | -5.892288042 | 4.125704e-09 |  0.1125250 |
| alt_shannon | diversif_alt:size_catmediano_2_5ha |  0.037746114 | 0.45826585 |  0.082367285 | 9.343588e-01 |  1.0384675 |
| alt_shannon | diversif_alt:size_catpequeno_<2ha | -0.327011121 | 0.47661361 | -0.686113686 | 4.926816e-01 |  0.7210757 |
| alt_num_crops | (Intercept) |  2.973650469 | 0.54411794 |  5.465084409 | 4.911486e-08 | 19.5632043 |
| alt_num_crops | diversif_alt2 |  0.240812922 | 0.07423817 |  3.243788614 | 1.189299e-03 |  1.2722830 |
| alt_num_crops | size_catmediano_2_5ha |  0.203312273 | 0.42437803 |  0.479082935 | 6.319061e-01 |  1.2254551 |
| alt_num_crops | size_catpequeno_<2ha | -0.254642172 | 0.45230907 | -0.562982678 | 5.734785e-01 |  0.7751938 |
| alt_num_crops | log_area | -0.011945058 | 0.16248640 | -0.073514203 | 9.414007e-01 |  0.9881260 |
| alt_num_crops | region_natural2 |  1.539091120 | 0.46670263 |  3.297798284 | 9.830571e-04 |  4.6603526 |
| alt_num_crops | region_natural3 | -2.233666270 | 0.36963367 | -6.042918802 | 1.652968e-09 |  0.1071349 |
| alt_num_crops | diversif_alt2:size_catmediano_2_5ha |  0.001107500 | 0.11262427 |  0.009833584 | 9.921546e-01 |  1.0011081 |
| alt_num_crops | diversif_alt2:size_catpequeno_<2ha |  0.018960766 | 0.10958780 |  0.173018948 | 8.626454e-01 |  1.0191417 |
| alt_outcome_two_plus | (Intercept) |  1.600686742 | 0.54039783 |  2.962052470 | 3.074112e-03 |  4.9564350 |
| alt_outcome_two_plus | diversificacion_area |  2.693405124 | 0.48547176 |  5.548016091 | 3.078032e-08 | 14.7819246 |
| alt_outcome_two_plus | size_catmediano_2_5ha |  0.552738161 | 0.36368210 |  1.519838765 | 1.286313e-01 |  1.7380054 |
| alt_outcome_two_plus | size_catpequeno_<2ha |  0.270666269 | 0.44551842 |  0.607531045 | 5.435334e-01 |  1.3108375 |
| alt_outcome_two_plus | log_area |  0.006725764 | 0.15484875 |  0.043434412 | 9.653574e-01 |  1.0067484 |
| alt_outcome_two_plus | region_natural2 |  1.563494330 | 0.42039206 |  3.719133817 | 2.026736e-04 |  4.7754792 |
| alt_outcome_two_plus | region_natural3 | -2.026641996 | 0.27338591 | -7.413117995 | 1.500154e-13 |  0.1317773 |
| alt_outcome_two_plus | diversificacion_area:size_catmediano_2_5ha | -0.650007110 | 0.60378876 | -1.076547218 | 2.817481e-01 |  0.5220421 |
| alt_outcome_two_plus | diversificacion_area:size_catpequeno_<2ha | -0.872244531 | 0.63129680 | -1.381671070 | 1.671506e-01 |  0.4180123 |
| small_only | (Intercept) |  2.311131663 | 0.50310873 |  4.593702152 | 4.547673e-06 | 10.0858320 |
| small_only | diversificacion_area |  1.601767721 | 0.62424517 |  2.565927310 | 1.034182e-02 |  4.9617957 |
| small_only | log_area |  0.808244887 | 0.51450896 |  1.570905375 | 1.163180e-01 |  2.2439661 |
| small_only | region_natural2 |  1.983788693 | 0.57787714 |  3.432890074 | 6.058852e-04 |  7.2702356 |
| small_only | region_natural3 | -2.212016148 | 0.47755771 | -4.631934771 | 3.788633e-06 |  0.1094797 |


## Definiciones de variables

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

## Limitaciones

- SFA no usa pesos por limitaciones del paquete.

- Algunas variables presentan faltantes; ver docs/DATA_GAPS.md.
