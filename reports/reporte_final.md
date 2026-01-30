# El rol de la diversificacion de cultivos en la productividad agropecuaria: El caso del Peru

## Motivacion y preguntas

Se evalua la relacion entre diversificacion de cultivos y productividad/eficiencia (SFA), asi como su asociacion con practicas sostenibles (logit) usando ENA 2024.

## Datos ENA 2024 y diseno muestral

Fuente: ENA 2024 (INEI). Diseno muestral con pesos (FACTOR_PRODUCTOR), estratos y PSU.

### Tabla 00. Resumen muestral

| group_type   | group         |     n |       weight_sum |   mean_area_ha |   mean_valor_total |   mean_diversif |   mean_practice_any |
|:-------------|:--------------|------:|-----------------:|---------------:|-------------------:|----------------:|--------------------:|
| overall      | overall       | 35187 |      2.12001e+06 |       4.59897  |           28857.5  |        0.504382 |            0.776069 |
| region       | 1             |  8263 | 261788           |       4.29902  |           70773.2  |        0.422817 |            0.784919 |
| region       | 2             | 20601 |      1.54026e+06 |       1.85572  |            7172.15 |        0.567544 |            0.906408 |
| region       | 3             |  6323 | 317957           |      14.0166   |           46391    |        0.394723 |            0.33987  |
| size         | grande_>5ha   |  5840 | 232992           |      20.6877   |          119622    |        0.532199 |            0.565068 |
| size         | mediano_2_5ha |  6278 | 355684           |       3.20459  |           29777.7  |        0.541143 |            0.739248 |
| size         | pequeno_<2ha  | 21957 |      1.53022e+06 |       0.718452 |            5667.01 |        0.486473 |            0.83599  |
| size         | nan           |  1112 |   1112           |     nan        |             nan    |      nan        |            0.909091 |

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

| model | term | estimate | std_error | z_value | p_value | component | inference_note | n_total | n_valid | share_dropped | gamma | gamma_near_boundary | cov_singular | cov_rank | cov_cond | cov_rcond | input_cost_var | ineffDecrease | truncNorm | timeEffect | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | 
 | main_area | (Intercept) |   8.40419653 | 0.051174008 | 164.227834 | 0.0000000 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | log_land |   0.90386454 | 0.005995433 | 150.758835 | 0.0000000 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | log_labor |   0.25382833 | 0.007286540 |  34.835234 | 0.0000000 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | log_inputs |   0.07007366 | 0.006689028 |  10.475910 | 0.0000000 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | Z_(Intercept) | -16.81278496 | 1.069054594 | -15.726779 | 0.0000000 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | Z_diversificacion_area |   1.92937853 | 0.200791530 |   9.608864 | 0.0000000 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | Z_size_mediano |   2.33356342 | 0.213122398 |  10.949405 | 0.0000000 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | Z_size_grande |   8.84211634 | 0.390458332 |  22.645480 | 0.0000000 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | Z_diversif_mediano |  -0.19952180 | 0.242915799 |  -0.821362 | 0.4114401 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | Z_diversif_grande |  -5.54253932 | 0.289242038 | -19.162288 | 0.0000000 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | Z_region_natural2 |  12.53650400 | 0.708688739 |  17.689718 | 0.0000000 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | Z_region_natural3 |   8.34711817 | 0.565194002 |  14.768589 | 0.0000000 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | sigmaSq |   7.03430138 | 0.333929212 |  21.065247 | 0.0000000 | variance |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| main_area | gamma |   0.93268439 | 0.003293945 | 283.151207 | 0.0000000 | variance |  | 31824 | 26594 | 0.1643414 | 0.9326844 | FALSE | FALSE | 14 | 5668883 | 1.764016e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |


### Robustez SFA

| model | term | estimate | std_error | z_value | p_value | component | inference_note | n_total | n_valid | share_dropped | gamma | gamma_near_boundary | cov_singular | cov_rank | cov_cond | cov_rcond | input_cost_var | ineffDecrease | truncNorm | timeEffect | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | 
 | alt_shannon | (Intercept) |   7.95240784 |  0.051755816 | 153.652450 | 0.000000e+00 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | log_land |   0.88986530 |  0.006255305 | 142.257697 | 0.000000e+00 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | log_labor |   0.29746931 |  0.008562729 |  34.740012 | 0.000000e+00 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | log_inputs |   0.10889603 |  0.006979520 |  15.602224 | 0.000000e+00 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | Z_(Intercept) | -59.83156927 |  8.661869179 |  -6.907466 | 4.933831e-12 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | Z_diversif_alt |  12.83486988 |  1.623545658 |   7.905457 | 2.664535e-15 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | Z_size_mediano |  -0.73288659 |  0.601284709 |  -1.218868 | 2.228944e-01 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | Z_size_grande |  33.34767559 |  4.371592069 |   7.628268 | 2.375877e-14 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | Z_diversif_alt_med |   4.98643039 |  0.868962570 |   5.738372 | 9.559103e-09 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | Z_diversif_alt_gra | -11.93816652 |  1.714295353 |  -6.963891 | 3.310019e-12 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | sigmaSq |  46.83065905 |  6.996507318 |   6.693434 | 2.179945e-11 | variance |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_shannon | gamma |   0.98870996 |  0.001802724 | 548.453452 | 0.000000e+00 | variance |  | 31824 | 26594 | 0.1643414 | 0.9887100 | FALSE | FALSE | 12 |  8358075418 | 1.196448e-10 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | (Intercept) |   7.99664086 |  0.053289916 | 150.059175 | 0.000000e+00 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | log_land |   0.88360814 |  0.006127905 | 144.194166 | 0.000000e+00 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | log_labor |   0.30438413 |  0.008691257 |  35.021878 | 0.000000e+00 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | log_inputs |   0.10227467 |  0.007107526 |  14.389630 | 0.000000e+00 | frontier |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | Z_(Intercept) | -54.73606967 | 10.360969364 |  -5.282910 | 1.271478e-07 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | Z_diversif_alt2 |   1.46812128 |  0.329802690 |   4.451514 | 8.526698e-06 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | Z_size_mediano |   5.31520736 |  1.222746081 |   4.346943 | 1.380482e-05 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | Z_size_grande |  18.18949045 |  3.686522747 |   4.934051 | 8.054148e-07 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | Z_diversif_alt2_med |   0.43687430 |  0.129213776 |   3.381020 | 7.221741e-04 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | Z_diversif_alt2_gra |   0.52549662 |  0.151281036 |   3.473645 | 5.134398e-04 | inefficiency |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | sigmaSq |  50.14243971 |  8.661405960 |   5.789180 | 7.073079e-09 | variance |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| alt_num_crops | gamma |   0.98934727 |  0.001869797 | 529.120075 | 0.000000e+00 | variance |  | 31824 | 26594 | 0.1643414 | 0.9893473 | FALSE | FALSE | 12 | 12565849285 | 7.958077e-11 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| small_only | (Intercept) |   8.57923204 |  0.073837442 | 116.190808 | 0.000000e+00 | frontier |  | 20692 | 16015 | 0.2260294 | 0.8440360 | FALSE | FALSE |  8 |     1033286 | 9.677860e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| small_only | log_land |   0.88505348 |  0.008604260 | 102.862247 | 0.000000e+00 | frontier |  | 20692 | 16015 | 0.2260294 | 0.8440360 | FALSE | FALSE |  8 |     1033286 | 9.677860e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| small_only | log_labor |   0.26972741 |  0.011957468 |  22.557234 | 0.000000e+00 | frontier |  | 20692 | 16015 | 0.2260294 | 0.8440360 | FALSE | FALSE |  8 |     1033286 | 9.677860e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| small_only | log_inputs |   0.03719875 |  0.008980297 |   4.142262 | 3.438969e-05 | frontier |  | 20692 | 16015 | 0.2260294 | 0.8440360 | FALSE | FALSE |  8 |     1033286 | 9.677860e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| small_only | Z_(Intercept) |  -2.87601424 |  0.707487219 |  -4.065111 | 4.800956e-05 | inefficiency |  | 20692 | 16015 | 0.2260294 | 0.8440360 | FALSE | FALSE |  8 |     1033286 | 9.677860e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| small_only | Z_diversificacion_area |   2.70549534 |  0.379984060 |   7.120023 | 1.079137e-12 | inefficiency |  | 20692 | 16015 | 0.2260294 | 0.8440360 | FALSE | FALSE |  8 |     1033286 | 9.677860e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| small_only | sigmaSq |   3.68577065 |  0.414921256 |   8.883061 | 0.000000e+00 | variance |  | 20692 | 16015 | 0.2260294 | 0.8440360 | FALSE | FALSE |  8 |     1033286 | 9.677860e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| small_only | gamma |   0.84403600 |  0.015092434 |  55.924446 | 0.000000e+00 | variance |  | 20692 | 16015 | 0.2260294 | 0.8440360 | FALSE | FALSE |  8 |     1033286 | 9.677860e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |


