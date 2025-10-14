#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extraer puntajes de resultados ICFES directamente desde la página web
y generar archivo Excel consolidado.

Fase 2 del proyecto: Extracción de puntajes y consolidación en Excel
"""

import pandas as pd
import os
import sys
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select

# Configuración
ARCHIVO_EXCEL_ENTRADA = 'INSCRITOS_EXAMEN SABER 11 (36).xls'
ARCHIVO_EXCEL_SALIDA = 'RESULTADOS-ICFES-AULA-REGULAR.xlsx'
CARPETA_LOGS = 'logs'
URL_ICFES = 'http://resultadossaber11.icfes.edu.co/'

# Mapeo de tipos de documento
TIPOS_DOCUMENTO = {
    'TI': 'TARJETA DE IDENTIDAD',
    'CC': 'CÉDULA DE CIUDADANÍA'
}

class ExtractorPuntajesICFES:
    """Clase para extraer puntajes de resultados ICFES desde la web"""
    
    def __init__(self, modo_prueba=False):
        self.modo_prueba = modo_prueba
        self.driver = None
        self.resultados = []
        self.errores = []
        
    def iniciar_navegador(self):
        """Inicia el navegador Firefox"""
        print('\n🌐 Iniciando navegador Firefox...')
        
        options = Options()
        # No usar headless para poder resolver CAPTCHAs
        # options.add_argument('--headless')
        
        self.driver = webdriver.Firefox(options=options)
        self.driver.maximize_window()
        print('✅ Navegador iniciado')
        
    def navegar_a_icfes(self):
        """Navega a la página del ICFES"""
        print(f'\n🌐 Navegando a: {URL_ICFES}')
        self.driver.get(URL_ICFES)
        time.sleep(3)
        print('✅ Página cargada')
        
    def ingresar_datos_estudiante(self, tipo_doc, numero_doc):
        """Ingresa los datos del estudiante en el formulario"""
        try:
            print(f'\n📝 Ingresando datos: {tipo_doc} - {numero_doc}')
            
            # Seleccionar tipo de documento
            wait = WebDriverWait(self.driver, 10)
            
            # Buscar el ng-select para tipo de documento
            print('   - Buscando selector de tipo de documento...')
            ng_select = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'ng-select[formcontrolname="tipoDocumento"]')
            ))
            
            # Hacer clic en el ng-select
            ng_select.click()
            time.sleep(1)
            
            # Buscar la opción correcta
            tipo_doc_texto = TIPOS_DOCUMENTO.get(tipo_doc, tipo_doc)
            print(f'   - Buscando opción: {tipo_doc_texto}')
            
            opciones = self.driver.find_elements(By.CSS_SELECTOR, '.ng-option')
            for opcion in opciones:
                if tipo_doc_texto.upper() in opcion.text.upper():
                    opcion.click()
                    print(f'   ✅ Tipo de documento seleccionado: {tipo_doc_texto}')
                    break
            
            time.sleep(1)
            
            # Ingresar número de documento
            print('   - Ingresando número de documento...')
            campo_doc = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[formcontrolname="numeroDocumento"]')
            ))
            campo_doc.clear()
            campo_doc.send_keys(str(numero_doc))
            print(f'   ✅ Número de documento ingresado: {numero_doc}')
            
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f'   ❌ Error al ingresar datos: {e}')
            return False
    
    def esperar_login_manual(self):
        """Espera a que el usuario resuelva el CAPTCHA y haga login"""
        print('\n⏸️  PAUSA PARA LOGIN MANUAL')
        print('='*80)
        print('👉 Por favor:')
        print('   1. Resuelve el CAPTCHA')
        print('   2. Haz clic en "Ingresar"')
        print('   3. Espera a que cargue la página de resultados')
        print('   4. Presiona ENTER en esta terminal cuando veas los resultados')
        print('='*80)
        
        input('\n⏸️  Presiona ENTER cuando hayas completado el login y veas los resultados...')
        
        print('\n✅ Continuando con la extracción de puntajes...')
        time.sleep(2)
        
    def extraer_puntaje_global(self):
        """Extrae el puntaje global de la página principal"""
        try:
            print('\n🔍 Extrayendo puntaje global...')

            # Esperar a que la página esté cargada
            time.sleep(3)

            # Obtener el HTML de la página
            html = self.driver.page_source

            # Buscar el puntaje global (formato: XXX/500)
            puntaje_global = None
            match_global = re.search(r'(\d{1,3})/500', html)
            if match_global:
                puntaje_global = int(match_global.group(1))
                print(f'   ✅ Puntaje Global: {puntaje_global}/500')
            else:
                print('   ⚠️  Puntaje Global no encontrado en HTML')
                # Intentar buscar en el texto visible
                try:
                    body_text = self.driver.find_element(By.TAG_NAME, 'body').text
                    match_text = re.search(r'(\d{1,3})/500', body_text)
                    if match_text:
                        puntaje_global = int(match_text.group(1))
                        print(f'   ✅ Puntaje Global encontrado en texto: {puntaje_global}/500')
                except:
                    pass

            return puntaje_global

        except Exception as e:
            print(f'   ❌ Error al extraer puntaje global: {e}')
            return None

    def extraer_puntaje_de_area(self, nombre_area):
        """
        Hace clic en un área específica y extrae su puntaje

        Args:
            nombre_area: Nombre del área (ej: "Lectura Crítica")

        Returns:
            int: Puntaje del área o None si no se pudo extraer
        """
        try:
            print(f'\n   🔍 Extrayendo puntaje de: {nombre_area}')

            # Guardar URL actual para volver
            url_principal = self.driver.current_url

            # Buscar el elemento clickeable del área
            # Intentar varios selectores posibles
            selectores = [
                f"//a[contains(text(), '{nombre_area}')]",
                f"//button[contains(text(), '{nombre_area}')]",
                f"//div[contains(text(), '{nombre_area}')]",
                f"//*[contains(text(), '{nombre_area}') and (self::a or self::button or self::div)]"
            ]

            elemento_clickeado = False
            for selector in selectores:
                try:
                    wait = WebDriverWait(self.driver, 5)
                    elemento = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))

                    if elemento.is_displayed():
                        print(f'      ✅ Elemento encontrado, haciendo clic...')
                        elemento.click()
                        elemento_clickeado = True
                        time.sleep(3)  # Esperar a que cargue la nueva vista
                        break
                except:
                    continue

            if not elemento_clickeado:
                print(f'      ⚠️  No se pudo hacer clic en el área')
                return None

            # Buscar el puntaje en la nueva página
            # El puntaje podría estar en diferentes formatos
            html = self.driver.page_source
            body_text = self.driver.find_element(By.TAG_NAME, 'body').text

            # Patrones para buscar puntajes
            patrones = [
                r'Puntaje[:\s]+(\d{1,3})',
                r'puntaje[:\s]+(\d{1,3})',
                r'PUNTAJE[:\s]+(\d{1,3})',
                r'Score[:\s]+(\d{1,3})',
                r'(\d{1,3})\s*/\s*100',
                r'Tu puntaje[:\s]+(\d{1,3})',
            ]

            puntaje = None
            for patron in patrones:
                match = re.search(patron, body_text, re.IGNORECASE)
                if match:
                    puntaje_candidato = int(match.group(1))
                    # Validar que sea un puntaje razonable (0-100)
                    if 0 <= puntaje_candidato <= 100:
                        puntaje = puntaje_candidato
                        print(f'      ✅ Puntaje encontrado: {puntaje}')
                        break

            if puntaje is None:
                print(f'      ⚠️  No se encontró puntaje en la página del área')
                # Guardar HTML para análisis
                with open(f'debug_{nombre_area.replace(" ", "_")}.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f'      💾 HTML guardado para análisis: debug_{nombre_area.replace(" ", "_")}.html')

            # Volver a la página principal
            self.driver.back()
            time.sleep(2)

            return puntaje

        except Exception as e:
            print(f'      ❌ Error al extraer puntaje de {nombre_area}: {e}')
            # Intentar volver a la página principal
            try:
                self.driver.back()
                time.sleep(2)
            except:
                pass
            return None

    def extraer_puntajes_de_pagina(self):
        """Extrae todos los puntajes de la página de resultados"""
        try:
            print('\n🔍 Extrayendo puntajes de la página...')

            # Extraer puntaje global
            puntaje_global = self.extraer_puntaje_global()

            # Áreas a extraer
            areas = {
                'Lectura Crítica': 'Lectura Crítica',
                'Matemáticas': 'Matemáticas',
                'Sociales y Ciudadanas': 'Sociales y Ciudadanas',
                'Ciencias Naturales': 'Ciencias Naturales',
                'Inglés': 'Inglés'
            }

            puntajes = {
                'Puntaje Global': puntaje_global
            }

            # Extraer puntaje de cada área
            for nombre_area, clave in areas.items():
                puntaje_area = self.extraer_puntaje_de_area(nombre_area)
                puntajes[clave] = puntaje_area

            # Mostrar resumen
            print('\n📊 RESUMEN DE PUNTAJES EXTRAÍDOS:')
            print('   ' + '-'*60)
            for area, puntaje in puntajes.items():
                if puntaje is not None:
                    print(f'   ✅ {area}: {puntaje}')
                else:
                    print(f'   ❌ {area}: No extraído')
            print('   ' + '-'*60)

            return puntajes

        except Exception as e:
            print(f'   ❌ Error al extraer puntajes: {e}')
            return None
    
    def hacer_logout(self):
        """Cierra la sesión del estudiante"""
        try:
            print('\n🚪 Cerrando sesión...')
            
            # Buscar el menú de usuario
            wait = WebDriverWait(self.driver, 5)
            boton_menu = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.dropdown-toggle')
            ))
            boton_menu.click()
            time.sleep(1)
            
            # Buscar la opción de "Salir"
            opciones_menu = self.driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu a, .dropdown-menu button')
            
            for opcion in opciones_menu:
                texto = opcion.text.strip().lower()
                if 'salir' in texto or 'cerrar' in texto or 'logout' in texto:
                    opcion.click()
                    print('   ✅ Sesión cerrada')
                    time.sleep(2)
                    return True
            
            # Si no encontramos opción de salir, navegar a login
            self.driver.get(URL_ICFES)
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f'   ⚠️  Error al cerrar sesión: {e}')
            self.driver.get(URL_ICFES)
            time.sleep(2)
            return True
    
    def procesar_estudiante(self, estudiante):
        """Procesa un estudiante completo"""
        nombre_completo = f"{estudiante['Primer Apellido']} {estudiante['Segundo Apellido']} {estudiante['Primer Nombre']} {estudiante.get('Segundo Nombre', '')}".strip()
        
        print('\n' + '='*80)
        print(f'👤 PROCESANDO: {nombre_completo}')
        print('='*80)
        
        try:
            # Navegar a la página
            self.navegar_a_icfes()
            
            # Ingresar datos
            if not self.ingresar_datos_estudiante(estudiante['Tipo de documento'], estudiante['Número de documento']):
                raise Exception('Error al ingresar datos')
            
            # Esperar login manual
            self.esperar_login_manual()
            
            # Extraer puntajes
            puntajes = self.extraer_puntajes_de_pagina()
            
            if puntajes:
                resultado = {
                    'Primer Apellido': estudiante['Primer Apellido'],
                    'Segundo Apellido': estudiante['Segundo Apellido'],
                    'Primer Nombre': estudiante['Primer Nombre'],
                    'Segundo Nombre': estudiante.get('Segundo Nombre', ''),
                    'Tipo de documento': estudiante['Tipo de documento'],
                    'Número de documento': estudiante['Número de documento'],
                    **puntajes
                }
                self.resultados.append(resultado)
                print(f'\n✅ Estudiante procesado exitosamente')
            else:
                raise Exception('No se pudieron extraer puntajes')
            
            # Cerrar sesión
            self.hacer_logout()
            
            return True
            
        except Exception as e:
            print(f'\n❌ Error al procesar estudiante: {e}')
            self.errores.append({
                'estudiante': nombre_completo,
                'error': str(e)
            })
            return False
    
    def cerrar_navegador(self):
        """Cierra el navegador"""
        if self.driver:
            print('\n🔒 Cerrando navegador...')
            self.driver.quit()
            print('✅ Navegador cerrado')

def main():
    """Función principal"""
    print('\n' + '='*80)
    print('🎓 EXTRACTOR DE PUNTAJES ICFES - FASE 2')
    print('='*80)
    
    # Verificar archivo de entrada
    if not os.path.exists(ARCHIVO_EXCEL_ENTRADA):
        print(f'\n❌ Error: No se encuentra el archivo {ARCHIVO_EXCEL_ENTRADA}')
        sys.exit(1)
    
    # Leer archivo Excel
    print(f'\n📂 Leyendo archivo: {ARCHIVO_EXCEL_ENTRADA}')
    df = pd.read_excel(ARCHIVO_EXCEL_ENTRADA, skiprows=3)
    print(f'✅ {len(df)} estudiantes encontrados')
    
    # Preguntar modo
    print('\n' + '='*80)
    print('SELECCIONA EL MODO DE EJECUCIÓN:')
    print('='*80)
    print('1. Modo PRUEBA (solo 1 estudiante)')
    print('2. Modo COMPLETO (todos los estudiantes)')
    print('='*80)
    
    opcion = input('\nSelecciona una opción (1 o 2): ').strip()
    
    modo_prueba = (opcion == '1')
    
    if modo_prueba:
        print('\n🧪 Modo PRUEBA activado (1 estudiante)')
        df = df.head(1)
    else:
        print(f'\n🚀 Modo COMPLETO activado ({len(df)} estudiantes)')
    
    # Crear extractor
    extractor = ExtractorPuntajesICFES(modo_prueba=modo_prueba)
    
    try:
        # Iniciar navegador
        extractor.iniciar_navegador()
        
        # Procesar estudiantes
        for idx, estudiante in df.iterrows():
            extractor.procesar_estudiante(estudiante)
            
            if not modo_prueba and idx < len(df) - 1:
                print('\n⏸️  Pausa de 3 segundos antes del siguiente estudiante...')
                time.sleep(3)
        
        # Generar Excel de salida
        if extractor.resultados:
            print('\n' + '='*80)
            print('📊 GENERANDO ARCHIVO EXCEL')
            print('='*80)
            
            df_resultados = pd.DataFrame(extractor.resultados)
            df_resultados.to_excel(ARCHIVO_EXCEL_SALIDA, index=False)
            
            print(f'\n✅ Archivo generado: {ARCHIVO_EXCEL_SALIDA}')
            print(f'📊 Total de estudiantes: {len(df_resultados)}')
        
        # Mostrar resumen
        print('\n' + '='*80)
        print('📊 RESUMEN FINAL')
        print('='*80)
        print(f'✅ Estudiantes procesados: {len(extractor.resultados)}')
        print(f'❌ Errores: {len(extractor.errores)}')
        
        if extractor.errores:
            print('\n⚠️  Estudiantes con errores:')
            for error in extractor.errores:
                print(f'   - {error["estudiante"]}: {error["error"]}')
        
    finally:
        extractor.cerrar_navegador()
    
    print('\n' + '='*80)
    print('✅ PROCESO COMPLETADO')
    print('='*80)

if __name__ == '__main__':
    main()

