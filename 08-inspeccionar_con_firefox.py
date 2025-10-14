#!/usr/bin/env python3
"""
Script para inspeccionar el sitio web del ICFES usando Selenium con Firefox
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

def inspeccionar_sitio():
    """Inspecciona el sitio web del ICFES para entender su estructura"""
    
    print('=' * 80)
    print('INSPECCIÓN DEL SITIO WEB DEL ICFES CON FIREFOX')
    print('=' * 80)
    
    # Configurar opciones de Firefox
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Ejecutar sin interfaz gráfica
    
    print('\n🌐 Iniciando navegador Firefox...')
    
    driver = None
    try:
        # Inicializar el driver
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        # Navegar al sitio
        url = 'http://resultadossaber11.icfes.edu.co/'
        print(f'\n📍 Navegando a: {url}')
        driver.get(url)
        
        # Esperar a que la página cargue (Angular necesita tiempo)
        print('\n⏳ Esperando a que la página cargue...')
        time.sleep(5)
        
        print(f'\n📄 Título de la página: {driver.title}')
        print(f'🔗 URL actual: {driver.current_url}')
        
        # Guardar el HTML de la página después de que JavaScript se ejecute
        with open('pagina_login_completa.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print('\n💾 HTML completo guardado en: pagina_login_completa.html')
        
        # Buscar formularios
        print('\n🔍 Buscando formularios...')
        forms = driver.find_elements(By.TAG_NAME, 'form')
        print(f'   Formularios encontrados: {len(forms)}')
        
        # Buscar campos de entrada
        print('\n📝 Buscando campos de entrada...')
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        print(f'   Total de inputs: {len(inputs)}')
        
        for i, input_elem in enumerate(inputs, 1):
            try:
                input_type = input_elem.get_attribute('type')
                input_name = input_elem.get_attribute('name')
                input_id = input_elem.get_attribute('id')
                input_placeholder = input_elem.get_attribute('placeholder')
                input_class = input_elem.get_attribute('class')
                is_visible = input_elem.is_displayed()
                
                print(f'\n   Input #{i}:')
                print(f'      - Tipo: {input_type}')
                print(f'      - Name: {input_name}')
                print(f'      - ID: {input_id}')
                print(f'      - Placeholder: {input_placeholder}')
                print(f'      - Class: {input_class}')
                print(f'      - Visible: {is_visible}')
            except Exception as e:
                print(f'   Input #{i}: Error al obtener atributos - {e}')
        
        # Buscar selects (desplegables)
        print('\n📋 Buscando campos select...')
        selects = driver.find_elements(By.TAG_NAME, 'select')
        print(f'   Total de selects: {len(selects)}')
        
        for i, select_elem in enumerate(selects, 1):
            try:
                select_name = select_elem.get_attribute('name')
                select_id = select_elem.get_attribute('id')
                is_visible = select_elem.is_displayed()
                
                print(f'\n   Select #{i}:')
                print(f'      - Name: {select_name}')
                print(f'      - ID: {select_id}')
                print(f'      - Visible: {is_visible}')
                
                # Obtener opciones
                options = select_elem.find_elements(By.TAG_NAME, 'option')
                print(f'      - Opciones ({len(options)}):')
                for opt in options[:10]:  # Mostrar solo las primeras 10
                    print(f'         * {opt.get_attribute("value")} - {opt.text}')
            except Exception as e:
                print(f'   Select #{i}: Error al obtener atributos - {e}')
        
        # Buscar botones
        print('\n🔘 Buscando botones...')
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        print(f'   Total de botones: {len(buttons)}')
        
        for i, button in enumerate(buttons, 1):
            try:
                button_text = button.text
                button_type = button.get_attribute('type')
                button_class = button.get_attribute('class')
                is_visible = button.is_displayed()
                
                print(f'\n   Botón #{i}:')
                print(f'      - Texto: {button_text}')
                print(f'      - Tipo: {button_type}')
                print(f'      - Class: {button_class}')
                print(f'      - Visible: {is_visible}')
            except Exception as e:
                print(f'   Botón #{i}: Error al obtener atributos - {e}')
        
        # Buscar CAPTCHAs
        print('\n🤖 Buscando CAPTCHAs...')
        
        # Buscar reCAPTCHA
        try:
            recaptcha = driver.find_elements(By.CLASS_NAME, 'g-recaptcha')
            if recaptcha:
                print(f'   ⚠️  reCAPTCHA detectado! ({len(recaptcha)} elementos)')
                for i, elem in enumerate(recaptcha, 1):
                    print(f'      - reCAPTCHA #{i}:')
                    print(f'         * Site key: {elem.get_attribute("data-sitekey")}')
                    print(f'         * Visible: {elem.is_displayed()}')
        except Exception as e:
            print(f'   Error buscando reCAPTCHA: {e}')
        
        # Buscar iframes (común en CAPTCHAs)
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        print(f'\n🖼️  Iframes encontrados: {len(iframes)}')
        for i, iframe in enumerate(iframes, 1):
            try:
                iframe_src = iframe.get_attribute('src')
                iframe_title = iframe.get_attribute('title')
                print(f'      - Iframe #{i}:')
                print(f'         * Src: {iframe_src}')
                print(f'         * Title: {iframe_title}')
            except Exception as e:
                print(f'      - Iframe #{i}: Error - {e}')
        
        # Tomar captura de pantalla
        driver.save_screenshot('captura_login_firefox.png')
        print('\n📸 Captura de pantalla guardada en: captura_login_firefox.png')
        
        print('\n✅ Inspección completada!')
        
    except Exception as e:
        print(f'\n❌ Error durante la inspección: {e}')
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
            print('\n🔒 Navegador cerrado.')

if __name__ == '__main__':
    inspeccionar_sitio()

