# 🎓 Descargador Automático de Resultados ICFES Saber 11

Sistema automatizado para descargar masivamente los resultados del examen ICFES Saber 11 desde el portal oficial.

**Repositorio**: Extracción, análisis y publicación de resultados ICFES
**GitHub**: https://github.com/alvaretto/resultados-icfes

## ✅ Estado del Proyecto

**🎉 PROYECTO COMPLETADO Y PROBADO**

- ✅ **36/36 estudiantes procesados exitosamente** (14 de octubre de 2025)
- ✅ **100% de tasa de éxito** en la primera ejecución completa
- ✅ **0 errores** durante la ejecución
- ✅ **Sistema completamente funcional y probado**

## 📋 Requisitos

### Software Necesario:
- Python 3.7 o superior
- Firefox (navegador)
- Conexión a Internet estable

### Librerías Python:
Todas las dependencias están en el entorno virtual `venv/` que ya está configurado.

## 🚀 Instalación

### 1. Activar el entorno virtual:

```bash
source venv/bin/activate
```

### 2. Verificar instalación:

```bash
python3 --version
pip list | grep -E "selenium|pandas|webdriver"
```

## 📖 Uso

### 📑 Ver Índice Completo del Proyecto

```bash
cat 00-INDICE.md
```

### Modo de Prueba (Recomendado para primera vez)

Procesa solo 1 estudiante para verificar que todo funciona correctamente:

```bash
python3 12-descargar_resultados_icfes.py
```

Cuando se te pregunte, selecciona la opción `1` para modo de prueba.

### Modo Completo

Para procesar todos los estudiantes:

```bash
python3 12-descargar_resultados_icfes.py
```

Selecciona la opción `2` cuando se te pregunte.

## 🔄 Flujo del Proceso

1. **Lectura del Excel**: El script lee el archivo `INSCRITOS_EXAMEN SABER 11 (36).xls`
2. **Inicio del navegador**: Se abre Firefox automáticamente
3. **Para cada estudiante**:
   - Se navega al portal del ICFES
   - Se llena el formulario automáticamente con los datos del estudiante
     - Mapeo automático de tipos de documento: "TI" → "TARJETA DE IDENTIDAD", "CC" → "CÉDULA DE CIUDADANÍA"
   - **⚠️ PAUSA PARA CAPTCHA Y LOGIN**: El script se detiene y espera a que:
     - Resuelvas el CAPTCHA (si aparece)
     - Hagas clic en "Ingresar"
     - Esperes a que cargue la página de resultados
   - Presionas ENTER en la terminal para continuar
   - Se genera el PDF usando Selenium print_page()
   - Se guarda el PDF con formato: `APELLIDO1_APELLIDO2_NOMBRE_DOCUMENTO.pdf`
   - Se cierra la sesión automáticamente
   - Se espera 3 segundos antes del siguiente estudiante

4. **Finalización**: Se generan logs con el resumen de la ejecución

## 📁 Estructura de Archivos

```
Resultados-ICFES-2025/
├── .git/                                   # Repositorio Git (sincronizado con GitHub)
├── .gitignore                              # Archivos excluidos del repositorio
├── venv/                                   # Entorno virtual de Python
├── INSCRITOS_EXAMEN SABER 11 (36).xls      # Archivo Excel con los datos (no se sube a GitHub)
│
├── 00-INDICE.md                            # Índice del proyecto ⭐
├── 12-descargar_resultados_icfes.py        # Script principal ⭐
├── 13-verificar_pdfs_completos.py          # Script de verificación ⭐
├── 18-sincronizar_github.sh                # Script de sincronización con GitHub ⭐
├── 04-analizar_excel.py                    # Script de análisis del Excel
├── inspeccionar_con_firefox.py             # Script de inspección del sitio
├── inspeccionar_pagina_resultados.py       # Script de inspección de resultados
│
├── README.md                               # Este archivo
├── INICIO_RAPIDO.txt                       # Guía rápida de inicio
├── GITHUB_SYNC.md                          # Guía de sincronización con GitHub ⭐
├── NOTAS_TECNICAS.md                       # Notas técnicas del fix
├── SOLUCION_FINAL.md                       # Documentación de la solución
├── RESUMEN_FINAL_DESCARGA.md               # Resumen de la descarga exitosa ⭐
├── CHANGELOG.md                            # Historial de cambios ⭐
│
├── pdfs_descargados/                       # PDFs descargados (36 archivos) ✅
│   ├── .gitkeep                            # (no se suben PDFs a GitHub por privacidad)
│   ├── VELASQUEZ_GONZALEZ_ALEXANDER_1095208929.pdf
│   ├── RIOS_URBANO_ANDRES_FELIPE_1111677398.pdf
│   ├── ... (34 archivos más)
│   └── ZAPATA_VARGAS_LAURA_CAMILA_1060506690.pdf
│
└── logs/                                   # Logs de ejecución
    ├── .gitkeep                            # (no se suben logs a GitHub por privacidad)
    ├── exitosos_20251014_124233.txt        # 36 estudiantes exitosos ✅
    ├── errores_20251014_*.txt              # Errores (si los hay)
    └── sin_resultados_20251014_*.txt       # Sin resultados (si los hay)
```

