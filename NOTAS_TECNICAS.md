# 📝 Notas Técnicas - Descargador ICFES

## Correcciones y Mejoras Implementadas

### 1. Corrección del Selector de Tipo de Documento (2025-10-14)

#### Problema Identificado:
El script original no mapeaba correctamente los valores del Excel a las opciones del formulario web del portal ICFES.

**Valores en el Excel:**
- `TI` = Tarjeta de Identidad
- `CC` = Cédula de Ciudadanía

**Opciones en el formulario web:**
- `TARJETA DE IDENTIDAD` (texto completo en mayúsculas)
- `CÉDULA DE CIUDADANÍA` (texto completo en mayúsculas)

#### Solución Implementada:

Se agregó un diccionario de mapeo en la función `llenar_formulario()`:

```python
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
```

#### Mejoras en la Lógica:

1. **Conversión a mayúsculas**: Se convierte el tipo de documento del Excel a mayúsculas antes de buscar en el mapeo
2. **Búsqueda exacta**: Se compara el texto completo de la opción (en mayúsculas) con el valor mapeado
3. **Mensajes de depuración**: Se agregaron mensajes detallados para facilitar el diagnóstico
4. **Manejo de errores**: Si no se encuentra la opción, se muestra una lista de opciones disponibles

#### Código Corregido:

```python
def llenar_formulario(self, estudiante):
    # ... código anterior ...
    
    tipo_doc = str(estudiante['Tipo documento']).strip().upper()
    
    # Mapeo de tipos de documento
    mapeo_tipos_doc = { ... }
    
    # Obtener el texto completo para buscar en el formulario
    tipo_doc_formulario = mapeo_tipos_doc.get(tipo_doc, tipo_doc)
    
    # Hacer clic en el ng-select
    ng_select = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'ng-select')))
    ng_select.click()
    
    # Buscar la opción correspondiente
    opciones = self.driver.find_elements(By.CSS_SELECTOR, '.ng-option')
    opcion_encontrada = False
    
    for opcion in opciones:
        texto_opcion = opcion.text.strip().upper()
        if tipo_doc_formulario.upper() == texto_opcion:
            opcion.click()
            opcion_encontrada = True
            break
    
    if not opcion_encontrada:
        raise Exception(f'Tipo de documento "{tipo_doc}" no encontrado')
```

#### Pruebas Realizadas:

Se creó el script `probar_seleccion_tipo_doc.py` que verifica:
- ✅ Selección correcta de `TI` → `TARJETA DE IDENTIDAD`
- ✅ Selección correcta de `CC` → `CÉDULA DE CIUDADANÍA`

**Resultado**: ✅ Todas las pruebas pasaron exitosamente

---

## Opciones Completas del Selector de Tipo de Documento

El portal ICFES ofrece las siguientes 15 opciones de tipo de documento:

1. TARJETA DE IDENTIDAD
2. CÉDULA DE CIUDADANÍA
3. CÉDULA DE EXTRANJERÍA
4. CONTRASEÑA REGISTRADURÍA
5. PASAPORTE COLOMBIANO
6. PASAPORTE EXTRANJERO
7. PERMISO ESPECIAL DE PERMANENCIA
8. NÚMERO DE IDENTIFICACIÓN ESTABLECIDO POR LA SECRETARÍA DE EDUCACIÓN
9. CERTIFICADO CABILDO
10. NÚMERO ÚNICO DE IDENTIFICACIÓN PERSONAL
11. NÚMERO DE IDENTIFICACIÓN PERSONAL
12. REGISTRO CIVIL DE NACIMIENTO
13. DOCUMENTO NACIONAL DE IDENTIDAD VENEZOLANA
14. PERMISO TEMPORAL DE PERMANENCIA
15. PERMISO DE PROTECCION TEMPORAL

---

## Estructura del Formulario Web

### Campos del Formulario:

1. **Tipo de documento** (obligatorio)
   - Selector: `ng-select`
   - Opciones: `.ng-option`
   - Valor seleccionado: `.ng-value`

2. **Número de documento** (obligatorio)
   - ID: `identificacion`
   - Tipo: `text`
   - Max length: 20 caracteres
   - Transform: uppercase

