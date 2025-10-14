#!/usr/bin/env python3
"""
Script para inspeccionar la página de resultados después del login
IMPORTANTE: Este script requiere que resuelvas el CAPTCHA manualmente
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

# Datos de prueba (primer estudiante del Excel)
TIPO_DOC = 'CC'
NUM_DOC = '1095208929'
NUM_REGISTRO = 'AC202530812826'

# Mapeo de tipos de documento
mapeo_tipos_doc = {
    'TI': 'TARJETA DE IDENTIDAD',
    'CC': 'CÉDULA DE CIUDADANÍA',
}

# Configurar Firefox
firefox_options = Options()
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    print('='*80)
    print('INSPECCIÓN DE PÁGINA DE RESULTADOS')
    print('='*80)
    
    print('\n1. Navegando al portal ICFES...')
    driver.get('http://resultadossaber11.icfes.edu.co/')
    time.sleep(5)
    
    print('2. Llenando formulario...')
    wait = WebDriverWait(driver, 10)
    
    # Seleccionar tipo de documento
    tipo_doc_formulario = mapeo_tipos_doc.get(TIPO_DOC, TIPO_DOC)
    print(f'   - Tipo de documento: {TIPO_DOC} → {tipo_doc_formulario}')
    
    ng_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ng-select')))
    ng_select.click()
    time.sleep(1)
    
    opciones = driver.find_elements(By.CSS_SELECTOR, '.ng-option')
    for opcion in opciones:
        if tipo_doc_formulario.upper() == opcion.text.strip().upper():
            opcion.click()
            break
    time.sleep(0.5)
    
    # Ingresar número de documento
    print(f'   - Número de documento: {NUM_DOC}')
    input_identificacion = wait.until(EC.presence_of_element_located((By.ID, 'identificacion')))
    input_identificacion.clear()
    input_identificacion.send_keys(NUM_DOC)
    time.sleep(0.5)
    
    # Ingresar número de registro
    print(f'   - Número de registro: {NUM_REGISTRO}')
    input_registro = wait.until(EC.presence_of_element_located((By.ID, 'numeroRegistro')))
    input_registro.clear()
    input_registro.send_keys(NUM_REGISTRO)
    time.sleep(0.5)
    
    print('\n3. Formulario llenado. Ahora debes:')
    print('   👉 Resolver el CAPTCHA en el navegador')
    print('   👉 Hacer clic en el botón "Ingresar"')
    print('   👉 Esperar a que cargue la página de resultados')
    print('   👉 Presionar ENTER aquí cuando veas la página de resultados')
    
    input('\nPresiona ENTER cuando estés en la página de resultados...')
    
    print('\n4. Inspeccionando página de resultados...')
    time.sleep(3)
    
    # Guardar el HTML de la página de resultados
    html_resultados = driver.page_source
    with open('pagina_resultados.html', 'w', encoding='utf-8') as f:
        f.write(html_resultados)
    print('   ✅ HTML guardado en: pagina_resultados.html')
    
    # Tomar captura de pantalla
    driver.save_screenshot('captura_resultados.png')
    print('   ✅ Captura guardada en: captura_resultados.png')
    
    # Buscar todos los enlaces
    print('\n5. Buscando enlaces en la página...')
    enlaces = driver.find_elements(By.TAG_NAME, 'a')
    print(f'   Se encontraron {len(enlaces)} enlaces:')
    print('   ' + '='*76)
    
    for i, enlace in enumerate(enlaces, 1):
        href = enlace.get_attribute('href')
        texto = enlace.text.strip()
        if href or texto:
            print(f'   {i}. Texto: "{texto}"')
            if href:
                print(f'      URL: {href}')
            print('   ' + '-'*76)
    
    # Buscar botones
    print('\n6. Buscando botones en la página...')
    botones = driver.find_elements(By.TAG_NAME, 'button')
    print(f'   Se encontraron {len(botones)} botones:')
    print('   ' + '='*76)
    
    for i, boton in enumerate(botones, 1):
        texto = boton.text.strip()
        onclick = boton.get_attribute('onclick')
        clase = boton.get_attribute('class')
        if texto or onclick:
            print(f'   {i}. Texto: "{texto}"')
            if clase:
                print(f'      Clase: {clase}')
            if onclick:
                print(f'      onclick: {onclick}')
            print('   ' + '-'*76)
    
    # Buscar elementos con "pdf" en el texto o atributos
    print('\n7. Buscando elementos relacionados con PDF...')
    elementos_pdf = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'PDF', 'pdf'), 'pdf') or contains(translate(@href, 'PDF', 'pdf'), 'pdf') or contains(translate(@class, 'PDF', 'pdf'), 'pdf')]")
    
    if elementos_pdf:
        print(f'   Se encontraron {len(elementos_pdf)} elementos con "pdf":')
        print('   ' + '='*76)
        for i, elem in enumerate(elementos_pdf, 1):
            tag = elem.tag_name
            texto = elem.text.strip()
            href = elem.get_attribute('href')
            clase = elem.get_attribute('class')
            print(f'   {i}. Tag: <{tag}>')
            if texto:
                print(f'      Texto: "{texto}"')
            if href:
                print(f'      href: {href}')
            if clase:
                print(f'      class: {clase}')
            print('   ' + '-'*76)
    else:
        print('   ⚠️  No se encontraron elementos con "pdf"')
    
    # Buscar elementos con "descargar" en el texto
    print('\n8. Buscando elementos relacionados con "descargar"...')
    elementos_descargar = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'DESCARGAR', 'descargar'), 'descargar')]")
    
    if elementos_descargar:
        print(f'   Se encontraron {len(elementos_descargar)} elementos con "descargar":')
        print('   ' + '='*76)
        for i, elem in enumerate(elementos_descargar, 1):
            tag = elem.tag_name
            texto = elem.text.strip()
            href = elem.get_attribute('href')
            onclick = elem.get_attribute('onclick')
            print(f'   {i}. Tag: <{tag}>')
            if texto:
                print(f'      Texto: "{texto}"')
            if href:
                print(f'      href: {href}')
            if onclick:
                print(f'      onclick: {onclick}')
            print('   ' + '-'*76)
    else:
        print('   ⚠️  No se encontraron elementos con "descargar"')
    
    print('\n9. Información adicional:')
    print(f'   URL actual: {driver.current_url}')
    print(f'   Título: {driver.title}')
    
    print('\n✅ Inspección completada!')
    print('\nRevisa los archivos:')
    print('   - pagina_resultados.html')
    print('   - captura_resultados.png')
    
    print('\nManteniendo navegador abierto por 30 segundos para inspección manual...')
    time.sleep(30)
    
except Exception as e:
    print(f'\n❌ Error: {e}')
    import traceback
    traceback.print_exc()
    time.sleep(10)

finally:
    driver.quit()
    print('\n🔒 Navegador cerrado')

