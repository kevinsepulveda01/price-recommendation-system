
# 📊 Análisis de Precios y Elasticidad de la Demanda

Este proyecto está diseñado para analizar datos históricos de precios y cantidades vendidas de productos, con el objetivo de identificar precios óptimos que maximicen la utilidad, ajustar precios frente a la competencia, y modelar la elasticidad de la demanda. Además, genera gráficos para facilitar la visualización de los resultados por cada número de parte analizado.

---

## 📁 Estructura del Proyecto

```
proyecto/
│
├── modelo_precios.py          # Código principal con funciones y ejecución
├── precio_parte_ejemplo.xlsx  # Archivo de entrada de datos
├── graficos/                  # Carpeta de salida para los gráficos generados
└── README.md                  # Este documento
```

---

## ⚙️ Requisitos

- Python ≥ 3.7
- Pandas
- NumPy
- Matplotlib
- Statsmodels
- Scipy
- OpenPyXL (para leer archivos Excel)

Puedes instalar los paquetes necesarios con:

```bash
pip install pandas numpy matplotlib statsmodels scipy openpyxl
```

---

## 📌 Parámetros Clave del Modelo

| Parámetro                  | Descripción                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `PRECIO_OBJETIVO`         | Precio que se desea alcanzar o evaluar.                                    |
| `DELTAS`                  | Lista de márgenes para sensibilidad frente a precios de la competencia.    |
| `MIN_DIAS`                | Días mínimos necesarios para considerar válida la serie histórica.         |
| `PRECIO_COMPETENCIA`      | Precio actual de la competencia.                                           |
| `DEMANDA_ESPERADA`        | Cantidad objetivo de ventas para estimar precio basado en elasticidad.     |
| `PENALIZACION_OUTLIER`    | Factor de penalización por precios fuera del rango intercuartílico.        |
| `MARGEN_MINIMO`           | Margen mínimo de ganancia sobre el costo.                                  |
| `COSTO`                   | Costo base del producto.                                                   |

---

## 📈 Funcionalidades

### 1. Limpieza y transformación de datos

- Filtrado de precios extremos.
- Eliminación de cantidades negativas.
- Estandarización de columnas de interés.

### 2. Detección de outliers

- Usando el método de rango intercuartílico (IQR).
- Se identifican precios y cantidades atípicas.

### 3. Cálculo del precio óptimo histórico

- Maximiza la utilidad `(precio - costo) * cantidad`.
- Penaliza precios fuera del rango histórico.

### 4. Ajuste frente a la competencia

- Se limita el precio a un rango ajustado por `±delta` y por desviación máxima permitida.
- Se escoge el precio con mayor utilidad dentro de este rango.

### 5. Modelado de elasticidad de demanda

- Regresión lineal en logaritmos: `log(cantidad) = β₀ + β₁ * log(precio)`
- Se calcula la elasticidad, intercepto y se estima el precio que logra la demanda esperada.

### 6. Visualización

- Gráficos por número de parte.
- Incluye puntos históricos, curvas de elasticidad, precios recomendados y líneas de competencia.

---

## ▶️ Cómo usarlo

1. Asegúrate de tener el archivo Excel con la hoja **BASE_MODELOS**.
2. Configura el nombre del archivo en la línea final del script:

```python
archivo_entrada = r"C:\ruta\a\tu\archivo.xlsx"
```

3. Ejecuta el script:

```bash
python modelo_precios.py
```

4. Revisa:
   - La tabla resumen de resultados impresos.
   - El archivo Excel exportado con los resultados (si lo agregas al final del script).
   - Los gráficos individuales en la carpeta `graficos/`.

---

## 📦 Salida Esperada

- Un **DataFrame** con columnas clave:
  - `PRECIO_OPTIMO_HISTORICO`
  - `PRECIO_AJUSTADO_COMPETENCIA`
  - `PRECIO_DEMANDA_ESPERADA`
  - `CANTIDAD_PREDICHA`
  - `ELASTICIDAD`
  - `OUTLIERS`
- Archivos `.png` con visualizaciones por cada número de parte.

---

## ✍️ Autor

Desarrollado por [Tu Nombre], con el objetivo de optimizar decisiones de pricing en productos de consumo y competencia directa.
