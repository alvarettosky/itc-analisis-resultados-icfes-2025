#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis detallado de un PDF de resultados ICFES usando OCR
para identificar todos los puntajes posibles.
"""

import sys
import re
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def extraer_texto_ocr(pdf_path, dpi=300):
    """Extrae texto de todas las páginas del PDF"""
    print(f'\n📄 Procesando: {pdf_path}')
    print(f'   DPI: {dpi}')
    
    try:
        # Convertir PDF a imágenes
        print('   🔄 Convirtiendo PDF a imágenes...')
        images = convert_from_path(pdf_path, dpi=dpi)
        print(f'   ✅ {len(images)} páginas convertidas')
        
        textos_por_pagina = []
        
        for i, image in enumerate(images, 1):
            print(f'\n   📄 Página {i}/{len(images)}')
            print(f'      Tamaño: {image.size}')
            
            # Extraer texto con diferentes configuraciones
            print('      🔍 Extrayendo texto (modo normal)...')
            texto_normal = pytesseract.image_to_string(image, lang='spa')
            
            print('      🔍 Extrayendo texto (modo con configuración)...')
            # Configuración para mejorar detección de números
            custom_config = r'--oem 3 --psm 6'
            texto_config = pytesseract.image_to_string(image, lang='spa', config=custom_config)
            
            textos_por_pagina.append({
                'pagina': i,
                'texto_normal': texto_normal,
                'texto_config': texto_config
            })
            
            print(f'      ✅ Texto extraído: {len(texto_normal)} caracteres')
        
        return textos_por_pagina
        
    except Exception as e:
        print(f'   ❌ Error: {e}')
        return None

def analizar_texto(textos):
    """Analiza el texto extraído buscando puntajes"""
    print('\n' + '='*80)
    print('🔍 ANÁLISIS DE TEXTO EXTRAÍDO')
    print('='*80)
    
    for datos in textos:
        pagina = datos['pagina']
        texto = datos['texto_normal']
        
        print(f'\n📄 PÁGINA {pagina}')
        print('='*80)
        
        # Mostrar texto completo
        print('\n📝 TEXTO COMPLETO:')
        print('-'*80)
        lineas = texto.split('\n')
        for i, linea in enumerate(lineas, 1):
            if linea.strip():
                print(f'{i:3d}: {linea}')
        
        # Buscar puntaje global
        print('\n🎯 PUNTAJE GLOBAL:')
        print('-'*80)
        matches_global = re.finditer(r'(\d{1,3})\s*/\s*500', texto, re.IGNORECASE)
        for match in matches_global:
            puntaje = match.group(1)
            contexto_inicio = max(0, match.start() - 50)
            contexto_fin = min(len(texto), match.end() + 50)
            contexto = texto[contexto_inicio:contexto_fin]
            print(f'   ✅ Encontrado: {puntaje}/500')
            print(f'   Contexto: ...{contexto}...')
        
        # Buscar palabras clave de áreas
        print('\n📚 ÁREAS DE PRUEBA:')
        print('-'*80)
        areas = [
            'Lectura Crítica',
            'Lectura Critica',
            'LECTURA CRÍTICA',
            'LECTURA CRITICA',
            'Matemáticas',
            'Matematicas',
            'MATEMÁTICAS',
            'MATEMATICAS',
            'Sociales y Ciudadanas',
            'Sociales',
            'SOCIALES',
            'Ciencias Naturales',
            'Ciencias',
            'CIENCIAS',
            'Inglés',
            'Ingles',
            'INGLÉS',
            'INGLES'
        ]
        
        for area in areas:
            if area in texto:
                # Encontrar contexto
                pos = texto.find(area)
                contexto_inicio = max(0, pos - 30)
                contexto_fin = min(len(texto), pos + len(area) + 100)
                contexto = texto[contexto_inicio:contexto_fin]
                
                print(f'\n   ✅ "{area}" encontrado')
                print(f'      Contexto: ...{contexto}...')
                
                # Buscar números cerca
                numeros = re.findall(r'\b(\d{1,3})\b', contexto)
                if numeros:
                    print(f'      Números cercanos: {numeros}')
        
        # Buscar todos los números de 2-3 dígitos
        print('\n🔢 TODOS LOS NÚMEROS (2-3 dígitos):')
        print('-'*80)
        numeros = re.findall(r'\b(\d{2,3})\b', texto)
        numeros_unicos = list(set(numeros))
        numeros_unicos.sort(key=lambda x: int(x), reverse=True)
        
        print(f'   Números encontrados: {numeros_unicos}')
        
        # Buscar patrones de puntaje (número seguido de contexto)
        print('\n📊 POSIBLES PUNTAJES:')
        print('-'*80)
        
        # Patrón: número de 2-3 dígitos que podría ser un puntaje
        for num in numeros_unicos:
            if 0 <= int(num) <= 100 or int(num) <= 500:
                # Buscar contexto de este número
                pattern = re.compile(r'.{0,50}' + re.escape(num) + r'.{0,50}')
                matches = pattern.findall(texto)
                if matches:
                    print(f'\n   {num}:')
                    for match in matches[:3]:  # Mostrar máximo 3 contextos
                        print(f'      {match.strip()}')

def main():
    """Función principal"""
    print('\n' + '='*80)
    print('🔍 ANÁLISIS DETALLADO DE PDF CON OCR')
    print('='*80)
    
    # PDF a analizar
    pdf_path = 'pdfs_descargados/ALGARIN_MOVILLA_JUAN_JOSE_1043592724.pdf'
    
    # Extraer texto
    textos = extraer_texto_ocr(pdf_path, dpi=300)
    
    if textos:
        # Analizar texto
        analizar_texto(textos)
        
        # Guardar texto completo
        print('\n' + '='*80)
        print('💾 GUARDANDO RESULTADOS')
        print('='*80)
        
        with open('analisis_detallado_ocr.txt', 'w', encoding='utf-8') as f:
            for datos in textos:
                f.write(f'\n{"="*80}\n')
                f.write(f'PÁGINA {datos["pagina"]}\n')
                f.write(f'{"="*80}\n\n')
                f.write('TEXTO NORMAL:\n')
                f.write('-'*80 + '\n')
                f.write(datos['texto_normal'])
                f.write('\n\n')
                f.write('TEXTO CON CONFIGURACIÓN:\n')
                f.write('-'*80 + '\n')
                f.write(datos['texto_config'])
                f.write('\n\n')
        
        print('✅ Análisis guardado en: analisis_detallado_ocr.txt')
    
    print('\n' + '='*80)
    print('✅ ANÁLISIS COMPLETADO')
    print('='*80)

if __name__ == '__main__':
    main()

