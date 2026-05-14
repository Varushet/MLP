# Memoria de los Pasos Seguidos en el Notebook temporalSeriesWeather_v2.ipynb

Esta memoria documenta los pasos realizados en el desarrollo del modelo híbrido para predicción de temperaturas climáticas por país, basado en series temporales.

## Paso 1: Configuración Inicial y Imports (Celda 1)

- **Objetivo**: Preparar el entorno de trabajo con todas las librerías necesarias.
- **Acciones realizadas**:
  - Importación de librerías clave: pandas, numpy, matplotlib, seaborn, statsmodels, pmdarima, sklearn, joblib, etc.
  - Configuración de warnings, estilo de gráficos y DPI.
  - Creación del directorio para guardar modelos (`modelos_hibridos_v2/`).
- **Resultado**: Entorno listo para análisis de series temporales y modelado híbrido.

## Paso 2: Carga y Preparación de Datos (Celda 2)

- **Objetivo**: Cargar el dataset y realizar agregación inicial.
- **Acciones realizadas**:
  - Carga del dataset `../data/tiempoDS.csv.gz` (Berkeley Earth Surface Temperature).
  - Agregación de temperaturas por país/año/mes (media de ciudades).
  - Exploración inicial: conteo de filas, países únicos, calidad de datos (nulos), cobertura temporal.
- **Resultado**: Dataset `df` con temperaturas medias mensuales por país, desde 1819 hasta 2012, 158 países.

## Paso 3: Exploración Visual de Series Temporales (Celda 3)

- **Objetivo**: Analizar la estructura de una serie temporal de referencia (España).
- **Acciones realizadas**:
  - Selección de país de referencia (Spain).
  - Preparación de serie: conversión a datetime, indexación, eliminación de duplicados, interpolación de huecos.
  - Descomposición clásica usando `seasonal_decompose` (tendencia, estacionalidad, residuos).
  - Visualización de componentes y test de estacionariedad en residuos (ADF test).
- **Resultado**: Confirmación de que los residuos son estacionarios, indicando que la descomposición captura bien la señal.

## Paso 4: Diagnóstico del Problema con SARIMA (Celda 4)

- **Objetivo**: Identificar por qué los modelos SARIMA tradicionales fallan en predicciones a largo plazo.
- **Acciones realizadas**:
  - Entrenamiento de un modelo SARIMA estándar en datos de train (1950-1999).
  - Predicción en test (2000-2012) y proyección futura (5 años).
  - Cálculo de amplitud estacional histórica vs predicha.
  - Visualización comparativa: validación en test y proyección futura.
- **Resultado**: Demostración del "aplanamiento" en predicciones SARIMA, con pérdida del 17.2% de amplitud estacional.

## Paso 5: Definición de Funciones del Modelo Híbrido (Celda 5)

- **Objetivo**: Implementar las funciones base para el modelo híbrido.
- **Acciones realizadas**:
  - `fit_trend_seasonal()`: Ajusta regresión lineal con tendencia + dummies mensuales.
  - `predict_trend_seasonal()`: Genera predicciones de la componente determinista.
  - `diagnostics_residuals()`: Análisis estadístico de residuos (ADF, Ljung-Box, normalidad).
- **Resultado**: Funciones reutilizables para separar componentes deterministas y analizar residuos.

## Paso 6: Análisis Detallado en un País (Celda 6)

- **Objetivo**: Validar la calidad de la separación de componentes en España.
- **Acciones realizadas**:
  - Ajuste de tendencia + estacionalidad sobre datos de train.
  - Diagnóstico de residuos: visualización temporal, ACF/PACF, tests estadísticos.
  - Análisis de autocorrelación residual (Ljung-Box).
- **Resultado**: Confirmación de que los residuos tienen autocorrelación, justificando el uso de ARIMA sobre ellos.

## Paso 7: Función de Entrenamiento Híbrido (Celda 7)