## Resultados logit (practicas sostenibles)

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main | (Intercept) |  0.0149381886 | 0.4369383 |  0.034188325 | 9.727287e-01 | 1.0150503 |
| main | diversificacion_area |  1.3818975540 | 0.3352644 |  4.121813565 | 3.835921e-05 | 3.9824514 |
| main | size_catmediano_2_5ha |  0.2393949845 | 0.3058043 |  0.782837197 | 4.337695e-01 | 1.2704803 |
| main | size_catpequeno_<2ha |  0.3695917757 | 0.3834822 |  0.963778295 | 3.352159e-01 | 1.4471437 |
| main | log_area | -0.0009314792 | 0.1503100 | -0.006197055 | 9.950558e-01 | 0.9990690 |
| main | region_natural2 |  1.1784446547 | 0.1751995 |  6.726301967 | 1.989392e-11 | 3.2493165 |
| main | region_natural3 | -1.1739101930 | 0.1402366 | -8.370924121 | 7.832356e-17 | 0.3091557 |
| main | diversificacion_area:size_catmediano_2_5ha |  0.1066186030 | 0.4350723 |  0.245059497 | 8.064231e-01 | 1.1125099 |
| main | diversificacion_area:size_catpequeno_<2ha |  0.1168454834 | 0.4562331 |  0.256109154 | 7.978798e-01 | 1.1239457 |


### Robustez logit

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | alt_shannon | (Intercept) |  0.16670782 | 0.42216332 |  0.39488939 | 6.929458e-01 | 1.1814090 |
| alt_shannon | diversif_alt |  0.64128120 | 0.14909690 |  4.30110346 | 1.740442e-05 | 1.8989122 |
| alt_shannon | size_catmediano_2_5ha |  0.10475439 | 0.28398544 |  0.36887240 | 7.122425e-01 | 1.1104378 |
| alt_shannon | size_catpequeno_<2ha |  0.27920199 | 0.36825217 |  0.75818152 | 4.483874e-01 | 1.3220744 |
| alt_shannon | log_area | -0.02724144 | 0.15014454 | -0.18143479 | 8.560356e-01 | 0.9731263 |
| alt_shannon | region_natural2 |  1.12993130 | 0.17581286 |  6.42689788 | 1.456711e-10 | 3.0954438 |
| alt_shannon | region_natural3 | -1.16455847 | 0.14003384 | -8.31626481 | 1.233829e-16 | 0.3120604 |
| alt_shannon | diversif_alt:size_catmediano_2_5ha |  0.16732324 | 0.19620468 |  0.85279943 | 3.938221e-01 | 1.1821363 |
| alt_shannon | diversif_alt:size_catpequeno_<2ha |  0.12879302 | 0.21385469 |  0.60224547 | 5.470452e-01 | 1.1374547 |
| alt_num_crops | (Intercept) |  0.27431214 | 0.41298965 |  0.66421071 | 5.065941e-01 | 1.3156254 |
| alt_num_crops | diversif_alt2 |  0.11723844 | 0.03057719 |  3.83417931 | 1.279408e-04 | 1.1243875 |
| alt_num_crops | size_catmediano_2_5ha | -0.06072619 | 0.27754463 | -0.21879793 | 8.268187e-01 | 0.9410809 |
| alt_num_crops | size_catpequeno_<2ha | -0.01177693 | 0.36640028 | -0.03214225 | 9.743602e-01 | 0.9882921 |
| alt_num_crops | log_area |  0.01624820 | 0.14673231 |  0.11073361 | 9.118332e-01 | 1.0163809 |
| alt_num_crops | region_natural2 |  1.29877816 | 0.16898417 |  7.68579771 | 1.904695e-14 | 3.6648161 |
| alt_num_crops | region_natural3 | -1.24345724 | 0.14104997 | -8.81572169 | 1.748950e-18 | 0.2883855 |
| alt_num_crops | diversif_alt2:size_catmediano_2_5ha |  0.08780090 | 0.04468441 |  1.96491132 | 4.949426e-02 | 1.0917707 |
| alt_num_crops | diversif_alt2:size_catpequeno_<2ha |  0.11419478 | 0.05699517 |  2.00358699 | 4.518228e-02 | 1.1209704 |
| alt_outcome_two_plus | (Intercept) | -1.09284853 | 0.45394138 | -2.40746621 | 1.610908e-02 | 0.3352601 |
| alt_outcome_two_plus | diversificacion_area |  1.28989653 | 0.36019035 |  3.58115234 | 3.461878e-04 | 3.6324107 |
| alt_outcome_two_plus | size_catmediano_2_5ha |  0.40787714 | 0.34250823 |  1.19085355 | 2.337824e-01 | 1.5036224 |
| alt_outcome_two_plus | size_catpequeno_<2ha |  0.19202980 | 0.44021512 |  0.43621809 | 6.627023e-01 | 1.2117066 |
| alt_outcome_two_plus | log_area | -0.17169296 | 0.15973623 | -1.07485297 | 2.825060e-01 | 0.8422377 |
| alt_outcome_two_plus | region_natural2 |  1.12916560 | 0.13004151 |  8.68311670 | 5.538594e-18 | 3.0930746 |
| alt_outcome_two_plus | region_natural3 | -1.16760938 | 0.14555738 | -8.02164323 | 1.361905e-15 | 0.3111098 |
| alt_outcome_two_plus | diversificacion_area:size_catmediano_2_5ha | -0.26496175 | 0.60998109 | -0.43437700 | 6.640383e-01 | 0.7672353 |
| alt_outcome_two_plus | diversificacion_area:size_catpequeno_<2ha |  0.08601866 | 0.49457697 |  0.17392371 | 8.619343e-01 | 1.0898267 |
| small_only | (Intercept) | -0.00397690 | 0.23070252 | -0.01723822 | 9.862478e-01 | 0.9960310 |
| small_only | diversificacion_area |  1.36222065 | 0.32221070 |  4.22773254 | 2.436455e-05 | 3.9048550 |
| small_only | log_area |  0.33770246 | 0.32881962 |  1.02701433 | 3.045027e-01 | 1.4017234 |
| small_only | region_natural2 |  1.53104146 | 0.21153692 |  7.23770336 | 5.871784e-13 | 4.6229890 |
| small_only | region_natural3 | -0.78789128 | 0.21622328 | -3.64387817 | 2.734567e-04 | 0.4548028 |


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

| model | term | estimate | std_error | z_value | p_value | component | inference_note | n_total | n_valid | share_dropped | gamma | gamma_near_boundary | cov_singular | cov_rank | cov_cond | cov_rcond | input_cost_var | ineffDecrease | truncNorm | timeEffect | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | 
 | xgeo_prcp | (Intercept) |  8.203741e+00 | 0.060699858 | 135.1525558 | 0.000000e+00 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | log_land |  9.006359e-01 | 0.006045910 | 148.9661359 | 0.000000e+00 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | log_labor |  2.576675e-01 | 0.007920127 |  32.5332595 | 0.000000e+00 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | log_inputs |  6.970296e-02 | 0.006780131 |  10.2804732 | 0.000000e+00 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | log_surface_km2 |  3.179726e-02 | 0.005753679 |   5.5264222 | 3.268271e-08 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | prcp_total_z | -2.269706e-04 | 0.008738814 |  -0.0259727 | 9.792791e-01 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | Z_(Intercept) | -1.759011e+01 | 1.250742054 | -14.0637395 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | Z_diversificacion_area |  1.926751e+00 | 0.185106469 |  10.4088819 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | Z_size_mediano |  2.461598e+00 | 0.280967783 |   8.7611401 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | Z_size_grande |  9.141758e+00 | 0.488847168 |  18.7006468 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | Z_diversif_mediano | -2.080866e-01 | 0.281648634 |  -0.7388161 | 4.600186e-01 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | Z_diversif_grande | -5.670511e+00 | 0.363747276 | -15.5891500 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | Z_region_natural2 |  1.298194e+01 | 0.833601522 |  15.5733196 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | Z_region_natural3 |  8.791813e+00 | 0.641999871 |  13.6944152 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | sigmaSq |  7.325154e+00 | 0.392894264 |  18.6440836 | 0.000000e+00 | variance |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| xgeo_prcp | gamma |  9.352408e-01 | 0.003304719 | 283.0016281 | 0.000000e+00 | variance |  | 31824 | 26578 | 0.1648441 | 0.9352408 | FALSE | FALSE | 16 | 11982341 | 8.345614e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | (Intercept) |  8.201175e+00 | 0.060948709 | 134.5586305 | 0.000000e+00 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | log_land |  9.042981e-01 | 0.005970480 | 151.4615419 | 0.000000e+00 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | log_labor |  2.460347e-01 | 0.007836322 |  31.3967095 | 0.000000e+00 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | log_inputs |  7.255563e-02 | 0.006907014 |  10.5046306 | 0.000000e+00 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | log_surface_km2 |  3.253513e-02 | 0.005526509 |   5.8871026 | 3.930247e-09 | frontier |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_(Intercept) | -1.740252e+01 | 1.074701481 | -16.1928878 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_diversificacion_area |  2.100153e+00 | 0.198608266 |  10.5743464 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_size_mediano |  2.327524e+00 | 0.251043840 |   9.2713856 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_size_grande |  8.756853e+00 | 0.457493223 |  19.1409456 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_diversif_mediano | -1.469793e-01 | 0.280870060 |  -0.5233001 | 6.007654e-01 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_diversif_grande | -5.593843e+00 | 0.350757207 | -15.9479068 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_prcp_total_z | -7.150248e-01 | 0.047791262 | -14.9614122 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_region_natural2 |  1.264605e+01 | 0.683397796 |  18.5046733 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | Z_region_natural3 |  8.165664e+00 | 0.509567746 |  16.0246867 | 0.000000e+00 | inefficiency |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | sigmaSq |  7.144010e+00 | 0.341139483 |  20.9416087 | 0.000000e+00 | variance |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| zgeo_prcp | gamma |  9.340107e-01 | 0.003116903 | 299.6598555 | 0.000000e+00 | variance |  | 31824 | 26578 | 0.1648441 | 0.9340107 | FALSE | FALSE | 16 | 11036727 | 9.060657e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |


