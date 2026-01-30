# Viabilidad economica y de datos: controles ENA, temperatura y topografia

Este analisis se basa en el diccionario ENA 2024 (`data/intermediate/ena2024_dictionary.csv`) y la estructura de modulos en `data/raw/ENA_2024/`.

## A) Controles ENA (potenciales omitidos)

### Riego y acceso/uso de agua
- Existe en ENA: 
  - Fuente y sistema de riego a nivel parcela/uso de tierra: `P120`, `P121` en `data/raw/ENA_2024/973-Modulo1893/01_CAP100A_04.csv` (y `USOSTIERRA.csv`).
  - Fuente y sistema de riego a nivel cultivo: `P212`, `P213` en `data/raw/ENA_2024/973-Modulo1895/03_CAP200AB.csv`.
  - Semilla usada por cultivo (posible proxy de tecnologia): `P214` en `03_CAP200AB.csv`.
  - Usuario de agua / comite: `P810` en `data/raw/ENA_2024/973-Modulo1908/16_CAP800.csv`.
  - Gasto en agua de riego: `P1001A_3` en `data/raw/ENA_2024/973-Modulo1910/18_CAP1000.csv`.
  - Institucion que instalo riego tecnificado: `P141_*` en `data/raw/ENA_2024/973-Modulo1893/01_CAP100A_03.csv`.
- Tipo de variable: categorial (fuente/sistema), dummy (usuario de agua), gasto (S/).
- Endogeneidad: el uso de riego y gasto en agua es un input productivo (potencialmente endogeno). La afiliacion a comite de usuarios (P810) es mas institucional y puede ser mas exogena.
- Ubicacion recomendada:
  - SFA: variables de riego como condicion ambiental/infraestructura en `X` (frontera) o como tecnologia en `Z` (ineficiencia). Preferencia: P810 en `Z` (capacidad institucional) y un indicador de sistema de riego tecnificado en `X`.
  - Logit de practicas: evitar usar practicas incluidas en el outcome (P301A_1-4C, P301A_11, P301A_16, P301A_17). Usar P810 o gasto en agua como control exogeno; no usar “manejo de riego” como control.
- Signo esperado: riego tecnificado y acceso a agua -> mayor productividad (coef positivo en `X`) y menor ineficiencia (coef negativo en `Z`).

### Capital/maquinaria/equipos
- Existe en ENA:
  - Uso de maquinaria/equipo: `P1206` en `18_CAP1000.csv`.
  - Numero y tipo de maquinaria/equipo: `P1207_N`, `P1207_TIPO` en `data/raw/ENA_2024/973-Modulo1913/21_CAP1200B_ME.csv`.
  - Gastos en compra/alquiler/mantenimiento: `P1001A_5A`, `P1001A_5B`, `P1001A_6A` en `18_CAP1000.csv`.
- Tipo de variable: dummy (uso), conteo (numero de equipos), gasto (S/), categorial (tipo).
- Endogeneidad: capital fijo es cuasi-predeterminado pero correlacionado con productividad (seleccion). Riesgo de endogeneidad moderado.
- Ubicacion recomendada:
  - SFA: tratar como input de capital en `X` (preferido). Robustez alternativa: incluir en `Z` como proxy de tecnologia.
  - Logit: puede usarse como control de capacidad productiva; evitar si se interpreta como mediador directo de practicas.
- Signo esperado: mas capital/maquinaria -> mayor frontera productiva y menor ineficiencia.

### Fertilizacion e insumos (incluye plaguicidas)
- Existe en ENA (modulo cultivo): `P236` (uso de abono), `P237_VAL` (gasto en abono), `P238` (uso de fertilizantes), `P239` (gasto), `P241` (gasto en plaguicidas) en `data/raw/ENA_2024/973-Modulo1899/07_CAP200E.csv`.
- Tipo de variable: dummies de uso y gastos (S/). Nota: estas variables son por cultivo y requieren agregacion a nivel productor/UA.
- Endogeneidad: son inputs directos de produccion; alta endogeneidad.
- Ubicacion recomendada:
  - SFA: solo en `X` (frontera) como insumos, nunca en `Z`.
  - Logit: evitar como controles cuando el outcome incluye practicas relacionadas (P301A_13-15), por “bad control”.
- Signo esperado: positivo en frontera; no se interpreta en `Z`.

### Semillas mejoradas (o proxies)
- Existe en ENA:
  - Tipo de semilla usada por cultivo: `P122` (CAP100A_04) y `P214` (CAP200AB). Categorial.
  - Origen de la semilla: `P235A_1` a `P235A_10` en `07_CAP200E.csv` (p.ej., semilleros, viveros, establecimientos comerciales).
  - Gasto en semilla: `P235_VAL` en `07_CAP200E.csv`.
- Tipo de variable: categorial/dummy, gasto.
- Endogeneidad: eleccion de semilla es tecnologia/input; endogena.
- Ubicacion recomendada:
  - SFA: incluir en `X` como insumo/tecnologia (p.ej., dummy de semilla certificada/semillero si el codigo lo permite). Alternativa de robustez en `Z`.
  - Logit: cuidado si la semilla es parte de la practica de manejo; usar solo proxies de acceso (p.ej., semillero) como control si no esta en el outcome.
- Signo esperado: semilla mejorada -> mayor frontera y menor ineficiencia.

