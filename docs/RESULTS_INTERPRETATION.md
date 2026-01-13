# Interpretacion de resultados finales

## Resumen ejecutivo
- **Productividad (SFA)**: los insumos tierra, trabajo e insumos intermedios presentan elasticidades positivas y altamente significativas. La suma de elasticidades es ~1.08, lo que sugiere retornos a escala levemente crecientes (con cautela por medicion de insumos).
- **Diversificacion y eficiencia**: en el modelo principal, el coeficiente de diversificacion en la ecuacion de ineficiencia es negativo y significativo; esto implica mayor ineficiencia (menor eficiencia) para productores pequenos, pero la interaccion con productores medianos revierte el signo (mejora de eficiencia), mientras que en productores grandes el efecto vuelve a ser negativo. Al incluir geo/clima, el efecto base para pequenos se atenúa y deja de ser significativo en la especificacion ZGEO, mientras que el efecto positivo en medianos se mantiene.
- **Practicas sostenibles (logit)**: la diversificacion esta asociada a una mayor probabilidad de adoptar al menos una practica sostenible. Un aumento de 0.1 en diversificacion (0-1) eleva las odds en ~31% (OR ~1.31). Este resultado es robusto a indices alternativos y se mantiene con controles geo/clima.
- **Geo/clima (CHIRPS)**: la anomalia de precipitacion esta asociada a mayor produccion en la frontera y a mayor adopcion de practicas; en la ecuacion de ineficiencia, mayores lluvias relativas se vinculan a mayor ineficiencia (interpretacion condicional).

## SFA: productividad y eficiencia
- **Frontera de produccion**: `log_land`, `log_labor` y `log_inputs` son positivos y estadisticamente significativos, con la tierra como el insumo mas elastico. Esto sugiere que el aumento en superficie explica buena parte del valor de produccion.
- **Efectos regionales**: en comparacion con la region natural base (region_natural=1), las regiones 2 y 3 presentan niveles de produccion menores, manteniendo constantes insumos.
- **Ecuacion de ineficiencia (Z_)**: el paquete `frontier` usa `ineffDecrease=TRUE`, por lo que un coeficiente **positivo** en Z_ indica **menor ineficiencia** (mayor eficiencia) y un coeficiente **negativo** indica **mayor ineficiencia**.
  - Productores **pequenos** (categoria base): `Z_diversificacion_area` es negativo y significativo, asociado a mayor ineficiencia a mayor diversificacion.
  - Productores **medianos**: la interaccion positiva y significativa (`Z_diversif_mediano`) mas que compensa el efecto base, lo que sugiere que la diversificacion mejora la eficiencia en este grupo.
  - Productores **grandes**: la interaccion es negativa, reforzando el efecto base; la diversificacion se asocia a mayor ineficiencia.
- **Controles geo/clima**:
  - **XGEO**: `prcp_total_z` entra en la frontera con signo positivo y significativo, lo que sugiere mayor produccion en distritos relativamente mas lluviosos.
  - **ZGEO**: `Z_prcp_total_z` es negativo y significativo, consistente con mayor ineficiencia en anomalias positivas (condicional a insumos y region).
  - El efecto base de diversificacion en pequenos se reduce fuertemente y deja de ser significativo en ZGEO; el efecto positivo en medianos y negativo en grandes persiste, aunque con magnitudes menores.
- **Robustez**: el signo del efecto de diversificacion cambia con el indice de Shannon y en la submuestra de pequenos. Esto indica sensibilidad al indicador y al grupo, por lo que la evidencia SFA debe tomarse con cautela.
- **Gamma alto (~1)**: el parametro `gamma` cerca de 1 indica que la variacion de ineficiencia domina la varianza total del error; puede reflejar especificacion limitada o variables omitidas.

## Logit: practicas sostenibles
- **Efecto principal**: la diversificacion tiene un efecto positivo y significativo sobre la probabilidad de adoptar al menos una practica sostenible. En terminos de magnitud, un aumento de 0.1 en diversificacion implica OR ~1.31.
- **Interacciones por tamano**: los terminos de interaccion no son estadisticamente significativos, por lo que no se observa heterogeneidad clara por tamano.
- **Efectos regionales**: la region natural 2 muestra mayor probabilidad de practicas; la region 3, menor probabilidad respecto a la base.
- **Controles geo/clima**: `prcp_total_z` es positivo y significativo (OR ~1.89 por 1 desviacion), y el efecto de diversificacion se mantiene practicamente sin cambios.
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