### Tabla 08. Comparacion efectos SFA

| model | term | estimate | std_error | p_value | 
| --- | --- | --- | --- | --- | 
 | main_area | Z_diversificacion_area |  1.9293785 | 0.2007915 | 0.0000000 |
| main_area | Z_diversif_mediano | -0.1995218 | 0.2429158 | 0.4114401 |
| main_area | Z_diversif_grande | -5.5425393 | 0.2892420 | 0.0000000 |
| xgeo_prcp | Z_diversificacion_area |  1.9267514 | 0.1851065 | 0.0000000 |
| xgeo_prcp | Z_diversif_mediano | -0.2080866 | 0.2816486 | 0.4600186 |
| xgeo_prcp | Z_diversif_grande | -5.6705108 | 0.3637473 | 0.0000000 |
| zgeo_prcp | Z_diversificacion_area |  2.1001526 | 0.1986083 | 0.0000000 |
| zgeo_prcp | Z_diversif_mediano | -0.1469793 | 0.2808701 | 0.6007654 |
| zgeo_prcp | Z_diversif_grande | -5.5938432 | 0.3507572 | 0.0000000 |


### Tabla 09. Logit con controles geo/clima

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main_geo | (Intercept) |  0.1903851531 | 0.42310271 |  0.44997385 | 6.527539e-01 | 1.2097154 |
| main_geo | diversificacion_area |  1.4002741293 | 0.35351810 |  3.96096868 | 7.595851e-05 | 4.0563118 |
| main_geo | size_catmediano_2_5ha |  0.2474332392 | 0.30653160 |  0.80720304 | 4.195980e-01 | 1.2807339 |
| main_geo | size_catpequeno_<2ha |  0.4478786604 | 0.38273484 |  1.17020615 | 2.419884e-01 | 1.5649888 |
| main_geo | log_area |  0.0564980289 | 0.14611835 |  0.38665937 | 6.990292e-01 | 1.0581245 |
| main_geo | region_natural2 |  1.1921981089 | 0.16527567 |  7.21339146 | 6.506623e-13 | 3.2943145 |
| main_geo | region_natural3 | -0.9830809765 | 0.14141779 | -6.95160767 | 4.205064e-12 | 0.3741566 |
| main_geo | prcp_total_z |  0.5501213448 | 0.07951153 |  6.91876187 | 5.290165e-12 | 1.7334634 |
| main_geo | diversificacion_area:size_catmediano_2_5ha |  0.0807410756 | 0.44271967 |  0.18237517 | 8.552976e-01 | 1.0840902 |
| main_geo | diversificacion_area:size_catpequeno_<2ha |  0.0008807157 | 0.46929701 |  0.00187667 | 9.985027e-01 | 1.0008811 |


### Tabla 10. Comparacion efectos logit

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main | diversificacion_area | 1.3818975540 | 0.3352644 | 4.12181357 | 3.835921e-05 | 3.982451 |
| main | diversificacion_area:size_catmediano_2_5ha | 0.1066186030 | 0.4350723 | 0.24505950 | 8.064231e-01 | 1.112510 |
| main | diversificacion_area:size_catpequeno_<2ha | 0.1168454834 | 0.4562331 | 0.25610915 | 7.978798e-01 | 1.123946 |
| main_geo | diversificacion_area | 1.4002741293 | 0.3535181 | 3.96096868 | 7.595851e-05 | 4.056312 |
| main_geo | diversificacion_area:size_catmediano_2_5ha | 0.0807410756 | 0.4427197 | 0.18237517 | 8.552976e-01 | 1.084090 |
| main_geo | diversificacion_area:size_catpequeno_<2ha | 0.0008807157 | 0.4692970 | 0.00187667 | 9.985027e-01 | 1.000881 |


## Controles ENA adicionales

Se incorporan controles de capital, riego, semillas, asistencia tecnica, credito y educacion. Las tablas siguientes muestran cobertura y efectos econometricos.

### Tabla 11. Cobertura controles ENA

