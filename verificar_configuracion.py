#!/usr/bin/env python3
"""
Script para verificar que todo está configurado correctamente
antes de ejecutar la descarga masiva
"""

import sys
import os

def verificar_python():
    """Verifica la versión de Python"""
    print('\n🐍 Verificando Python...')
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f'   ✅ Python {version.major}.{version.minor}.{version.micro} - OK')
        return True
    else:
        print(f'   ❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.7+')
        return False

def verificar_librerias():
    """Verifica que las librerías necesarias estén instaladas"""
    print('\n📚 Verificando librerías...')
    
    librerias = {
        'pandas': 'Lectura de archivos Excel',
        'selenium': 'Automatización del navegador',
        'webdriver_manager': 'Gestión de drivers',
        'openpyxl': 'Soporte para archivos .xlsx',
        'xlrd': 'Soporte para archivos .xls'
    }
    
    todas_ok = True
    for libreria, descripcion in librerias.items():
        try:
            __import__(libreria)
            print(f'   ✅ {libreria:20} - OK ({descripcion})')
        except ImportError:
            print(f'   ❌ {libreria:20} - NO INSTALADA ({descripcion})')
            todas_ok = False
    
    return todas_ok

def verificar_firefox():
    """Verifica que Firefox esté instalado"""
    print('\n🦊 Verificando Firefox...')
    
    import subprocess
    try:
        result = subprocess.run(['firefox', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f'   ✅ {version} - OK')
            return True
        else:
            print('   ❌ Firefox no encontrado')
            return False
    except FileNotFoundError:
        print('   ❌ Firefox no está instalado')
        return False
    except Exception as e:
        print(f'   ⚠️  No se pudo verificar Firefox: {e}')
        return False

def verificar_archivo_excel():
    """Verifica que el archivo Excel exista"""
    print('\n📄 Verificando archivo Excel...')
    
    ruta = '/home/proyectos/Escritorio/Resultados-ICFES-2025/INSCRITOS_EXAMEN SABER 11 (36).xls'
    
    if os.path.exists(ruta):
        size = os.path.getsize(ruta)
        print(f'   ✅ Archivo encontrado - {size:,} bytes')
        
        # Intentar leerlo
        try:
            import pandas as pd
            df = pd.read_excel(ruta, skiprows=3)
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)
            print(f'   ✅ Archivo legible - {len(df)} estudiantes encontrados')
            return True
        except Exception as e:
            print(f'   ❌ Error al leer el archivo: {e}')
            return False
    else:
        print(f'   ❌ Archivo no encontrado: {ruta}')
        return False

def verificar_carpetas():
    """Verifica que las carpetas necesarias existan o puedan crearse"""
    print('\n📁 Verificando carpetas...')
    
    carpetas = ['pdfs_descargados', 'logs']
    todas_ok = True
    
    for carpeta in carpetas:
        try:
            os.makedirs(carpeta, exist_ok=True)
            if os.path.exists(carpeta) and os.access(carpeta, os.W_OK):
                print(f'   ✅ {carpeta:20} - OK (con permisos de escritura)')
            else:
                print(f'   ❌ {carpeta:20} - Sin permisos de escritura')
                todas_ok = False
        except Exception as e:
            print(f'   ❌ {carpeta:20} - Error: {e}')
            todas_ok = False
    
    return todas_ok

def verificar_conexion_icfes():
    """Verifica la conexión al portal del ICFES"""
    print('\n🌐 Verificando conexión al portal ICFES...')
    
    try:
        import requests
        url = 'http://resultadossaber11.icfes.edu.co/'
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f'   ✅ Portal accesible - Status {response.status_code}')
            return True
        else:
            print(f'   ⚠️  Portal responde con status {response.status_code}')
            return False
    except Exception as e:
        print(f'   ❌ No se pudo conectar al portal: {e}')
        return False

def probar_selenium():
    """Prueba que Selenium pueda iniciar Firefox"""
    print('\n🔧 Probando Selenium con Firefox...')
    
    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.service import Service
        from selenium.webdriver.firefox.options import Options
        from webdriver_manager.firefox import GeckoDriverManager
        
        print('   - Descargando/verificando GeckoDriver...')
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        print('   - Navegando a una página de prueba...')
        driver.get('http://example.com')
        
        title = driver.title
        driver.quit()
        
        print(f'   ✅ Selenium funciona correctamente (título: "{title}")')
        return True
        
    except Exception as e:
        print(f'   ❌ Error al probar Selenium: {e}')
        return False

def main():
    """Función principal"""
    print('='*80)
    print('🔍 VERIFICACIÓN DE CONFIGURACIÓN - DESCARGADOR ICFES')
    print('='*80)
    
    resultados = {
        'Python': verificar_python(),
        'Librerías': verificar_librerias(),
        'Firefox': verificar_firefox(),
        'Archivo Excel': verificar_archivo_excel(),
        'Carpetas': verificar_carpetas(),
        'Conexión ICFES': verificar_conexion_icfes(),
        'Selenium': probar_selenium()
    }
    
    print('\n' + '='*80)
    print('📊 RESUMEN DE VERIFICACIÓN')
    print('='*80)
    
    for componente, resultado in resultados.items():
        estado = '✅' if resultado else '❌'
        print(f'{estado} {componente}')
    
    print('\n' + '='*80)
    
    if all(resultados.values()):
        print('✅ ¡TODO ESTÁ CONFIGURADO CORRECTAMENTE!')
        print('👉 Puedes ejecutar el script principal: python3 descargar_resultados_icfes.py')
    else:
        print('❌ HAY PROBLEMAS DE CONFIGURACIÓN')
        print('👉 Por favor, revisa los errores anteriores y corrígelos antes de continuar')
        print('\n💡 Sugerencias:')
        
        if not resultados['Python']:
            print('   - Actualiza Python a la versión 3.7 o superior')
        
        if not resultados['Librerías']:
            print('   - Activa el entorno virtual: source venv/bin/activate')
            print('   - O instala las librerías: pip install pandas selenium webdriver-manager openpyxl xlrd')
        
        if not resultados['Firefox']:
            print('   - Instala Firefox: sudo pacman -S firefox (Arch) o sudo apt install firefox (Ubuntu)')
        
        if not resultados['Archivo Excel']:
            print('   - Verifica que el archivo Excel esté en la ruta correcta')
            print('   - Verifica que el archivo no esté corrupto')
        
        if not resultados['Carpetas']:
            print('   - Verifica los permisos de escritura en el directorio actual')
        
        if not resultados['Conexión ICFES']:
            print('   - Verifica tu conexión a Internet')
            print('   - El portal del ICFES podría estar temporalmente no disponible')
        
        if not resultados['Selenium']:
            print('   - Verifica que Firefox esté correctamente instalado')
            print('   - Intenta reinstalar las librerías de Selenium')
    
    print('='*80)

if __name__ == '__main__':
    main()

