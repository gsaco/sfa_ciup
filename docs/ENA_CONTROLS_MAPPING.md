# ENA 2024: Mapping de controles adicionales

Fuente principal: `DICCIONARIO DE DATOS ENA-2024.pdf` y modulos en `data/raw/ENA_2024/`.

## Regla general de missingness (actual)
- **Missing ≠ 0**: los NA se mantienen como NA salvo que exista un indicador explícito de “no” que implique cero.
- **Dummies sí/no**: mapeo estandarizado `1 → 1`, `2/0 → 0`, otros códigos → NA.
- **Indicadores de missing**: se crean columnas `*_missing` para dummies y conteos clave.
- **Sumas por UA**: usan `min_count=1` (todo missing → NA).

## Variables base (raw -> estandar)

| raw_name | standardized_name | definicion | unidad | limpieza / reglas |
|---|---|---|---|---|
| P212 | water_source | Fuente de agua para riego del cultivo (1 lluvia/secano, 2 rio, 3 manantial, 4 pozo, 5 reservorio, 6 pequeno reservorio, 7 otro). | codigo | Mantener codigo; para riego usar P212 != 1 como irrigado. |
| P213 | irrigation_system | Sistema de riego usado (1 exudacion, 2 goteo, 3 microaspersion, 4 aspersion, 5 multicompuertas, 6 mangas, 7 gravedad, 8 otro). | codigo | Tecnificado: codigos 1-6. |
| P214 | seed_certified | Semilla certificada (1 si, 2 no). | dummy | `1→1`, `2→0`, otros → NA. |
| P810 | usuario_agua | Usuario de agua o miembro de comite. | dummy | `1→1`, `2/0→0`, otros → NA; se crea `usuario_agua_missing`. |
| P1001A_3 | gasto_agua_riego | Gasto en agua de riego para cultivos. | S/ | Numerico; solo se rellena con 0 si `usuario_agua == 0`. |
| P1206 | uso_maquinaria | Uso de maquinaria/equipo en ultimos 12 meses. | dummy | `1→1`, `2/0→0`, otros → NA; `uso_maquinaria_missing`. |
| P1207_N | num_maquinaria_equipo | Numero de maquinaria/equipo reportado. | conteo | Numerico; suma por UA con `min_count=1` (todo missing → NA). |
| P1001A_5A | gasto_compra_equipos | Compra de equipos agricolas. | S/ | Numerico; cero solo si `uso_maquinaria == 0`. |
| P1001A_5B | gasto_compra_maquinaria | Compra de maquinaria agricola. | S/ | Numerico; cero solo si `uso_maquinaria == 0`. |
| P1001A_6A | gasto_alquiler_mant_equipos | Alquiler/mantenimiento de equipos agricolas. | S/ | Numerico; cero solo si `uso_maquinaria == 0`. |
| P235_VAL | gasto_semilla | Gasto en semilla. | S/ | Numerico; suma por UA con `min_count=1`. |
| P235A_4 | semilla_semillero | Semilla comprada a semilleros. | dummy | `1→1`, `2/0→0`, otros → NA. |
| P235A_9 | semilla_comercial | Semilla comprada en establecimientos comerciales. | dummy | `1→1`, `2/0→0`, otros → NA. |
| P236 | usa_abono | Uso de abono (1 si, 2 no). | dummy | `1→1`, `2/0→0`, otros → NA. |
| P238 | usa_fertilizantes | Uso de fertilizantes (1 si, 2 no). | dummy | `1→1`, `2/0→0`, otros → NA. |
| P701 | capacitacion_recibida | Recibio capacitacion (ultimos 3 anos). | dummy | `1→1`, `2/0→0`, otros → NA. |
| P704 | asistencia_tecnica_recibida | Recibio asistencia tecnica (ultimos 3 anos). | dummy | `1→1`, `2/0→0`, otros → NA. |
| P902 | credito_obtenido | Obtuvo credito solicitado (1 si, 2 no). | dummy | `1→1`, `2/0→0`, otros → NA. |
| P1105 | nivel_educacion | Nivel de educacion alcanzado. | codigo | Numerico; NA → mediana (imputacion explicita). |
| P801 | asociacion_miembro | Pertenece a asociacion/cooperativa/comite. | dummy | `1→1`, `2/0→0`, otros → NA. |
| P801_1 | asociacion_num | Numero de asociaciones. | conteo | Numerico; cero solo si `asociacion_miembro == 0`. |

## Variables derivadas (features finales)

| feature | definicion | construccion |
|---|---|---|
| riego_any | Indicador de riego en al menos un cultivo. | `max(riego_crop)` por UA; si todos NA → NA. |
| riego_share | Proporcion de cultivos con riego. | `mean(riego_crop)` por UA (ignora NA; todo NA → NA). |
| riego_tecnificado_any | Indicador de riego tecnificado en al menos un cultivo. | `max(riego_tecnificado_crop)` por UA; todo NA → NA. |
| riego_tecnificado_share | Proporcion de cultivos con riego tecnificado. | `mean(riego_tecnificado_crop)` por UA (NA ignorado; todo NA → NA). |
| semilla_certificada_any | Indicador de uso de semilla certificada. | `max(semilla_certificada_crop)` por UA (NA ignorado; todo NA → NA). |
| semilla_certificada_share | Proporcion de cultivos con semilla certificada. | `mean(semilla_certificada_crop)` por UA (todo NA → NA). |
| semilla_semillero_any | Indicador de semilla de semillero en algun cultivo. | `max(semilla_semillero)` por UA (NA ignorado; todo NA → NA). |
| semilla_comercial_any | Indicador de semilla comercial en algun cultivo. | `max(semilla_comercial)` por UA (NA ignorado; todo NA → NA). |

## Controles usados en modelos (actual)
- **Incluidos (alta completitud)**: `nivel_educacion`, `capacitacion_recibida`, `asistencia_tecnica_recibida`, `usuario_agua`, `asociacion_miembro`, `riego_any`, `uso_maquinaria`, `usa_abono`, `usa_fertilizantes`, `semilla_semillero_any`, `semilla_comercial_any`.
- **Excluidos del main por alta missingness**: `credito_obtenido`, `riego_tecnificado_any/share`, `gasto_semilla`, `semilla_certificada_*`, `num_maquinaria_equipo`. Se mantienen para robustez o como descriptivos.