| group_type   | group         | variable                    |   missing_pct |           mean |         p50 |           p90 |
|:-------------|:--------------|:----------------------------|--------------:|---------------:|------------:|--------------:|
| overall      | overall       | riego_any                   |   0           |      0.596811  |    1        |      1        |
| overall      | overall       | riego_share                 |   0           |      0.506873  |    0.5      |      1        |
| overall      | overall       | riego_tecnificado_any       |   0.403189    |      0.313143  |    0        |      1        |
| overall      | overall       | riego_tecnificado_share     |   0.403189    |      0.26256   |    0        |      1        |
| overall      | overall       | usuario_agua                |   0.0495353   |      0.449916  |    0        |      1        |
| overall      | overall       | gasto_agua_riego            |   0.000198937 |   9864.84      |    0        |    700        |
| overall      | overall       | uso_maquinaria              |   0.000113678 |      0.715914  |    1        |      1        |
| overall      | overall       | num_maquinaria_equipo       |   0.284167    |      3.54971   |    1        |      6        |
| overall      | overall       | gasto_compra_equipos        |   0.000198937 |   1194.66      |    0        |      0        |
| overall      | overall       | gasto_compra_maquinaria     |   0.000198937 |   2911.23      |    0        |      0        |
| overall      | overall       | gasto_alquiler_mant_equipos |   0.000198937 |   4172.6       |    0        |    240        |
| overall      | overall       | gasto_semilla               |   0.315685    |   5115.16      |  445        |   3900        |
| overall      | overall       | usa_abono                   |   5.68392e-05 |      0.607333  |    1        |      1        |
| overall      | overall       | usa_fertilizantes           |   5.68392e-05 |      0.587012  |    1        |      1        |
| overall      | overall       | semilla_semillero_any       |   5.68392e-05 |      0.12241   |    0        |      1        |
| overall      | overall       | semilla_comercial_any       |   5.68392e-05 |      0.273327  |    0        |      1        |
| overall      | overall       | semilla_certificada_any     |   0.286498    |      0.144189  |    0        |      1        |
| overall      | overall       | semilla_certificada_share   |   0.286498    |      0.117558  |    0        |      0.666667 |
| overall      | overall       | capacitacion_recibida       |   8.52588e-05 |      0.0976296 |    0        |      0        |
| overall      | overall       | asistencia_tecnica_recibida |   8.52588e-05 |      0.0573272 |    0        |      0        |
| overall      | overall       | credito_obtenido            |   0.86603     |      0.932541  |    1        |      1        |
| overall      | overall       | nivel_educacion             |   0.031631    |      4.5444    |    4        |      8        |
| overall      | overall       | asociacion_miembro          |   8.52588e-05 |      0.0795248 |    0        |      0        |
| overall      | overall       | asociacion_num              |   8.52588e-05 |      0.0836744 |    0        |      0        |
| region       | 1             | riego_any                   |   0           |      0.95849   |    1        |      1        |
| region       | 1             | riego_share                 |   0           |      0.949754  |    1        |      1        |
| region       | 1             | riego_tecnificado_any       |   0.0415103   |      0.239268  |    0        |      1        |
| region       | 1             | riego_tecnificado_share     |   0.0415103   |      0.202277  |    0        |      1        |
| region       | 1             | usuario_agua                |   0.108435    |      0.74698   |    1        |      1        |
| region       | 1             | gasto_agua_riego            |   0.000605107 |  41741.5       |  400        |   6000        |
| region       | 1             | uso_maquinaria              |   0.000242043 |      0.837913  |    1        |      1        |
| region       | 1             | num_maquinaria_equipo       |   0.16229     |      5.12612   |    3        |     10        |
| region       | 1             | gasto_compra_equipos        |   0.000605107 |   4633.41      |    0        |      0        |
| region       | 1             | gasto_compra_maquinaria     |   0.000605107 |  11520.6       |    0        |      0        |
| region       | 1             | gasto_alquiler_mant_equipos |   0.000605107 |  16576.9       |    0        |   1000        |
| region       | 1             | gasto_semilla               |   0.462302    |  22328.7       | 1500        |  18473.2      |
| region       | 1             | usa_abono                   |   0.000121021 |      0.447954  |    0        |      1        |
| region       | 1             | usa_fertilizantes           |   0.000121021 |      0.853788  |    1        |      1        |
| region       | 1             | semilla_semillero_any       |   0.000121021 |      0.171871  |    0        |      1        |
| region       | 1             | semilla_comercial_any       |   0.000121021 |      0.302832  |    0        |      1        |
| region       | 1             | semilla_certificada_any     |   0.437371    |      0.518391  |    1        |      1        |
| region       | 1             | semilla_certificada_share   |   0.437371    |      0.439631  |    0.285714 |      1        |
| region       | 1             | capacitacion_recibida       |   0.000121021 |      0.122004  |    0        |      1        |
| region       | 1             | asistencia_tecnica_recibida |   0.000121021 |      0.110022  |    0        |      1        |
| region       | 1             | credito_obtenido            |   0.758199    |      0.944444  |    1        |      1        |
| region       | 1             | nivel_educacion             |   0.0936706   |      5.41755   |    6        |      9        |
| region       | 1             | asociacion_miembro          |   0.000121021 |      0.0876301 |    0        |      0        |
| region       | 1             | asociacion_num              |   0.000121021 |      0.0984023 |    0        |      0        |
| region       | 2             | riego_any                   |   0           |      0.593515  |    1        |      1        |
| region       | 2             | riego_share                 |   0           |      0.4517    |    0.333333 |      1        |
| region       | 2             | riego_tecnificado_any       |   0.406485    |      0.370655  |    0        |      1        |
| region       | 2             | riego_tecnificado_share     |   0.406485    |      0.30998   |    0        |      1        |
| region       | 2             | usuario_agua                |   0.0290763   |      0.455404  |    0        |      1        |
| region       | 2             | gasto_agua_riego            |   4.85413e-05 |     50.9551    |    0        |    100        |
| region       | 2             | uso_maquinaria              |   4.85413e-05 |      0.660922  |    1        |      1        |
| region       | 2             | num_maquinaria_equipo       |   0.33911     |      2.68939   |    1        |      6        |
| region       | 2             | gasto_compra_equipos        |   4.85413e-05 |     47.8061    |    0        |      0        |
| region       | 2             | gasto_compra_maquinaria     |   4.85413e-05 |     50.3641    |    0        |      0        |
| region       | 2             | gasto_alquiler_mant_equipos |   4.85413e-05 |     53.1662    |    0        |     60        |
| region       | 2             | gasto_semilla               |   0.14907     |    959.554     |  390        |   1900        |
| region       | 2             | usa_abono                   |   4.85413e-05 |      0.782816  |    1        |      1        |
| region       | 2             | usa_fertilizantes           |   4.85413e-05 |      0.522282  |    1        |      1        |
| region       | 2             | semilla_semillero_any       |   4.85413e-05 |      0.100777  |    0        |      1        |
| region       | 2             | semilla_comercial_any       |   4.85413e-05 |      0.301117  |    0        |      1        |
| region       | 2             | semilla_certificada_any     |   0.13213     |      0.0299793 |    0        |      0        |
| region       | 2             | semilla_certificada_share   |   0.13213     |      0.0165889 |    0        |      0        |
| region       | 2             | capacitacion_recibida       |   4.85413e-05 |      0.0721845 |    0        |      0        |
| region       | 2             | asistencia_tecnica_recibida |   4.85413e-05 |      0.026699  |    0        |      0        |
| region       | 2             | credito_obtenido            |   0.916023    |      0.936416  |    1        |      1        |
| region       | 2             | nivel_educacion             |   0.00961118  |      4.22624   |    4        |      6        |
| region       | 2             | asociacion_miembro          |   4.85413e-05 |      0.0636893 |    0        |      0        |
| region       | 2             | asociacion_num              |   4.85413e-05 |      0.0658738 |    0        |      0        |
| region       | 3             | riego_any                   |   0           |      0.134904  |    0        |      1        |
| region       | 3             | riego_share                 |   0           |      0.107868  |    0        |      0.612308 |
| region       | 3             | riego_tecnificado_any       |   0.865096    |      0.174678  |    0        |      1        |
| region       | 3             | riego_tecnificado_share     |   0.865096    |      0.14256   |    0        |      1        |
| region       | 3             | usuario_agua                |   0.0392219   |      0.0716049 |    0        |      0        |
| region       | 3             | gasto_agua_riego            |   0.000158153 |    204.696     |    0        |      0        |
| region       | 3             | uso_maquinaria              |   0.000158153 |      0.735685  |    1        |      1        |
| region       | 3             | num_maquinaria_equipo       |   0.264431    |      3.722     |    3        |     10        |
| region       | 3             | gasto_compra_equipos        |   0.000158153 |    439.842     |    0        |    750        |
| region       | 3             | gasto_compra_maquinaria     |   0.000158153 |    987.403     |    0        |      0        |
| region       | 3             | gasto_alquiler_mant_equipos |   0.000158153 |   1392.75      |    0        |    350        |
| region       | 3             | gasto_semilla               |   0.66693     |   3390.62      |  300        |   6422.5      |
| region       | 3             | usa_abono                   |   0           |      0.243872  |    0        |      1        |
| region       | 3             | usa_fertilizantes           |   0           |      0.449312  |    0        |      1        |
| region       | 3             | semilla_semillero_any       |   0           |      0.128262  |    0        |      1        |
| region       | 3             | semilla_comercial_any       |   0           |      0.144235  |    0        |      1        |
| region       | 3             | semilla_certificada_any     |   0.592282    |      0.261443  |    0        |      1        |
| region       | 3             | semilla_certificada_share   |   0.592282    |      0.236992  |    0        |      1        |
| region       | 3             | capacitacion_recibida       |   0.000158153 |      0.148687  |    0        |      1        |
| region       | 3             | asistencia_tecnica_recibida |   0.000158153 |      0.0882632 |    0        |      0        |
| region       | 3             | credito_obtenido            |   0.844061    |      0.901623  |    1        |      1        |
| region       | 3             | nivel_educacion             |   0.0222995   |      4.53672   |    4        |      7        |
| region       | 3             | asociacion_miembro          |   0.000158153 |      0.120531  |    0        |      1        |
| region       | 3             | asociacion_num              |   0.000158153 |      0.12243   |    0        |      1        |
| size         | grande_>5ha   | riego_any                   |   0           |      0.467123  |    0        |      1        |
| size         | grande_>5ha   | riego_share                 |   0           |      0.416134  |    0        |      1        |
| size         | grande_>5ha   | riego_tecnificado_any       |   0.532877    |      0.258431  |    0        |      1        |
| size         | grande_>5ha   | riego_tecnificado_share     |   0.532877    |      0.201002  |    0        |      1        |
| size         | grande_>5ha   | usuario_agua                |   0.0126712   |      0.381374  |    0        |      1        |
| size         | grande_>5ha   | gasto_agua_riego            |   0           |   1348.39      |    0        |   2971        |
| size         | grande_>5ha   | uso_maquinaria              |   0           |      0.839384  |    1        |      1        |
| size         | grande_>5ha   | num_maquinaria_equipo       |   0.160616    |      4.67503   |    3        |     10        |
| size         | grande_>5ha   | gasto_compra_equipos        |   0           |    291.88      |    0        |    800        |
| size         | grande_>5ha   | gasto_compra_maquinaria     |   0           |    415.087     |    0        |      0        |
| size         | grande_>5ha   | gasto_alquiler_mant_equipos |   0           |    555.397     |    0        |    720        |
| size         | grande_>5ha   | gasto_semilla               |   0.393664    |   8493.82      | 2860        |  20590        |
| size         | grande_>5ha   | usa_abono                   |   0           |      0.400856  |    0        |      1        |
| size         | grande_>5ha   | usa_fertilizantes           |   0           |      0.635445  |    1        |      1        |
| size         | grande_>5ha   | semilla_semillero_any       |   0           |      0.200171  |    0        |      1        |
| size         | grande_>5ha   | semilla_comercial_any       |   0           |      0.355137  |    0        |      1        |
| size         | grande_>5ha   | semilla_certificada_any     |   0.352397    |      0.418033  |    0        |      1        |
| size         | grande_>5ha   | semilla_certificada_share   |   0.352397    |      0.346018  |    0        |      1        |
| size         | grande_>5ha   | capacitacion_recibida       |   0           |      0.132021  |    0        |      1        |
| size         | grande_>5ha   | asistencia_tecnica_recibida |   0           |      0.0936644 |    0        |      0        |
| size         | grande_>5ha   | credito_obtenido            |   0.731507    |      0.948342  |    1        |      1        |
| size         | grande_>5ha   | nivel_educacion             |   0           |      5.10788   |    5        |      9        |
| size         | grande_>5ha   | asociacion_miembro          |   0           |      0.12226   |    0        |      1        |
| size         | grande_>5ha   | asociacion_num              |   0           |      0.125685  |    0        |      1        |
| size         | mediano_2_5ha | riego_any                   |   0           |      0.584263  |    1        |      1        |
| size         | mediano_2_5ha | riego_share                 |   0           |      0.496715  |    0.5      |      1        |
| size         | mediano_2_5ha | riego_tecnificado_any       |   0.415737    |      0.308888  |    0        |      1        |
| size         | mediano_2_5ha | riego_tecnificado_share     |   0.415737    |      0.247583  |    0        |      1        |
| size         | mediano_2_5ha | usuario_agua                |   0.0146543   |      0.454413  |    0        |      1        |
| size         | mediano_2_5ha | gasto_agua_riego            |   0           |    393.752     |    0        |    931.6      |
| size         | mediano_2_5ha | uso_maquinaria              |   0           |      0.800733  |    1        |      1        |
| size         | mediano_2_5ha | num_maquinaria_equipo       |   0.199267    |      3.34892   |    3        |      6        |
| size         | mediano_2_5ha | gasto_compra_equipos        |   0           |    122.543     |    0        |      0        |
| size         | mediano_2_5ha | gasto_compra_maquinaria     |   0           |     73.7416    |    0        |      0        |
| size         | mediano_2_5ha | gasto_alquiler_mant_equipos |   0           |    117.817     |    0        |    300        |
| size         | mediano_2_5ha | gasto_semilla               |   0.316661    |   2115.09      | 1040        |   4800        |
| size         | mediano_2_5ha | usa_abono                   |   0           |      0.58028   |    1        |      1        |
| size         | mediano_2_5ha | usa_fertilizantes           |   0           |      0.662631  |    1        |      1        |
| size         | mediano_2_5ha | semilla_semillero_any       |   0           |      0.152596  |    0        |      1        |
| size         | mediano_2_5ha | semilla_comercial_any       |   0           |      0.295954  |    0        |      1        |
| size         | mediano_2_5ha | semilla_certificada_any     |   0.291494    |      0.197392  |    0        |      1        |
| size         | mediano_2_5ha | semilla_certificada_share   |   0.291494    |      0.158674  |    0        |      1        |
| size         | mediano_2_5ha | capacitacion_recibida       |   0           |      0.11596   |    0        |      1        |
| size         | mediano_2_5ha | asistencia_tecnica_recibida |   0           |      0.0672189 |    0        |      0        |
| size         | mediano_2_5ha | credito_obtenido            |   0.811246    |      0.933333  |    1        |      1        |
| size         | mediano_2_5ha | nivel_educacion             |   0           |      4.73622   |    4        |      8        |
| size         | mediano_2_5ha | asociacion_miembro          |   0           |      0.104173  |    0        |      1        |
| size         | mediano_2_5ha | asociacion_num              |   0           |      0.105925  |    0        |      1        |
| size         | missing       | riego_any                   |   0           |      0.868705  |    1        |      1        |
| size         | missing       | riego_share                 |   0           |      0.838909  |    1        |      1        |
| size         | missing       | riego_tecnificado_any       |   0.131295    |      0.624224  |    1        |      1        |
| size         | missing       | riego_tecnificado_share     |   0.131295    |      0.573508  |    1        |      1        |
| size         | missing       | usuario_agua                |   1           |    nan         |  nan        |    nan        |
| size         | missing       | gasto_agua_riego            |   0.00539568  | 301561         | 2800        | 180000        |
| size         | missing       | uso_maquinaria              |   0.00269784  |      0.940487  |    1        |      1        |
| size         | missing       | num_maquinaria_equipo       |   0.0620504   |     16.7824    |    6        |     36        |
| size         | missing       | gasto_compra_equipos        |   0.00539568  |  35100.4       |    0        |  10000        |
| size         | missing       | gasto_compra_maquinaria     |   0.00539568  |  89623.2       |    0        |      0        |
| size         | missing       | gasto_alquiler_mant_equipos |   0.00539568  | 128516         | 1000        | 121071        |
| size         | missing       | gasto_semilla               |   0.667266    | 204083         | 4500        | 232066        |
| size         | missing       | usa_abono                   |   0.000899281 |      0.517552  |    1        |      1        |
| size         | missing       | usa_fertilizantes           |   0.000899281 |      0.825383  |    1        |      1        |
| size         | missing       | semilla_semillero_any       |   0.000899281 |      0.184518  |    0        |      1        |
| size         | missing       | semilla_comercial_any       |   0.000899281 |      0.244824  |    0        |      1        |
| size         | missing       | semilla_certificada_any     |   0.659173    |      0.501319  |    1        |      1        |
| size         | missing       | semilla_certificada_share   |   0.659173    |      0.437668  |    0.1      |      1        |
| size         | missing       | capacitacion_recibida       |   0.00179856  |      0.478378  |    0        |      1        |
| size         | missing       | asistencia_tecnica_recibida |   0.00179856  |      0.357658  |    0        |      1        |
| size         | missing       | credito_obtenido            |   0.693345    |      0.964809  |    1        |      1        |
| size         | missing       | nivel_educacion             |   1           |    nan         |  nan        |    nan        |
| size         | missing       | asociacion_miembro          |   0.00179856  |      0.258559  |    0        |      1        |
| size         | missing       | asociacion_num              |   0.00179856  |      0.333333  |    0        |      1        |
| size         | pequeno_<2ha  | riego_any                   |   0           |      0.621123  |    1        |      1        |
| size         | pequeno_<2ha  | riego_share                 |   0           |      0.517096  |    0.5      |      1        |
| size         | pequeno_<2ha  | riego_tecnificado_any       |   0.378877    |      0.303197  |    0        |      1        |
| size         | pequeno_<2ha  | riego_tecnificado_share     |   0.378877    |      0.256877  |    0        |      1        |
| size         | pequeno_<2ha  | usuario_agua                |   0.0211778   |      0.467011  |    0        |      1        |
| size         | pequeno_<2ha  | gasto_agua_riego            |   4.55436e-05 |    144.484     |    0        |    191        |
| size         | pequeno_<2ha  | uso_maquinaria              |   4.55436e-05 |      0.647477  |    1        |      1        |
| size         | pequeno_<2ha  | num_maquinaria_equipo       |   0.352553    |      2.26182   |    1        |      6        |
| size         | pequeno_<2ha  | gasto_compra_equipos        |   4.55436e-05 |     33.3931    |    0        |      0        |
| size         | pequeno_<2ha  | gasto_compra_maquinaria     |   4.55436e-05 |     18.528     |    0        |      0        |
| size         | pequeno_<2ha  | gasto_alquiler_mant_equipos |   4.55436e-05 |     30.5194    |    0        |     80        |
| size         | pequeno_<2ha  | gasto_semilla               |   0.276859    |    535.768     |  294.5      |   1200        |
| size         | pequeno_<2ha  | usa_abono                   |   4.55436e-05 |      0.674531  |    1        |      1        |
| size         | pequeno_<2ha  | usa_fertilizantes           |   4.55436e-05 |      0.540445  |    1        |      1        |
| size         | pequeno_<2ha  | semilla_semillero_any       |   4.55436e-05 |      0.0899526 |    0        |      0        |
| size         | pequeno_<2ha  | semilla_comercial_any       |   4.55436e-05 |      0.246539  |    0        |      1        |
| size         | pequeno_<2ha  | semilla_certificada_any     |   0.248668    |      0.0588592 |    0        |      0        |
| size         | pequeno_<2ha  | semilla_certificada_share   |   0.248668    |      0.0467418 |    0        |      0        |
| size         | pequeno_<2ha  | capacitacion_recibida       |   4.55436e-05 |      0.0639916 |    0        |      0        |
| size         | pequeno_<2ha  | asistencia_tecnica_recibida |   4.55436e-05 |      0.0296502 |    0        |      0        |
| size         | pequeno_<2ha  | credito_obtenido            |   0.926219    |      0.909877  |    1        |      1        |
| size         | pequeno_<2ha  | nivel_educacion             |   4.55436e-05 |      4.33968   |    4        |      6        |
| size         | pequeno_<2ha  | asociacion_miembro          |   4.55436e-05 |      0.0520587 |    0        |      0        |
| size         | pequeno_<2ha  | asociacion_num              |   4.55436e-05 |      0.0535161 |    0        |      0        |

