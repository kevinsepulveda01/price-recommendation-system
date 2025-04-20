import pandas as pd
import numpy as np
from scipy.optimize import minimize_scalar
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

# ======================
# CONFIGURACIÓN FINAL
# ======================
PRECIO_OBJETIVO = 29000
DELTAS = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
MIN_DIAS = 3
PRECIO_COMPETENCIA = 28500
DEMANDA_ESPERADA = 7
OUTLIER_IQR_THRESHOLD = 1.5
PENALIZACION_OUTLIER = 0.3
MARGEN_MINIMO = 0.10
MAX_DESVIACION_COMPETENCIA = 0.2
COSTO = 20000

# ======================
# FUNCIONES CLAVE MEJORADAS
# ======================

def transformar_datos(df):
    """Limpieza básica de datos manteniendo transacciones individuales"""
    df = df[
        (df['PRECIO'] > 27000) & 
        (df['PRECIO'] < 39000) &
        (df['CANTIDAD'] >= 0)
    ].copy()
    return df[['FECHA', 'PRECIO', 'CANTIDAD']]

def detectar_outliers(df):
    """Detección robusta de outliers usando método IQR modificado"""
    outliers = []
    try:
        for col in ['PRECIO', 'CANTIDAD']:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            
            if iqr == 0: continue
                
            lim_inf = q1 - OUTLIER_IQR_THRESHOLD * iqr
            lim_sup = q3 + OUTLIER_IQR_THRESHOLD * iqr
            
            for idx in df[(df[col] < lim_inf) | (df[col] > lim_sup)].index:
                registro = f"{df.at[idx, 'PRECIO']}:{df.at[idx, 'CANTIDAD']}"
                if registro not in outliers:
                    outliers.append(registro)
                    
        return outliers
    except Exception as e:
        print(f"Error detectando outliers: {str(e)}")
        return []

def calcular_utilidad_optima(precios, cantidades, costo, q1_hist, q3_hist):
    """Calcula el precio óptimo considerando costos y penalización por outliers"""
    mejor_utilidad = -np.inf
    mejor_precio = np.nan
    
    for p, q in zip(precios, cantidades):
        utilidad = (p - costo) * q
        
        # Penalizar precios fuera del rango histórico
        if p < q1_hist or p > q3_hist:
            utilidad *= (1 - PENALIZACION_OUTLIER)
            
        if utilidad > mejor_utilidad and not np.isnan(utilidad):
            mejor_utilidad = utilidad
            mejor_precio = p
            
    return mejor_precio

def modelo_elasticidad(df_diario):
    """Modelo mejorado con restricción de margen mínimo"""
    try:
        X = np.log(df_diario['PRECIO'])
        X = sm.add_constant(X)
        y = np.log(df_diario['CANTIDAD'] + 0.001)
        
        modelo = sm.OLS(y, X).fit()
        elasticidad = modelo.params[1]
        intercept = modelo.params[0]
        
        # Calcular precio para demanda esperada con restricciones
        if DEMANDA_ESPERADA > 0:
            ln_q = np.log(DEMANDA_ESPERADA)
            precio_teorico = np.exp((ln_q - intercept) / elasticidad)
            precio_demanda = max(precio_teorico, COSTO * (1 + MARGEN_MINIMO))
        else:
            precio_demanda = None
            
        return elasticidad, intercept, precio_demanda
        
    except Exception as e:
        print(f"Error en modelo: {str(e)}")
        return None, None, None

# ======================
# NÚCLEO DEL MODELO
# ======================

