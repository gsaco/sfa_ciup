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


## Mejoras con datos externos (UBIGEO + CHIRPS)

Se incorporaron coordenadas y area distrital, y precipitacion CHIRPS como control exogeno. Las tablas siguientes comparan resultados base vs controles geo/clima.

### Tabla 06. Cobertura geo/clima

| group_type   | group   |     n |   share_geo_match |   share_chirps_match |   mean_prcp_total_z |   sd_prcp_total_z |
|:-------------|:--------|------:|------------------:|---------------------:|--------------------:|------------------:|
| overall      | overall | 35187 |          0.968397 |             0.968397 |           -0.448926 |          0.8133   |
| region       | 1       |  8263 |          0.906329 |             0.906329 |           -0.458567 |          0.528105 |
| region       | 2       | 20601 |          0.990437 |             0.990437 |           -0.290769 |          0.774407 |
| region       | 3       |  6323 |          0.9777   |             0.9777   |           -0.959249 |          0.992875 |

### Tabla 07. SFA con controles geo/clima

| model | term | estimate | std_error | z_value | p_value | component | 
| --- | --- | --- | --- | --- | --- | --- | 
 | xgeo_prcp | (Intercept) |    8.66619978 | 4.129273e-02 |  209.8722763 | 0.000000e+00 | frontier |
| xgeo_prcp | log_land |    0.73118445 | 5.056946e-03 |  144.5901177 | 0.000000e+00 | frontier |
| xgeo_prcp | log_labor |    0.23945529 | 5.907768e-03 |   40.5322797 | 0.000000e+00 | frontier |
| xgeo_prcp | log_inputs |    0.11104136 | 2.484275e-03 |   44.6976936 | 0.000000e+00 | frontier |
| xgeo_prcp | region_natural2 |   -1.00494983 | 1.402775e-02 |  -71.6401334 | 0.000000e+00 | frontier |
| xgeo_prcp | region_natural3 |   -0.16403178 | 2.064174e-02 |   -7.9466070 | 1.998401e-15 | frontier |
| xgeo_prcp | log_surface_km2 |    0.01446090 | 5.408218e-03 |    2.6738755 | 7.498029e-03 | frontier |
| xgeo_prcp | prcp_total_z |    0.01455123 | 7.216358e-03 |    2.0164229 | 4.375577e-02 | frontier |
| xgeo_prcp | Z_(Intercept) | -315.05932210 | 3.034157e+01 |  -10.3837499 | 0.000000e+00 | inefficiency |
| xgeo_prcp | Z_diversificacion_area |  -10.32626883 | 1.232804e+00 |   -8.3762431 | 0.000000e+00 | inefficiency |
| xgeo_prcp | Z_size_mediano |  -31.08852658 | 1.275193e+00 |  -24.3794709 | 0.000000e+00 | inefficiency |
| xgeo_prcp | Z_size_grande |  174.24048611 | 1.824269e+01 |    9.5512472 | 0.000000e+00 | inefficiency |
| xgeo_prcp | Z_diversif_mediano |  155.63581183 | 1.051659e+01 |   14.7990738 | 0.000000e+00 | inefficiency |
| xgeo_prcp | Z_diversif_grande |  -58.85856996 | 9.973392e+00 |   -5.9015598 | 3.600808e-09 | inefficiency |
| xgeo_prcp | sigmaSq |  245.55241096 | 2.283592e+01 |   10.7529025 | 0.000000e+00 | variance |
| xgeo_prcp | gamma |    0.99778149 | 2.224445e-04 | 4485.5294404 | 0.000000e+00 | variance |
| zgeo_prcp | (Intercept) |    8.66519932 | 4.024360e-02 |  215.3186689 | 0.000000e+00 | frontier |
| zgeo_prcp | log_land |    0.73320076 | 5.255855e-03 |  139.5016994 | 0.000000e+00 | frontier |
| zgeo_prcp | log_labor |    0.23481199 | 5.898053e-03 |   39.8117811 | 0.000000e+00 | frontier |
| zgeo_prcp | log_inputs |    0.11132296 | 2.509702e-03 |   44.3570427 | 0.000000e+00 | frontier |
| zgeo_prcp | region_natural2 |   -1.00035964 | 1.545413e-02 |  -64.7308748 | 0.000000e+00 | frontier |
| zgeo_prcp | region_natural3 |   -0.14528044 | 2.076859e-02 |   -6.9952006 | 2.648770e-12 | frontier |
| zgeo_prcp | log_surface_km2 |    0.01292904 | 5.307003e-03 |    2.4362229 | 1.484154e-02 | frontier |
| zgeo_prcp | Z_(Intercept) | -142.91725346 | 1.987679e+01 |   -7.1901594 | 6.472600e-13 | inefficiency |
| zgeo_prcp | Z_diversificacion_area |   -0.17454426 | 4.207120e-01 |   -0.4148783 | 6.782310e-01 | inefficiency |
| zgeo_prcp | Z_size_mediano |  -15.09597425 | 3.799652e+00 |   -3.9729888 | 7.097639e-05 | inefficiency |
| zgeo_prcp | Z_size_grande |   69.51060255 | 9.900570e+00 |    7.0208686 | 2.204903e-12 | inefficiency |
| zgeo_prcp | Z_diversif_mediano |   69.03718986 | 1.228076e+01 |    5.6215729 | 1.892266e-08 | inefficiency |
| zgeo_prcp | Z_diversif_grande |  -23.37312740 | 3.707608e+00 |   -6.3040982 | 2.898768e-10 | inefficiency |
| zgeo_prcp | Z_prcp_total_z |  -11.83888695 | 1.657252e+00 |   -7.1436840 | 9.086065e-13 | inefficiency |
| zgeo_prcp | sigmaSq |  106.26869466 | 1.494298e+01 |    7.1116135 | 1.146860e-12 | variance |
| zgeo_prcp | gamma |    0.99486304 | 7.861645e-04 | 1265.4642825 | 0.000000e+00 | variance |


### Tabla 08. Comparacion efectos SFA

| model | term | estimate | std_error | p_value | 
| --- | --- | --- | --- | --- | 
 | main_area | Z_diversificacion_area | -14.9304685 |  1.820617 | 2.220446e-16 |
| main_area | Z_diversif_mediano | 174.7929733 | 23.979256 | 3.115286e-13 |
| main_area | Z_diversif_grande | -69.9012745 | 10.234233 | 8.482992e-12 |
| xgeo_prcp | Z_diversificacion_area | -10.3262688 |  1.232804 | 0.000000e+00 |
| xgeo_prcp | Z_diversif_mediano | 155.6358118 | 10.516591 | 0.000000e+00 |
| xgeo_prcp | Z_diversif_grande | -58.8585700 |  9.973392 | 3.600808e-09 |
| zgeo_prcp | Z_diversificacion_area |  -0.1745443 |  0.420712 | 6.782310e-01 |
| zgeo_prcp | Z_diversif_mediano |  69.0371899 | 12.280760 | 1.892266e-08 |
| zgeo_prcp | Z_diversif_grande | -23.3731274 |  3.707608 | 2.898768e-10 |