### Tabla 13. SFA con controles ENA

| model | term | estimate | std_error | z_value | p_value | component | inference_note | n_total | n_valid | share_dropped | gamma | gamma_near_boundary | cov_singular | cov_rank | cov_cond | cov_rcond | input_cost_var | ineffDecrease | truncNorm | timeEffect | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | 
 | controls_ena | (Intercept) |  8.88961932 | 0.050245162 | 176.924880 | 0.000000e+00 | frontier |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | log_land |  0.90192284 | 0.005861943 | 153.860721 | 0.000000e+00 | frontier |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | log_labor |  0.22316323 | 0.007588724 |  29.407215 | 0.000000e+00 | frontier |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | log_inputs | -0.01193091 | 0.006777077 |  -1.760479 | 7.832655e-02 | frontier |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | log_irrigation_cost |  0.07254403 | 0.002653471 |  27.339294 | 0.000000e+00 | frontier |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | log_capital |  0.04080565 | 0.002622328 |  15.560848 | 0.000000e+00 | frontier |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_(Intercept) | -6.90350723 | 0.399877624 | -17.264050 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_diversificacion_area |  0.91670758 | 0.133699894 |   6.856457 | 7.059020e-12 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_size_mediano |  1.13041577 | 0.176237015 |   6.414179 | 1.415839e-10 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_size_grande |  6.12371889 | 0.268576181 |  22.800678 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_diversif_mediano |  0.71785667 | 0.250950146 |   2.860555 | 4.229003e-03 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_diversif_grande | -3.64536812 | 0.252212574 | -14.453554 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_region_natural2 |  5.98311143 | 0.243268368 |  24.594696 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_region_natural3 |  2.12589207 | 0.167157140 |  12.717926 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_nivel_educacion | -0.02592597 | 0.011532055 |  -2.248165 | 2.456564e-02 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_capacitacion_recibida | -0.23538285 | 0.085961758 |  -2.738227 | 6.177133e-03 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_asistencia_tecnica_recibida | -0.81587837 | 0.123937375 |  -6.582989 | 4.610845e-11 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_usuario_agua |  0.51349448 | 0.073681031 |   6.969154 | 3.188561e-12 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_asociacion_miembro |  0.03818231 | 0.085434148 |   0.446921 | 6.549321e-01 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_riego_any | -1.57459886 | 0.089045336 | -17.683114 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_uso_maquinaria |  0.49097620 | 0.057370090 |   8.558052 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_usa_abono | -0.05774677 | 0.054529094 |  -1.059008 | 2.895959e-01 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_usa_fertilizantes | -2.53419504 | 0.099991071 | -25.344213 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_semilla_semillero_any |  0.12357561 | 0.070798833 |   1.745447 | 8.090710e-02 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | Z_semilla_comercial_any |  1.37948121 | 0.066863812 |  20.631208 | 0.000000e+00 | inefficiency |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | sigmaSq |  4.97594424 | 0.191637825 |  25.965355 | 0.000000e+00 | variance |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_ena | gamma |  0.91452002 | 0.003665908 | 249.466142 | 0.000000e+00 | variance |  | 31824 | 26121 | 0.1792044 | 0.91452 | FALSE | FALSE | 27 | 1456479 | 6.865875e-07 | costo_total_agropecuario | TRUE | FALSE | FALSE |


