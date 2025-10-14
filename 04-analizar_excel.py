#!/usr/bin/env python3
"""
Script para analizar el archivo Excel de inscritos al ICFES
"""
import pandas as pd

def analizar_excel(ruta_archivo):
    """Analiza el archivo Excel y muestra información relevante"""
    
    # Leer el archivo saltando las primeras 3 filas de encabezado
    df = pd.read_excel(ruta_archivo, skiprows=3)
    
    # La primera fila contiene los nombres de las columnas
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    
    print('=' * 80)
    print('ANÁLISIS DEL ARCHIVO EXCEL DE INSCRITOS AL ICFES')
    print('=' * 80)
    
    print(f'\n📊 Total de estudiantes: {len(df)}')
    
    print('\n📋 Columnas disponibles:')
    for i, col in enumerate(df.columns, 1):
        print(f'   {i}. {col}')
    
    print('\n👥 Muestra de datos (primeros 3 estudiantes):')
    print(df.head(3).to_string())
    
    print('\n📈 Estadísticas:')
    print(f'   - Tipos de documento únicos: {df["Tipo documento"].unique()}')
    print(f'   - Distribución por tipo de documento:')
    print(df["Tipo documento"].value_counts().to_string())
    
    print(f'\n   - Departamentos: {df["Departamento"].unique()}')
    print(f'   - Municipios: {df["Municipio"].unique()}')
    
    print('\n⚠️  Valores nulos por columna:')
    nulos = df.isnull().sum()
    for col, count in nulos.items():
        if count > 0:
            print(f'   - {col}: {count} valores nulos')
    
    print('\n✅ Datos necesarios para el login:')
    print('   - Tipo de documento: ✓')
    print('   - Número de documento: ✓')
    print('   - Nombres y apellidos: ✓ (para nombrar archivos)')
    
    return df

if __name__ == '__main__':
    ruta = '/home/proyectos/Escritorio/Resultados-ICFES-2025/INSCRITOS_EXAMEN SABER 11 (36).xls'
    df = analizar_excel(ruta)