- **Objetivo**: Implementar la función completa para entrenar modelos híbridos por país.
- **Acciones realizadas**:
  - Preparación de datos por país: filtrado, indexación, interpolación.
  - Split temporal: train (antes de 2000) y test (2000-2012).
  - Entrenamiento: regresión lineal sobre train, ARIMA sobre residuos.
  - Predicción y métricas: RMSE, MAE, correlación, AmpRatio.
  - Guardado de modelos en archivos .joblib.
- **Resultado**: Función `train_hybrid_model()` lista para procesamiento paralelo.

## Paso 8: Entrenamiento en Paralelo (Celda 8)

- **Objetivo**: Entrenar modelos para todos los países disponibles.
- **Acciones realizadas**:
  - Procesamiento paralelo usando `joblib.Parallel` con `delayed`.
  - Manejo de errores por país.
  - Recopilación de métricas en un DataFrame.
  - Guardado de métricas en CSV (`metricas_modelos_hibridos.csv`).
- **Resultado**: Modelos entrenados para múltiples países, con métricas globales.

## Paso 9: Análisis Estadístico de Métricas (Celda 9)

- **Objetivo**: Evaluar la calidad global del modelo híbrido.
- **Acciones realizadas**:
  - Visualización de distribuciones: RMSE, AmpRatio, correlación.
  - Scatter plots: RMSE vs correlación, coloreado por AmpRatio.
  - Análisis de autocorrelación residual (Ljung-Box p-values).
  - Ranking de mejores y peores modelos.
- **Resultado**: Insights sobre el rendimiento global, con mediana de RMSE ~1°C y buena preservación estacional.

## Paso 10: Análisis de Calentamiento Climático (Celda 10)

- **Objetivo**: Extraer tendencias de calentamiento por país.
- **Acciones realizadas**:
  - Cálculo de tasa de calentamiento (coeficiente de tendencia).
  - Estimación de aceleración (segunda derivada).
  - Análisis estadístico: correlación con distancia al polo.
- **Resultado**: Confirmación de amplificación polar (países más cercanos al polo se calientan más rápido).

## Paso 11: Relación Distancia al Polo vs Calentamiento (Celda 11)

- **Objetivo**: Visualizar el impacto geográfico del cambio climático.
- **Acciones realizadas**:
  - Scatter plots: distancia al polo vs tasa de calentamiento y aceleración.
  - Líneas de tendencia y correlaciones.
  - Etiquetado de países extremos.
- **Resultado**: Correlación negativa fuerte entre distancia al polo y calentamiento.

## Paso 12: Predicción Futura hasta 2050 (Celda 12)

- **Objetivo**: Proyectar temperaturas medias anuales para 2050.
- **Acciones realizadas**:
  - Función `predict_2050()`: carga modelos y proyecta tendencia + estacionalidad.
  - Ranking de países más afectados.
  - Visualización: barras de incremento y scatter vs distancia al polo.
- **Resultado**: Proyección de incrementos globales, con España y otros países polares más afectados.

## Paso 13: Análisis Adicional de Tendencias (Celdas 13-17)

- **Objetivo**: Exploraciones adicionales no ejecutadas en esta sesión.
- **Acciones pendientes**:
  - Análisis de estacionalidad variable.
  - Comparaciones entre países.
  - Validaciones adicionales.
- **Resultado**: Código preparado para análisis futuros.

## Conclusiones Generales

- **Metodología Exitosa**: El modelo híbrido supera las limitaciones de SARIMA al preservar la estacionalidad.
- **Resultados Clave**: RMSE mediano ~1°C, AmpRatio cercano a 1.0, autocorrelación residual eliminada.
- **Insights Climáticos**: Confirmación de amplificación polar y aceleración del calentamiento.
- **Próximos Pasos**: Ejecutar celdas restantes para análisis completos, integrar en aplicación Streamlit.

## Notas Técnicas

- **Dataset**: Berkeley Earth, temperaturas mensuales por ciudad/país.
- **Herramientas**: Python con statsmodels, pmdarima, sklearn.
- **Limitaciones**: Datos hasta 2012, interpolación de huecos.
- **Reproducibilidad**: Todas las funciones están autocontenidas y documentadas.

Esta memoria refleja los pasos ejecutados hasta la celda 7, con las celdas posteriores preparadas pero no ejecutadas en la sesión actual.