### Tabla 09. Logit con controles geo/clima

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main_geo | (Intercept) |  2.7251941 | 0.5556447 |  4.9045625 | 9.739317e-07 | 15.2593751 |
| main_geo | diversificacion_area |  2.7232890 | 0.6104945 |  4.4607918 | 8.392251e-06 | 15.2303331 |
| main_geo | size_catmediano_2_5ha |  0.4624174 | 0.4009134 |  1.1534098 | 2.488118e-01 |  1.5879080 |
| main_geo | size_catpequeno_<2ha |  0.3330951 | 0.4617783 |  0.7213314 | 4.707482e-01 |  1.3952801 |
| main_geo | log_area |  0.1109765 | 0.1633812 |  0.6792487 | 4.970200e-01 |  1.1173686 |
| main_geo | region_natural2 |  1.4024037 | 0.4710133 |  2.9774186 | 2.924471e-03 |  4.0649591 |
| main_geo | region_natural3 | -1.8989866 | 0.3854254 | -4.9269884 | 8.691812e-07 |  0.1497203 |
| main_geo | prcp_total_z |  0.6373037 | 0.1302650 |  4.8923645 | 1.035909e-06 |  1.8913742 |
| main_geo | diversificacion_area:size_catmediano_2_5ha | -0.4173759 | 0.8206206 | -0.5086101 | 6.110539e-01 |  0.6587732 |
| main_geo | diversificacion_area:size_catpequeno_<2ha | -0.9244165 | 0.8339937 | -1.1084214 | 2.677471e-01 |  0.3967629 |


### Tabla 10. Comparacion efectos logit

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main | diversificacion_area |  2.7379459 | 0.5720020 |  4.7866017 | 1.758159e-06 | 15.4552053 |
| main | diversificacion_area:size_catmediano_2_5ha | -0.3240044 | 0.7803323 | -0.4152133 | 6.780082e-01 |  0.7232471 |
| main | diversificacion_area:size_catpequeno_<2ha | -0.8807614 | 0.8227013 | -1.0705725 | 2.844269e-01 |  0.4144672 |
| main_geo | diversificacion_area |  2.7232890 | 0.6104945 |  4.4607918 | 8.392251e-06 | 15.2303331 |
| main_geo | diversificacion_area:size_catmediano_2_5ha | -0.4173759 | 0.8206206 | -0.5086101 | 6.110539e-01 |  0.6587732 |
| main_geo | diversificacion_area:size_catpequeno_<2ha | -0.9244165 | 0.8339937 | -1.1084214 | 2.677471e-01 |  0.3967629 |


## Controles ENA adicionales

Se incorporan controles de capital, riego, semillas, asistencia tecnica, credito y educacion. Las tablas siguientes muestran cobertura y efectos econometricos.

### Tabla 11. Cobertura controles ENA

