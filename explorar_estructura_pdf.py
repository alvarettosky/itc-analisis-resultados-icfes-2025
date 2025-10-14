#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de exploración para analizar la estructura de los PDFs del ICFES
y determinar la mejor estrategia para extraer los puntajes.
"""

import pdfplumber
import PyPDF2
import os
import sys

def explorar_con_pdfplumber(pdf_path):
    """Explora el PDF usando pdfplumber"""
    print("\n" + "="*80)
    print("EXPLORACIÓN CON PDFPLUMBER")
    print("="*80)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"\n📄 Archivo: {os.path.basename(pdf_path)}")
            print(f"📊 Total de páginas: {len(pdf.pages)}")
            
            # Analizar cada página
            for i, page in enumerate(pdf.pages, 1):
                print(f"\n{'─'*80}")
                print(f"PÁGINA {i}")
                print(f"{'─'*80}")
                
                # Extraer texto
                text = page.extract_text()
                if text:
                    print("\n📝 TEXTO EXTRAÍDO:")
                    print(text[:2000])  # Primeros 2000 caracteres
                    if len(text) > 2000:
                        print(f"\n... (texto truncado, total: {len(text)} caracteres)")
                
                # Buscar tablas
                tables = page.extract_tables()
                if tables:
                    print(f"\n📊 TABLAS ENCONTRADAS: {len(tables)}")
                    for j, table in enumerate(tables, 1):
                        print(f"\n  Tabla {j}:")
                        for row in table[:5]:  # Primeras 5 filas
                            print(f"    {row}")
                        if len(table) > 5:
                            print(f"    ... ({len(table)} filas en total)")
                
                # Información de la página
                print(f"\n📐 Dimensiones: {page.width} x {page.height}")
                
    except Exception as e:
        print(f"❌ Error con pdfplumber: {e}")

def explorar_con_pypdf2(pdf_path):
    """Explora el PDF usando PyPDF2"""
    print("\n" + "="*80)
    print("EXPLORACIÓN CON PyPDF2")
    print("="*80)
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            print(f"\n📄 Archivo: {os.path.basename(pdf_path)}")
            print(f"📊 Total de páginas: {len(pdf_reader.pages)}")
            
            # Analizar cada página
            for i, page in enumerate(pdf_reader.pages, 1):
                print(f"\n{'─'*80}")
                print(f"PÁGINA {i}")
                print(f"{'─'*80}")
                
                # Extraer texto
                text = page.extract_text()
                if text:
                    print("\n📝 TEXTO EXTRAÍDO:")
                    print(text[:2000])  # Primeros 2000 caracteres
                    if len(text) > 2000:
                        print(f"\n... (texto truncado, total: {len(text)} caracteres)")
                
    except Exception as e:
        print(f"❌ Error con PyPDF2: {e}")

def buscar_puntajes_en_texto(text):
    """Busca patrones de puntajes en el texto"""
    print("\n" + "="*80)
    print("BÚSQUEDA DE PUNTAJES")
    print("="*80)
    
    # Palabras clave a buscar
    keywords = [
        "Lectura Crítica",
        "Matemáticas",
        "Sociales y Ciudadanas",
        "Ciencias Naturales",
        "Inglés",
        "Puntaje Global",
        "puntaje",
        "PUNTAJE",
        "Prueba",
        "PRUEBA",
        "Resultado",
        "RESULTADO"
    ]
    
    print("\n🔍 Buscando palabras clave...")
    for keyword in keywords:
        if keyword in text:
            # Encontrar contexto alrededor de la palabra clave
            index = text.find(keyword)
            start = max(0, index - 50)
            end = min(len(text), index + 150)
            context = text[start:end]
            print(f"\n✅ Encontrado: '{keyword}'")
            print(f"   Contexto: ...{context}...")

def main():
    """Función principal"""
    print("\n" + "="*80)
    print("🔍 EXPLORADOR DE ESTRUCTURA DE PDFs DEL ICFES")
    print("="*80)
    
    # Buscar el primer PDF en la carpeta
    pdf_dir = "pdfs_descargados"
    
    if not os.path.exists(pdf_dir):
        print(f"\n❌ Error: No se encuentra la carpeta '{pdf_dir}'")
        sys.exit(1)
    
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"\n❌ Error: No se encontraron archivos PDF en '{pdf_dir}'")
        sys.exit(1)
    
    # Usar el primer PDF como ejemplo
    pdf_path = os.path.join(pdf_dir, pdf_files[0])
    
    print(f"\n📁 Carpeta: {pdf_dir}")
    print(f"📄 Total de PDFs: {len(pdf_files)}")
    print(f"🎯 Analizando: {pdf_files[0]}")
    
    # Explorar con ambas librerías
    explorar_con_pdfplumber(pdf_path)
    explorar_con_pypdf2(pdf_path)
    
    # Buscar puntajes en el texto extraído
    print("\n" + "="*80)
    print("ANÁLISIS DE CONTENIDO")
    print("="*80)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            buscar_puntajes_en_texto(full_text)
            
    except Exception as e:
        print(f"❌ Error en análisis de contenido: {e}")
    
    print("\n" + "="*80)
    print("✅ EXPLORACIÓN COMPLETADA")
    print("="*80)
    print("\nRevisa la salida para determinar:")
    print("  1. ¿Qué librería extrae mejor el texto?")
    print("  2. ¿Dónde están ubicados los puntajes?")
    print("  3. ¿Hay tablas que podamos extraer?")
    print("  4. ¿Qué patrones podemos usar para extraer los datos?")
    print()

if __name__ == "__main__":
    main()