## 🎯 Características

### ✅ Implementado y Probado:
- ✅ Lectura automática del archivo Excel con manejo correcto de encabezados
- ✅ Llenado automático del formulario con mapeo de tipos de documento
  - "TI" → "TARJETA DE IDENTIDAD"
  - "CC" → "CÉDULA DE CIUDADANÍA"
  - Soporte para CE, CR, PC, PE, PEP, NUIP, RC
- ✅ Pausa para resolución manual del CAPTCHA y login
- ✅ Generación automática de PDFs usando Selenium print_page()
- ✅ Nombrado inteligente de archivos: `APELLIDO1_APELLIDO2_NOMBRE_DOCUMENTO.pdf`
- ✅ Cierre automático de sesión entre estudiantes
- ✅ Manejo robusto de errores con logs detallados
- ✅ Modo de prueba (1 estudiante) y modo completo (todos)
- ✅ Delays apropiados entre solicitudes (3 segundos)
- ✅ Script de verificación de completitud (`13-verificar_pdfs_completos.py`)
- ✅ Detección automática de login completado

### ⚠️ Limitaciones:
- ⚠️ Requiere intervención manual para resolver el CAPTCHA y hacer clic en "Ingresar"
- ⚠️ Tiempo estimado: ~35 segundos por estudiante (probado)
- ⚠️ Requiere supervisión durante la ejecución

## 🔧 Configuración Avanzada

Puedes modificar las siguientes variables en `descargar_resultados_icfes.py`:

```python
# Ruta del archivo Excel
EXCEL_PATH = '/ruta/a/tu/archivo.xls'

# URL del portal ICFES
URL_ICFES = 'http://resultadossaber11.icfes.edu.co/'

# Carpeta donde se guardarán los PDFs
CARPETA_PDFS = 'pdfs_descargados'

# Carpeta donde se guardarán los logs
CARPETA_LOGS = 'logs'

# Tiempo de espera entre estudiantes (en segundos)
DELAY_ENTRE_ESTUDIANTES = 3
```

## 📊 Logs Generados

El sistema genera 3 tipos de logs:

### 1. `exitosos_[timestamp].txt`
Lista de estudiantes procesados exitosamente con sus PDFs descargados.

### 2. `errores_[timestamp].txt`
Lista de estudiantes que tuvieron errores durante el proceso, con detalles del error.

### 3. `sin_resultados_[timestamp].txt`
Lista de estudiantes que no tienen resultados disponibles en el portal.

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'selenium'"

**Solución**: Asegúrate de haber activado el entorno virtual:
```bash
source venv/bin/activate
```

### Error: "GeckoDriver not found"

**Solución**: El script descarga automáticamente GeckoDriver. Si falla, instala Firefox:
```bash
# En Arch Linux
sudo pacman -S firefox

# En Ubuntu/Debian
sudo apt install firefox
```

### El navegador no se abre

**Solución**: Verifica que Firefox esté instalado y accesible desde la terminal:
```bash
firefox --version
```

### Los PDFs no se descargan

**Solución**: 
1. Verifica que la carpeta `pdfs_descargados/` tenga permisos de escritura
2. Revisa los logs en la carpeta `logs/` para más detalles
3. Ejecuta primero en modo de prueba para identificar el problema

### El CAPTCHA no aparece o no se puede resolver

**Solución**:
1. Asegúrate de que el navegador esté visible (no en modo headless)
2. Verifica tu conexión a Internet
3. Intenta resolver el CAPTCHA manualmente en el navegador
4. Si persiste, puede ser que el ICFES haya cambiado su sistema

## ⏱️ Estimación de Tiempo

### Tiempos Reales (Probados el 14/10/2025)

Para **36 estudiantes**:
- Tiempo por estudiante: **~35 segundos** (incluyendo CAPTCHA manual)
- Tiempo total real: **21 minutos** ✅
- Inicio: 12:21:18
- Finalización: 12:42:30

**Nota**: Los tiempos pueden variar dependiendo de:
- Velocidad de resolución del CAPTCHA
- Velocidad de la conexión a Internet
- Carga del servidor del ICFES

**Recomendación**: Ejecutar en horarios de baja demanda (noches o fines de semana) para mejor rendimiento.

## 🔐 Consideraciones de Seguridad

- ✅ El script NO almacena contraseñas
- ✅ Solo accede a datos públicos del portal ICFES
- ✅ Respeta los términos de servicio con delays entre solicitudes
- ✅ No realiza scraping agresivo

## 🔄 Sincronización con GitHub

Este proyecto está sincronizado con GitHub para respaldo y colaboración.

### Sincronizar cambios:

```bash
# Opción 1: Script automático (recomendado)
./18-sincronizar_github.sh "Descripción de los cambios"

# Opción 2: Comandos manuales
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

### Ver el repositorio:
🌐 https://github.com/alvaretto/resultados-icfes

### Guía completa:
📖 Ver `19-GITHUB_SYNC.md` para instrucciones detalladas

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs en la carpeta `logs/`
2. Consulta la documentación:
   - `00-INDICE.md` - Índice completo del proyecto
   - `15-SOLUCION_FINAL.md` - Solución técnica completa
   - `14-NOTAS_TECNICAS.md` - Notas técnicas del fix de tipos de documento
   - `16-RESUMEN_FINAL_DESCARGA.md` - Resumen de la descarga exitosa
   - `02-INICIO_RAPIDO.txt` - Guía rápida de inicio
   - `19-GITHUB_SYNC.md` - Guía de sincronización con GitHub
3. Verifica que el portal del ICFES esté disponible: http://resultadossaber11.icfes.edu.co/
4. Ejecuta el script de verificación: `python3 13-verificar_pdfs_completos.py`

## 📝 Notas Importantes

1. **Supervisión requerida**: Este script requiere que estés presente para resolver los CAPTCHAs y hacer clic en "Ingresar"
2. **Conexión estable**: Asegúrate de tener una conexión a Internet estable durante todo el proceso
3. **No cerrar el navegador**: No cierres el navegador Firefox mientras el script está ejecutándose
4. **Backup del Excel**: Haz una copia de seguridad del archivo Excel antes de comenzar
5. **Verificación post-descarga**: Usa `13-verificar_pdfs_completos.py` para confirmar que todos los PDFs se descargaron

## ✅ Verificar PDFs Descargados

Después de ejecutar el script, verifica que todos los PDFs se descargaron correctamente:

```bash
python3 13-verificar_pdfs_completos.py
```

Este script te mostrará:
- ✅ Estudiantes con PDF descargado
- ❌ Estudiantes sin PDF (si los hay)
- 📊 Resumen completo de la descarga

## 🎉 Resultados de la Primera Ejecución Completa

**Fecha**: 14 de octubre de 2025
**Resultado**: ✅ **100% EXITOSO**

### Estadísticas:
- **Total de estudiantes**: 36
- **PDFs descargados**: 36 ✅
- **Errores**: 0 ✅
- **Tasa de éxito**: 100% 🎉
- **Duración**: 21 minutos
- **Promedio por estudiante**: ~35 segundos

### Detalles:
- **31 estudiantes con TI** (Tarjeta de Identidad) ✅
- **5 estudiantes con CC** (Cédula de Ciudadanía) ✅
- **Todos los PDFs verificados** con `13-verificar_pdfs_completos.py` ✅

Ver detalles completos en: `RESUMEN_FINAL_DESCARGA.md`

---

## 💡 Alternativas al CAPTCHA Manual

Si el proceso manual es muy tedioso, considera:

### Opción 1: Servicios de Resolución de CAPTCHA (Pago)
- **2Captcha**: ~$1-3 USD por 1000 CAPTCHAs
- **Anti-Captcha**: Similar pricing
- **Implementación**: Requiere modificar el script para integrar la API

### Opción 2: Contactar al ICFES
- Solicitar acceso API oficial
- Solicitar descarga masiva de resultados
- Explicar que eres una institución educativa

### Opción 3: Dividir el Trabajo
- Varias personas resolviendo CAPTCHAs simultáneamente
- Ejecutar el script en múltiples computadoras

**Nota**: Con el tiempo real probado (~35 segundos por estudiante), el proceso manual es bastante eficiente.

## 🔧 Problemas Resueltos Durante el Desarrollo

### 1. Selección de Tipo de Documento ✅
**Problema**: Los valores del Excel ("TI", "CC") no se mapeaban a las opciones del formulario web.
**Solución**: Creado diccionario de mapeo y comparación exacta.
**Resultado**: Funciona para todos los tipos de documento.

### 2. Descarga del PDF ✅
**Problema**: El botón "Imprimir PDF" abre el diálogo de impresión en lugar de descargar.
**Solución**: Implementada la función `print_page()` de Selenium 4+.
**Resultado**: PDFs se generan y guardan automáticamente.

### 3. Manejo de Sesiones ✅
**Problema**: El navegador mantenía la sesión activa, mostrando siempre los resultados del primer estudiante.
**Solución**: Implementada función `hacer_logout()` para cerrar sesión entre estudiantes.
**Resultado**: Cada estudiante se procesa correctamente con sus propios datos.

### 4. Manejo del CAPTCHA y Login ✅
**Problema**: El script fallaba si el usuario hacía clic en "Ingresar" antes que el script.
**Solución**: Implementada detección de estado de la página.
**Resultado**: Funciona tanto con login manual como automático.

Ver detalles técnicos completos en: `SOLUCION_FINAL.md` y `NOTAS_TECNICAS.md`

---

## 📜 Licencia

Este script es para uso educativo y administrativo. Asegúrate de cumplir con los términos de servicio del ICFES.

---

**Desarrollado con ❤️ para facilitar la gestión educativa**

**Última actualización**: 14 de octubre de 2025
**Versión**: 2.0 (Completamente funcional y probado)