# 🎓 Descargador Automático de Resultados ICFES Saber 11

[![Estado](https://img.shields.io/badge/Estado-Funcional%20100%25-success)](https://github.com/alvaretto/resultados-icfes)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green)](https://www.selenium.dev/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)](LICENSE)

Sistema automatizado para descargar masivamente los resultados del examen ICFES Saber 11 desde el portal oficial del ICFES.

**🌐 Portal ICFES**: http://resultadossaber11.icfes.gov.co/

---

## ✅ Estado del Proyecto

**🎉 PROYECTO COMPLETADO Y PROBADO EN PRODUCCIÓN**

| Métrica | Resultado |
|---------|-----------|
| **Estudiantes procesados** | 36/36 ✅ |
| **Tasa de éxito** | 100% 🎯 |
| **Errores** | 0 ✅ |
| **Tiempo total** | ~21 minutos ⚡ |
| **Promedio por estudiante** | ~35 segundos 📊 |
| **Fecha de prueba** | 14 de octubre de 2025 📅 |

---

## 🚀 Características Principales

### ✨ Funcionalidades Implementadas

- ✅ **Descarga automática de PDFs** de resultados ICFES Saber 11
- ✅ **Lectura automática de Excel** con datos de estudiantes
- ✅ **Manejo de tipos de documento** (TI - Tarjeta de Identidad, CC - Cédula de Ciudadanía)
- ✅ **Gestión automática de sesiones** (logout entre estudiantes)
- ✅ **Generación de PDFs** usando Selenium 4 print_page()
- ✅ **Logs detallados** de ejecución (exitosos, errores, sin resultados)
- ✅ **Modo de prueba** (1 estudiante) y **modo completo** (todos)
- ✅ **Verificación de completitud** de PDFs descargados
- ✅ **Manejo de nombres con acentos** en español
- ✅ **Delays apropiados** entre solicitudes (3 segundos)
- ✅ **Detección automática** de login completado

### 🔐 Seguridad y Privacidad

- ✅ **Archivos sensibles protegidos** con `.gitignore`
- ✅ **PDFs de estudiantes NO se suben** a GitHub
- ✅ **Logs con información personal NO se suben** a GitHub
- ✅ **Archivos Excel con datos NO se suben** a GitHub

---

## 📋 Requisitos

### Software Necesario

- **Python 3.7 o superior**
- **Firefox** (navegador)
- **Git** (para clonar el repositorio)
- **Conexión a Internet estable**

### Librerías Python

Las siguientes librerías están incluidas en el entorno virtual:

- `selenium` - Automatización del navegador
- `pandas` - Lectura de archivos Excel
- `openpyxl` - Soporte para archivos .xlsx
- `xlrd` - Soporte para archivos .xls
- `webdriver-manager` - Gestión automática de drivers

---

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/alvaretto/resultados-icfes.git
cd resultados-icfes
```

### 2. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install selenium pandas openpyxl xlrd webdriver-manager
```

### 4. Preparar archivo Excel

Coloca tu archivo Excel con los datos de estudiantes en la raíz del proyecto. El archivo debe tener las siguientes columnas:

- Primer Apellido
- Segundo Apellido
- Primer Nombre
- Segundo Nombre
- Tipo de documento (TI o CC)
- Número de documento

---

## 📖 Uso

### 📑 Ver Índice Completo del Proyecto

```bash
cat 00-INDICE.md
```

### 🚀 Ejecución Rápida

#### Modo de Prueba (Recomendado para primera vez)

Procesa solo 1 estudiante para verificar que todo funciona:

```bash
python3 12-descargar_resultados_icfes.py
```

Selecciona la opción `1` cuando se te pregunte.

#### Modo Completo

Para procesar todos los estudiantes:

```bash
python3 12-descargar_resultados_icfes.py
```

Selecciona la opción `2` cuando se te pregunte.

### ✅ Verificar PDFs Descargados

Después de ejecutar el script, verifica que todos los PDFs se descargaron correctamente:

```bash
python3 13-verificar_pdfs_completos.py
```

---

## 📁 Estructura del Proyecto

```
resultados-icfes/
│
├── 00-INDICE.md                          📑 Índice completo del proyecto ⭐
├── 01-README.md                          📚 Documentación detallada
├── 02-INICIO_RAPIDO.txt                  📚 Guía rápida de inicio
│
├── 03-verificar_configuracion.py        ⚙️ Verificación de configuración
│
├── 04-analizar_excel.py                  🔍 Análisis del archivo Excel
├── 05-RESUMEN_ANALISIS.md                🔍 Resumen del análisis
│
├── 06-11-*.py                            🔬 Scripts de inspección (desarrollo)
│
├── 12-descargar_resultados_icfes.py      🚀 SCRIPT PRINCIPAL ⭐⭐⭐
│
├── 13-verificar_pdfs_completos.py        ✅ Verificación post-descarga ⭐
│
├── 14-NOTAS_TECNICAS.md                  📖 Notas técnicas
├── 15-SOLUCION_FINAL.md                  📖 Solución técnica completa
├── 16-RESUMEN_FINAL_DESCARGA.md          📖 Resumen de descarga exitosa
├── 17-CHANGELOG.md                       📖 Historial de cambios
│
├── 18-sincronizar_github.sh              🔄 Sincronización con GitHub ⭐
├── 19-GITHUB_SYNC.md                     🔄 Guía de sincronización
│
├── 20-mostrar_ayuda.py                   🛠️ Utilidades
│
├── pdfs_descargados/                     📄 PDFs descargados
│   └── *.pdf                             (no se suben a GitHub)
│
└── logs/                                 📝 Logs de ejecución
    └── *.txt                             (no se suben a GitHub)
```

---

## 🎯 Flujo de Trabajo

### 1️⃣ Preparación
- Activar entorno virtual
- Verificar configuración
- Preparar archivo Excel

### 2️⃣ Ejecución
- Ejecutar script principal
- Resolver CAPTCHAs manualmente
- Esperar a que termine el proceso

### 3️⃣ Verificación
- Verificar PDFs descargados
- Revisar logs de ejecución
- Confirmar completitud

### 4️⃣ Sincronización (Opcional)
- Sincronizar cambios con GitHub
- Mantener respaldo en la nube

---

## ⚠️ Notas Importantes

### Durante la Ejecución

1. **Supervisión requerida**: Debes estar presente para resolver los CAPTCHAs y hacer clic en "Ingresar"
2. **Conexión estable**: Asegúrate de tener una conexión a Internet estable durante todo el proceso
3. **No cerrar el navegador**: No cierres el navegador Firefox mientras el script está ejecutándose
4. **Backup del Excel**: Haz una copia de seguridad del archivo Excel antes de comenzar
5. **Verificación post-descarga**: Usa `13-verificar_pdfs_completos.py` para confirmar que todos los PDFs se descargaron

### Proceso por Estudiante

El script se **PAUSARÁ** en cada estudiante para que:
1. Resuelvas el CAPTCHA (si aparece)
2. Hagas clic en "Ingresar"
3. Esperes a que cargue la página de resultados
4. Presiones ENTER en la terminal después de ver los resultados

El script automáticamente:
- Generará el PDF
- Cerrará la sesión
- Continuará con el siguiente estudiante

---

## 📊 Resultados de la Primera Ejecución Completa

### Estadísticas

- **Fecha**: 14 de octubre de 2025
- **Hora de inicio**: 12:21:18
- **Hora de finalización**: 12:42:30
- **Duración total**: 21 minutos y 12 segundos
- **Estudiantes procesados**: 36/36 ✅
- **Tasa de éxito**: 100% 🎉
- **Errores**: 0 ✅

### Distribución por Tipo de Documento

- **31 estudiantes con TI** (Tarjeta de Identidad) ✅
- **5 estudiantes con CC** (Cédula de Ciudadanía) ✅
- **Todos los PDFs verificados** con `13-verificar_pdfs_completos.py` ✅

Ver detalles completos en: `16-RESUMEN_FINAL_DESCARGA.md`

---

## 🔄 Sincronización con GitHub

Este proyecto está sincronizado con GitHub para respaldo y colaboración.

### Sincronizar cambios

```bash
# Opción 1: Script automático (recomendado)
./18-sincronizar_github.sh "Descripción de los cambios"

# Opción 2: Comandos manuales
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

### Ver el repositorio

🌐 https://github.com/alvaretto/resultados-icfes

### Guía completa

📖 Ver `19-GITHUB_SYNC.md` para instrucciones detalladas

---

## 📞 Soporte y Documentación

Si encuentras problemas:

1. Revisa los logs en la carpeta `logs/`
2. Consulta la documentación:
   - `00-INDICE.md` - Índice completo del proyecto
   - `01-README.md` - Documentación detallada (este archivo)
   - `02-INICIO_RAPIDO.txt` - Guía rápida de inicio
   - `15-SOLUCION_FINAL.md` - Solución técnica completa
   - `14-NOTAS_TECNICAS.md` - Notas técnicas del fix de tipos de documento
   - `16-RESUMEN_FINAL_DESCARGA.md` - Resumen de la descarga exitosa
   - `19-GITHUB_SYNC.md` - Guía de sincronización con GitHub
3. Verifica que el portal del ICFES esté disponible: http://resultadossaber11.icfes.gov.co/
4. Ejecuta el script de verificación: `python3 13-verificar_pdfs_completos.py`

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.13** - Lenguaje de programación
- **Selenium 4** - Automatización del navegador
- **Firefox/GeckoDriver** - Navegador y driver
- **Pandas** - Procesamiento de datos
- **Git/GitHub** - Control de versiones

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Álvaro Ángel Molina** ([@alvaretto](https://github.com/alvaretto))

---

## 🙏 Agradecimientos

- Portal ICFES por proporcionar acceso a los resultados
- Comunidad de Selenium por la excelente documentación
- Todos los que contribuyen a mejorar este proyecto

---

## 🚀 Fase 2: Extracción de Puntajes (En Desarrollo)

### Objetivo
Extraer automáticamente los puntajes de los resultados ICFES y generar un archivo Excel consolidado.

### Estado Actual
🔄 **En Desarrollo** (30% completado)

### Scripts Creados
- `explorar_estructura_pdf.py` - Análisis de estructura de PDFs ✅
- `explorar_pdf_con_ocr.py` - Extracción con OCR ✅
- `inspeccionar_html_resultados.py` - Inspección de HTML ✅
- `21-extraer_puntajes_desde_web.py` - Extracción desde web 🔄

### Próximos Pasos
1. Analizar estructura HTML de la página de resultados
2. Identificar selectores para puntajes individuales
3. Completar script de extracción
4. Generar archivo Excel consolidado: `RESULTADOS-ICFES-AULA-REGULAR.xlsx`

Ver plan completo en: `FASE2-PLAN.md`

---

## 📅 Historial de Versiones

### Versión 2.1 (En Desarrollo)
- 🔄 Fase 2: Extracción de puntajes desde web
- 🔄 Generación de Excel consolidado
- ✅ Instaladas librerías: pdfplumber, PyPDF2, pytesseract, pdf2image
- ✅ Scripts de exploración y análisis creados

### Versión 2.0 (14 de octubre de 2025)
- ✅ Sistema 100% funcional y probado en producción
- ✅ 36/36 estudiantes procesados exitosamente
- ✅ Gestión automática de sesiones implementada
- ✅ Verificación de completitud de PDFs
- ✅ Sincronización con GitHub configurada
- ✅ Documentación completa y actualizada
- ✅ Archivos organizados con prefijos numéricos

Ver historial completo en: `17-CHANGELOG.md`

---

**Desarrollado con ❤️ para facilitar la gestión educativa**

**Última actualización**: 14 de octubre de 2025
**Versión**: 2.1 (Fase 2 en desarrollo)