| group_type   | group         | variable                    |   missing_pct |           mean |         p50 |           p90 |
|:-------------|:--------------|:----------------------------|--------------:|---------------:|------------:|--------------:|
| overall      | overall       | riego_any                   |   0           |      0.596811  |    1        |      1        |
| overall      | overall       | riego_share                 |   0           |      0.506854  |    0.5      |      1        |
| overall      | overall       | riego_tecnificado_any       |   0           |      0.186887  |    0        |      1        |
| overall      | overall       | riego_tecnificado_share     |   0           |      0.120354  |    0        |      0.6      |
| overall      | overall       | usuario_agua                |   0           |      0.42763   |    0        |      1        |
| overall      | overall       | gasto_agua_riego            |   0           |   9862.88      |    0        |    700        |
| overall      | overall       | uso_maquinaria              |   8.52588e-05 |      0.715894  |    1        |      1        |
| overall      | overall       | num_maquinaria_equipo       |   8.52588e-05 |      2.54121   |    1        |      6        |
| overall      | overall       | gasto_compra_equipos        |   8.52588e-05 |   1194.53      |    0        |      0        |
| overall      | overall       | gasto_compra_maquinaria     |   8.52588e-05 |   2910.9       |    0        |      0        |
| overall      | overall       | gasto_alquiler_mant_equipos |   8.52588e-05 |   4172.13      |    0        |    240        |
| overall      | overall       | gasto_semilla               |   5.68392e-05 |   3500.58      |  175        |   2430        |
| overall      | overall       | usa_abono                   |   5.68392e-05 |      0.607333  |    1        |      1        |
| overall      | overall       | usa_fertilizantes           |   5.68392e-05 |      0.587012  |    1        |      1        |
| overall      | overall       | semilla_semillero_any       |   5.68392e-05 |      0.12241   |    0        |      1        |
| overall      | overall       | semilla_comercial_any       |   5.68392e-05 |      0.273327  |    0        |      1        |
| overall      | overall       | semilla_certificada_any     |   5.68392e-05 |      0.102885  |    0        |      1        |
| overall      | overall       | semilla_certificada_share   |   5.68392e-05 |      0.0838824 |    0        |      0.2      |
| overall      | overall       | capacitacion_recibida       |   8.52588e-05 |      0.0976296 |    0        |      0        |
| overall      | overall       | asistencia_tecnica_recibida |   8.52588e-05 |      0.0573272 |    0        |      0        |
| overall      | overall       | credito_obtenido            |   8.52588e-05 |      0.124943  |    0        |      1        |
| overall      | overall       | nivel_educacion             |   0.031631    |      4.5444    |    4        |      8        |
| overall      | overall       | asociacion_miembro          |   8.52588e-05 |      0.0795248 |    0        |      0        |
| overall      | overall       | asociacion_num              |   8.52588e-05 |      0.0836744 |    0        |      0        |
| region       | 1             | riego_any                   |   0           |      0.95849   |    1        |      1        |
| region       | 1             | riego_share                 |   0           |      0.949674  |    1        |      1        |
| region       | 1             | riego_tecnificado_any       |   0           |      0.229336  |    0        |      1        |
| region       | 1             | riego_tecnificado_share     |   0           |      0.19264   |    0        |      1        |
| region       | 1             | usuario_agua                |   0           |      0.665981  |    1        |      1        |
| region       | 1             | gasto_agua_riego            |   0           |  41716.2       |  400        |   6000        |
| region       | 1             | uso_maquinaria              |   0.000121021 |      0.837812  |    1        |      1        |
| region       | 1             | num_maquinaria_equipo       |   0.000121021 |      4.29472   |    3        |     10        |
| region       | 1             | gasto_compra_equipos        |   0.000121021 |   4631.17      |    0        |      0        |
| region       | 1             | gasto_compra_maquinaria     |   0.000121021 |  11515         |    0        |      0        |
| region       | 1             | gasto_alquiler_mant_equipos |   0.000121021 |  16568.9       |    0        |   1000        |
| region       | 1             | gasto_semilla               |   0.000121021 |  12007.6       |   50        |   9200        |
| region       | 1             | usa_abono                   |   0.000121021 |      0.447954  |    0        |      1        |
| region       | 1             | usa_fertilizantes           |   0.000121021 |      0.853788  |    1        |      1        |
| region       | 1             | semilla_semillero_any       |   0.000121021 |      0.171871  |    0        |      1        |
| region       | 1             | semilla_comercial_any       |   0.000121021 |      0.302832  |    0        |      1        |
| region       | 1             | semilla_certificada_any     |   0.000121021 |      0.291697  |    0        |      1        |
| region       | 1             | semilla_certificada_share   |   0.000121021 |      0.247379  |    0        |      1        |
| region       | 1             | capacitacion_recibida       |   0.000121021 |      0.122004  |    0        |      1        |
| region       | 1             | asistencia_tecnica_recibida |   0.000121021 |      0.110022  |    0        |      1        |
| region       | 1             | credito_obtenido            |   0.000121021 |      0.228395  |    0        |      1        |
| region       | 1             | nivel_educacion             |   0.0936706   |      5.41755   |    6        |      9        |
| region       | 1             | asociacion_miembro          |   0.000121021 |      0.0876301 |    0        |      0        |
| region       | 1             | asociacion_num              |   0.000121021 |      0.0984023 |    0        |      0        |
| region       | 2             | riego_any                   |   0           |      0.593515  |    1        |      1        |
| region       | 2             | riego_share                 |   0           |      0.4517    |    0.333333 |      1        |
| region       | 2             | riego_tecnificado_any       |   0           |      0.219989  |    0        |      1        |
| region       | 2             | riego_tecnificado_share     |   0           |      0.12419   |    0        |      0.571429 |
| region       | 2             | usuario_agua                |   0           |      0.442163  |    0        |      1        |
| region       | 2             | gasto_agua_riego            |   0           |     50.9527    |    0        |    100        |
| region       | 2             | uso_maquinaria              |   4.85413e-05 |      0.660922  |    1        |      1        |
| region       | 2             | num_maquinaria_equipo       |   4.85413e-05 |      1.77748   |    1        |      3        |
| region       | 2             | gasto_compra_equipos        |   4.85413e-05 |     47.8061    |    0        |      0        |
| region       | 2             | gasto_compra_maquinaria     |   4.85413e-05 |     50.3641    |    0        |      0        |
| region       | 2             | gasto_alquiler_mant_equipos |   4.85413e-05 |     53.1662    |    0        |     60        |
| region       | 2             | gasto_semilla               |   4.85413e-05 |    816.552     |  290        |   1705        |
| region       | 2             | usa_abono                   |   4.85413e-05 |      0.782816  |    1        |      1        |
| region       | 2             | usa_fertilizantes           |   4.85413e-05 |      0.522282  |    1        |      1        |
| region       | 2             | semilla_semillero_any       |   4.85413e-05 |      0.100777  |    0        |      1        |
| region       | 2             | semilla_comercial_any       |   4.85413e-05 |      0.301117  |    0        |      1        |
| region       | 2             | semilla_certificada_any     |   4.85413e-05 |      0.0260194 |    0        |      0        |
| region       | 2             | semilla_certificada_share   |   4.85413e-05 |      0.0143977 |    0        |      0        |
| region       | 2             | capacitacion_recibida       |   4.85413e-05 |      0.0721845 |    0        |      0        |
| region       | 2             | asistencia_tecnica_recibida |   4.85413e-05 |      0.026699  |    0        |      0        |
| region       | 2             | credito_obtenido            |   4.85413e-05 |      0.0786408 |    0        |      0        |
| region       | 2             | nivel_educacion             |   0.00961118  |      4.22624   |    4        |      6        |
| region       | 2             | asociacion_miembro          |   4.85413e-05 |      0.0636893 |    0        |      0        |
| region       | 2             | asociacion_num              |   4.85413e-05 |      0.0658738 |    0        |      0        |
| region       | 3             | riego_any                   |   0           |      0.134904  |    0        |      1        |
| region       | 3             | riego_share                 |   0           |      0.107868  |    0        |      0.612308 |
| region       | 3             | riego_tecnificado_any       |   0           |      0.0235648 |    0        |      0        |
| region       | 3             | riego_tecnificado_share     |   0           |      0.0133947 |    0        |      0        |
| region       | 3             | usuario_agua                |   0           |      0.0687965 |    0        |      0        |
| region       | 3             | gasto_agua_riego            |   0           |    204.663     |    0        |      0        |
| region       | 3             | uso_maquinaria              |   0.000158153 |      0.735685  |    1        |      1        |
| region       | 3             | num_maquinaria_equipo       |   0.000158153 |      2.73822   |    1        |      6        |
| region       | 3             | gasto_compra_equipos        |   0.000158153 |    439.842     |    0        |    750        |
| region       | 3             | gasto_compra_maquinaria     |   0.000158153 |    987.403     |    0        |      0        |
| region       | 3             | gasto_alquiler_mant_equipos |   0.000158153 |   1392.75      |    0        |    350        |
| region       | 3             | gasto_semilla               |   0           |   1129.31      |    0        |   1274        |
| region       | 3             | usa_abono                   |   0           |      0.243872  |    0        |      1        |
| region       | 3             | usa_fertilizantes           |   0           |      0.449312  |    0        |      1        |
| region       | 3             | semilla_semillero_any       |   0           |      0.128262  |    0        |      1        |
| region       | 3             | semilla_comercial_any       |   0           |      0.144235  |    0        |      1        |
| region       | 3             | semilla_certificada_any     |   0           |      0.106595  |    0        |      1        |
| region       | 3             | semilla_certificada_share   |   0           |      0.0966259 |    0        |      0.5      |
| region       | 3             | capacitacion_recibida       |   0.000158153 |      0.148687  |    0        |      1        |
| region       | 3             | asistencia_tecnica_recibida |   0.000158153 |      0.0882632 |    0        |      0        |
| region       | 3             | credito_obtenido            |   0.000158153 |      0.14062   |    0        |      1        |
| region       | 3             | nivel_educacion             |   0.0222995   |      4.53672   |    4        |      7        |
| region       | 3             | asociacion_miembro          |   0.000158153 |      0.120531  |    0        |      1        |
| region       | 3             | asociacion_num              |   0.000158153 |      0.12243   |    0        |      1        |
| size         | grande_>5ha   | riego_any                   |   0           |      0.467123  |    0        |      1        |
| size         | grande_>5ha   | riego_share                 |   0           |      0.416134  |    0        |      1        |
| size         | grande_>5ha   | riego_tecnificado_any       |   0           |      0.120719  |    0        |      1        |
| size         | grande_>5ha   | riego_tecnificado_share     |   0           |      0.0765176 |    0        |      0.2      |
| size         | grande_>5ha   | usuario_agua                |   0           |      0.376541  |    0        |      1        |
| size         | grande_>5ha   | gasto_agua_riego            |   0           |   1348.39      |    0        |   2971        |
| size         | grande_>5ha   | uso_maquinaria              |   0           |      0.839384  |    1        |      1        |
| size         | grande_>5ha   | num_maquinaria_equipo       |   0           |      3.92414   |    3        |     10        |
| size         | grande_>5ha   | gasto_compra_equipos        |   0           |    291.88      |    0        |    800        |
| size         | grande_>5ha   | gasto_compra_maquinaria     |   0           |    415.087     |    0        |      0        |
| size         | grande_>5ha   | gasto_alquiler_mant_equipos |   0           |    555.397     |    0        |    720        |
| size         | grande_>5ha   | gasto_semilla               |   0           |   5150.1       |  370        |  12454        |
| size         | grande_>5ha   | usa_abono                   |   0           |      0.400856  |    0        |      1        |
| size         | grande_>5ha   | usa_fertilizantes           |   0           |      0.635445  |    1        |      1        |
| size         | grande_>5ha   | semilla_semillero_any       |   0           |      0.200171  |    0        |      1        |
| size         | grande_>5ha   | semilla_comercial_any       |   0           |      0.355137  |    0        |      1        |
| size         | grande_>5ha   | semilla_certificada_any     |   0           |      0.270719  |    0        |      1        |
| size         | grande_>5ha   | semilla_certificada_share   |   0           |      0.224082  |    0        |      1        |
| size         | grande_>5ha   | capacitacion_recibida       |   0           |      0.132021  |    0        |      1        |
| size         | grande_>5ha   | asistencia_tecnica_recibida |   0           |      0.0936644 |    0        |      0        |
| size         | grande_>5ha   | credito_obtenido            |   0           |      0.254623  |    0        |      1        |
| size         | grande_>5ha   | nivel_educacion             |   0           |      5.10788   |    5        |      9        |
| size         | grande_>5ha   | asociacion_miembro          |   0           |      0.12226   |    0        |      1        |
| size         | grande_>5ha   | asociacion_num              |   0           |      0.125685  |    0        |      1        |
| size         | mediano_2_5ha | riego_any                   |   0           |      0.584263  |    1        |      1        |
| size         | mediano_2_5ha | riego_share                 |   0           |      0.496715  |    0.5      |      1        |
| size         | mediano_2_5ha | riego_tecnificado_any       |   0           |      0.180471  |    0        |      1        |
| size         | mediano_2_5ha | riego_tecnificado_share     |   0           |      0.110612  |    0        |      0.5      |
| size         | mediano_2_5ha | usuario_agua                |   0           |      0.447754  |    0        |      1        |
| size         | mediano_2_5ha | gasto_agua_riego            |   0           |    393.752     |    0        |    931.6      |
| size         | mediano_2_5ha | uso_maquinaria              |   0           |      0.800733  |    1        |      1        |
| size         | mediano_2_5ha | num_maquinaria_equipo       |   0           |      2.68159   |    1        |      6        |
| size         | mediano_2_5ha | gasto_compra_equipos        |   0           |    122.543     |    0        |      0        |
| size         | mediano_2_5ha | gasto_compra_maquinaria     |   0           |     73.7416    |    0        |      0        |
| size         | mediano_2_5ha | gasto_alquiler_mant_equipos |   0           |    117.817     |    0        |    300        |
| size         | mediano_2_5ha | gasto_semilla               |   0           |   1445.32      |  460        |   3480        |
| size         | mediano_2_5ha | usa_abono                   |   0           |      0.58028   |    1        |      1        |
| size         | mediano_2_5ha | usa_fertilizantes           |   0           |      0.662631  |    1        |      1        |
| size         | mediano_2_5ha | semilla_semillero_any       |   0           |      0.152596  |    0        |      1        |
| size         | mediano_2_5ha | semilla_comercial_any       |   0           |      0.295954  |    0        |      1        |
| size         | mediano_2_5ha | semilla_certificada_any     |   0           |      0.139853  |    0        |      1        |
| size         | mediano_2_5ha | semilla_certificada_share   |   0           |      0.112422  |    0        |      0.666667 |
| size         | mediano_2_5ha | capacitacion_recibida       |   0           |      0.11596   |    0        |      1        |
| size         | mediano_2_5ha | asistencia_tecnica_recibida |   0           |      0.0672189 |    0        |      0        |
| size         | mediano_2_5ha | credito_obtenido            |   0           |      0.176171  |    0        |      1        |
| size         | mediano_2_5ha | nivel_educacion             |   0           |      4.73622   |    4        |      8        |
| size         | mediano_2_5ha | asociacion_miembro          |   0           |      0.104173  |    0        |      1        |
| size         | mediano_2_5ha | asociacion_num              |   0           |      0.105925  |    0        |      1        |
| size         | missing       | riego_any                   |   0           |      0.868705  |    1        |      1        |
| size         | missing       | riego_share                 |   0           |      0.838309  |    1        |      1        |
| size         | missing       | riego_tecnificado_any       |   0           |      0.542266  |    1        |      1        |
| size         | missing       | riego_tecnificado_share     |   0           |      0.489406  |    0.5      |      1        |
| size         | missing       | usuario_agua                |   0           |      0         |    0        |      0        |
| size         | missing       | gasto_agua_riego            |   0           | 299934         | 2730        | 179694        |
| size         | missing       | uso_maquinaria              |   0.00179856  |      0.93964   |    1        |      1        |
| size         | missing       | num_maquinaria_equipo       |   0.00179856  |     15.7694    |    6        |     36        |
| size         | missing       | gasto_compra_equipos        |   0.00179856  |  34974         |    0        |  10000        |
| size         | missing       | gasto_compra_maquinaria     |   0.00179856  |  89300.3       |    0        |      0        |
| size         | missing       | gasto_alquiler_mant_equipos |   0.00179856  | 128053         | 1000        | 120214        |
| size         | missing       | gasto_semilla               |   0.000899281 |  67966.5       |    0        |  19482        |
| size         | missing       | usa_abono                   |   0.000899281 |      0.517552  |    1        |      1        |
| size         | missing       | usa_fertilizantes           |   0.000899281 |      0.825383  |    1        |      1        |
| size         | missing       | semilla_semillero_any       |   0.000899281 |      0.184518  |    0        |      1        |
| size         | missing       | semilla_comercial_any       |   0.000899281 |      0.244824  |    0        |      1        |
| size         | missing       | semilla_certificada_any     |   0.000899281 |      0.171017  |    0        |      1        |
| size         | missing       | semilla_certificada_share   |   0.000899281 |      0.149304  |    0        |      1        |
| size         | missing       | capacitacion_recibida       |   0.00179856  |      0.478378  |    0        |      1        |
| size         | missing       | asistencia_tecnica_recibida |   0.00179856  |      0.357658  |    0        |      1        |
| size         | missing       | credito_obtenido            |   0.00179856  |      0.296396  |    0        |      1        |
| size         | missing       | nivel_educacion             |   1           |    nan         |  nan        |    nan        |
| size         | missing       | asociacion_miembro          |   0.00179856  |      0.258559  |    0        |      1        |
| size         | missing       | asociacion_num              |   0.00179856  |      0.333333  |    0        |      1        |
| size         | pequeno_<2ha  | riego_any                   |   0           |      0.621123  |    1        |      1        |
| size         | pequeno_<2ha  | riego_share                 |   0           |      0.517096  |    0.5      |      1        |
| size         | pequeno_<2ha  | riego_tecnificado_any       |   0           |      0.188323  |    0        |      1        |
| size         | pequeno_<2ha  | riego_tecnificado_share     |   0           |      0.116109  |    0        |      0.5      |
| size         | pequeno_<2ha  | usuario_agua                |   0           |      0.457121  |    0        |      1        |
| size         | pequeno_<2ha  | gasto_agua_riego            |   0           |    144.478     |    0        |    190.8      |
| size         | pequeno_<2ha  | uso_maquinaria              |   4.55436e-05 |      0.647477  |    1        |      1        |
| size         | pequeno_<2ha  | num_maquinaria_equipo       |   4.55436e-05 |      1.46447   |    1        |      3        |
| size         | pequeno_<2ha  | gasto_compra_equipos        |   4.55436e-05 |     33.3931    |    0        |      0        |
| size         | pequeno_<2ha  | gasto_compra_maquinaria     |   4.55436e-05 |     18.528     |    0        |      0        |
| size         | pequeno_<2ha  | gasto_alquiler_mant_equipos |   4.55436e-05 |     30.5194    |    0        |     80        |
| size         | pequeno_<2ha  | gasto_semilla               |   4.55436e-05 |    387.453     |  150        |    960        |
| size         | pequeno_<2ha  | usa_abono                   |   4.55436e-05 |      0.674531  |    1        |      1        |
| size         | pequeno_<2ha  | usa_fertilizantes           |   4.55436e-05 |      0.540445  |    1        |      1        |
| size         | pequeno_<2ha  | semilla_semillero_any       |   4.55436e-05 |      0.0899526 |    0        |      0        |
| size         | pequeno_<2ha  | semilla_comercial_any       |   4.55436e-05 |      0.246539  |    0        |      1        |
| size         | pequeno_<2ha  | semilla_certificada_any     |   4.55436e-05 |      0.0442248 |    0        |      0        |
| size         | pequeno_<2ha  | semilla_certificada_share   |   4.55436e-05 |      0.0351202 |    0        |      0        |
| size         | pequeno_<2ha  | capacitacion_recibida       |   4.55436e-05 |      0.0639916 |    0        |      0        |
| size         | pequeno_<2ha  | asistencia_tecnica_recibida |   4.55436e-05 |      0.0296502 |    0        |      0        |
| size         | pequeno_<2ha  | credito_obtenido            |   4.55436e-05 |      0.0671343 |    0        |      0        |
| size         | pequeno_<2ha  | nivel_educacion             |   4.55436e-05 |      4.33968   |    4        |      6        |
| size         | pequeno_<2ha  | asociacion_miembro          |   4.55436e-05 |      0.0520587 |    0        |      0        |
| size         | pequeno_<2ha  | asociacion_num              |   4.55436e-05 |      0.0535161 |    0        |      0        |