### Tabla 16. Logit con controles ENA

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | controls_ena | (Intercept) | -1.039885577 | 0.47922813 | -2.169917660 | 3.007300e-02 | 0.3534951 |
| controls_ena | diversificacion_area |  0.781186788 | 0.31945556 |  2.445369239 | 1.451413e-02 | 2.1840627 |
| controls_ena | size_catmediano_2_5ha |  0.008855540 | 0.29630225 |  0.029886848 | 9.761588e-01 | 1.0088949 |
| controls_ena | size_catpequeno_<2ha |  0.351688074 | 0.36072920 |  0.974936531 | 3.296519e-01 | 1.4214651 |
| controls_ena | log_area | -0.113752133 | 0.13568650 | -0.838345247 | 4.018880e-01 | 0.8924791 |
| controls_ena | region_natural2 |  1.121043170 | 0.18956654 |  5.913718683 | 3.630480e-09 | 3.0680530 |
| controls_ena | region_natural3 | -0.692261072 | 0.20511333 | -3.375017388 | 7.452902e-04 | 0.5004433 |
| controls_ena | nivel_educacion | -0.014291392 | 0.02941412 | -0.485868419 | 6.270876e-01 | 0.9858102 |
| controls_ena | capacitacion_recibida |  0.749689195 | 0.21463041 |  3.492930991 | 4.830333e-04 | 2.1163421 |
| controls_ena | asistencia_tecnica_recibida |  0.006557223 | 0.32908408 |  0.019925676 | 9.841037e-01 | 1.0065788 |
| controls_ena | usuario_agua |  0.467182143 | 0.16214522 |  2.881257532 | 3.982445e-03 | 1.5954920 |
| controls_ena | asociacion_miembro |  0.000861925 | 0.24712237 |  0.003487847 | 9.972173e-01 | 1.0008623 |
| controls_ena | riego_any |  0.299243343 | 0.16708058 |  1.791012171 | 7.336853e-02 | 1.3488378 |
| controls_ena | uso_maquinaria |  0.504194028 | 0.17342131 |  2.907336124 | 3.665683e-03 | 1.6556506 |
| controls_ena | usa_abono |  1.481706752 | 0.16962639 |  8.735119216 | 3.546472e-18 | 4.4004498 |
| controls_ena | usa_fertilizantes |  0.097907104 | 0.17038865 |  0.574610482 | 5.655878e-01 | 1.1028603 |
| controls_ena | semilla_semillero_any | -0.041546968 | 0.15809884 | -0.262791105 | 7.927254e-01 | 0.9593043 |
| controls_ena | semilla_comercial_any |  0.471542748 | 0.14299258 |  3.297672918 | 9.835961e-04 | 1.6024645 |
| controls_ena | diversificacion_area:size_catmediano_2_5ha |  0.239077548 | 0.43702133 |  0.547061505 | 5.843676e-01 | 1.2700770 |
| controls_ena | diversificacion_area:size_catpequeno_<2ha | -0.073983959 | 0.45799636 | -0.161538313 | 8.716778e-01 | 0.9286866 |


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

