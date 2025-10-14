#!/usr/bin/env python3
"""
Script para inspeccionar el sitio web del ICFES y entender su estructura
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def inspeccionar_sitio():
    """Inspecciona el sitio web del ICFES para entender su estructura"""
    
    print('=' * 80)
    print('INSPECCIÓN DEL SITIO WEB DEL ICFES')
    print('=' * 80)
    
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Ejecutar sin interfaz gráfica
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    print('\n🌐 Iniciando navegador...')
    
    try:
        # Inicializar el driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Navegar al sitio
        url = 'http://resultadossaber11.icfes.edu.co/'
        print(f'\n📍 Navegando a: {url}')
        driver.get(url)
        
        # Esperar a que la página cargue
        time.sleep(3)
        
        print(f'\n📄 Título de la página: {driver.title}')
        print(f'🔗 URL actual: {driver.current_url}')
        
        # Guardar el HTML de la página
        with open('pagina_login.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print('\n💾 HTML guardado en: pagina_login.html')
        
        # Buscar formularios
        print('\n🔍 Buscando formularios...')
        forms = driver.find_elements(By.TAG_NAME, 'form')
        print(f'   Formularios encontrados: {len(forms)}')
        
        # Buscar campos de entrada
        print('\n📝 Buscando campos de entrada...')
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        print(f'   Total de inputs: {len(inputs)}')
        
        for i, input_elem in enumerate(inputs, 1):
            input_type = input_elem.get_attribute('type')
            input_name = input_elem.get_attribute('name')
            input_id = input_elem.get_attribute('id')
            input_placeholder = input_elem.get_attribute('placeholder')
            input_class = input_elem.get_attribute('class')
            
            print(f'\n   Input #{i}:')
            print(f'      - Tipo: {input_type}')
            print(f'      - Name: {input_name}')
            print(f'      - ID: {input_id}')
            print(f'      - Placeholder: {input_placeholder}')
            print(f'      - Class: {input_class}')
        
        # Buscar selects (desplegables)
        print('\n📋 Buscando campos select...')
        selects = driver.find_elements(By.TAG_NAME, 'select')
        print(f'   Total de selects: {len(selects)}')
        
        for i, select_elem in enumerate(selects, 1):
            select_name = select_elem.get_attribute('name')
            select_id = select_elem.get_attribute('id')
            
            print(f'\n   Select #{i}:')
            print(f'      - Name: {select_name}')
            print(f'      - ID: {select_id}')
            
            # Obtener opciones
            options = select_elem.find_elements(By.TAG_NAME, 'option')
            print(f'      - Opciones ({len(options)}):')
            for opt in options[:10]:  # Mostrar solo las primeras 10
                print(f'         * {opt.get_attribute("value")} - {opt.text}')
        
        # Buscar botones
        print('\n🔘 Buscando botones...')
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        print(f'   Total de botones: {len(buttons)}')
        
        for i, button in enumerate(buttons, 1):
            button_text = button.text
            button_type = button.get_attribute('type')
            button_class = button.get_attribute('class')
            
            print(f'\n   Botón #{i}:')
            print(f'      - Texto: {button_text}')
            print(f'      - Tipo: {button_type}')
            print(f'      - Class: {button_class}')
        
        # Buscar CAPTCHAs
        print('\n🤖 Buscando CAPTCHAs...')
        
        # Buscar reCAPTCHA
        recaptcha = driver.find_elements(By.CLASS_NAME, 'g-recaptcha')
        if recaptcha:
            print('   ⚠️  reCAPTCHA detectado!')
        
        # Buscar hCaptcha
        hcaptcha = driver.find_elements(By.CLASS_NAME, 'h-captcha')
        if hcaptcha:
            print('   ⚠️  hCaptcha detectado!')
        
        # Buscar iframes (común en CAPTCHAs)
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        print(f'   Iframes encontrados: {len(iframes)}')
        for i, iframe in enumerate(iframes, 1):
            iframe_src = iframe.get_attribute('src')
            print(f'      - Iframe #{i}: {iframe_src}')
        
        # Tomar captura de pantalla
        driver.save_screenshot('captura_login.png')
        print('\n📸 Captura de pantalla guardada en: captura_login.png')
        
        print('\n✅ Inspección completada!')
        
    except Exception as e:
        print(f'\n❌ Error durante la inspección: {e}')
        import traceback
        traceback.print_exc()
    
    finally:
        if 'driver' in locals():
            driver.quit()
            print('\n🔒 Navegador cerrado.')

if __name__ == '__main__':
    inspeccionar_sitio()