### Tabla 13. SFA con controles ENA

| model | term | estimate | std_error | z_value | p_value | component | 
| --- | --- | --- | --- | --- | --- | --- | 
 | controls_ena | (Intercept) |    8.67787649 | 2.385583e-02 |  363.7633895 | 0.000000e+00 | frontier |
| controls_ena | log_land |    0.76004592 | 5.388211e-03 |  141.0571881 | 0.000000e+00 | frontier |
| controls_ena | log_labor |    0.22796869 | 5.822969e-03 |   39.1499035 | 0.000000e+00 | frontier |
| controls_ena | log_inputs |    0.10568179 | 2.428492e-03 |   43.5174567 | 0.000000e+00 | frontier |
| controls_ena | region_natural2 |   -0.71516353 | 1.693544e-02 |  -42.2288099 | 0.000000e+00 | frontier |
| controls_ena | region_natural3 |    0.00297901 | 2.302372e-02 |    0.1293887 | 8.970501e-01 | frontier |
| controls_ena | log_seed |   -0.04697006 | 2.180708e-03 |  -21.5389009 | 0.000000e+00 | frontier |
| controls_ena | log_irrigation_cost |    0.04847155 | 2.578596e-03 |   18.7976531 | 0.000000e+00 | frontier |
| controls_ena | log_capital |    0.01315481 | 2.293398e-03 |    5.7359468 | 9.696910e-09 | frontier |
| controls_ena | riego_tecnificado_any |    0.04705091 | 1.466374e-02 |    3.2086578 | 1.333561e-03 | frontier |
| controls_ena | Z_(Intercept) | -381.05273943 | 4.791440e+01 |   -7.9527808 | 1.776357e-15 | inefficiency |
| controls_ena | Z_diversificacion_area |  -14.86033452 | 1.394045e+00 |  -10.6598679 | 0.000000e+00 | inefficiency |
| controls_ena | Z_size_mediano |  -18.45895312 | 3.321192e+00 |   -5.5579309 | 2.729914e-08 | inefficiency |
| controls_ena | Z_size_grande |  223.78953244 | 2.639327e+01 |    8.4790385 | 0.000000e+00 | inefficiency |
| controls_ena | Z_diversif_mediano |  166.96489033 | 2.221321e+01 |    7.5164672 | 5.617729e-14 | inefficiency |
| controls_ena | Z_diversif_grande |  -61.31011781 | 6.053377e+00 |  -10.1282503 | 0.000000e+00 | inefficiency |
| controls_ena | Z_nivel_educacion |   -2.11934863 | 1.547520e-01 |  -13.6951328 | 0.000000e+00 | inefficiency |
| controls_ena | Z_credito_obtenido |  -49.41225411 | 6.234458e+00 |   -7.9256691 | 2.220446e-15 | inefficiency |
| controls_ena | Z_capacitacion_recibida |   -3.89003760 | 1.160145e-01 |  -33.5306090 | 0.000000e+00 | inefficiency |
| controls_ena | Z_asistencia_tecnica_recibida |  -89.34677154 | 1.150913e+01 |   -7.7631212 | 8.215650e-15 | inefficiency |
| controls_ena | Z_usuario_agua |  -60.45972575 | 7.353610e+00 |   -8.2217752 | 2.220446e-16 | inefficiency |
| controls_ena | Z_asociacion_miembro |   27.76742921 | 3.898151e+00 |    7.1232313 | 1.054268e-12 | inefficiency |
| controls_ena | sigmaSq |  333.57743515 | 4.148932e+01 |    8.0400801 | 8.881784e-16 | variance |
| controls_ena | gamma |    0.99854166 | 1.972739e-04 | 5061.7021429 | 0.000000e+00 | variance |


