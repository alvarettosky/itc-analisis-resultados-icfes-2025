#!/usr/bin/env python3
"""
Script para adaptar el archivo ITC-RESULTADOS-ICFES-2025.xlsx
al formato esperado por la aplicación Streamlit
"""

import pandas as pd
import re

# Leer archivo original
df_original = pd.read_excel('ITC-RESULTADOS-ICFES-2025.xlsx')

print("📊 Archivo original:")
print(f"   Columnas: {list(df_original.columns)}")
print(f"   Filas totales: {len(df_original)}")

# Eliminar filas con nombres vacíos (filas de totales/promedios)
df_original = df_original[df_original['NOMBRES Y APELLIDOS'].notna()].copy()
print(f"   Estudiantes válidos: {len(df_original)}")

# Crear DataFrame adaptado
df_adaptado = pd.DataFrame()

# Procesar nombres
def separar_nombres(nombre_completo):
    """Separa el nombre completo en componentes"""
    if pd.isna(nombre_completo):
        return '', '', '', ''
    
    partes = str(nombre_completo).strip().split()
    
    if len(partes) == 0:
        return '', '', '', ''
    elif len(partes) == 1:
        return '', '', partes[0], ''
    elif len(partes) == 2:
        return partes[0], '', partes[1], ''
    elif len(partes) == 3:
        return partes[0], partes[1], partes[2], ''
    else:  # 4 o más partes
        # Asumimos: Primer_Apellido Segundo_Apellido Primer_Nombre Segundo_Nombre
        return partes[0], partes[1], partes[2], ' '.join(partes[3:])

# Aplicar separación de nombres
nombres_separados = df_original['NOMBRES Y APELLIDOS'].apply(separar_nombres)
df_adaptado['Primer Apellido'] = [n[0] for n in nombres_separados]
df_adaptado['Segundo Apellido'] = [n[1] for n in nombres_separados]
df_adaptado['Primer Nombre'] = [n[2] for n in nombres_separados]
df_adaptado['Segundo Nombre'] = [n[3] for n in nombres_separados]

# Agregar grupo (todos son del mismo grupo por defecto)
df_adaptado['Grupo'] = '11A'

# Agregar tipo y número de documento (valores por defecto)
df_adaptado['Tipo documento'] = 'CC'
df_adaptado['Número de documento'] = range(1000000000, 1000000000 + len(df_original))

# Copiar puntajes (ajustando nombres de columnas)
df_adaptado['Lectura Crítica'] = df_original['LECTURA CRITICA']
df_adaptado['Matemáticas'] = df_original['MATEMATICAS']
df_adaptado['Sociales y Ciudadanas'] = df_original['SOCIALES Y CIUDADANAS']
df_adaptado['Ciencias Naturales'] = df_original['CIENCIAS NATURALES']
df_adaptado['Inglés'] = df_original['INGLES']
df_adaptado['Puntaje Global'] = df_original['PUNTAJE']

# Reordenar columnas en el orden esperado
columnas_orden = [
    'Grupo',
    'Primer Apellido',
    'Segundo Apellido',
    'Primer Nombre',
    'Segundo Nombre',
    'Tipo documento',
    'Número de documento',
    'Lectura Crítica',
    'Matemáticas',
    'Sociales y Ciudadanas',
    'Ciencias Naturales',
    'Inglés',
    'Puntaje Global'
]

df_adaptado = df_adaptado[columnas_orden]

# Guardar archivo adaptado
df_adaptado.to_excel('ITC-RESULTADOS-ICFES-2025-ADAPTADO.xlsx', index=False)

print("\n✅ Archivo adaptado creado:")
print(f"   Nombre: ITC-RESULTADOS-ICFES-2025-ADAPTADO.xlsx")
print(f"   Columnas: {list(df_adaptado.columns)}")
print(f"   Filas: {len(df_adaptado)}")
print("\n📋 Primeras 3 filas:")
print(df_adaptado.head(3).to_string())