### Asistencia tecnica / extension / capacitacion
- Existe en ENA: `P701` (capacitacion), `P704` (asistencia tecnica) en `data/raw/ENA_2024/973-Modulo1907/15_CAP700.csv`. Temas especificos en `P702_*` y `P705_*`.
- Tipo de variable: dummy (recibio), dummies por tema.
- Endogeneidad: potencial seleccion (programas focalizados), pero es razonable como control institucional.
- Ubicacion recomendada:
  - SFA: `Z` (ineficiencia) por su rol en capacidades/management.
  - Logit: control clave, no es “bad control” (es determinante de adopcion).
- Signo esperado: reduce ineficiencia, aumenta adopcion de practicas.

### Acceso a credito
- Existe en ENA: `P901` (solicito), `P902` (obtuvo), `P903_*` (fuente), `P904_*` (uso) en `data/raw/ENA_2024/973-Modulo1909/17_CAP900.csv`.
- Tipo de variable: dummy y dummies por fuente/uso.
- Endogeneidad: credito responde a necesidades/inversion, pero es razonable como control socioeconomico.
- Ubicacion recomendada:
  - SFA: `Z` (capacidad financiera). Evitar `P904_*` como controles si reflejan inputs directos.
  - Logit: control valido (financiamiento para adoptar practicas), evitar uso especifico de insumos como control.
- Signo esperado: mayor acceso a credito -> menor ineficiencia y mayor adopcion.

### Educacion del productor/a
- Existe en ENA: `P1105` (nivel educativo) en `data/raw/ENA_2024/973-Modulo1911/19_CAP1100.csv`.
- Tipo de variable: ordinal.
- Endogeneidad: relativamente exogena.
- Ubicacion recomendada:
  - SFA: `Z` (capital humano).
  - Logit: control basico.
- Signo esperado: mas educacion -> menor ineficiencia y mayor adopcion.

### Otros socioeconomicos razonables
- Existe en ENA:
  - Pertenencia a asociacion/cooperativa: `P801`, `P801_1` en `data/raw/ENA_2024/973-Modulo1908/16_CAP800.csv`.
  - Beneficios/servicios por asociacion: `P805_*` en `16_CAP800.csv`.
- Tipo de variable: dummy / conteo.
- Endogeneidad: seleccion (productores mas productivos se asocian). Aun asi, puede capturar acceso a mercados e informacion.
- Ubicacion recomendada: `Z` en SFA; control en logit. Usar como robustez (“nice-to-have”).
- Signo esperado: asociacion -> menor ineficiencia y mayor adopcion.

## B) Temperatura (solo 2023-2024)
- Variable recomendada: `tmean` (promedio de tmax y tmin). Es mas estable y menos ruidosa que extremos, y refleja condiciones termicas promedio del ciclo agricola.
- Relevancia 2023-2024: output 2024 depende de condiciones climaticas recientes (ciclo agricola 2023-2024 y shocks de corto plazo). Usar 2023 y 2024 reduce mezcla con climatologia de largo plazo.
- Features propuestos:
  - `tmean_2023`, `tmean_2024`, `delta_tmean_24_23`.
  - Opcional (si es viable): medias en temporada humeda vs seca para 2023-2024.
- Riesgos: colinealidad con region_natural/altitud. Mitigar con especificaciones alternativas (con/sin region_natural) y estandarizacion.
- Ubicacion recomendada:
  - SFA: preferible en `X` (condicion exogena del entorno productivo).
  - Logit: control exogeno.

## C) Topografia (elevacion, slope, ruggedness)
- Exogeneidad y relevancia: topografia afecta productividad via suelos, acceso, mecanizacion, erosion y microclima. Es exogena al productor.
- DEM viable: SRTM 30m (Plan A) o Copernicus GLO-30 (Plan B), por cobertura abierta y resolucion adecuada para Peru.
- Metodo: extraer valores en centroide/capital distrital y calcular slope/ruggedness en vecindario (3x3 o 5x5). Agregar a nivel distrito.
- Limitaciones: uso de punto distrital ignora variacion intra-distrital; se documentara como error de medicion.
- Ubicacion recomendada:
  - SFA: `X` (condiciones exogenas de produccion).
  - Logit: control exogeno.

## Plan de implementacion (propuesta)

### Must-have (controles ENA)
- Riego/agua: `water_user` (P810), `irrigation_cost` (P1001A_3), dummy de riego tecnificado (a partir de P121/P213 si los codigos lo permiten).
- Capital/maquinaria: `machinery_any` (P1206), `machinery_count` (sum P1207_N), `machinery_capex` (P1001A_5B), `equipment_capex` (P1001A_5A), `equipment_maint` (P1001A_6A).
- Insumos/semilla: `seed_spend` (P235_VAL), `abono_use` (P236), `fertilizer_use` (P238).
- Asistencia/capacitacion: `training_any` (P701), `tech_assist_any` (P704).
- Credito: `credit_obtained` (P902).
- Educacion: `educ_level` (P1105).

### Nice-to-have (si hay tiempo y codigos claros)
- Detalle de sistema/fuente de riego (P120/P121 o P212/P213) en categorias: gravedad vs tecnificado.
- Proxies de semilla mejorada: `seed_from_semillero` (P235A_4), `seed_commercial` (P235A_9).
- Asociacion/cooperativa: `assoc_member` (P801) y beneficios P805_*.
- Temas de capacitacion/asistencia (P702_*, P705_*) para explorar heterogeneidad.

### Ubicacion en modelos (resumen)
- SFA (X): variables de insumos/capital y condiciones exogenas (riego tecnificado, seed_spend, temperatura, topografia).
- SFA (Z): educacion, credito, asistencia, capacitacion, asociacion, acceso a agua institucional (P810).
- Logit: educacion, credito, asistencia/capacitacion, asociacion, acceso a agua; evitar variables directamente ligadas a practicas del outcome.