### Tabla 16. Logit con controles ENA

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | controls_ena | (Intercept) |  0.84007045 | 0.58608058 |  1.4333702 | 1.518311e-01 |   2.3165302 |
| controls_ena | diversificacion_area |  2.64523170 | 0.57712539 |  4.5834610 | 4.714530e-06 |  14.0867085 |
| controls_ena | size_catmediano_2_5ha |  0.39033685 | 0.38608524 |  1.0110121 | 3.120725e-01 |   1.4774784 |
| controls_ena | size_catpequeno_<2ha |  0.33458704 | 0.46760654 |  0.7155311 | 4.743231e-01 |   1.3973632 |
| controls_ena | log_area | -0.07476799 | 0.16836720 | -0.4440769 | 6.570113e-01 |   0.9279588 |
| controls_ena | region_natural2 |  2.10733053 | 0.46607065 |  4.5214831 | 6.320508e-06 |   8.2262522 |
| controls_ena | region_natural3 | -1.15579489 | 0.38834314 | -2.9762207 | 2.935916e-03 |   0.3148072 |
| controls_ena | nivel_educacion |  0.10278247 | 0.03401848 |  3.0213717 | 2.532419e-03 |   1.1082503 |
| controls_ena | credito_obtenido |  0.79622859 | 0.29301704 |  2.7173457 | 6.609434e-03 |   2.2171633 |
| controls_ena | capacitacion_recibida |  1.43651941 | 0.33092237 |  4.3409559 | 1.454112e-05 |   4.2060308 |
| controls_ena | asistencia_tecnica_recibida | -0.11298698 | 0.47744698 | -0.2366482 | 8.129420e-01 |   0.8931623 |
| controls_ena | usuario_agua |  5.06563777 | 0.71068902 |  7.1277839 | 1.206591e-12 | 158.4814838 |
| controls_ena | asociacion_miembro |  0.62724300 | 0.32241755 |  1.9454369 | 5.179314e-02 |   1.8724411 |
| controls_ena | diversificacion_area:size_catmediano_2_5ha | -0.22480601 | 0.76258763 | -0.2947937 | 7.681670e-01 |   0.7986711 |
| controls_ena | diversificacion_area:size_catpequeno_<2ha | -0.80616414 | 0.81003923 | -0.9952162 | 3.196920e-01 |   0.4465678 |