| model | term | estimate | std_error | z_value | p_value | component | inference_note | n_total | n_valid | share_dropped | gamma | gamma_near_boundary | cov_singular | cov_rank | cov_cond | cov_rcond | input_cost_var | ineffDecrease | truncNorm | timeEffect | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | 
 | temp_topo | (Intercept) |  7.080488e+00 | 0.070432797 | 100.52828762 | 0.000000e+00 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | log_land |  8.625234e-01 | 0.006357900 | 135.66167862 | 0.000000e+00 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | log_labor |  2.897297e-01 | 0.007900528 |  36.67219124 | 0.000000e+00 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | log_inputs |  4.608420e-02 | 0.006947909 |   6.63281572 | 3.293432e-11 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | log_surface_km2 |  7.662187e-03 | 0.005949867 |   1.28779115 | 1.978187e-01 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | tmean_2024 |  5.397771e-02 | 0.001796626 |  30.04392813 | 0.000000e+00 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | delta_tmean_24_23 | -3.995008e-01 | 0.015034171 | -26.57285415 | 0.000000e+00 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | slope_deg |  1.557744e-02 | 0.005440959 |   2.86299521 | 4.196569e-03 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | ruggedness | -7.494287e-03 | 0.003901240 |  -1.92100130 | 5.473154e-02 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | prcp_total_z | -6.543668e-03 | 0.008663238 |  -0.75533753 | 4.500465e-01 | frontier |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | Z_(Intercept) | -3.569833e+01 | 3.746103425 |  -9.52945536 | 0.000000e+00 | inefficiency |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | Z_diversificacion_area |  2.734332e-01 | 0.246436363 |   1.10954887 | 2.671935e-01 | inefficiency |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | Z_size_mediano |  4.099557e+00 | 0.763052003 |   5.37257940 | 7.761823e-08 | inefficiency |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | Z_size_grande |  1.750091e+01 | 1.648821885 |  10.61418969 | 0.000000e+00 | inefficiency |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | Z_diversif_mediano |  2.531471e+00 | 0.341521810 |   7.41232614 | 1.241229e-13 | inefficiency |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | Z_diversif_grande | -7.969953e+00 | 0.845918959 |  -9.42165082 | 0.000000e+00 | inefficiency |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | Z_region_natural2 |  2.112972e+01 | 2.038165752 |  10.36702885 | 0.000000e+00 | inefficiency |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | Z_region_natural3 |  1.471645e+01 | 1.613400013 |   9.12138911 | 0.000000e+00 | inefficiency |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | sigmaSq |  1.634529e+01 | 1.534150169 |  10.65429434 | 0.000000e+00 | variance |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| temp_topo | gamma |  9.698759e-01 | 0.002757124 | 351.77088140 | 0.000000e+00 | variance |  | 31792 | 26546 | 0.1650101 | 0.9698759 | FALSE | FALSE | 20 | 658239108 | 1.519205e-09 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | (Intercept) |  7.659935e+00 | 0.071009203 | 107.87243264 | 0.000000e+00 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | log_land |  8.635287e-01 | 0.006683444 | 129.20415036 | 0.000000e+00 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | log_labor |  2.535185e-01 | 0.007717720 |  32.84888307 | 0.000000e+00 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | log_inputs | -1.763810e-02 | 0.006982063 |  -2.52620134 | 1.153034e-02 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | log_surface_km2 |  2.503843e-02 | 0.005573287 |   4.49257911 | 7.036577e-06 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | tmean_2024 |  4.343187e-02 | 0.001767748 |  24.56904269 | 0.000000e+00 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | delta_tmean_24_23 | -2.575045e-01 | 0.015059312 | -17.09935413 | 0.000000e+00 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | slope_deg |  9.091418e-03 | 0.005197589 |   1.74916042 | 8.026329e-02 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | ruggedness |  8.464979e-05 | 0.003779286 |   0.02239836 | 9.821302e-01 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | prcp_total_z |  4.533240e-03 | 0.008028376 |   0.56465219 | 5.723104e-01 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | log_irrigation_cost |  6.961558e-02 | 0.002792168 |  24.93244310 | 0.000000e+00 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | log_capital |  3.141270e-02 | 0.002522056 |  12.45519573 | 0.000000e+00 | frontier |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_(Intercept) | -8.493161e+00 | 0.608314178 | -13.96180042 | 0.000000e+00 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_diversificacion_area |  1.831940e-02 | 0.135322843 |   0.13537554 | 8.923150e-01 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_size_mediano |  1.115330e+00 | 0.168070396 |   6.63608661 | 3.221201e-11 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_size_grande |  7.537475e+00 | 0.364797792 |  20.66206181 | 0.000000e+00 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_diversif_mediano |  1.961124e+00 | 0.265404237 |   7.38919650 | 1.476597e-13 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_diversif_grande | -3.585455e+00 | 0.291684236 | -12.29224884 | 0.000000e+00 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_region_natural2 |  6.052384e+00 | 0.371088608 |  16.30980944 | 0.000000e+00 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_region_natural3 |  1.981968e+00 | 0.254420432 |   7.79012953 | 6.661338e-15 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_nivel_educacion | -4.145724e-02 | 0.018379322 |  -2.25564551 | 2.409284e-02 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_capacitacion_recibida | -3.399026e-01 | 0.102476488 |  -3.31688390 | 9.102743e-04 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_asistencia_tecnica_recibida | -1.134940e+00 | 0.140434493 |  -8.08163083 | 6.661338e-16 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_usuario_agua |  7.422440e-01 | 0.082776971 |   8.96679369 | 0.000000e+00 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_asociacion_miembro |  1.239295e-02 | 0.104859196 |   0.11818661 | 9.059198e-01 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_riego_any | -2.153776e+00 | 0.107224463 | -20.08661464 | 0.000000e+00 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_uso_maquinaria |  4.601973e-01 | 0.057918164 |   7.94564744 | 1.998401e-15 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_usa_abono | -3.744650e-01 | 0.058774620 |  -6.37120267 | 1.875515e-10 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_usa_fertilizantes | -3.736008e+00 | 0.171788120 | -21.74776959 | 0.000000e+00 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_semilla_semillero_any |  1.640101e-01 | 0.073209868 |   2.24027348 | 2.507317e-02 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | Z_semilla_comercial_any |  1.945327e+00 | 0.093670993 |  20.76765502 | 0.000000e+00 | inefficiency |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | sigmaSq |  7.095727e+00 | 0.317563944 |  22.34424587 | 0.000000e+00 | variance |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |
| controls_temp_topo | gamma |  9.383766e-01 | 0.002806385 | 334.37195285 | 0.000000e+00 | variance |  | 31792 | 26073 | 0.1798880 | 0.9383766 | FALSE | FALSE | 33 |  29214266 | 3.422985e-08 | costo_total_agropecuario | TRUE | FALSE | FALSE |


### Tabla 17. Logit con temperatura/topografia

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | temp_topo | (Intercept) |  4.1257201926 | 0.9814590575 |  4.20366001 | 2.684421e-05 | 61.9123820 |
| temp_topo | diversificacion_area |  1.2665810737 | 0.3862531738 |  3.27914736 | 1.050229e-03 |  3.5486991 |
| temp_topo | size_catmediano_2_5ha |  0.2816251932 | 0.3171857565 |  0.88788726 | 3.746554e-01 |  1.3252819 |
| temp_topo | size_catpequeno_<2ha |  0.6350395566 | 0.3887249953 |  1.63364735 | 1.024126e-01 |  1.8870968 |
| temp_topo | log_area |  0.1986698008 | 0.1449493832 |  1.37061501 | 1.705728e-01 |  1.2197791 |
| temp_topo | region_natural2 |  0.8145410459 | 0.2969463011 |  2.74305840 | 6.114427e-03 |  2.2581391 |
| temp_topo | region_natural3 | -0.3958384670 | 0.2098865829 | -1.88596366 | 5.937310e-02 |  0.6731154 |
| temp_topo | tmean_2024 | -0.1823545968 | 0.0397632970 | -4.58600294 | 4.657967e-06 |  0.8333058 |
| temp_topo | delta_tmean_24_23 | -0.0661322208 | 0.1365083767 | -0.48445540 | 6.280895e-01 |  0.9360071 |
| temp_topo | elev_m | -0.0003512511 | 0.0001793542 | -1.95842176 | 5.025077e-02 |  0.9996488 |
| temp_topo | slope_deg |  0.1263770594 | 0.0564450240 |  2.23894066 | 2.521520e-02 |  1.1347099 |
| temp_topo | ruggedness | -0.1142868121 | 0.0387131359 | -2.95214556 | 3.174308e-03 |  0.8920021 |
| temp_topo | prcp_total_z |  0.4889854925 | 0.0817228215 |  5.98346317 | 2.378300e-09 |  1.6306611 |
| temp_topo | diversificacion_area:size_catmediano_2_5ha |  0.2589707978 | 0.4616683966 |  0.56094547 | 5.748665e-01 |  1.2955960 |
| temp_topo | diversificacion_area:size_catpequeno_<2ha |  0.0953936414 | 0.4667392401 |  0.20438316 | 8.380646e-01 |  1.1000918 |
| controls_temp_topo | (Intercept) |  0.5998357070 | 1.1786568453 |  0.50891463 | 6.108408e-01 |  1.8218195 |
| controls_temp_topo | diversificacion_area |  0.7910089964 | 0.3582162589 |  2.20818842 | 2.728901e-02 |  2.2056208 |
| controls_temp_topo | size_catmediano_2_5ha |  0.0455111628 | 0.3084943353 |  0.14752674 | 8.827239e-01 |  1.0465627 |
| controls_temp_topo | size_catpequeno_<2ha |  0.4497899769 | 0.3635729502 |  1.23713818 | 2.161101e-01 |  1.5679828 |
| controls_temp_topo | log_area | -0.0127362013 | 0.1335226050 | -0.09538611 | 9.240130e-01 |  0.9873446 |
| controls_temp_topo | region_natural2 |  0.9425532736 | 0.2983086572 |  3.15965779 | 1.591609e-03 |  2.5665261 |
| controls_temp_topo | region_natural3 | -0.3624551088 | 0.2603261475 | -1.39231158 | 1.639073e-01 |  0.6959656 |
| controls_temp_topo | tmean_2024 | -0.0709091281 | 0.0460223058 | -1.54075566 | 1.234572e-01 |  0.9315465 |
| controls_temp_topo | delta_tmean_24_23 | -0.1434396929 | 0.1371529362 | -1.04583757 | 2.957007e-01 |  0.8663730 |
| controls_temp_topo | elev_m | -0.0001122828 | 0.0001992130 | -0.56363216 | 5.730368e-01 |  0.9998877 |
| controls_temp_topo | slope_deg |  0.0578248715 | 0.0548459386 |  1.05431456 | 2.918041e-01 |  1.0595294 |
| controls_temp_topo | ruggedness | -0.0507654191 | 0.0371425003 | -1.36677441 | 1.717747e-01 |  0.9505016 |
| controls_temp_topo | prcp_total_z |  0.2698078634 | 0.0738199186 |  3.65494664 | 2.606171e-04 |  1.3097128 |
| controls_temp_topo | nivel_educacion | -0.0192769808 | 0.0309510258 | -0.62282203 | 5.334378e-01 |  0.9809076 |
| controls_temp_topo | capacitacion_recibida |  0.7183133435 | 0.2227923847 |  3.22413777 | 1.273924e-03 |  2.0509710 |
| controls_temp_topo | asistencia_tecnica_recibida | -0.0457107867 | 0.3337410570 | -0.13696483 | 8.910657e-01 |  0.9553182 |
| controls_temp_topo | usuario_agua |  0.3965601337 | 0.1574538494 |  2.51858011 | 1.182253e-02 |  1.4867018 |
| controls_temp_topo | asociacion_miembro |  0.0390626036 | 0.2483395731 |  0.15729512 | 8.750204e-01 |  1.0398356 |
| controls_temp_topo | riego_any |  0.2451146492 | 0.1667702593 |  1.46977435 | 1.417034e-01 |  1.2777678 |
| controls_temp_topo | uso_maquinaria |  0.4705954019 | 0.1699094243 |  2.76968393 | 5.637572e-03 |  1.6009471 |
| controls_temp_topo | usa_abono |  1.3224571744 | 0.1640833214 |  8.05966849 | 1.007402e-15 |  3.7526309 |
| controls_temp_topo | usa_fertilizantes |  0.1206975281 | 0.1606777961 |  0.75117739 | 4.525911e-01 |  1.1282836 |
| controls_temp_topo | semilla_semillero_any |  0.0119060514 | 0.1547987535 |  0.07691310 | 9.386966e-01 |  1.0119772 |
| controls_temp_topo | semilla_comercial_any |  0.4427833069 | 0.1476680838 |  2.99850378 | 2.730184e-03 |  1.5570349 |
| controls_temp_topo | diversificacion_area:size_catmediano_2_5ha |  0.2752944681 | 0.4576928021 |  0.60148306 | 5.475532e-01 |  1.3169184 |
| controls_temp_topo | diversificacion_area:size_catpequeno_<2ha | -0.0613191433 | 0.4475434725 | -0.13701271 | 8.910278e-01 |  0.9405230 |


