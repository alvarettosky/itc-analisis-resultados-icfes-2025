# 📋 FASE 2: Extracción de Puntajes y Consolidación en Excel

## 🎯 Objetivo

Crear un sistema automatizado que extraiga los puntajes de los resultados ICFES y genere un archivo Excel consolidado con todos los datos.

---

## 📥 Entrada

### Archivo Base
- **Nombre**: `INSCRITOS_EXAMEN SABER 11 (36).xls`
- **Contenido**: Datos de 36 estudiantes
- **Columnas**:
  - Primer Apellido
  - Segundo Apellido
  - Primer Nombre
  - Segundo Nombre
  - Tipo de documento (TI/CC)
  - Número de documento

### PDFs Descargados (Fase 1)
- **Carpeta**: `pdfs_descargados/`
- **Total**: 36 archivos PDF
- **Formato**: `APELLIDO1_APELLIDO2_NOMBRE1_NOMBRE2_DOCUMENTO.pdf`
- **Estado**: ✅ Completados en Fase 1

---

## 📤 Salida

### Archivo Excel Consolidado
- **Nombre**: `RESULTADOS-ICFES-AULA-REGULAR.xlsx`
- **Ubicación**: Raíz del proyecto
- **Contenido**:
  - Todas las columnas originales del archivo de entrada
  - Nuevas columnas con puntajes:
    - Lectura Crítica
    - Matemáticas
    - Sociales y Ciudadanas
    - Ciencias Naturales
    - Inglés
    - Puntaje Global

---

## 🔍 Análisis Técnico

### Problema Identificado

Los PDFs generados en la Fase 1 con `print_page()` de Selenium son renderizaciones de la página web que:
- ✅ Contienen el **Puntaje Global** (formato: XXX/500)
- ❌ **NO contienen** los puntajes individuales por área
- ❌ Requieren OCR para extraer texto (no tienen texto seleccionable)
- ⚠️  Los puntajes individuales solo son visibles al hacer clic en cada área

### Solución Propuesta

**Opción 1: Extracción Directa desde la Web** (RECOMENDADA)
- Modificar el script de descarga para extraer puntajes del HTML antes de generar PDF
- Ventajas:
  - ✅ Más confiable (datos directos del HTML)
  - ✅ No requiere OCR
  - ✅ Puede extraer todos los puntajes haciendo clic en cada área
- Desventajas:
  - ⚠️  Requiere re-ejecutar el proceso de login para cada estudiante
  - ⚠️  Más tiempo de ejecución

**Opción 2: OCR sobre PDFs Existentes**
- Usar Tesseract OCR para extraer texto de los PDFs
- Ventajas:
  - ✅ No requiere volver a hacer login
  - ✅ Usa los PDFs ya descargados
- Desventajas:
  - ❌ Solo puede extraer el Puntaje Global (171/500)
  - ❌ No puede extraer puntajes individuales (no están en el PDF)
  - ⚠️  Menos confiable (errores de OCR)

**Opción 3: Híbrida**
- Extraer Puntaje Global de PDFs con OCR
- Extraer puntajes individuales desde la web (solo para estudiantes que los necesiten)

---

## 🛠️ Implementación

### Scripts Creados

#### 1. `explorar_estructura_pdf.py` ✅
- **Estado**: Completado
- **Propósito**: Analizar estructura de PDFs con pdfplumber y PyPDF2
- **Resultado**: PDFs no tienen texto extraíble (son imágenes)

#### 2. `explorar_pdf_con_ocr.py` ✅
- **Estado**: Completado
- **Propósito**: Extraer texto de PDFs usando Tesseract OCR
- **Resultado**: 
  - ✅ Puntaje Global detectado (171/500)
  - ❌ Puntajes individuales NO detectados

#### 3. `inspeccionar_html_resultados.py` ✅
- **Estado**: Creado, pendiente de prueba
- **Propósito**: Inspeccionar estructura HTML de la página de resultados
- **Objetivo**: Determinar dónde están los puntajes individuales y cómo extraerlos

#### 4. `21-extraer_puntajes_desde_web.py` ✅
- **Estado**: Creado, pendiente de prueba
- **Propósito**: Extraer puntajes directamente desde la web
- **Características**:
  - Modo prueba (1 estudiante)
  - Modo completo (36 estudiantes)
  - Extracción de puntajes del HTML
  - Generación de Excel consolidado

---

## 📝 Tareas Pendientes

### Fase de Investigación
- [ ] Ejecutar `inspeccionar_html_resultados.py` para analizar estructura HTML
- [ ] Determinar si los puntajes individuales están en la página principal
- [ ] Identificar si es necesario hacer clic en cada área para ver puntajes
- [ ] Documentar selectores CSS/XPath para cada puntaje

