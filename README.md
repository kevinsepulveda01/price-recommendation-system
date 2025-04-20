# Modelo de Optimización de Precios para Retail

Herramienta avanzada para análisis de precios óptimos en retail utilizando datos históricos, elasticidad de demanda y competencia. Genera recomendaciones estratégicas y visualizaciones detalladas.

## 🔍 Visión General

Este proyecto implementa un modelo de machine learning para determinar precios óptimos de productos considerando múltiples factores:
- Comportamiento histórico de ventas
- Precios de la competencia
- Elasticidad de la demanda
- Restricciones de margen mínimo
- Detección de outliers en datos

Incluye capacidades de:

✅ Análisis multivariable  
✅ Modelado econométrico  
✅ Optimización no lineal  
✅ Visualización interactiva  
✅ Reportes ejecutivos automáticos

## 🚀 Características Principales

1. **Algoritmo de Optimización Híbrida**
   - Combina análisis histórico con ajustes competitivos
   - Balancea márgenes vs volumen de ventas
   - Restricciones configurables de mercado

2. **Modelo de Elasticidad Avanzado**
   - Regresión logarítmica multivariable
   - Predicción de demanda esperada
   - Intervalos de confianza estadísticos

3. **Gestión Inteligente de Datos**
   - Limpieza automática de datos
   - Detección adaptativa de outliers
   - Transformaciones no lineales

4. **Sistema de Penalizaciones Ajustables**
   - Control de márgenes mínimos
   - Límites de desviación competitiva
   - Factores de riesgo personalizables

## ⚙️ Instalación

1. Clonar repositorio:
   ```bash
   git clone https://github.com/tu-usuario/modelo-precios-retail.git
   cd modelo-precios-retail

2. Instalar dependencias:

pip install -r requirements.txt

## Requisitos del Sistema:

Python 3.8+
Bibliotecas principales:
pandas, numpy, scipy, statsmodels, matplotlib, openpyxl

## 📊 Uso Básico
1. Preparar archivo Excel con:
- Hoja "BASE_MODELOS" con columnas:
  - FECHA (formato fecha)
  - PRECIO (numérico)
  - CANTIDAD (entero)
  - NUMERO DE PARTE (identificador único)

2. Ejecutar modelo:
   python modelo_precios.py

3. Resultados generados:
   resultados_optimizacion.xlsx: Recomendaciones detalladas
   Directorio graficos/: Análisis visual por producto

## ⚙️ Configuración Avanzada
Editar constantes en el script principal:

# Estrategia de Precios
- PRECIO_OBJETIVO = 29000        # Precio ideal de referencia
- DELTAS = [0.05, 0.06, 0.07]    # Rangos de variación vs competencia
- PRECIO_COMPETENCIA = 28500      # Precio base de competidores

# Parámetros del Modelo
- MARGEN_MINIMO = 0.10            # Margen de ganancia mínimo requerido
- DEMANDA_ESPERADA = 7            # Unidades diarias objetivo
- COSTO = 20000                   # Costo unitario de producción

# Configuración Técnica
- MIN_DIAS = 3                    # Mínimo días de datos requeridos
- OUTLIER_IQR_THRESHOLD = 1.5     # Sensibilidad para detección de outliers

## 📊 Interpretación de Resultados

### Archivo de Salida (`resultados_optimizacion.xlsx`)

| Columna                     | Descripción                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| `PRECIO_OPTIMO_HISTORICO`   | Precio que maximizó la utilidad histórica considerando costos y outliers    |
| `PRECIO_AJUSTADO_COMPETENCIA` | Precio óptimo dentro del rango permitido (± delta) vs competencia           |
| `PRECIO_DEMANDA_ESPERADA`   | Precio requerido para alcanzar la demanda objetivo de **7 unidades/día**    |
| `ELASTICIDAD`               | Coeficiente de sensibilidad demanda-precio (valores negativos = demanda elástica) |
| `CANTIDAD_PREDICHA`         | Unidades estimadas al precio objetivo de $29,000                            |
| `OUTLIERS`                  | Transacciones atípicas detectadas (formato: `PRECIO:CANTIDAD`)              |
| `DIAS_ANALIZADOS`           | Número de días considerados en el análisis                                  |

### Gráficos Generados (`graficos/precios_[NUMERO_PARTE].png`)

- **Relación Precio-Demanda Histórica**
  - Puntos azules: Transacciones reales
  - Eje X: Precio de venta
  - Eje Y: Cantidad vendida

- **Curva Teórica de Elasticidad**
  - Línea roja discontinua: Modelo de regresión logarítmica
  - Ecuación: `ln(Cantidad) = Intercept + Elasticidad*ln(Precio)`

- **Marcadores de Precios Clave**
  - Línea verde (:): Mejor precio histórico
  - Línea magenta (-.): Precio para demanda objetivo
  - Líneas grises (transparentes): Variaciones por delta vs competencia

- **Zonas Estratégicas**
  - Área sombreada: Rango entre percentiles 25-75 de precios históricos
  - Región roja: Precios bajo costo mínimo ($20,000 * 1.10 = $22,000)
  - Banda amarilla: Rango de ±20% vs competencia ($28,500 ± $5,700)

### Clave de Símbolos en Gráficos
![Leyenda Gráficos](https://via.placeholder.com/600x400?text=Ejemplo+Visual+de+Gráfico)
*(Nota: La imagen muestra un ejemplo conceptual de cómo interpretar los elementos visuales)*

## 🗂 Estructura del Repositorio
modelo-precios-retail/
├── .gitignore
├── Graficos.png                # Muestra de visualizaciones
├── LICENSE
├── README.md                   # Este archivo
├── modelo_precios.py           # Script principal
└── requirements.txt            # Dependencias


## 🤝 Contribuciones
1. Haz fork del proyecto
2. Crea tu rama (git checkout -b feature/nueva-funcionalidad)
3. Realiza commit de tus cambios
4. Haz push a la rama
5. Abre un Pull Request

## Reporte de Issues:
Usa el tablero de GitHub para reportar bugs o sugerir mejoras.

## 📄 Licencia
Distribuido bajo licencia MIT. Ver LICENSE para más detalles.