## Comparaciones de robustez (controles + geo/clima)

Se comparan los coeficientes de diversificacion e interacciones en las especificaciones baseline, con controles ENA y con temperatura/topografia.

### Tabla 15. Comparacion efectos SFA

| model | term | estimate | std_error | p_value | 
| --- | --- | --- | --- | --- | 
 | main_area | Z_diversificacion_area |  1.9293785 | 0.2007915 | 0.000000e+00 |
| main_area | Z_diversif_mediano | -0.1995218 | 0.2429158 | 4.114401e-01 |
| main_area | Z_diversif_grande | -5.5425393 | 0.2892420 | 0.000000e+00 |
| controls_ena | Z_diversificacion_area |  0.9167076 | 0.1336999 | 7.059020e-12 |
| controls_ena | Z_diversif_mediano |  0.7178567 | 0.2509501 | 4.229003e-03 |
| controls_ena | Z_diversif_grande | -3.6453681 | 0.2522126 | 0.000000e+00 |
| temp_topo | Z_diversificacion_area |  0.2734332 | 0.2464364 | 2.671935e-01 |
| temp_topo | Z_diversif_mediano |  2.5314710 | 0.3415218 | 1.241229e-13 |
| temp_topo | Z_diversif_grande | -7.9699531 | 0.8459190 | 0.000000e+00 |
| controls_temp_topo | Z_diversificacion_area |  0.0183194 | 0.1353228 | 8.923150e-01 |
| controls_temp_topo | Z_diversif_mediano |  1.9611241 | 0.2654042 | 1.476597e-13 |
| controls_temp_topo | Z_diversif_grande | -3.5854552 | 0.2916842 | 0.000000e+00 |


### Tabla 18. Comparacion efectos logit

| model | term | estimate | std_error | z_value | p_value | odds_ratio | 
| --- | --- | --- | --- | --- | --- | --- | 
 | main | diversificacion_area |  1.38189755 | 0.3352644 |  4.1218136 | 3.835921e-05 | 3.9824514 |
| main | diversificacion_area:size_catmediano_2_5ha |  0.10661860 | 0.4350723 |  0.2450595 | 8.064231e-01 | 1.1125099 |
| main | diversificacion_area:size_catpequeno_<2ha |  0.11684548 | 0.4562331 |  0.2561092 | 7.978798e-01 | 1.1239457 |
| controls_ena | diversificacion_area |  0.78118679 | 0.3194556 |  2.4453692 | 1.451413e-02 | 2.1840627 |
| controls_ena | diversificacion_area:size_catmediano_2_5ha |  0.23907755 | 0.4370213 |  0.5470615 | 5.843676e-01 | 1.2700770 |
| controls_ena | diversificacion_area:size_catpequeno_<2ha | -0.07398396 | 0.4579964 | -0.1615383 | 8.716778e-01 | 0.9286866 |
| temp_topo | diversificacion_area |  1.26658107 | 0.3862532 |  3.2791474 | 1.050229e-03 | 3.5486991 |
| temp_topo | diversificacion_area:size_catmediano_2_5ha |  0.25897080 | 0.4616684 |  0.5609455 | 5.748665e-01 | 1.2955960 |
| temp_topo | diversificacion_area:size_catpequeno_<2ha |  0.09539364 | 0.4667392 |  0.2043832 | 8.380646e-01 | 1.1000918 |
| controls_temp_topo | diversificacion_area |  0.79100900 | 0.3582163 |  2.2081884 | 2.728901e-02 | 2.2056208 |
| controls_temp_topo | diversificacion_area:size_catmediano_2_5ha |  0.27529447 | 0.4576928 |  0.6014831 | 5.475532e-01 | 1.3169184 |
| controls_temp_topo | diversificacion_area:size_catpequeno_<2ha | -0.06131914 | 0.4475435 | -0.1370127 | 8.910278e-01 | 0.9405230 |


### Analisis de perdida muestral

| sample_type   | group_type   | group         |   n_base |   n_geo2 |   share_remaining |      weight_base |      weight_geo2 |
|:--------------|:-------------|:--------------|---------:|---------:|------------------:|-----------------:|-----------------:|
| logit         | overall      | overall       |    34074 |    34039 |          0.998973 |      2.11889e+06 |      2.11703e+06 |
| logit         | region       | 1             |     7489 |     7489 |          1        | 261014           | 261014           |
| logit         | region       | 2             |    20403 |    20380 |          0.998873 |      1.54006e+06 |      1.539e+06   |
| logit         | region       | 3             |     6182 |     6170 |          0.998059 | 317816           | 317015           |
| logit         | size         | pequeno_<2ha  |    21956 |    21932 |          0.998907 |      1.53022e+06 |      1.52888e+06 |
| logit         | size         | mediano_2_5ha |     6278 |     6270 |          0.998726 | 355684           | 355235           |
| logit         | size         | grande_>5ha   |     5840 |     5837 |          0.999486 | 232992           | 232920           |
| sfa           | overall      | overall       |    26594 |    26546 |          0.998195 |    nan           |    nan           |
| sfa           | region       | 1             |     6470 |     6470 |          1        |    nan           |    nan           |
| sfa           | region       | 2             |    14805 |    14782 |          0.998446 |    nan           |    nan           |
| sfa           | region       | 3             |     5319 |     5294 |          0.9953   |    nan           |    nan           |
| sfa           | size         | pequeno_<2ha  |    16015 |    15990 |          0.998439 |    nan           |    nan           |
| sfa           | size         | mediano_2_5ha |     5512 |     5498 |          0.99746  |    nan           |    nan           |
| sfa           | size         | grande_>5ha   |     5067 |     5058 |          0.998224 |    nan           |    nan           |

## Definiciones de variables

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

## Limitaciones

- SFA no usa pesos por limitaciones del paquete.

- Algunas variables presentan faltantes; ver docs/DATA_GAPS.md.