### Fase de Desarrollo
- [ ] Completar función `extraer_puntajes_de_pagina()` con selectores correctos
- [ ] Implementar navegación a cada área si es necesario
- [ ] Agregar manejo de errores robusto
- [ ] Implementar logs detallados

### Fase de Pruebas
- [ ] Probar con 1 estudiante (modo prueba)
- [ ] Verificar que todos los puntajes se extraen correctamente
- [ ] Probar con 3-5 estudiantes
- [ ] Ejecutar con los 36 estudiantes

### Fase de Verificación
- [ ] Crear script `22-verificar_extraccion_puntajes.py`
- [ ] Verificar que todos los estudiantes tienen puntajes
- [ ] Comparar puntajes extraídos con PDFs (manualmente para muestra)
- [ ] Validar formato del Excel de salida

### Fase de Documentación
- [ ] Actualizar README.md con información de Fase 2
- [ ] Crear `FASE2-RESULTADOS.md` con estadísticas
- [ ] Actualizar CHANGELOG.md
- [ ] Actualizar 00-INDICE.md con nuevos archivos

---

## 🔧 Dependencias Instaladas

```bash
# Librerías para extracción de PDFs
pip install pdfplumber PyPDF2 tabula-py

# Librerías para OCR
pip install pytesseract pdf2image pillow

# Herramientas del sistema (ya instaladas)
- tesseract-ocr
- poppler-utils
```

---

## 📊 Estructura de Datos

### Archivo de Entrada (Excel)
```
Primer Apellido | Segundo Apellido | Primer Nombre | Segundo Nombre | Tipo de documento | Número de documento
----------------|------------------|---------------|----------------|-------------------|--------------------
ALGARIN         | MOVILLA          | JUAN          | JOSE           | TI                | 1043592724
...
```

### Archivo de Salida (Excel)
```
Primer Apellido | ... | Número de documento | Lectura Crítica | Matemáticas | Sociales y Ciudadanas | Ciencias Naturales | Inglés | Puntaje Global
----------------|-----|---------------------|-----------------|-------------|----------------------|-------------------|--------|---------------
ALGARIN         | ... | 1043592724          | 45              | 52          | 48                   | 50                | 55     | 171
...
```

---

## ⏱️ Estimación de Tiempo

### Modo Prueba (1 estudiante)
- Login manual: ~30 segundos
- Extracción de puntajes: ~10 segundos
- **Total**: ~40 segundos

### Modo Completo (36 estudiantes)
- Por estudiante: ~40 segundos
- Delays entre estudiantes: 3 segundos
- **Total estimado**: ~25-30 minutos

---

## 🎯 Criterios de Éxito

- ✅ Archivo Excel generado con nombre correcto
- ✅ Todas las columnas originales presentes
- ✅ 6 nuevas columnas de puntajes agregadas
- ✅ 36 estudiantes con puntajes completos
- ✅ Sin errores en la extracción
- ✅ Puntajes validados contra PDFs (muestra)
- ✅ Logs detallados de la ejecución
- ✅ Script de verificación funcional

---

## 📝 Notas Técnicas

### Formato del Puntaje Global
- **Formato en HTML**: `XXX/500` (ejemplo: `171/500`)
- **Regex**: `(\d{1,3})/500`
- **Ubicación**: Página principal de resultados

### Puntajes Individuales
- **Rango**: 0-100 puntos por área
- **Áreas**: 5 (Lectura Crítica, Matemáticas, Sociales, Ciencias, Inglés)
- **Ubicación**: Por determinar (página principal o sub-páginas)

### Consideraciones
- Los puntajes pueden no estar visibles inmediatamente
- Puede ser necesario hacer scroll o clic en elementos
- Algunos estudiantes pueden no tener resultados en todas las áreas
- Manejar casos de "Sin resultados" o "No disponible"

---

## 🔄 Próximos Pasos

1. **Ejecutar `inspeccionar_html_resultados.py`** para entender la estructura
2. **Completar `21-extraer_puntajes_desde_web.py`** con los selectores correctos
3. **Probar en modo prueba** con 1 estudiante
4. **Iterar** hasta que la extracción sea 100% confiable
5. **Ejecutar en modo completo** con los 36 estudiantes
6. **Verificar** resultados y generar documentación

---

**Fecha de inicio**: 14 de octubre de 2025  
**Estado actual**: En desarrollo  
**Progreso**: 30% (Investigación y scripts base creados)

