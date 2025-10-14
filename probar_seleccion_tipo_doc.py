#!/usr/bin/env python3
"""
Script para probar la selección del tipo de documento
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

# Mapeo de tipos de documento
mapeo_tipos_doc = {
    'TI': 'TARJETA DE IDENTIDAD',
    'CC': 'CÉDULA DE CIUDADANÍA',
    'CE': 'CÉDULA DE EXTRANJERÍA',
}

def probar_seleccion(tipo_doc_excel):
    """Prueba la selección de un tipo de documento"""
    
    # Configurar Firefox
    firefox_options = Options()
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
    try:
        print(f'\n{"="*80}')
        print(f'PROBANDO: {tipo_doc_excel}')
        print(f'{"="*80}')
        
        print('\n1. Navegando al portal ICFES...')
        driver.get('http://resultadossaber11.icfes.edu.co/')
        time.sleep(5)
        
        print('2. Buscando el ng-select...')
        wait = WebDriverWait(driver, 10)
        
        # Obtener el texto completo para buscar
        tipo_doc_formulario = mapeo_tipos_doc.get(tipo_doc_excel, tipo_doc_excel)
        
        print(f'3. Haciendo clic en el ng-select...')
        ng_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ng-select')))
        ng_select.click()
        time.sleep(1)
        
        print(f'4. Buscando la opción: "{tipo_doc_formulario}"...')
        opciones = driver.find_elements(By.CSS_SELECTOR, '.ng-option')
        
        opcion_encontrada = False
        for opcion in opciones:
            texto_opcion = opcion.text.strip().upper()
            if tipo_doc_formulario.upper() == texto_opcion:
                print(f'   ✅ Opción encontrada: "{opcion.text}"')
                print(f'5. Haciendo clic en la opción...')
                opcion.click()
                opcion_encontrada = True
                break
        
        if not opcion_encontrada:
            print(f'   ❌ Opción NO encontrada')
            print(f'\n   Opciones disponibles:')
            for i, opcion in enumerate(opciones, 1):
                print(f'      {i}. {opcion.text}')
            return False
        
        time.sleep(2)
        
        # Verificar que se seleccionó correctamente
        print('6. Verificando selección...')
        ng_value = driver.find_element(By.CSS_SELECTOR, '.ng-value')
        texto_seleccionado = ng_value.text
        print(f'   Texto seleccionado: "{texto_seleccionado}"')
        
        if tipo_doc_formulario.upper() in texto_seleccionado.upper():
            print(f'\n✅ ¡ÉXITO! Se seleccionó correctamente: {tipo_doc_excel} → {tipo_doc_formulario}')
            time.sleep(3)
            return True
        else:
            print(f'\n❌ ERROR: Se esperaba "{tipo_doc_formulario}" pero se obtuvo "{texto_seleccionado}"')
            time.sleep(3)
            return False
        
    except Exception as e:
        print(f'\n❌ Error: {e}')
        import traceback
        traceback.print_exc()
        time.sleep(3)
        return False
    
    finally:
        driver.quit()
        print('\nNavegador cerrado\n')


def main():
    """Función principal"""
    print('='*80)
    print('PRUEBA DE SELECCIÓN DE TIPO DE DOCUMENTO')
    print('='*80)
    
    # Probar los dos tipos más comunes
    tipos_a_probar = ['TI', 'CC']
    
    resultados = {}
    
    for tipo in tipos_a_probar:
        resultado = probar_seleccion(tipo)
        resultados[tipo] = resultado
        time.sleep(2)
    
    # Resumen
    print('\n' + '='*80)
    print('RESUMEN DE PRUEBAS')
    print('='*80)
    
    for tipo, resultado in resultados.items():
        estado = '✅ ÉXITO' if resultado else '❌ FALLO'
        print(f'{tipo}: {estado}')
    
    print('='*80)
    
    if all(resultados.values()):
        print('\n✅ ¡TODAS LAS PRUEBAS PASARON!')
        print('El script principal debería funcionar correctamente.')
    else:
        print('\n❌ ALGUNAS PRUEBAS FALLARON')
        print('Revisa el código antes de ejecutar el script principal.')


if __name__ == '__main__':
    main()

