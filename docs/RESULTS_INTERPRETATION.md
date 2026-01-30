# Interpretacion de resultados finales

## Resumen ejecutivo
- **Productividad (SFA)**: tierra, trabajo e insumos muestran elasticidades positivas y altamente significativas. La suma es ~**1.23**, consistente con retornos levemente crecientes (con cautela por medicion de insumos).
- **Diversificacion y eficiencia**: con `ineffDecrease=TRUE`, el coeficiente base de diversificacion en la ecuacion de ineficiencia es **positivo** (mayor eficiencia) y significativo. La interaccion con productores grandes es **negativa y fuerte**, revirtiendo el efecto neto en ese grupo; para medianos no hay diferencia estadistica clara.
- **Practicas sostenibles (logit)**: la diversificacion tiene un efecto positivo y significativo. Un aumento de 0.1 en diversificacion implica OR ≈ **1.15** (OR ≈ **3.98** por 1 punto). El outcome no esta saturado (media ~0.776), pero sigue siendo frecuente.
- **Geo/clima (CHIRPS)**: en SFA, `prcp_total_z` en la frontera no es significativo; en la ecuacion de ineficiencia (ZGEO) es negativo y significativo (mayor ineficiencia). En logit, `prcp_total_z` es positivo (OR ≈ 1.73 por 1 desviacion).

## SFA: productividad y eficiencia
- **Frontera de produccion**: `log_land`, `log_labor` y `log_inputs` son positivos y estadisticamente significativos, con la tierra como el insumo mas elastico. Esto sugiere que el aumento en superficie explica buena parte del valor de produccion.
- **Efectos regionales**: las regiones entran en la ecuacion de ineficiencia (Z), no en la frontera. Sus coeficientes positivos indican mayor eficiencia relativa en regiones 2 y 3 (condicional a insumos).
- **Ecuacion de ineficiencia (Z_)**: el paquete `frontier` usa `ineffDecrease=TRUE`, por lo que un coeficiente **positivo** en Z_ indica **menor ineficiencia** (mayor eficiencia) y un coeficiente **negativo** indica **mayor ineficiencia**.
  - Productores **pequenos** (categoria base): `Z_diversificacion_area` es positivo y significativo, asociado a **mayor eficiencia** con mayor diversificacion.
  - Productores **medianos**: la interaccion no es estadisticamente significativa; el efecto neto sigue siendo positivo pero con mayor incertidumbre.
  - Productores **grandes**: la interaccion es negativa y fuerte, por lo que la diversificacion se asocia a **mayor ineficiencia** en este grupo.
- **Controles geo/clima**:
  - **XGEO**: `prcp_total_z` en la frontera no es estadisticamente significativo.
  - **ZGEO**: `Z_prcp_total_z` es negativo y significativo (ineficiencia aumenta con anomalias positivas).
  - El efecto base de diversificacion se atenúa en algunas especificaciones con temp/topo, pero la interaccion negativa para grandes persiste.
- **Robustez**: con indices alternativos (Shannon, numero de cultivos) los coeficientes mantienen magnitudes distintas y `gamma` se acerca mas a 1. Esto sugiere sensibilidad a la medicion del indice y refuerza la cautela en la interpretacion.
- **Gamma alto (~0.93)**: el parametro `gamma` indica que la variacion de ineficiencia domina la varianza total del error; es alto pero no esta en el limite. Se debe interpretar con cautela y revisar `outputs/tables/02_sfa_diagnostics.csv`.

## Logit: practicas sostenibles
- **Efecto principal**: la diversificacion tiene un efecto positivo y significativo sobre la probabilidad de adoptar al menos una practica sostenible. En terminos de magnitud, un aumento de 0.1 en diversificacion implica OR ~1.15.
- **Interacciones por tamano**: los terminos de interaccion no son estadisticamente significativos, por lo que no se observa heterogeneidad clara por tamano.
- **Efectos regionales**: la region natural 2 muestra mayor probabilidad de practicas; la region 3, menor probabilidad respecto a la base.
- **Controles geo/clima**: `prcp_total_z` es positivo y significativo (OR ~1.73 por 1 desviacion), y el efecto de diversificacion se mantiene practicamente sin cambios.
- **Robustez**: los resultados se mantienen usando Shannon y numero de cultivos como indices alternativos, y con un outcome mas estricto (>=2 practicas).

## Como mejorar los resultados
### Datos y medicion
- **Mejorar la variable de output**: deflactar valores monetarios, ajustar por precios regionales y considerar incluir produccion pecuaria si es relevante para el productor.
- **Capital y tecnologia**: incorporar variables de maquinaria, infraestructura o acceso a riego para capturar tecnologia productiva y reducir sesgo por omitidas.
- **Trabajo**: complementar con costos de mano de obra o dias-hombre si estan disponibles; los conteos pueden subestimar intensidad laboral.
- **Manejo de missing**: aplicar imputacion multiple o reglas de consistencia para variables clave (area, valor, practicas) para reducir perdida de muestra.
- **Geo/clima**: ampliar el baseline CHIRPS a 1991-2020 y agregar elevacion, pendientes, suelo y acceso a mercados para capturar condiciones agroecologicas.
- **Geocodificacion**: si existe GPS de ENA, usarlo en lugar de capitales distritales para reducir error de localizacion.

### Modelos y especificaciones
- **SFA con pesos**: explorar aproximaciones con ponderacion (pseudo-likelihood o re-muestreo ponderado) o paquetes alternativos que permitan pesos.
- **Funciones de produccion flexibles**: probar translog y comparar con Cobb-Douglas para verificar elasticidades y retornos a escala.
- **Endogeneidad de diversificacion**: instrumentar diversificacion (clima, acceso a mercados, shocks) o usar metodos de control para sesgo de seleccion.
- **Heterogeneidad**: estimar modelos separados por region y tamano para verificar estabilidad de signos y magnitudes.
- **Colinealidad geo**: evaluar especificaciones alternativas con FE departamental o sin `region_natural` cuando la climatologia explique gran parte de la variacion.

### Analisis complementarios
- **Resultados por cultivos clave**: evaluar si la relacion diversificacion-productividad difiere en productores especializados vs. mixtos.
- **External data**: agregar controles climaticos o de calidad de suelo si se dispone de coordenadas confiables.
- **Outcome mas estricto**: usar conteos de practicas o un indice continuo para capturar intensidad de sostenibilidad.

## Lectura economica
Los resultados sugieren que la diversificacion esta consistentemente asociada a mayor adopcion de practicas sostenibles, mientras que su relacion con eficiencia productiva es heterogenea y sensible al indice, al tamano y a controles geo/clima. Esto apunta a un posible trade-off: diversificar puede facilitar la sostenibilidad pero no siempre maximiza eficiencia tecnica, especialmente en extremos de tamano. La mejora en mediciones e identificacion causal es clave para concluir sobre mecanismos.