3. **Fecha de nacimiento** (opcional)
   - ID: `fechaNacimiento`
   - Tipo: `date`
   - Min: 1900-01-01
   - Max: fecha actual

4. **Número de registro** (opcional)
   - ID: `numeroRegistro`
   - Tipo: `text`
   - Max length: 16 caracteres
   - Transform: uppercase

5. **reCAPTCHA v2** (obligatorio)
   - Site key: `6LcUWNIaAAAAANABrv20gXn9edUFplvFJ8210ly6`
   - Requiere intervención humana

6. **Botón Ingresar**
   - Tipo: `submit`
   - Texto: "Ingresar"

---

## Tecnologías del Portal ICFES

- **Framework**: Angular 9.1.13
- **Tipo**: Single Page Application (SPA)
- **Selector de opciones**: ng-select (componente de Angular)
- **Seguridad**: Google reCAPTCHA v2
- **URL**: http://resultadossaber11.icfes.edu.co/

---

## Scripts de Utilidad Creados

### 1. `inspeccionar_opciones_tipo_doc.py`
Inspecciona y lista todas las opciones disponibles en el selector de tipo de documento.

**Uso:**
```bash
python3 inspeccionar_opciones_tipo_doc.py
```

### 2. `probar_seleccion_tipo_doc.py`
Prueba la selección automática de tipos de documento (TI y CC).

**Uso:**
```bash
python3 probar_seleccion_tipo_doc.py
```

**Resultado esperado:**
```
TI: ✅ ÉXITO
CC: ✅ ÉXITO
```

---

## Recomendaciones para Futuros Desarrollos

### 1. Agregar más tipos de documento al mapeo
Si en el futuro se necesitan procesar estudiantes con otros tipos de documento, agregar las entradas correspondientes al diccionario `mapeo_tipos_doc`.

### 2. Validación de datos del Excel
Antes de procesar, validar que todos los tipos de documento en el Excel estén en el mapeo.

### 3. Logs más detallados
Considerar agregar logging a archivo para facilitar el diagnóstico de problemas.

### 4. Reintentos automáticos
Implementar lógica de reintentos para casos donde la selección falle por problemas de red o carga lenta.

### 5. Modo batch con múltiples navegadores
Para acelerar el proceso, considerar ejecutar múltiples instancias del navegador en paralelo (con cuidado de no sobrecargar el servidor).

---

## Problemas Conocidos y Limitaciones

### 1. CAPTCHA Manual
- **Problema**: Google reCAPTCHA v2 requiere intervención humana
- **Impacto**: ~5-10 minutos por estudiante
- **Solución actual**: Pausa manual para resolver el CAPTCHA
- **Alternativas**: Servicios de pago (2Captcha, Anti-Captcha) o contactar al ICFES

### 2. Dependencia de la estructura del HTML
- **Problema**: Si el ICFES cambia la estructura del formulario, el script puede fallar
- **Mitigación**: Scripts de inspección para verificar la estructura actual
- **Recomendación**: Ejecutar `inspeccionar_opciones_tipo_doc.py` antes de procesar lotes grandes

### 3. Velocidad de procesamiento
- **Tiempo por estudiante**: 5-10 minutos (incluyendo CAPTCHA)
- **Tiempo total (36 estudiantes)**: 3-6 horas
- **Limitación**: No se puede acelerar significativamente sin violar términos de servicio

---

## Historial de Cambios

### Versión 1.1 (2025-10-14)
- ✅ Corregido el mapeo de tipos de documento
- ✅ Agregada validación de opciones
- ✅ Mejorados los mensajes de depuración
- ✅ Creados scripts de prueba

### Versión 1.0 (2025-10-14)
- ✅ Implementación inicial
- ✅ Lectura de Excel
- ✅ Automatización del formulario
- ✅ Manejo de CAPTCHA manual
- ✅ Descarga de PDFs
- ✅ Generación de logs

---

## Contacto y Soporte

Para reportar problemas o sugerir mejoras:
1. Revisar los logs en la carpeta `logs/`
2. Ejecutar los scripts de verificación
3. Consultar este documento de notas técnicas
4. Revisar el archivo `RESUMEN_ANALISIS.md` para más detalles

---

**Última actualización**: 2025-10-14
**Autor**: Sistema de Automatización ICFES