## Temperatura 2023-2024 y topografia

Se agregan controles exogenos de temperatura (2023-2024) y topografia a nivel distrital.

### Tabla 12. Cobertura temperatura/topografia

| group_type   | group   |     n |   share_temp_match |   mean_tmean_2024 |   mean_tmean_2023 |   mean_delta_tmean |   share_topo_match |   mean_elev_m |   mean_slope_deg |   mean_ruggedness |
|:-------------|:--------|------:|-------------------:|------------------:|------------------:|-------------------:|-------------------:|--------------:|-----------------:|------------------:|
| overall      | overall | 35187 |           0.968397 |           17.0955 |           17.8286 |          -0.733068 |           0.967744 |      2113.13  |          5.14179 |           7.57611 |
| region       | 1       |  8263 |           0.906329 |           21.0451 |           21.9681 |          -0.922994 |           0.906329 |       563.034 |          3.30094 |           4.63841 |
| region       | 2       | 20601 |           0.990437 |           13.2902 |           14.111  |          -0.820726 |           0.989321 |      3105.81  |          6.33296 |           9.3871  |
| region       | 3       |  6323 |           0.9777   |           24.8705 |           25.0842 |          -0.213669 |           0.9777   |       718.223 |          3.44145 |           5.15766 |

### Tabla 14. SFA con temperatura/topografia

| model | term | estimate | std_error | z_value | p_value | component | 
| --- | --- | --- | --- | --- | --- | --- | 
 | temp_topo | (Intercept) |  8.842702e+00 | 1.001070e-01 |    88.3324917 | 0.000000e+00 | frontier |
| temp_topo | log_land |  7.161754e-01 | 5.098636e-03 |   140.4641180 | 0.000000e+00 | frontier |
| temp_topo | log_labor |  2.372393e-01 | 5.847673e-03 |    40.5698631 | 0.000000e+00 | frontier |
| temp_topo | log_inputs |  1.108855e-01 | 2.447129e-03 |    45.3124813 | 0.000000e+00 | frontier |
| temp_topo | region_natural2 | -4.268370e-01 | 2.603259e-02 |   -16.3962559 | 0.000000e+00 | frontier |
| temp_topo | region_natural3 |  7.033720e-02 | 2.572959e-02 |     2.7337084 | 6.262547e-03 | frontier |
| temp_topo | log_surface_km2 |  2.065734e-03 | 5.531651e-03 |     0.3734390 | 7.088217e-01 | frontier |
| temp_topo | tmean_2024 | -7.281565e-03 | 3.637348e-03 |    -2.0018881 | 4.529677e-02 | frontier |
| temp_topo | delta_tmean_24_23 | -1.861242e-01 | 1.575189e-02 |   -11.8159919 | 0.000000e+00 | frontier |
| temp_topo | elev_m | -2.794247e-04 | 1.583783e-05 |   -17.6428604 | 0.000000e+00 | frontier |
| temp_topo | slope_deg | -5.434740e-04 | 4.803333e-03 |    -0.1131452 | 9.099155e-01 | frontier |
| temp_topo | ruggedness |  1.043831e-02 | 3.483081e-03 |     2.9968622 | 2.727740e-03 | frontier |
| temp_topo | prcp_total_z |  3.734642e-02 | 7.523820e-03 |     4.9637570 | 6.914246e-07 | frontier |
| temp_topo | Z_(Intercept) | -2.206611e+02 | 5.445123e+01 |    -4.0524533 | 5.068334e-05 | inefficiency |
| temp_topo | Z_diversificacion_area | -3.505566e+01 | 9.836902e+00 |    -3.5636888 | 3.656795e-04 | inefficiency |
| temp_topo | Z_size_mediano | -2.259315e+01 | 9.586730e+00 |    -2.3567113 | 1.843758e-02 | inefficiency |
| temp_topo | Z_size_grande |  1.226119e+02 | 3.062377e+01 |     4.0038147 | 6.232921e-05 | inefficiency |
| temp_topo | Z_diversif_mediano |  1.155689e+02 | 3.523244e+01 |     3.2801844 | 1.037393e-03 | inefficiency |
| temp_topo | Z_diversif_grande | -2.841762e+01 | 7.026647e+00 |    -4.0442648 | 5.248756e-05 | inefficiency |
| temp_topo | sigmaSq |  1.776173e+02 | 4.434168e+01 |     4.0056507 | 6.184698e-05 | variance |
| temp_topo | gamma |  9.969742e-01 | 7.883305e-04 |  1264.6652122 | 0.000000e+00 | variance |
| controls_temp_topo | (Intercept) |  8.679295e+00 | 9.986626e-02 |    86.9091825 | 0.000000e+00 | frontier |
| controls_temp_topo | log_land |  7.428318e-01 | 5.119993e-03 |   145.0845280 | 0.000000e+00 | frontier |
| controls_temp_topo | log_labor |  2.258908e-01 | 5.788279e-03 |    39.0255533 | 0.000000e+00 | frontier |
| controls_temp_topo | log_inputs |  1.056489e-01 | 2.512471e-03 |    42.0497913 | 0.000000e+00 | frontier |
| controls_temp_topo | region_natural2 | -2.901242e-01 | 2.563603e-02 |   -11.3170476 | 0.000000e+00 | frontier |
| controls_temp_topo | region_natural3 |  1.568146e-01 | 2.708866e-02 |     5.7889363 | 7.083355e-09 | frontier |
| controls_temp_topo | log_surface_km2 |  6.099768e-03 | 5.257502e-03 |     1.1602027 | 2.459663e-01 | frontier |
| controls_temp_topo | tmean_2024 | -3.536120e-03 | 3.516957e-03 |    -1.0054486 | 3.146809e-01 | frontier |
| controls_temp_topo | delta_tmean_24_23 | -1.356429e-01 | 1.562190e-02 |    -8.6828642 | 0.000000e+00 | frontier |
| controls_temp_topo | elev_m | -2.216548e-04 | 1.545843e-05 |   -14.3387716 | 0.000000e+00 | frontier |
| controls_temp_topo | slope_deg |  2.339684e-03 | 4.681141e-03 |     0.4998107 | 6.172084e-01 | frontier |
| controls_temp_topo | ruggedness |  8.914506e-03 | 3.383157e-03 |     2.6349667 | 8.414553e-03 | frontier |
| controls_temp_topo | prcp_total_z |  2.906265e-02 | 7.253172e-03 |     4.0068881 | 6.152400e-05 | frontier |
| controls_temp_topo | log_seed | -3.859766e-02 | 2.228249e-03 |   -17.3219692 | 0.000000e+00 | frontier |
| controls_temp_topo | log_irrigation_cost |  4.325198e-02 | 2.683592e-03 |    16.1171976 | 0.000000e+00 | frontier |
| controls_temp_topo | log_capital |  1.051663e-02 | 2.370920e-03 |     4.4356735 | 9.178485e-06 | frontier |
| controls_temp_topo | riego_tecnificado_any |  5.073698e-02 | 1.469754e-02 |     3.4520726 | 5.562981e-04 | frontier |
| controls_temp_topo | Z_(Intercept) | -5.939574e+02 | 5.400977e+01 |   -10.9972204 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_diversificacion_area | -1.021219e+02 | 9.482710e+00 |   -10.7692778 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_size_mediano | -3.838085e+01 | 4.032875e+00 |    -9.5169957 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_size_grande |  3.545403e+02 | 3.141340e+01 |    11.2862752 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_diversif_mediano |  3.092079e+02 | 2.905736e+01 |    10.6412959 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_diversif_grande | -5.279317e+01 | 3.832613e+00 |   -13.7747183 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_nivel_educacion | -4.952308e+00 | 4.509231e-01 |   -10.9826003 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_credito_obtenido | -8.171938e+01 | 7.730639e+00 |   -10.5708448 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_capacitacion_recibida | -1.437719e+01 | 5.907257e-01 |   -24.3381784 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_asistencia_tecnica_recibida | -1.453724e+02 | 1.298935e+01 |   -11.1916563 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_usuario_agua | -9.049769e+01 | 8.118412e+00 |   -11.1472150 | 0.000000e+00 | inefficiency |
| controls_temp_topo | Z_asociacion_miembro |  3.367364e+01 | 2.245015e+00 |    14.9992895 | 0.000000e+00 | inefficiency |
| controls_temp_topo | sigmaSq |  5.378190e+02 | 4.924547e+01 |    10.9211881 | 0.000000e+00 | variance |
| controls_temp_topo | gamma |  9.990890e-01 | 8.757231e-05 | 11408.7327499 | 0.000000e+00 | variance |


