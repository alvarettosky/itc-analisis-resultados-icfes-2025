#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de exploración para analizar PDFs del ICFES usando OCR
"""

import pytesseract
from pdf2image import convert_from_path
import os
import sys
import re

def extraer_texto_con_ocr(pdf_path, max_pages=3):
    """Extrae texto de un PDF usando OCR"""
    print(f"\n🔍 Convirtiendo PDF a imágenes...")
    
    try:
        # Convertir PDF a imágenes
        images = convert_from_path(pdf_path, dpi=300, first_page=1, last_page=max_pages)
        
        print(f"✅ {len(images)} páginas convertidas a imágenes")
        
        full_text = ""
        
        for i, image in enumerate(images, 1):
            print(f"\n📄 Procesando página {i} con OCR...")
            
            # Aplicar OCR
            text = pytesseract.image_to_string(image, lang='spa')
            
            print(f"✅ Página {i} procesada ({len(text)} caracteres)")
            
            full_text += f"\n{'='*80}\n"
            full_text += f"PÁGINA {i}\n"
            full_text += f"{'='*80}\n"
            full_text += text
            full_text += "\n"
        
        return full_text
        
    except Exception as e:
        print(f"❌ Error en OCR: {e}")
        return None

def buscar_puntajes(text):
    """Busca y extrae puntajes del texto"""
    print("\n" + "="*80)
    print("🔍 BÚSQUEDA DE PUNTAJES")
    print("="*80)
    
    # Patrones a buscar
    patterns = {
        "Lectura Crítica": [
            r"Lectura\s+Cr[ií]tica[:\s]+(\d+)",
            r"LECTURA\s+CR[IÍ]TICA[:\s]+(\d+)",
            r"Lectura\s+critica[:\s]+(\d+)"
        ],
        "Matemáticas": [
            r"Matem[áa]ticas[:\s]+(\d+)",
            r"MATEM[ÁA]TICAS[:\s]+(\d+)",
            r"Matematicas[:\s]+(\d+)"
        ],
        "Sociales y Ciudadanas": [
            r"Sociales\s+y\s+Ciudadanas[:\s]+(\d+)",
            r"SOCIALES\s+Y\s+CIUDADANAS[:\s]+(\d+)",
            r"Sociales\s+y\s+ciudadanas[:\s]+(\d+)"
        ],
        "Ciencias Naturales": [
            r"Ciencias\s+Naturales[:\s]+(\d+)",
            r"CIENCIAS\s+NATURALES[:\s]+(\d+)",
            r"Ciencias\s+naturales[:\s]+(\d+)"
        ],
        "Inglés": [
            r"Ingl[ée]s[:\s]+(\d+)",
            r"INGL[ÉE]S[:\s]+(\d+)",
            r"Ingles[:\s]+(\d+)"
        ],
        "Puntaje Global": [
            r"Puntaje\s+Global[:\s]+(\d+)",
            r"PUNTAJE\s+GLOBAL[:\s]+(\d+)",
            r"Puntaje\s+global[:\s]+(\d+)",
            r"Global[:\s]+(\d+)"
        ]
    }
    
    resultados = {}
    
    for area, pattern_list in patterns.items():
        encontrado = False
        for pattern in pattern_list:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                puntaje = matches[0]
                resultados[area] = puntaje
                print(f"✅ {area}: {puntaje}")
                encontrado = True
                break
        
        if not encontrado:
            print(f"❌ {area}: No encontrado")
            resultados[area] = None
    
    return resultados

def mostrar_contexto_palabras_clave(text):
    """Muestra el contexto alrededor de palabras clave"""
    print("\n" + "="*80)
    print("📝 CONTEXTO DE PALABRAS CLAVE")
    print("="*80)
    
    keywords = [
        "Lectura",
        "Matemática",
        "Sociales",
        "Ciencias",
        "Inglés",
        "Global",
        "Puntaje",
        "PUNTAJE",
        "Prueba",
        "PRUEBA"
    ]
    
    for keyword in keywords:
        # Buscar todas las ocurrencias (case insensitive)
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        matches = list(pattern.finditer(text))
        
        if matches:
            print(f"\n🔍 '{keyword}' encontrado {len(matches)} veces:")
            for i, match in enumerate(matches[:3], 1):  # Mostrar solo las primeras 3
                start = max(0, match.start() - 80)
                end = min(len(text), match.end() + 80)
                context = text[start:end].replace('\n', ' ')
                print(f"   {i}. ...{context}...")

def main():
    """Función principal"""
    print("\n" + "="*80)
    print("🔍 EXPLORADOR DE PDFs DEL ICFES CON OCR")
    print("="*80)
    
    # Buscar el primer PDF
    pdf_dir = "pdfs_descargados"
    
    if not os.path.exists(pdf_dir):
        print(f"\n❌ Error: No se encuentra la carpeta '{pdf_dir}'")
        sys.exit(1)
    
    pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
    
    if not pdf_files:
        print(f"\n❌ Error: No se encontraron archivos PDF en '{pdf_dir}'")
        sys.exit(1)
    
    # Usar el primer PDF
    pdf_path = os.path.join(pdf_dir, pdf_files[0])
    
    print(f"\n📁 Carpeta: {pdf_dir}")
    print(f"📄 Total de PDFs: {len(pdf_files)}")
    print(f"🎯 Analizando: {pdf_files[0]}")
    
    # Extraer texto con OCR
    text = extraer_texto_con_ocr(pdf_path, max_pages=3)
    
    if text:
        # Guardar texto extraído
        output_file = "texto_extraido_ocr.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\n💾 Texto guardado en: {output_file}")
        
        # Mostrar primeros 3000 caracteres
        print("\n" + "="*80)
        print("📝 TEXTO EXTRAÍDO (primeros 3000 caracteres)")
        print("="*80)
        print(text[:3000])
        if len(text) > 3000:
            print(f"\n... (texto truncado, total: {len(text)} caracteres)")
        
        # Buscar puntajes
        resultados = buscar_puntajes(text)
        
        # Mostrar contexto
        mostrar_contexto_palabras_clave(text)
        
        # Resumen
        print("\n" + "="*80)
        print("📊 RESUMEN DE EXTRACCIÓN")
        print("="*80)
        print(f"\nPuntajes encontrados:")
        for area, puntaje in resultados.items():
            status = "✅" if puntaje else "❌"
            print(f"  {status} {area}: {puntaje if puntaje else 'No encontrado'}")
        
        encontrados = sum(1 for p in resultados.values() if p)
        total = len(resultados)
        print(f"\n📊 Total: {encontrados}/{total} puntajes encontrados")
        
    print("\n" + "="*80)
    print("✅ EXPLORACIÓN COMPLETADA")
    print("="*80)
    print("\n💡 Revisa el archivo 'texto_extraido_ocr.txt' para ver el texto completo")
    print()

if __name__ == "__main__":
    main()

