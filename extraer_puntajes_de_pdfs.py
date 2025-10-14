#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer puntajes de los PDFs de resultados ICFES usando OCR mejorado.
Los puntajes SÍ están en los PDFs en la sección "Puntaje por pruebas".
"""

import pandas as pd
import os
import sys
import re
from pdf2image import convert_from_path
import pytesseract
from datetime import datetime

# Configuración
ARCHIVO_EXCEL_ENTRADA = 'INSCRITOS_EXAMEN SABER 11 (36).xls'
ARCHIVO_EXCEL_SALIDA = 'RESULTADOS-ICFES-AULA-REGULAR.xlsx'
CARPETA_PDFS = 'pdfs_descargados'
CARPETA_LOGS = 'logs'

def extraer_texto_pdf(pdf_path):
    """Extrae texto de la primera página del PDF usando OCR"""
    try:
        # Convertir solo la primera página (donde están los puntajes)
        images = convert_from_path(pdf_path, dpi=300, first_page=1, last_page=1)
        
        if not images:
            return None
        
        # Extraer texto con configuración optimizada para números
        custom_config = r'--oem 3 --psm 6'
        texto = pytesseract.image_to_string(images[0], lang='spa', config=custom_config)
        
        return texto
        
    except Exception as e:
        print(f'   ❌ Error al extraer texto: {e}')
        return None

def extraer_puntajes(texto):
    """
    Extrae los puntajes del texto OCR.

    Formato esperado en el PDF:
    Lectura Crítica 57/100
    Matemáticas 52/100
    Sociales y Ciudadanas 46/100
    Ciencias Naturales 44/100
    Inglés 48/100
    Puntaje Global: XXX/500

    El OCR puede leer "57/100" como "57100" o "157 00", etc.
    """
    puntajes = {
        'Lectura Crítica': None,
        'Matemáticas': None,
        'Sociales y Ciudadanas': None,
        'Ciencias Naturales': None,
        'Inglés': None,
        'Puntaje Global': None
    }

    if not texto:
        return puntajes

    # Buscar puntaje global (XXX/500)
    match_global = re.search(r'(\d{1,3})\s*/\s*500', texto)
    if match_global:
        puntajes['Puntaje Global'] = int(match_global.group(1))

    # Buscar la línea que contiene "Puntaje por pruebas" y la siguiente línea con los nombres
    # Luego buscar la línea con los números
    lineas = texto.split('\n')

    # Encontrar la línea con los nombres de las áreas
    idx_nombres = -1
    for i, linea in enumerate(lineas):
        if 'Lectura' in linea and 'Matemáticas' in linea and 'Sociales' in linea:
            idx_nombres = i
            break

    # Si encontramos la línea de nombres, buscar números en las siguientes 3 líneas
    if idx_nombres >= 0:
        # Buscar en las siguientes líneas
        for i in range(idx_nombres + 1, min(idx_nombres + 4, len(lineas))):
            linea = lineas[i]

            # Buscar todos los números de 2-6 dígitos en esta línea
            # El OCR puede leer "57/100" como "57100", "157 00", "5700", "407100", etc.
            numeros = re.findall(r'(\d{2,6})', linea)

            if len(numeros) >= 5:
                # Tenemos al menos 5 números, probablemente son los puntajes
                puntajes_candidatos = []

                for num_str in numeros:
                    # Intentar extraer el puntaje
                    # Puede ser: "57100" → 57, "407100" → 40, "5700" → 57, "157" → 57
                    num = int(num_str)

                    if num >= 100000:  # Formato: 407100 → 40
                        puntaje = num // 10000
                    elif num >= 10000:  # Formato: 57100 → 57, 42100 → 42
                        puntaje = num // 1000
                    elif num >= 1000:  # Formato: 5700 → 57, 4700 → 47, 2900 → 29
                        puntaje = num // 100
                    elif num > 100:  # Formato: 157 → 57 (quitar primer dígito)
                        puntaje = num % 100
                    else:  # Formato: 57, 00
                        puntaje = num

                    # Validar rango y excluir 0 (que suele ser ruido del OCR como "00")
                    if 1 <= puntaje <= 100:
                        puntajes_candidatos.append(puntaje)

                # Si tenemos exactamente 5 puntajes, asignarlos en orden
                if len(puntajes_candidatos) >= 5:
                    puntajes['Lectura Crítica'] = puntajes_candidatos[0]
                    puntajes['Matemáticas'] = puntajes_candidatos[1]
                    puntajes['Sociales y Ciudadanas'] = puntajes_candidatos[2]
                    puntajes['Ciencias Naturales'] = puntajes_candidatos[3]
                    puntajes['Inglés'] = puntajes_candidatos[4]
                    break

    return puntajes

def procesar_pdf(pdf_path, nombre_estudiante):
    """Procesa un PDF y extrae los puntajes"""
    print(f'\n📄 Procesando: {os.path.basename(pdf_path)}')
    
    # Extraer texto
    texto = extraer_texto_pdf(pdf_path)
    
    if not texto:
        print('   ❌ No se pudo extraer texto del PDF')
        return None
    
    # Extraer puntajes
    puntajes = extraer_puntajes(texto)
    
    # Mostrar resultados
    print('   📊 Puntajes extraídos:')
    for area, puntaje in puntajes.items():
        if puntaje is not None:
            print(f'      ✅ {area}: {puntaje}')
        else:
            print(f'      ❌ {area}: No encontrado')
    
    # Verificar si se extrajeron todos los puntajes
    puntajes_faltantes = [area for area, puntaje in puntajes.items() if puntaje is None]
    if puntajes_faltantes:
        print(f'   ⚠️  Puntajes faltantes: {", ".join(puntajes_faltantes)}')
        # Guardar texto para análisis
        with open(f'debug_{nombre_estudiante}.txt', 'w', encoding='utf-8') as f:
            f.write(texto)
        print(f'   💾 Texto guardado para análisis: debug_{nombre_estudiante}.txt')
    
    return puntajes

def construir_nombre_pdf(estudiante):
    """Construye el nombre del archivo PDF basado en los datos del estudiante"""
    primer_apellido = str(estudiante['Primer Apellido']).strip().upper()
    segundo_apellido = str(estudiante['Segundo Apellido']).strip().upper()
    primer_nombre = str(estudiante['Primer Nombre']).strip().upper()

    # Manejar segundo nombre (puede ser NaN o vacío)
    segundo_nombre = estudiante.get('Segundo Nombre', '')
    if pd.isna(segundo_nombre) or segundo_nombre == '' or str(segundo_nombre).upper() == 'NAN':
        segundo_nombre = ''
    else:
        segundo_nombre = str(segundo_nombre).strip().upper()

    numero_doc = str(int(estudiante['Número de documento']))  # Convertir a int para quitar decimales

    # Construir nombre
    if segundo_nombre:
        nombre_pdf = f"{primer_apellido}_{segundo_apellido}_{primer_nombre}_{segundo_nombre}_{numero_doc}.pdf"
    else:
        nombre_pdf = f"{primer_apellido}_{segundo_apellido}_{primer_nombre}_{numero_doc}.pdf"

    return nombre_pdf

def main():
    """Función principal"""
    print('\n' + '='*80)
    print('📊 EXTRACTOR DE PUNTAJES ICFES DESDE PDFs')
    print('='*80)
    
    # Verificar archivos
    if not os.path.exists(ARCHIVO_EXCEL_ENTRADA):
        print(f'\n❌ Error: No se encuentra {ARCHIVO_EXCEL_ENTRADA}')
        sys.exit(1)
    
    if not os.path.exists(CARPETA_PDFS):
        print(f'\n❌ Error: No se encuentra la carpeta {CARPETA_PDFS}')
        sys.exit(1)
    
    # Leer Excel
    print(f'\n📂 Leyendo archivo: {ARCHIVO_EXCEL_ENTRADA}')
    df = pd.read_excel(ARCHIVO_EXCEL_ENTRADA, skiprows=4)

    # Limpiar nombres de columnas (quitar espacios)
    df.columns = df.columns.str.strip()

    print(f'✅ {len(df)} estudiantes encontrados')
    
    # Preguntar modo
    print('\n' + '='*80)
    print('SELECCIONA EL MODO DE EJECUCIÓN:')
    print('='*80)
    print('1. Modo PRUEBA (solo 1 estudiante)')
    print('2. Modo COMPLETO (todos los estudiantes)')
    print('='*80)
    
    opcion = input('\nSelecciona una opción (1 o 2): ').strip()
    
    modo_prueba = (opcion == '1')
    
    if modo_prueba:
        print('\n🧪 Modo PRUEBA activado (1 estudiante)')
        df = df.head(1)
    else:
        print(f'\n🚀 Modo COMPLETO activado ({len(df)} estudiantes)')
    
    # Procesar estudiantes
    resultados = []
    errores = []
    
    print('\n' + '='*80)
    print('🔄 PROCESANDO ESTUDIANTES')
    print('='*80)
    
    for idx, estudiante in df.iterrows():
        nombre_completo = f"{estudiante['Primer Apellido']} {estudiante['Segundo Apellido']} {estudiante['Primer Nombre']} {estudiante.get('Segundo Nombre', '')}".strip()
        
        print(f'\n👤 [{idx+1}/{len(df)}] {nombre_completo}')
        
        # Construir nombre del PDF
        nombre_pdf = construir_nombre_pdf(estudiante)
        ruta_pdf = os.path.join(CARPETA_PDFS, nombre_pdf)
        
        # Verificar que existe el PDF
        if not os.path.exists(ruta_pdf):
            print(f'   ❌ PDF no encontrado: {nombre_pdf}')
            errores.append({
                'estudiante': nombre_completo,
                'error': 'PDF no encontrado'
            })
            continue
        
        # Procesar PDF
        puntajes = procesar_pdf(ruta_pdf, nombre_completo.replace(' ', '_'))
        
        if puntajes:
            # Agregar datos del estudiante
            resultado = {
                'Primer Apellido': estudiante['Primer Apellido'],
                'Segundo Apellido': estudiante['Segundo Apellido'],
                'Primer Nombre': estudiante['Primer Nombre'],
                'Segundo Nombre': estudiante.get('Segundo Nombre', ''),
                'Tipo documento': estudiante['Tipo documento'],
                'Número de documento': estudiante['Número de documento'],
                **puntajes
            }
            resultados.append(resultado)
            print(f'   ✅ Estudiante procesado exitosamente')
        else:
            errores.append({
                'estudiante': nombre_completo,
                'error': 'No se pudieron extraer puntajes'
            })
    
    # Generar Excel de salida
    if resultados:
        print('\n' + '='*80)
        print('📊 GENERANDO ARCHIVO EXCEL')
        print('='*80)
        
        df_resultados = pd.DataFrame(resultados)
        
        # Reordenar columnas
        columnas_orden = [
            'Primer Apellido', 'Segundo Apellido', 'Primer Nombre', 'Segundo Nombre',
            'Tipo documento', 'Número de documento',
            'Lectura Crítica', 'Matemáticas', 'Sociales y Ciudadanas',
            'Ciencias Naturales', 'Inglés', 'Puntaje Global'
        ]
        df_resultados = df_resultados[columnas_orden]
        
        # Guardar Excel
        df_resultados.to_excel(ARCHIVO_EXCEL_SALIDA, index=False, engine='openpyxl')
        
        print(f'\n✅ Archivo generado: {ARCHIVO_EXCEL_SALIDA}')
        print(f'📊 Total de estudiantes: {len(df_resultados)}')
        
        # Estadísticas
        print('\n📈 ESTADÍSTICAS:')
        print('   ' + '-'*60)
        for columna in ['Lectura Crítica', 'Matemáticas', 'Sociales y Ciudadanas', 
                        'Ciencias Naturales', 'Inglés', 'Puntaje Global']:
            valores = df_resultados[columna].dropna()
            if len(valores) > 0:
                print(f'   {columna}:')
                print(f'      Promedio: {valores.mean():.1f}')
                print(f'      Mínimo: {valores.min():.0f}')
                print(f'      Máximo: {valores.max():.0f}')
    
    # Mostrar resumen
    print('\n' + '='*80)
    print('📊 RESUMEN FINAL')
    print('='*80)
    print(f'✅ Estudiantes procesados: {len(resultados)}')
    print(f'❌ Errores: {len(errores)}')
    
    if errores:
        print('\n⚠️  Estudiantes con errores:')
        for error in errores:
            print(f'   - {error["estudiante"]}: {error["error"]}')
    
    print('\n' + '='*80)
    print('✅ PROCESO COMPLETADO')
    print('='*80)

if __name__ == '__main__':
    main()