### Tabla 17. Logit con temperatura/topografia

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | temp_topo | (Intercept) |  9.0720490326 | 2.0761457119 |  4.36965911 | 1.276353e-05 | 8708.4494333 |
| temp_topo | diversificacion_area |  2.4872841375 | 0.6475925267 |  3.84081662 | 1.245475e-04 |   12.0285638 |
| temp_topo | size_catmediano_2_5ha |  0.4632275037 | 0.4225914424 |  1.09615921 | 2.730759e-01 |    1.5891948 |
| temp_topo | size_catpequeno_<2ha |  0.3818096782 | 0.4682539291 |  0.81539023 | 4.148981e-01 |    1.4649332 |
| temp_topo | log_area |  0.2347642107 | 0.1718295049 |  1.36626251 | 1.719343e-01 |    1.2646106 |
| temp_topo | region_natural2 |  1.2851219562 | 0.8208168911 |  1.56566217 | 1.175078e-01 |    3.6151088 |
| temp_topo | region_natural3 | -1.2511356970 | 0.5012137202 | -2.49621199 | 1.259318e-02 |    0.2861796 |
| temp_topo | tmean_2024 | -0.2733252233 | 0.0783665385 | -3.48777971 | 4.923567e-04 |    0.7608453 |
| temp_topo | delta_tmean_24_23 |  0.0934328286 | 0.2220735744 |  0.42072916 | 6.739757e-01 |    1.0979369 |
| temp_topo | elev_m | -0.0008704977 | 0.0004415812 | -1.97131971 | 4.875696e-02 |    0.9991299 |
| temp_topo | slope_deg |  0.0737956385 | 0.0878433779 |  0.84008198 | 4.009132e-01 |    1.0765868 |
| temp_topo | ruggedness | -0.0344787834 | 0.0581672919 | -0.59275208 | 5.533810e-01 |    0.9661088 |
| temp_topo | prcp_total_z |  0.4687199547 | 0.1128270062 |  4.15432413 | 3.331468e-05 |    1.5979474 |
| temp_topo | diversificacion_area:size_catmediano_2_5ha | -0.3468759582 | 0.8687988834 | -0.39925921 | 6.897238e-01 |    0.7068930 |
| temp_topo | diversificacion_area:size_catpequeno_<2ha | -0.8352864049 | 0.8787458872 | -0.95054374 | 3.418941e-01 |    0.4337502 |
| controls_temp_topo | (Intercept) |  4.8398641804 | 2.2245150026 |  2.17569411 | 2.963728e-02 |  126.4521759 |
| controls_temp_topo | diversificacion_area |  2.3834604632 | 0.6426039735 |  3.70906587 | 2.108865e-04 |   10.8423576 |
| controls_temp_topo | size_catmediano_2_5ha |  0.2927797411 | 0.4183924213 |  0.69977305 | 4.841103e-01 |    1.3401476 |
| controls_temp_topo | size_catpequeno_<2ha |  0.2547670074 | 0.4837459710 |  0.52665453 | 5.984631e-01 |    1.2901610 |
| controls_temp_topo | log_area |  0.0925155232 | 0.1727677254 |  0.53549078 | 5.923407e-01 |    1.0969302 |
| controls_temp_topo | region_natural2 |  1.5473146285 | 0.7036406488 |  2.19901257 | 2.793484e-02 |    4.6988351 |
| controls_temp_topo | region_natural3 | -0.6465233037 | 0.4412451087 | -1.46522486 | 1.429392e-01 |    0.5238639 |
| controls_temp_topo | tmean_2024 | -0.1665901549 | 0.0806735762 | -2.06499033 | 3.898907e-02 |    0.8465465 |
| controls_temp_topo | delta_tmean_24_23 | -0.0256540920 | 0.2234248579 | -0.11482201 | 9.085920e-01 |    0.9746722 |
| controls_temp_topo | elev_m | -0.0003527935 | 0.0004039784 | -0.87329805 | 3.825538e-01 |    0.9996473 |
| controls_temp_topo | slope_deg |  0.0649061636 | 0.0855695214 |  0.75851965 | 4.481852e-01 |    1.0670589 |
| controls_temp_topo | ruggedness | -0.0184034352 | 0.0559343691 | -0.32901838 | 7.421593e-01 |    0.9817649 |
| controls_temp_topo | prcp_total_z |  0.3809936891 | 0.1043562199 |  3.65089584 | 2.647134e-04 |    1.4637384 |
| controls_temp_topo | nivel_educacion |  0.1008337121 | 0.0357107949 |  2.82361993 | 4.772267e-03 |    1.1060927 |
| controls_temp_topo | credito_obtenido |  0.7705945447 | 0.2934228950 |  2.62622501 | 8.667122e-03 |    2.1610507 |
| controls_temp_topo | capacitacion_recibida |  1.3910934277 | 0.3330010820 |  4.17744417 | 3.011784e-05 |    4.0192424 |
| controls_temp_topo | asistencia_tecnica_recibida | -0.0426940263 | 0.4551347652 | -0.09380524 | 9.252686e-01 |    0.9582045 |
| controls_temp_topo | usuario_agua |  4.9467879460 | 0.6974915593 |  7.09225492 | 1.556425e-12 |  140.7222298 |
| controls_temp_topo | asociacion_miembro |  0.5234464047 | 0.3258397016 |  1.60645373 | 1.082542e-01 |    1.6878346 |
| controls_temp_topo | diversificacion_area:size_catmediano_2_5ha | -0.1845790751 | 0.8264037981 | -0.22335216 | 8.232730e-01 |    0.8314542 |
| controls_temp_topo | diversificacion_area:size_catpequeno_<2ha | -0.7950144623 | 0.8761884178 | -0.90735559 | 3.642742e-01 |    0.4515747 |


