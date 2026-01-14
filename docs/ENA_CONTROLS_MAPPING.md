# ENA 2024: Mapping de controles adicionales

Fuente principal: `DICCIONARIO DE DATOS ENA-2024.pdf` y modulos en `data/raw/ENA_2024/`.

## Variables base (raw -> estandar)

| raw_name | standardized_name | definicion | unidad | limpieza / reglas |
|---|---|---|---|---|
| P212 | water_source | Fuente de agua para riego del cultivo (1 lluvia/secano, 2 rio, 3 manantial, 4 pozo, 5 reservorio, 6 pequeno reservorio, 7 otro). | codigo | Mantener codigo; para riego usar P212 != 1 como irrigado. |
| P213 | irrigation_system | Sistema de riego usado (1 exudacion, 2 goteo, 3 microaspersion, 4 aspersion, 5 multicompuertas, 6 mangas, 7 gravedad, 8 otro). | codigo | Tecnificado: codigos 1-6. |
| P214 | seed_certified | Semilla certificada (1 si, 2 no). | dummy | Convertir a 1/0; NA se deja para agregacion. |
| P810 | usuario_agua | Usuario de agua o miembro de comite. | dummy | 1 si -> 1; resto -> 0 (imputacion explicita). |
| P1001A_3 | gasto_agua_riego | Gasto en agua de riego para cultivos. | S/ | Convertir a numerico; NA -> 0. |
| P1206 | uso_maquinaria | Uso de maquinaria/equipo en ultimos 12 meses. | dummy | 1 si -> 1; 2 no -> 0; NA -> 0. |
| P1207_N | num_maquinaria_equipo | Numero de maquinaria/equipo reportado. | conteo | Convertir a numerico; sumar por UA; NA -> 0. |
| P1001A_5A | gasto_compra_equipos | Compra de equipos agricolas. | S/ | Convertir a numerico; NA -> 0. |
| P1001A_5B | gasto_compra_maquinaria | Compra de maquinaria agricola. | S/ | Convertir a numerico; NA -> 0. |
| P1001A_6A | gasto_alquiler_mant_equipos | Alquiler/mantenimiento de equipos agricolas. | S/ | Convertir a numerico; NA -> 0. |
| P235_VAL | gasto_semilla | Gasto en semilla. | S/ | Convertir a numerico; sumar por UA; NA -> 0. |
| P235A_4 | semilla_semillero | Semilla comprada a semilleros. | dummy | 1 -> 1; 0 -> 0; NA -> 0. |
| P235A_9 | semilla_comercial | Semilla comprada en establecimientos comerciales. | dummy | 1 -> 1; 0 -> 0; NA -> 0. |
| P236 | usa_abono | Uso de abono (1 si, 2 no). | dummy | 1 -> 1; 2 -> 0; NA -> 0. |
| P238 | usa_fertilizantes | Uso de fertilizantes (1 si, 2 no). | dummy | 1 -> 1; 2 -> 0; NA -> 0. |
| P701 | capacitacion_recibida | Recibio capacitacion (ultimos 3 anos). | dummy | 1 -> 1; 2 -> 0; NA -> 0. |
| P704 | asistencia_tecnica_recibida | Recibio asistencia tecnica (ultimos 3 anos). | dummy | 1 -> 1; 2 -> 0; NA -> 0. |
| P902 | credito_obtenido | Obtuvo credito solicitado (1 si, 2 no). | dummy | 1 -> 1; 2 -> 0; NA -> 0. |
| P1105 | nivel_educacion | Nivel de educacion alcanzado. | codigo | Numerico; NA -> mediana (imputacion). |
| P801 | asociacion_miembro | Pertenece a asociacion/cooperativa/comite. | dummy | 1 -> 1; 2 -> 0; NA -> 0. |
| P801_1 | asociacion_num | Numero de asociaciones. | conteo | Numerico; NA -> 0. |

## Variables derivadas (features finales)

| feature | definicion | construccion |
|---|---|---|
| riego_any | Indicador de riego en al menos un cultivo. | max(P212 != 1) por UA. |
| riego_share | Proporcion de cultivos con riego. | mean(P212 != 1) por UA. |
| riego_tecnificado_any | Indicador de riego tecnificado en al menos un cultivo. | max(P213 in {1..6}) por UA. |
| riego_tecnificado_share | Proporcion de cultivos con riego tecnificado. | mean(P213 in {1..6}) por UA. |
| semilla_certificada_any | Indicador de uso de semilla certificada. | max(P214 == 1) por UA (NA -> 0). |
| semilla_certificada_share | Proporcion de cultivos con semilla certificada. | mean(P214 == 1) por UA (NA ignorado, luego NA -> 0). |
| semilla_semillero_any | Indicador de semilla de semillero en algun cultivo. | max(P235A_4) por UA. |
| semilla_comercial_any | Indicador de semilla comercial en algun cultivo. | max(P235A_9) por UA. |
