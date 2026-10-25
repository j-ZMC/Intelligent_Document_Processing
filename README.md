# Intelligent Document Processing

Procesa reportes 10-K de la SEC: descarga el reporte, extrae el Item 7,
lo convierte a JSON con un LLM, calcula métricas financieras y genera gráficas.

## Cómo funciona

1. Descarga el 10-K desde SEC EDGAR.
2. Extrae el texto del Item 7 y lo limpia.
3. Envía el texto a un LLM y guarda la respuesta en `resultado.json`.
4. Arma la matriz financiera 3 x N (deuda, efectivo, obligaciones) y calcula totales, promedios y saldos.
5. Genera gráficas de barras en `graficas/`.
6. Muestra el análisis y las gráficas en la interfaz gráfica.

## Entradas y salidas

Entradas: ticker (ej. AAPL) y años (ej. 2023, 2024, 2025).

Salidas: `resultado.json` y las gráficas PNG en `graficas/`.

## Cómo ejecutarlo

1. Descarga el repositorio.
2. Instala las librerías de `requirements.txt`.
3. Ejecuta `main.py`.
