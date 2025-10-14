#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para verificar que todos los estudiantes del Excel tengan su PDF descargado
"""

import pandas as pd
import os
import re

# Configuración
ARCHIVO_EXCEL = 'INSCRITOS_EXAMEN SABER 11 (36).xls'
CARPETA_PDFS = 'pdfs_descargados'

def construir_nombre_archivo(estudiante):
    """Construye el nombre del archivo PDF esperado (igual que el script principal)"""
    primer_apellido = str(estudiante['Primer Apellido']).strip().upper()
    segundo_apellido = str(estudiante['Segundo Apellido']).strip().upper()
    primer_nombre = str(estudiante['Primer Nombre']).strip().upper()
    segundo_nombre = str(estudiante['Segundo Nombre']).strip().upper()
    num_documento = str(estudiante['Número de documento']).strip()

    # Construir nombre completo
    apellidos = f"{primer_apellido}_{segundo_apellido}"

    if segundo_nombre != 'NAN':
        nombres = f"{primer_nombre}_{segundo_nombre}"
    else:
        nombres = primer_nombre

    nombre_archivo = f"{apellidos}_{nombres}_{num_documento}"

    # Limpiar caracteres no válidos
    caracteres_invalidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in caracteres_invalidos:
        nombre_archivo = nombre_archivo.replace(char, '_')

    return nombre_archivo + '.pdf'

def main():
    print('='*80)
    print('🔍 VERIFICACIÓN DE PDFs DESCARGADOS')
    print('='*80)
    print()
    
    # Leer Excel
    print(f'📖 Leyendo archivo Excel: {ARCHIVO_EXCEL}')
    df = pd.read_excel(ARCHIVO_EXCEL, skiprows=3)

    # La primera fila contiene los nombres de las columnas
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    # Limpiar nombres de columnas (remover espacios)
    df.columns = df.columns.str.strip()

    print(f'✅ Se encontraron {len(df)} estudiantes en el Excel')
    print()
    
    # Obtener lista de PDFs descargados
    pdfs_descargados = set()
    if os.path.exists(CARPETA_PDFS):
        pdfs_descargados = set(os.listdir(CARPETA_PDFS))
    
    print(f'📁 Se encontraron {len(pdfs_descargados)} PDFs en la carpeta {CARPETA_PDFS}')
    print()
    
    # Verificar cada estudiante
    estudiantes_sin_pdf = []
    estudiantes_con_pdf = []
    
    for indice, (_, estudiante) in enumerate(df.iterrows()):
        nombre_esperado = construir_nombre_archivo(estudiante)
        
        # Buscar el PDF (puede tener sufijos como _1, _2, etc.)
        pdf_encontrado = None
        
        # Buscar exacto
        if nombre_esperado in pdfs_descargados:
            pdf_encontrado = nombre_esperado
        else:
            # Buscar con sufijos
            base_nombre = nombre_esperado.replace('.pdf', '')
            for pdf in pdfs_descargados:
                if pdf.startswith(base_nombre):
                    pdf_encontrado = pdf
                    break
        
        if pdf_encontrado:
            estudiantes_con_pdf.append({
                'nombre': nombre_esperado,
                'pdf': pdf_encontrado,
                'documento': estudiante['Número de documento']
            })
        else:
            estudiantes_sin_pdf.append({
                'nombre': nombre_esperado,
                'documento': estudiante['Número de documento'],
                'tipo_doc': estudiante['Tipo documento']
            })
    
    # Mostrar resultados
    print('='*80)
    print('📊 RESULTADOS DE LA VERIFICACIÓN')
    print('='*80)
    print()
    
    print(f'✅ Estudiantes con PDF: {len(estudiantes_con_pdf)}/{len(df)}')
    print(f'❌ Estudiantes sin PDF: {len(estudiantes_sin_pdf)}/{len(df)}')
    print()
    
    if estudiantes_sin_pdf:
        print('='*80)
        print('❌ ESTUDIANTES SIN PDF')
        print('='*80)
        print()
        for est in estudiantes_sin_pdf:
            print(f'  • {est["nombre"]}')
            print(f'    Documento: {est["tipo_doc"]} {est["documento"]}')
            print()
    else:
        print('🎉 ¡TODOS LOS ESTUDIANTES TIENEN SU PDF DESCARGADO!')
        print()
    
    # Verificar PDFs extra (que no corresponden a ningún estudiante)
    nombres_esperados = set()
    for _, estudiante in df.iterrows():
        nombre = construir_nombre_archivo(estudiante)
        nombres_esperados.add(nombre)
        # También agregar versiones con sufijos _1, _2, etc.
        base_nombre = nombre.replace('.pdf', '')
        for i in range(1, 10):
            nombres_esperados.add(f'{base_nombre}_{i}.pdf')

    pdfs_extra = []
    for pdf in pdfs_descargados:
        if pdf not in nombres_esperados:
            pdfs_extra.append(pdf)
    
    if pdfs_extra:
        print('='*80)
        print('⚠️  PDFs EXTRA (no corresponden a ningún estudiante del Excel)')
        print('='*80)
        print()
        for pdf in pdfs_extra:
            print(f'  • {pdf}')
        print()
    
    # Resumen final
    print('='*80)
    print('📋 RESUMEN')
    print('='*80)
    print(f'Total estudiantes en Excel: {len(df)}')
    print(f'Total PDFs descargados: {len(pdfs_descargados)}')
    print(f'Estudiantes con PDF: {len(estudiantes_con_pdf)}')
    print(f'Estudiantes sin PDF: {len(estudiantes_sin_pdf)}')
    print(f'PDFs extra: {len(pdfs_extra)}')
    print()
    
    if len(estudiantes_sin_pdf) == 0:
        print('✅ ¡VERIFICACIÓN EXITOSA! Todos los estudiantes tienen su PDF.')
    else:
        print('⚠️  VERIFICACIÓN INCOMPLETA. Faltan PDFs por descargar.')
    
    print('='*80)

if __name__ == '__main__':
    main()