def analisis_sensibilidad(archivo):
    df = pd.read_excel(archivo, sheet_name="BASE_MODELOS")
    resultados = []
    
    for delta in DELTAS:
        for num_parte, grupo in df.groupby('NUMERO DE PARTE'):
            try:
                df_clean = transformar_datos(grupo)
                if len(df_clean) < MIN_DIAS: continue
                
                # Estadísticas clave
                q1_hist = df_clean['PRECIO'].quantile(0.25)
                q3_hist = df_clean['PRECIO'].quantile(0.75)
                precios = df_clean['PRECIO'].values
                cantidades = df_clean['CANTIDAD'].values
                
                # 1. Precio óptimo histórico
                precio_optimo = calcular_utilidad_optima(
                    precios, cantidades, COSTO, q1_hist, q3_hist
                )
                
                # 2. Precio ajustado a competencia
                rango_ajuste = [
                    max(PRECIO_COMPETENCIA*(1 - delta), 
                    COSTO*(1 + MARGEN_MINIMO),
                    PRECIO_COMPETENCIA*(1 - MAX_DESVIACION_COMPETENCIA)
                ),
                    min(PRECIO_COMPETENCIA*(1 + delta),
                        PRECIO_COMPETENCIA*(1 + MAX_DESVIACION_COMPETENCIA))
                ]
                mascara = (precios >= rango_ajuste[0]) & (precios <= rango_ajuste[1])
                precio_ajustado = calcular_utilidad_optima(
                    precios[mascara], cantidades[mascara], COSTO, q1_hist, q3_hist
                ) if any(mascara) else np.nan
                
                # 3. Precio para demanda esperada
                elasticidad, intercept, precio_demanda = modelo_elasticidad(df_clean)
                pred_cantidad = np.exp(intercept) * (PRECIO_OBJETIVO**elasticidad) if elasticidad else np.nan
                
                # Validaciones finales
                precio_ajustado = min(precio_ajustado, rango_ajuste[1]) if not np.isnan(precio_ajustado) else PRECIO_COMPETENCIA
                precio_ajustado = max(precio_ajustado, rango_ajuste[0])
                
                resultados.append({
                    'DELTA': delta,
                    'NUMERO_PARTE': num_parte,
                    'PRECIO_OPTIMO_HISTORICO': precio_optimo,
                    'PRECIO_AJUSTADO_COMPETENCIA': precio_ajustado,
                    'PRECIO_DEMANDA_ESPERADA': precio_demanda,
                    'CANTIDAD_PREDICHA': pred_cantidad,
                    'ELASTICIDAD': elasticidad,
                    'INTERCEPT': intercept,
                    'DIAS_ANALIZADOS': len(df_clean),
                    'OUTLIERS': ', '.join(detectar_outliers(df_clean)) if detectar_outliers(df_clean) else 'Ninguno'
                })
                
            except Exception as e:
                print(f"Error procesando {num_parte}: {str(e)}")
                continue
    
    return pd.DataFrame(resultados)

# ======================
# FUNCIÓN PARA GRÁFICOS
# ======================

def generar_graficos(resultados, archivo_original, output_dir="graficos"):
    """Genera gráficos de análisis para cada número de parte"""
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Leer datos originales
    df_base = pd.read_excel(archivo_original, sheet_name="BASE_MODELOS")
    
    # Procesar cada parte única
    for num_parte in resultados['NUMERO_PARTE'].unique():
        try:
            # Filtrar datos relevantes
            df_parte = df_base[df_base['NUMERO DE PARTE'] == num_parte]
            df_clean = transformar_datos(df_parte)
            res_parte = resultados[resultados['NUMERO_PARTE'] == num_parte]
            
            if len(df_clean) < MIN_DIAS:
                continue
            
            # Configurar figura
            plt.figure(figsize=(12, 7))
            
            # Gráfico de dispersión histórico
            plt.scatter(df_clean['PRECIO'], df_clean['CANTIDAD'], 
                       alpha=0.5, label='Datos Históricos')
            
            # Modelo de elasticidad
            ejemplo = res_parte.iloc[0]
            precios_modelo = np.linspace(df_clean['PRECIO'].min(), df_clean['PRECIO'].max(), 100)
            cantidad_modelo = np.exp(ejemplo['INTERCEPT']) * (precios_modelo**ejemplo['ELASTICIDAD'])
            plt.plot(precios_modelo, cantidad_modelo, 'r--', label='Modelo de Elasticidad')
            
            # Líneas de referencia
            plt.axvline(ejemplo['PRECIO_OPTIMO_HISTORICO'], color='g', 
                       linestyle=':', label='Precio Óptimo Histórico')
            plt.axvline(ejemplo['PRECIO_DEMANDA_ESPERADA'], color='m', 
                       linestyle='-.', label='Precio Demanda Esperada')
            
            # Precios ajustados por delta
            for _, row in res_parte.iterrows():
                plt.axvline(row['PRECIO_AJUSTADO_COMPETENCIA'], alpha=0.3,
                           label=f'Δ={row["DELTA"]:.0%}')
            
            # Configuraciones del gráfico
            plt.title(f'Análisis de Precios - Parte {num_parte}')
            plt.xlabel('Precio')
            plt.ylabel('Cantidad Vendida')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Guardar gráfico
            plt.savefig(f"{output_dir}/precios_{num_parte}.png", dpi=300)
            plt.close()
            
        except Exception as e:
            print(f"Error generando gráfico para {num_parte}: {str(e)}")

# ======================
# EJECUCIÓN Y RESULTADOS
# ======================

if __name__ == "__main__":
    archivo_entrada = r""
    resultados = analisis_sensibilidad(archivo_entrada)
    
    if not resultados.empty:
        print("\nRESULTADOS OPTIMIZADOS:")
        cols = ['DELTA', 'NUMERO_PARTE', 'PRECIO_OPTIMO_HISTORICO', 
                'PRECIO_AJUSTADO_COMPETENCIA', 'PRECIO_DEMANDA_ESPERADA',
                'CANTIDAD_PREDICHA', 'ELASTICIDAD', 'OUTLIERS']
        print(resultados[cols].round(2))
        resultados.to_excel(r"", index=False)
        
        # Generar gráficos
        generar_graficos(resultados, archivo_entrada)
        print("\nGráficos generados en la carpeta 'graficos'")
    else:
        print("No se generaron resultados. Verificar datos de entrada.")