#!/usr/bin/env python3
"""
Script para descargar automáticamente los resultados del ICFES Saber 11
Autor: Automatización ICFES
Fecha: 2025-10-14
"""

import pandas as pd
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager

# Configuración
EXCEL_PATH = '/home/proyectos/Escritorio/Resultados-ICFES-2025/INSCRITOS_EXAMEN SABER 11 (36).xls'
URL_ICFES = 'http://resultadossaber11.icfes.edu.co/'
CARPETA_PDFS = 'pdfs_descargados'
CARPETA_LOGS = 'logs'
DELAY_ENTRE_ESTUDIANTES = 3  # segundos

# Crear carpetas si no existen
os.makedirs(CARPETA_PDFS, exist_ok=True)
os.makedirs(CARPETA_LOGS, exist_ok=True)


class DescargadorICFES:
    """Clase para manejar la descarga de resultados del ICFES"""
    
    def __init__(self, modo_headless=False):
        """
        Inicializa el descargador
        
        Args:
            modo_headless: Si True, ejecuta el navegador sin interfaz gráfica
        """
        self.modo_headless = modo_headless
        self.driver = None
        self.estudiantes_exitosos = []
        self.estudiantes_error = []
        self.estudiantes_sin_resultados = []
        
    def iniciar_navegador(self):
        """Inicia el navegador Firefox"""
        print('\n🌐 Iniciando navegador Firefox...')

        firefox_options = Options()
        if self.modo_headless:
            firefox_options.add_argument('--headless')

        # Configurar carpeta de descargas
        download_dir = os.path.abspath(CARPETA_PDFS)

        # Configuraciones para descargar PDFs automáticamente
        firefox_options.set_preference('browser.download.folderList', 2)
        firefox_options.set_preference('browser.download.dir', download_dir)
        firefox_options.set_preference('browser.download.useDownloadDir', True)
        firefox_options.set_preference('browser.download.manager.showWhenStarting', False)

        # Configurar para descargar PDFs automáticamente sin preguntar
        firefox_options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
        firefox_options.set_preference('browser.helperApps.neverAsk.openFile', 'application/pdf')

        # Deshabilitar el visor de PDF integrado de Firefox
        firefox_options.set_preference('pdfjs.disabled', True)

        # Configurar para que no abra PDFs en el navegador
        firefox_options.set_preference('browser.download.open_pdf_attachments_inline', False)

        # Deshabilitar la vista previa de impresión
        firefox_options.set_preference('print.always_print_silent', True)
        firefox_options.set_preference('print.show_print_progress', False)

        print(f'   📁 Carpeta de descargas: {download_dir}')

        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        self.driver.maximize_window()

        print('✅ Navegador iniciado correctamente')
    
    def cerrar_navegador(self):
        """Cierra el navegador"""
        if self.driver:
            self.driver.quit()
            print('\n🔒 Navegador cerrado')
    
    def leer_excel(self):
        """Lee el archivo Excel y retorna un DataFrame con los estudiantes"""
        print(f'\n📖 Leyendo archivo Excel: {EXCEL_PATH}')
        
        # Leer el archivo saltando las primeras 3 filas de encabezado
        df = pd.read_excel(EXCEL_PATH, skiprows=3)
        
        # La primera fila contiene los nombres de las columnas
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        
        print(f'✅ Se encontraron {len(df)} estudiantes')
        
        return df
    
    def construir_nombre_archivo(self, estudiante):
        """
        Construye el nombre del archivo PDF basado en los datos del estudiante
        
        Args:
            estudiante: Serie de pandas con los datos del estudiante
            
        Returns:
            Nombre del archivo sin extensión
        """
        primer_apellido = str(estudiante['Primer Apellido']).strip().upper()
        segundo_apellido = str(estudiante['Segundo Apellido']).strip().upper()
        primer_nombre = str(estudiante['Primer Nombre']).strip().upper()
        segundo_nombre = str(estudiante['Segundo Nombre ']).strip().upper()
        num_documento = str(estudiante['Número de documento']).strip()
        
        # Construir nombre completo
        apellidos = f"{primer_apellido}_{segundo_apellido}"
        
        if segundo_nombre != 'NAN':
            nombres = f"{primer_nombre}_{segundo_nombre}"
        else:
            nombres = primer_nombre
        
        nombre_archivo = f"{apellidos}_{nombres}_{num_documento}"
        
        # Limpiar caracteres no válidos
        caracteres_invalidos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in caracteres_invalidos:
            nombre_archivo = nombre_archivo.replace(char, '_')
        
        return nombre_archivo
    
    def navegar_a_login(self):
        """Navega a la página de login del ICFES"""
        print(f'\n📍 Navegando a: {URL_ICFES}')
        self.driver.get(URL_ICFES)
        
        # Esperar a que la página cargue
        time.sleep(3)
        
        print('✅ Página cargada')
    
    def llenar_formulario(self, estudiante):
        """
        Llena el formulario de login con los datos del estudiante

        Args:
            estudiante: Serie de pandas con los datos del estudiante
        """
        wait = WebDriverWait(self.driver, 10)

        tipo_doc = str(estudiante['Tipo documento']).strip().upper()
        num_doc = str(estudiante['Número de documento']).strip()
        num_registro = str(estudiante['Número de registro']).strip()

        print(f'\n📝 Llenando formulario para: {estudiante["Primer Nombre"]} {estudiante["Primer Apellido"]}')
        print(f'   Tipo doc: {tipo_doc}, Núm doc: {num_doc}, Núm registro: {num_registro}')

        # Mapeo de tipos de documento del Excel a las opciones del formulario web
        mapeo_tipos_doc = {
            'TI': 'TARJETA DE IDENTIDAD',
            'CC': 'CÉDULA DE CIUDADANÍA',
            'CE': 'CÉDULA DE EXTRANJERÍA',
            'CR': 'CONTRASEÑA REGISTRADURÍA',
            'PC': 'PASAPORTE COLOMBIANO',
            'PE': 'PASAPORTE EXTRANJERO',
            'PEP': 'PERMISO ESPECIAL DE PERMANENCIA',
            'NUIP': 'NÚMERO ÚNICO DE IDENTIFICACIÓN PERSONAL',
            'RC': 'REGISTRO CIVIL DE NACIMIENTO',
        }

        # Obtener el texto completo para buscar en el formulario
        tipo_doc_formulario = mapeo_tipos_doc.get(tipo_doc, tipo_doc)

        try:
            # 1. Seleccionar tipo de documento
            print(f'   - Seleccionando tipo de documento: {tipo_doc} → {tipo_doc_formulario}...')
            # Hacer clic en el ng-select para abrirlo
            ng_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ng-select')))
            ng_select.click()
            time.sleep(1)

            # Buscar la opción correspondiente
            opciones = self.driver.find_elements(By.CSS_SELECTOR, '.ng-option')
            opcion_encontrada = False

            for opcion in opciones:
                texto_opcion = opcion.text.strip().upper()
                if tipo_doc_formulario.upper() == texto_opcion:
                    print(f'   ✅ Opción encontrada: "{opcion.text}"')
                    opcion.click()
                    opcion_encontrada = True
                    break

            if not opcion_encontrada:
                print(f'   ⚠️  No se encontró la opción exacta para "{tipo_doc_formulario}"')
                print(f'   Opciones disponibles:')
                for i, opcion in enumerate(opciones[:5], 1):
                    print(f'      {i}. {opcion.text}')
                raise Exception(f'Tipo de documento "{tipo_doc}" no encontrado en el formulario')

            time.sleep(0.5)
            
            # 2. Ingresar número de documento
            print('   - Ingresando número de documento...')
            input_identificacion = wait.until(EC.presence_of_element_located((By.ID, 'identificacion')))
            input_identificacion.clear()
            input_identificacion.send_keys(num_doc)
            time.sleep(0.5)
            
            # 3. Ingresar número de registro
            print('   - Ingresando número de registro...')
            input_registro = wait.until(EC.presence_of_element_located((By.ID, 'numeroRegistro')))
            input_registro.clear()
            input_registro.send_keys(num_registro)
            time.sleep(0.5)
            
            print('✅ Formulario llenado correctamente')
            return True
            
        except Exception as e:
            print(f'❌ Error al llenar el formulario: {e}')
            return False
    
    def esperar_captcha_manual(self):
        """
        Espera a que el usuario resuelva el CAPTCHA manualmente y haga clic en Ingresar
        """
        print('\n' + '='*80)
        print('⚠️  ATENCIÓN: CAPTCHA Y LOGIN')
        print('='*80)
        print('\n👉 Por favor, sigue estos pasos en el navegador:')
        print('   1. Resuelve el CAPTCHA (si aparece)')
        print('   2. Haz clic en el botón "Ingresar"')
        print('   3. Espera a que cargue la página de resultados')
        print('   4. Presiona ENTER aquí cuando veas los resultados')
        print('\n' + '='*80)

        input()  # Esperar a que el usuario presione ENTER

        print('\n✅ Continuando con el proceso...')
        time.sleep(2)

    def hacer_clic_ingresar(self):
        """
        Verifica si ya se hizo login o intenta hacer clic en Ingresar
        """
        try:
            # Verificar si ya estamos en la página de resultados
            if 'resultadossaber11.icfes.edu.co' in self.driver.current_url:
                # Buscar elementos que indiquen que estamos en la página de resultados
                try:
                    wait = WebDriverWait(self.driver, 3)
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//button[contains(., 'Imprimir PDF')]")
                    ))
                    print('✅ Ya estás en la página de resultados')
                    return True
                except:
                    pass

            # Si no estamos en resultados, intentar hacer clic en Ingresar
            try:
                wait = WebDriverWait(self.driver, 5)
                boton_ingresar = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Ingresar')]")
                ))
                boton_ingresar.click()
                print('✅ Clic en botón Ingresar')
                time.sleep(5)
                return True
            except:
                # Si no encontramos el botón, asumir que ya se hizo login
                print('✅ Login completado (botón Ingresar no encontrado, asumiendo que ya se hizo clic)')
                return True

        except Exception as e:
            print(f'⚠️  Advertencia: {e}')
            print('   Asumiendo que el login ya se completó manualmente')
            return True

    def hacer_logout(self):
        """
        Cierra la sesión actual para poder procesar el siguiente estudiante
        """
        try:
            print('   - Cerrando sesión...')

            # Buscar el botón del menú de usuario (con el nombre del estudiante)
            try:
                wait = WebDriverWait(self.driver, 5)
                boton_menu = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button.dropdown-toggle')
                ))
                boton_menu.click()
                time.sleep(1)

                # Buscar la opción de "Salir" o "Cerrar sesión"
                opciones_menu = self.driver.find_elements(By.CSS_SELECTOR, '.dropdown-menu a, .dropdown-menu button')

                for opcion in opciones_menu:
                    texto = opcion.text.strip().lower()
                    if 'salir' in texto or 'cerrar' in texto or 'logout' in texto:
                        opcion.click()
                        print('   ✅ Sesión cerrada')
                        time.sleep(2)
                        return True

                # Si no encontramos opción de salir, simplemente navegar a la página de login
                print('   ⚠️  No se encontró opción de salir, navegando a login...')
                self.driver.get('http://resultadossaber11.icfes.edu.co/')
                time.sleep(2)
                return True

            except:
                # Si no encontramos el menú, simplemente navegar a la página de login
                print('   ⚠️  No se encontró menú de usuario, navegando a login...')
                self.driver.get('http://resultadossaber11.icfes.edu.co/')
                time.sleep(2)
                return True

        except Exception as e:
            print(f'   ⚠️  Error al cerrar sesión: {e}')
            # Como último recurso, borrar cookies y navegar a login
            print('   - Borrando cookies y navegando a login...')
            self.driver.delete_all_cookies()
            self.driver.get('http://resultadossaber11.icfes.edu.co/')
            time.sleep(3)
            return True
    
    def descargar_pdf(self, nombre_archivo):
        """
        Busca y descarga el PDF de resultados usando print_page de Selenium

        Args:
            nombre_archivo: Nombre base para el archivo PDF
        """
        try:
            print('   - Generando PDF de la página de resultados...')

            # Esperar a que la página esté completamente cargada
            time.sleep(3)

            # Usar la función print_page de Selenium para generar el PDF
            # Esta función está disponible en Selenium 4+
            try:
                from selenium.webdriver.common.print_page_options import PrintOptions

                print('   - Usando Selenium print_page...')

                # Configurar opciones de impresión
                print_options = PrintOptions()
                print_options.page_ranges = ['1-100']  # Imprimir todas las páginas

                # Generar el PDF
                pdf_data = self.driver.print_page(print_options)

                # Guardar el PDF
                ruta_pdf = os.path.join(CARPETA_PDFS, f'{nombre_archivo}.pdf')

                # Si ya existe, agregar un número
                contador = 1
                while os.path.exists(ruta_pdf):
                    ruta_pdf = os.path.join(CARPETA_PDFS, f'{nombre_archivo}_{contador}.pdf')
                    contador += 1

                # Decodificar y guardar
                import base64
                with open(ruta_pdf, 'wb') as f:
                    f.write(base64.b64decode(pdf_data))

                print(f'   ✅ PDF guardado: {os.path.basename(ruta_pdf)}')
                return True

            except ImportError:
                print('   ⚠️  Selenium 4+ no disponible, usando método alternativo...')

                # Método alternativo: hacer clic en el botón y capturar
                wait = WebDriverWait(self.driver, 15)

                try:
                    # Buscar el botón "Imprimir PDF"
                    boton_pdf = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(., 'Imprimir PDF')] | //a[contains(., 'Imprimir PDF')]")
                    ))
                    print('   ✅ Botón "Imprimir PDF" encontrado')
                    print('   ⚠️  NOTA: Deberás guardar el PDF manualmente')
                    print('   👉 El botón abrirá el diálogo de impresión')
                    print('   👉 Selecciona "Guardar como PDF" y guarda en la carpeta pdfs_descargados/')

                    boton_pdf.click()

                    # Esperar a que el usuario guarde el PDF
                    print('\n   ⏸️  Presiona ENTER después de guardar el PDF...')
                    input()

                    # Verificar si se guardó el PDF
                    archivos_pdf = [f for f in os.listdir(CARPETA_PDFS) if f.endswith('.pdf')]
                    if archivos_pdf:
                        print(f'   ✅ PDF encontrado en la carpeta')
                        return True
                    else:
                        print(f'   ⚠️  No se encontró el PDF en la carpeta')
                        return False

                except Exception as e:
                    print(f'   ❌ Error: {e}')
                    return False

        except Exception as e:
            print(f'   ❌ Error al descargar PDF: {e}')
            import traceback
            traceback.print_exc()
            return False
    
    def procesar_estudiante(self, estudiante, indice, total):
        """
        Procesa un estudiante completo: login, descarga PDF
        
        Args:
            estudiante: Serie de pandas con los datos del estudiante
            indice: Índice del estudiante (para mostrar progreso)
            total: Total de estudiantes
        """
        print('\n' + '='*80)
        print(f'📚 PROCESANDO ESTUDIANTE {indice + 1}/{total}')
        print('='*80)
        
        nombre_archivo = self.construir_nombre_archivo(estudiante)
        
        try:
            # Navegar a la página de login
            self.navegar_a_login()
            
            # Llenar el formulario
            if not self.llenar_formulario(estudiante):
                raise Exception('Error al llenar el formulario')
            
            # Esperar a que el usuario resuelva el CAPTCHA
            self.esperar_captcha_manual()
            
            # Hacer clic en Ingresar
            if not self.hacer_clic_ingresar():
                raise Exception('Error al hacer clic en Ingresar')
            
            # Descargar el PDF
            if self.descargar_pdf(nombre_archivo):
                self.estudiantes_exitosos.append({
                    'nombre': nombre_archivo,
                    'documento': estudiante['Número de documento'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                print(f'\n✅ Estudiante procesado exitosamente: {nombre_archivo}')
            else:
                self.estudiantes_sin_resultados.append({
                    'nombre': nombre_archivo,
                    'documento': estudiante['Número de documento'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                print(f'\n⚠️  Estudiante sin resultados disponibles: {nombre_archivo}')

            # Cerrar sesión para el siguiente estudiante
            self.hacer_logout()

        except Exception as e:
            self.estudiantes_error.append({
                'nombre': nombre_archivo,
                'documento': estudiante['Número de documento'],
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            print(f'\n❌ Error al procesar estudiante: {e}')

            # Intentar cerrar sesión incluso si hubo error
            try:
                self.hacer_logout()
            except:
                pass

        # Delay entre estudiantes
        if indice < total - 1:
            print(f'\n⏳ Esperando {DELAY_ENTRE_ESTUDIANTES} segundos antes del siguiente estudiante...')
            time.sleep(DELAY_ENTRE_ESTUDIANTES)
    
    def guardar_logs(self):
        """Guarda los logs de la ejecución"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Log de exitosos
        if self.estudiantes_exitosos:
            with open(f'{CARPETA_LOGS}/exitosos_{timestamp}.txt', 'w', encoding='utf-8') as f:
                f.write('ESTUDIANTES PROCESADOS EXITOSAMENTE\n')
                f.write('='*80 + '\n\n')
                for est in self.estudiantes_exitosos:
                    f.write(f"Nombre: {est['nombre']}\n")
                    f.write(f"Documento: {est['documento']}\n")
                    f.write(f"Timestamp: {est['timestamp']}\n")
                    f.write('-'*80 + '\n')
        
        # Log de errores
        if self.estudiantes_error:
            with open(f'{CARPETA_LOGS}/errores_{timestamp}.txt', 'w', encoding='utf-8') as f:
                f.write('ESTUDIANTES CON ERRORES\n')
                f.write('='*80 + '\n\n')
                for est in self.estudiantes_error:
                    f.write(f"Nombre: {est['nombre']}\n")
                    f.write(f"Documento: {est['documento']}\n")
                    f.write(f"Error: {est['error']}\n")
                    f.write(f"Timestamp: {est['timestamp']}\n")
                    f.write('-'*80 + '\n')
        
        # Log de sin resultados
        if self.estudiantes_sin_resultados:
            with open(f'{CARPETA_LOGS}/sin_resultados_{timestamp}.txt', 'w', encoding='utf-8') as f:
                f.write('ESTUDIANTES SIN RESULTADOS DISPONIBLES\n')
                f.write('='*80 + '\n\n')
                for est in self.estudiantes_sin_resultados:
                    f.write(f"Nombre: {est['nombre']}\n")
                    f.write(f"Documento: {est['documento']}\n")
                    f.write(f"Timestamp: {est['timestamp']}\n")
                    f.write('-'*80 + '\n')
        
        print(f'\n📝 Logs guardados en la carpeta: {CARPETA_LOGS}')
    
    def ejecutar(self, limite=None):
        """
        Ejecuta el proceso completo de descarga
        
        Args:
            limite: Número máximo de estudiantes a procesar (None = todos)
        """
        try:
            # Leer Excel
            df_estudiantes = self.leer_excel()
            
            # Limitar si se especifica
            if limite:
                df_estudiantes = df_estudiantes.head(limite)
                print(f'\n⚠️  Modo de prueba: procesando solo {limite} estudiante(s)')
            
            # Iniciar navegador
            self.iniciar_navegador()
            
            # Procesar cada estudiante
            total = len(df_estudiantes)
            for indice, (_, estudiante) in enumerate(df_estudiantes.iterrows()):
                self.procesar_estudiante(estudiante, indice, total)
            
            # Mostrar resumen
            print('\n' + '='*80)
            print('📊 RESUMEN DE LA EJECUCIÓN')
            print('='*80)
            print(f'✅ Exitosos: {len(self.estudiantes_exitosos)}')
            print(f'❌ Errores: {len(self.estudiantes_error)}')
            print(f'⚠️  Sin resultados: {len(self.estudiantes_sin_resultados)}')
            print(f'📁 Total procesados: {total}')
            
            # Guardar logs
            self.guardar_logs()
            
        except Exception as e:
            print(f'\n❌ Error fatal: {e}')
            import traceback
            traceback.print_exc()
        
        finally:
            # Cerrar navegador
            self.cerrar_navegador()


def main():
    """Función principal"""
    print('='*80)
    print('🎓 DESCARGADOR AUTOMÁTICO DE RESULTADOS ICFES SABER 11')
    print('='*80)
    
    # Preguntar si es modo de prueba
    print('\n¿Deseas ejecutar en modo de prueba?')
    print('1. Sí - Procesar solo 1 estudiante (recomendado para primera vez)')
    print('2. No - Procesar todos los estudiantes')
    
    opcion = input('\nSelecciona una opción (1 o 2): ').strip()
    
    limite = 1 if opcion == '1' else None
    
    # Crear instancia y ejecutar
    descargador = DescargadorICFES(modo_headless=False)
    descargador.ejecutar(limite=limite)
    
    print('\n✅ Proceso completado!')


if __name__ == '__main__':
    main()

