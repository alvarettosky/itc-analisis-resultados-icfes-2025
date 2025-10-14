# Resumen del Análisis - Portal ICFES Saber 11

## 📊 Análisis del Archivo Excel

### Datos Disponibles:
- **Total de estudiantes**: 36
- **Ubicación**: La Tebaida, Quindío
- **Tipos de documento**: 
  - TI (Tarjeta de Identidad): 31 estudiantes
  - CC (Cédula de Ciudadanía): 5 estudiantes

### Columnas del Excel:
1. Número de registro (ej: AC202530812826)
2. Tipo documento (CC o TI)
3. Número de documento
4. Primer Apellido
5. Segundo Apellido
6. Primer Nombre
7. Segundo Nombre (10 valores nulos)
8. Departamento
9. Municipio
10. Zona

## 🌐 Análisis del Sitio Web

### URL Correcta:
`http://resultadossaber11.icfes.edu.co/`

### Tecnología:
- **Framework**: Angular 9.1.13
- **Tipo**: Single Page Application (SPA)
- **Contenido**: Carga dinámica con JavaScript

### Formulario de Login:

#### Campos Requeridos:
1. **Tipo de documento** (Select/Dropdown) - OBLIGATORIO
   - ID: No tiene ID específico
   - Placeholder: "Seleccione"
   - Opciones: Probablemente CC, TI, CE, etc.

2. **Número de documento** (Input text) - OBLIGATORIO
   - ID: `identificacion`
   - Type: text
   - MaxLength: 20
   - Transform: uppercase

3. **Fecha de nacimiento** (Input date) - OPCIONAL
   - ID: `fechaNacimiento`
   - Type: date
   - Placeholder: 01/01/2000
   - Min: 1900-01-01
   - Max: fecha actual

4. **Número de registro** (Input text) - OPCIONAL
   - ID: `numeroRegistro`
   - Type: text
   - MaxLength: 16
   - Transform: uppercase

#### CAPTCHA:
- **Tipo**: Google reCAPTCHA v2
- **Site Key**: `6LcUWNIaAAAAANABrv20gXn9edUFplvFJ8210ly6`
- **Ubicación**: Antes del botón de envío
- **Desafío**: Este es el mayor obstáculo para la automatización

#### Botón de Envío:
- **Texto**: "Ingresar"
- **Type**: submit
- **Class**: btn-round btn-high mt-4

### Validación del Formulario:
- El formulario requiere **Tipo de documento** y **Número de documento** como campos obligatorios
- Debe completarse **al menos uno** de los campos opcionales: Fecha de nacimiento O Número de registro
- El reCAPTCHA debe ser resuelto antes de enviar

## 🚧 Desafíos Identificados

### 1. reCAPTCHA v2
**Problema**: Google reCAPTCHA v2 requiere interacción humana (hacer clic en "No soy un robot" y posiblemente resolver desafíos visuales).

**Soluciones posibles**:
- **Opción A (Recomendada)**: Intervención manual - pausar el script para que un humano resuelva el CAPTCHA
- **Opción B**: Servicios de resolución de CAPTCHA (2Captcha, Anti-Captcha, etc.) - COSTO MONETARIO
- **Opción C**: Intentar con técnicas de evasión (no recomendado, baja tasa de éxito)

### 2. Aplicación Angular
**Problema**: El contenido se carga dinámicamente, requiere un navegador real.

**Solución**: Usar Selenium con Firefox o Chrome (ya implementado).

### 3. Datos Faltantes
**Problema**: No tenemos la fecha de nacimiento de los estudiantes en el Excel.

**Solución**: Usar el número de registro que sí está disponible en el Excel.

## 📋 Estrategia de Automatización Propuesta

### Herramientas:
- **Selenium** con Firefox (mejor compatibilidad)
- **Pandas** para leer el Excel
- **Python 3** como lenguaje principal

### Flujo del Proceso:

1. **Leer el archivo Excel** y extraer los datos de cada estudiante
2. **Para cada estudiante**:
   a. Abrir el navegador y navegar al portal
   b. Seleccionar el tipo de documento
   c. Ingresar el número de documento
   d. Ingresar el número de registro
   e. **PAUSAR** y esperar a que el usuario resuelva el CAPTCHA manualmente
   f. Hacer clic en "Ingresar"
   g. Esperar a que cargue la página de resultados
   h. Buscar y descargar el PDF
   i. Renombrar el PDF con el formato: `{Apellidos}_{Nombres}_{NumDocumento}.pdf`
   j. Guardar en una carpeta organizada

3. **Manejo de errores**:
   - Registrar estudiantes sin resultados
   - Reintentar en caso de errores de conexión
   - Guardar progreso para poder reanudar

### Estructura de Carpetas Propuesta:
```
Resultados-ICFES-2025/
├── pdfs_descargados/
│   ├── VELASQUEZ_GONZALEZ_ALEXANDER_1095208929.pdf
│   ├── RIOS_URBANO_ANDRES_FELIPE_1111677398.pdf
│   └── ...
├── logs/
│   ├── exitosos.txt
│   ├── errores.txt
│   └── sin_resultados.txt
└── scripts/
    ├── descargar_resultados.py
    └── ...
```

## ⚠️ Consideraciones Importantes

### Legales y Éticas:
- ✅ Estás descargando resultados de tus propios estudiantes
- ✅ Tienes autorización para acceder a estos datos
- ⚠️ Respetar los términos de servicio del ICFES
- ⚠️ No sobrecargar el servidor (implementar delays entre solicitudes)

### Técnicas:
- **Delays recomendados**: 3-5 segundos entre cada estudiante
- **Tiempo estimado**: ~5-10 minutos por estudiante (incluyendo CAPTCHA manual)
- **Tiempo total estimado**: 3-6 horas para 36 estudiantes
- **Recomendación**: Ejecutar en horarios de baja demanda

### Alternativas al CAPTCHA Manual:
Si el proceso manual es muy tedioso, considerar:
1. **Servicios de resolución de CAPTCHA** (~$1-3 USD por 1000 CAPTCHAs)
2. **Contactar al ICFES** para solicitar acceso API o descarga masiva oficial
3. **Dividir el trabajo** entre varias personas

## 🎯 Próximos Pasos

1. ✅ Análisis del Excel - COMPLETADO
2. ✅ Inspección del sitio web - COMPLETADO
3. ⏳ Implementar script de automatización
4. ⏳ Probar con 1-2 estudiantes
5. ⏳ Ejecutar descarga masiva
6. ⏳ Verificar y organizar PDFs descargados

