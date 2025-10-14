#!/usr/bin/env python3
"""
Script para inspeccionar el sitio web del ICFES usando requests y BeautifulSoup
"""
import requests
from bs4 import BeautifulSoup

def inspeccionar_sitio():
    """Inspecciona el sitio web del ICFES para entender su estructura"""
    
    print('=' * 80)
    print('INSPECCIÓN DEL SITIO WEB DEL ICFES')
    print('=' * 80)
    
    url = 'http://resultadossaber11.icfes.edu.co/'
    
    try:
        print(f'\n🌐 Obteniendo página: {url}')
        
        # Hacer la petición
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f'✅ Respuesta recibida: {response.status_code}')
        print(f'📄 Content-Type: {response.headers.get("Content-Type")}')
        
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Guardar el HTML
        with open('pagina_login.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print('💾 HTML guardado en: pagina_login.html')
        
        # Título
        title = soup.find('title')
        print(f'\n📄 Título: {title.text if title else "No encontrado"}')
        
        # Buscar formularios
        print('\n🔍 Buscando formularios...')
        forms = soup.find_all('form')
        print(f'   Formularios encontrados: {len(forms)}')
        
        for i, form in enumerate(forms, 1):
            print(f'\n   Formulario #{i}:')
            print(f'      - Action: {form.get("action")}')
            print(f'      - Method: {form.get("method")}')
            print(f'      - ID: {form.get("id")}')
            print(f'      - Class: {form.get("class")}')
        
        # Buscar campos de entrada
        print('\n📝 Buscando campos de entrada...')
        inputs = soup.find_all('input')
        print(f'   Total de inputs: {len(inputs)}')
        
        for i, input_elem in enumerate(inputs, 1):
            input_type = input_elem.get('type')
            input_name = input_elem.get('name')
            input_id = input_elem.get('id')
            input_placeholder = input_elem.get('placeholder')
            input_value = input_elem.get('value')
            
            print(f'\n   Input #{i}:')
            print(f'      - Tipo: {input_type}')
            print(f'      - Name: {input_name}')
            print(f'      - ID: {input_id}')
            print(f'      - Placeholder: {input_placeholder}')
            print(f'      - Value: {input_value}')
        
        # Buscar selects
        print('\n📋 Buscando campos select...')
        selects = soup.find_all('select')
        print(f'   Total de selects: {len(selects)}')
        
        for i, select_elem in enumerate(selects, 1):
            select_name = select_elem.get('name')
            select_id = select_elem.get('id')
            
            print(f'\n   Select #{i}:')
            print(f'      - Name: {select_name}')
            print(f'      - ID: {select_id}')
            
            # Obtener opciones
            options = select_elem.find_all('option')
            print(f'      - Opciones ({len(options)}):')
            for opt in options[:15]:  # Mostrar solo las primeras 15
                print(f'         * {opt.get("value")} - {opt.text.strip()}')
        
        # Buscar botones
        print('\n🔘 Buscando botones...')
        buttons = soup.find_all('button')
        print(f'   Total de botones: {len(buttons)}')
        
        for i, button in enumerate(buttons, 1):
            button_text = button.text.strip()
            button_type = button.get('type')
            button_id = button.get('id')
            
            print(f'\n   Botón #{i}:')
            print(f'      - Texto: {button_text}')
            print(f'      - Tipo: {button_type}')
            print(f'      - ID: {button_id}')
        
        # Buscar scripts (para detectar CAPTCHAs)
        print('\n🤖 Buscando CAPTCHAs y scripts...')
        scripts = soup.find_all('script')
        
        captcha_found = False
        for script in scripts:
            script_src = script.get('src', '')
            script_content = script.string or ''
            
            if 'recaptcha' in script_src.lower() or 'recaptcha' in script_content.lower():
                print('   ⚠️  reCAPTCHA detectado!')
                print(f'      - Script: {script_src}')
                captcha_found = True
            
            if 'hcaptcha' in script_src.lower() or 'hcaptcha' in script_content.lower():
                print('   ⚠️  hCaptcha detectado!')
                print(f'      - Script: {script_src}')
                captcha_found = True
        
        if not captcha_found:
            print('   ✅ No se detectaron CAPTCHAs obvios')
        
        # Buscar iframes
        print('\n🖼️  Buscando iframes...')
        iframes = soup.find_all('iframe')
        print(f'   Iframes encontrados: {len(iframes)}')
        for i, iframe in enumerate(iframes, 1):
            iframe_src = iframe.get('src')
            print(f'      - Iframe #{i}: {iframe_src}')
        
        # Buscar enlaces importantes
        print('\n🔗 Buscando enlaces relevantes...')
        links = soup.find_all('a', href=True)
        pdf_links = [link for link in links if 'pdf' in link.get('href', '').lower()]
        if pdf_links:
            print(f'   Enlaces a PDF encontrados: {len(pdf_links)}')
            for link in pdf_links[:5]:
                print(f'      - {link.get("href")}')
        
        print('\n✅ Inspección completada!')
        
    except Exception as e:
        print(f'\n❌ Error durante la inspección: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    inspeccionar_sitio()

