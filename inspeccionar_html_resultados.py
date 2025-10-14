#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inspeccionar la estructura HTML de la página de resultados ICFES
y determinar dónde están ubicados los puntajes individuales.
"""

import pandas as pd
import os
import sys
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Configuración
ARCHIVO_EXCEL = 'INSCRITOS_EXAMEN SABER 11 (36).xls'
URL_ICFES = 'http://resultadossaber11.icfes.edu.co/'

TIPOS_DOCUMENTO = {
    'TI': 'TARJETA DE IDENTIDAD',
    'CC': 'CÉDULA DE CIUDADANÍA'
}

def iniciar_navegador():
    """Inicia el navegador Firefox"""
    print('\n🌐 Iniciando navegador Firefox...')
    options = Options()
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    print('✅ Navegador iniciado')
    return driver

def ingresar_datos(driver, tipo_doc, numero_doc):
    """Ingresa los datos del estudiante"""
    print(f'\n📝 Ingresando datos: {tipo_doc} - {numero_doc}')
    
    driver.get(URL_ICFES)
    time.sleep(3)
    
    # Seleccionar tipo de documento
    wait = WebDriverWait(driver, 10)
    ng_select = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'ng-select[formcontrolname="tipoDocumento"]')
    ))
    ng_select.click()
    time.sleep(1)
    
    tipo_doc_texto = TIPOS_DOCUMENTO.get(tipo_doc, tipo_doc)
    opciones = driver.find_elements(By.CSS_SELECTOR, '.ng-option')
    for opcion in opciones:
        if tipo_doc_texto.upper() in opcion.text.upper():
            opcion.click()
            break
    
    time.sleep(1)
    
    # Ingresar número de documento
    campo_doc = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'input[formcontrolname="numeroDocumento"]')
    ))
    campo_doc.clear()
    campo_doc.send_keys(str(numero_doc))
    
    print('✅ Datos ingresados')
    time.sleep(2)

def esperar_login():
    """Espera a que el usuario haga login"""
    print('\n⏸️  PAUSA PARA LOGIN MANUAL')
    print('='*80)
    print('👉 Por favor:')
    print('   1. Resuelve el CAPTCHA')
    print('   2. Haz clic en "Ingresar"')
    print('   3. Espera a que cargue la página de resultados')
    print('   4. Presiona ENTER en esta terminal')
    print('='*80)
    input('\n⏸️  Presiona ENTER cuando veas los resultados...')
    time.sleep(2)

def analizar_html(driver):
    """Analiza el HTML de la página de resultados"""
    print('\n' + '='*80)
    print('🔍 ANALIZANDO ESTRUCTURA HTML')
    print('='*80)
    
    # Obtener HTML completo
    html = driver.page_source
    
    # Guardar HTML para análisis
    with open('html_resultados.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('\n💾 HTML guardado en: html_resultados.html')
    
    # Buscar puntaje global
    print('\n📊 Buscando puntaje global...')
    match_global = re.search(r'(\d{1,3})/500', html)
    if match_global:
        print(f'   ✅ Puntaje Global encontrado: {match_global.group(1)}/500')
        # Buscar contexto
        pos = html.find(match_global.group(0))
        contexto = html[max(0, pos-200):min(len(html), pos+200)]
        print(f'\n   Contexto HTML:')
        print(f'   {contexto[:400]}')
    
    # Buscar elementos con clases relacionadas a puntajes
    print('\n🔍 Buscando elementos con clases de puntajes...')
    
    selectores = [
        '[class*="puntaje"]',
        '[class*="score"]',
        '[class*="resultado"]',
        '[class*="prueba"]',
        '[class*="test"]',
        '[class*="lectura"]',
        '[class*="matematica"]',
        '[class*="social"]',
        '[class*="ciencia"]',
        '[class*="ingles"]'
    ]
    
    for selector in selectores:
        try:
            elementos = driver.find_elements(By.CSS_SELECTOR, selector)
            if elementos:
                print(f'\n   ✅ Selector "{selector}" encontró {len(elementos)} elementos:')
                for i, elem in enumerate(elementos[:3], 1):
                    try:
                        texto = elem.text.strip()
                        if texto:
                            print(f'      {i}. Texto: {texto[:100]}')
                            print(f'         Clase: {elem.get_attribute("class")}')
                            print(f'         Tag: {elem.tag_name}')
                    except:
                        pass
        except Exception as e:
            pass
    
    # Buscar todos los números de 2-3 dígitos en el HTML visible
    print('\n🔍 Buscando números que podrían ser puntajes...')
    try:
        body = driver.find_element(By.TAG_NAME, 'body')
        texto_visible = body.text
        
        # Buscar números de 2-3 dígitos
        numeros = re.findall(r'\b(\d{2,3})\b', texto_visible)
        numeros_unicos = list(set(numeros))
        numeros_unicos.sort(key=lambda x: int(x), reverse=True)
        
        print(f'\n   Números encontrados (2-3 dígitos): {numeros_unicos[:20]}')
        
        # Buscar contexto de cada número
        print('\n   Contexto de números encontrados:')
        for num in numeros_unicos[:10]:
            pattern = re.compile(r'.{0,50}' + re.escape(num) + r'.{0,50}')
            matches = pattern.findall(texto_visible)
            if matches:
                print(f'\n   {num}: {matches[0][:100]}')
        
    except Exception as e:
        print(f'   ⚠️  Error: {e}')
    
    # Buscar palabras clave
    print('\n🔍 Buscando palabras clave en el texto visible...')
    keywords = ['Lectura Crítica', 'Matemáticas', 'Sociales', 'Ciencias', 'Inglés', 'Global']
    
    try:
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        for keyword in keywords:
            if keyword in body_text:
                # Encontrar contexto
                pos = body_text.find(keyword)
                contexto = body_text[max(0, pos-50):min(len(body_text), pos+150)]
                print(f'\n   ✅ "{keyword}": ...{contexto}...')
    except Exception as e:
        print(f'   ⚠️  Error: {e}')
    
    # Intentar hacer clic en cada área para ver si aparecen puntajes
    print('\n🔍 Intentando hacer clic en áreas de prueba...')
    areas = ['Lectura Crítica', 'Matemáticas', 'Sociales y Ciudadanas', 'Ciencias Naturales', 'Inglés']
    
    for area in areas:
        try:
            print(f'\n   🖱️  Buscando botón/enlace para: {area}')
            
            # Buscar elemento clickeable con el nombre del área
            elementos = driver.find_elements(By.XPATH, f"//*[contains(text(), '{area}')]")
            
            for elem in elementos:
                try:
                    if elem.is_displayed():
                        print(f'      ✅ Elemento encontrado: {elem.tag_name} - {elem.get_attribute("class")}')
                        print(f'         ¿Es clickeable? Intentando...')
                        
                        # Guardar HTML antes del clic
                        html_antes = driver.page_source
                        
                        # Hacer clic
                        elem.click()
                        time.sleep(2)
                        
                        # Verificar si cambió algo
                        html_despues = driver.page_source
                        
                        if html_antes != html_despues:
                            print(f'         ✅ ¡El HTML cambió después del clic!')
                            
                            # Buscar puntajes en el nuevo HTML
                            numeros = re.findall(r'\b(\d{2,3})\b', driver.find_element(By.TAG_NAME, 'body').text)
                            print(f'         Números visibles ahora: {list(set(numeros))[:10]}')
                            
                            # Guardar HTML de esta vista
                            with open(f'html_{area.replace(" ", "_")}.html', 'w', encoding='utf-8') as f:
                                f.write(html_despues)
                            print(f'         💾 HTML guardado en: html_{area.replace(" ", "_")}.html')
                            
                            # Volver atrás
                            driver.back()
                            time.sleep(2)
                        else:
                            print(f'         ⚠️  El HTML no cambió')
                        
                        break
                except Exception as e:
                    print(f'         ⚠️  Error al hacer clic: {e}')
        except Exception as e:
            print(f'   ⚠️  Error: {e}')

def main():
    """Función principal"""
    print('\n' + '='*80)
    print('🔍 INSPECTOR DE HTML DE RESULTADOS ICFES')
    print('='*80)
    
    # Leer primer estudiante
    if not os.path.exists(ARCHIVO_EXCEL):
        print(f'\n❌ Error: No se encuentra {ARCHIVO_EXCEL}')
        sys.exit(1)
    
    df = pd.read_excel(ARCHIVO_EXCEL, skiprows=3)
    estudiante = df.iloc[0]
    
    print(f'\n👤 Estudiante de prueba:')
    print(f'   Nombre: {estudiante["Primer Apellido"]} {estudiante["Segundo Apellido"]} {estudiante["Primer Nombre"]}')
    print(f'   Documento: {estudiante["Tipo de documento"]} - {estudiante["Número de documento"]}')
    
    driver = None
    try:
        driver = iniciar_navegador()
        ingresar_datos(driver, estudiante['Tipo de documento'], estudiante['Número de documento'])
        esperar_login()
        analizar_html(driver)
        
        print('\n' + '='*80)
        print('✅ ANÁLISIS COMPLETADO')
        print('='*80)
        print('\n💡 Revisa los archivos HTML generados para más detalles')
        print('   - html_resultados.html')
        print('   - html_*.html (si se hizo clic en áreas)')
        
        input('\n⏸️  Presiona ENTER para cerrar el navegador...')
        
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()

