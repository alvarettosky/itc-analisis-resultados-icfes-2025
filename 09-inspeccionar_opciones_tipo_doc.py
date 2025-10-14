#!/usr/bin/env python3
"""
Script para inspeccionar las opciones del selector de tipo de documento
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

# Configurar Firefox
firefox_options = Options()
# firefox_options.add_argument('--headless')  # Comentado para ver el navegador

service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    print('Navegando al portal ICFES...')
    driver.get('http://resultadossaber11.icfes.edu.co/')
    
    # Esperar a que la página cargue
    time.sleep(5)
    
    print('\nBuscando el ng-select...')
    wait = WebDriverWait(driver, 10)
    
    # Hacer clic en el ng-select para abrirlo
    ng_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ng-select')))
    print('ng-select encontrado, haciendo clic...')
    ng_select.click()
    
    # Esperar a que aparezcan las opciones
    time.sleep(2)
    
    # Buscar todas las opciones
    print('\nBuscando opciones...')
    opciones = driver.find_elements(By.CSS_SELECTOR, '.ng-option')
    
    print(f'\n✅ Se encontraron {len(opciones)} opciones:\n')
    print('='*80)
    
    for i, opcion in enumerate(opciones, 1):
        texto = opcion.text
        print(f'{i}. "{texto}"')
        
        # Intentar obtener atributos adicionales
        try:
            value = opcion.get_attribute('value')
            if value:
                print(f'   value="{value}"')
        except:
            pass
        
        print('-'*80)
    
    print('\n✅ Inspección completada')
    
    # Mantener el navegador abierto por 10 segundos para inspección manual
    print('\nManteniendo navegador abierto por 10 segundos...')
    time.sleep(10)
    
except Exception as e:
    print(f'\n❌ Error: {e}')
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print('\nNavegador cerrado')