## Comparaciones de robustez (controles + geo/clima)

Se comparan los coeficientes de diversificacion e interacciones en las especificaciones baseline, con controles ENA y con temperatura/topografia.

### Tabla 15. Comparacion efectos SFA

| model | term | estimate | std_error | p_value | 
| --- | --- | --- | --- | --- | 
 | main_area | Z_diversificacion_area |  -14.93047 |  1.820617 | 2.220446e-16 |
| main_area | Z_diversif_mediano |  174.79297 | 23.979256 | 3.115286e-13 |
| main_area | Z_diversif_grande |  -69.90127 | 10.234233 | 8.482992e-12 |
| controls_ena | Z_diversificacion_area |  -14.86033 |  1.394045 | 0.000000e+00 |
| controls_ena | Z_diversif_mediano |  166.96489 | 22.213213 | 5.617729e-14 |
| controls_ena | Z_diversif_grande |  -61.31012 |  6.053377 | 0.000000e+00 |
| temp_topo | Z_diversificacion_area |  -35.05566 |  9.836902 | 3.656795e-04 |
| temp_topo | Z_diversif_mediano |  115.56889 | 35.232437 | 1.037393e-03 |
| temp_topo | Z_diversif_grande |  -28.41762 |  7.026647 | 5.248756e-05 |
| controls_temp_topo | Z_diversificacion_area | -102.12193 |  9.482710 | 0.000000e+00 |
| controls_temp_topo | Z_diversif_mediano |  309.20792 | 29.057355 | 0.000000e+00 |
| controls_temp_topo | Z_diversif_grande |  -52.79317 |  3.832613 | 0.000000e+00 |


### Tabla 18. Comparacion efectos logit

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main | diversificacion_area |  2.7379459 | 0.5720020 |  4.7866017 | 1.758159e-06 | 15.4552053 |
| main | diversificacion_area:size_catmediano_2_5ha | -0.3240044 | 0.7803323 | -0.4152133 | 6.780082e-01 |  0.7232471 |
| main | diversificacion_area:size_catpequeno_<2ha | -0.8807614 | 0.8227013 | -1.0705725 | 2.844269e-01 |  0.4144672 |
| controls_ena | diversificacion_area |  2.6452317 | 0.5771254 |  4.5834610 | 4.714530e-06 | 14.0867085 |
| controls_ena | diversificacion_area:size_catmediano_2_5ha | -0.2248060 | 0.7625876 | -0.2947937 | 7.681670e-01 |  0.7986711 |
| controls_ena | diversificacion_area:size_catpequeno_<2ha | -0.8061641 | 0.8100392 | -0.9952162 | 3.196920e-01 |  0.4465678 |
| temp_topo | diversificacion_area |  2.4872841 | 0.6475925 |  3.8408166 | 1.245475e-04 | 12.0285638 |
| temp_topo | diversificacion_area:size_catmediano_2_5ha | -0.3468760 | 0.8687989 | -0.3992592 | 6.897238e-01 |  0.7068930 |
| temp_topo | diversificacion_area:size_catpequeno_<2ha | -0.8352864 | 0.8787459 | -0.9505437 | 3.418941e-01 |  0.4337502 |
| controls_temp_topo | diversificacion_area |  2.3834605 | 0.6426040 |  3.7090659 | 2.108865e-04 | 10.8423576 |
| controls_temp_topo | diversificacion_area:size_catmediano_2_5ha | -0.1845791 | 0.8264038 | -0.2233522 | 8.232730e-01 |  0.8314542 |
| controls_temp_topo | diversificacion_area:size_catpequeno_<2ha | -0.7950145 | 0.8761884 | -0.9073556 | 3.642742e-01 |  0.4515747 |


### Analisis de perdida muestral

| sample_type   | group_type   | group         |   n_base |   n_geo2 |   share_remaining |      weight_base |      weight_geo2 |
|:--------------|:-------------|:--------------|---------:|---------:|------------------:|-----------------:|-----------------:|
| logit         | overall      | overall       |    34074 |    34051 |          0.999325 |      2.11889e+06 |      2.11783e+06 |
| logit         | region       | 1             |     7489 |     7489 |          1        | 261014           | 261014           |
| logit         | region       | 2             |    20403 |    20380 |          0.998873 |      1.54006e+06 |      1.539e+06   |
| logit         | region       | 3             |     6182 |     6182 |          1        | 317816           | 317816           |
| logit         | size         | pequeno_<2ha  |    21956 |    21938 |          0.99918  |      1.53022e+06 |      1.52926e+06 |
| logit         | size         | mediano_2_5ha |     6278 |     6275 |          0.999522 | 355684           | 355627           |
| logit         | size         | grande_>5ha   |     5840 |     5838 |          0.999658 | 232992           | 232947           |
| sfa           | overall      | overall       |    31824 |    31804 |          0.999372 |    nan           |    nan           |
| sfa           | region       | 1             |     7289 |     7289 |          1        |    nan           |    nan           |
| sfa           | region       | 2             |    18759 |    18739 |          0.998934 |    nan           |    nan           |
| sfa           | region       | 3             |     5776 |     5776 |          1        |    nan           |    nan           |
| sfa           | size         | pequeno_<2ha  |    20692 |    20677 |          0.999275 |    nan           |    nan           |
| sfa           | size         | mediano_2_5ha |     5905 |     5902 |          0.999492 |    nan           |    nan           |
| sfa           | size         | grande_>5ha   |     5227 |     5225 |          0.999617 |    nan           |    nan           |

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
