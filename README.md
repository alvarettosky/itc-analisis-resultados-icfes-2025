# 📊 Análisis de Resultados ICFES Saber 11 - 2025

[![Estado](https://img.shields.io/badge/Estado-Activo-success)](https://github.com/alvarettosky/itc-analisis-resultados-icfes-2025)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29%2B-red)](https://streamlit.io/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)](LICENSE)

Aplicación web interactiva desarrollada con **Streamlit** para visualización y análisis estadístico de resultados del examen ICFES Saber 11.

**🚀 Despliegue**: Streamlit Community Cloud
**📍 Ubicación**: `/media/disco1tb/ITC-Resultados-ICFES-2025`

---

## ✅ Estado del Proyecto

**🎉 APLICACIÓN WEB FUNCIONAL Y LISTA PARA DESPLIEGUE**

| Característica | Estado |
|----------------|--------|
| **Aplicación Streamlit** | ✅ Funcional |
| **Análisis Estadístico** | ✅ Completo |
| **Visualizaciones** | ✅ Interactivas |
| **Datos de Ejemplo** | ✅ Incluidos |
| **Listo para Cloud** | ✅ Configurado |

---

## 🚀 Características Principales

### ✨ Funcionalidades de la Aplicación Web

- ✅ **Dashboard Interactivo** con métricas clave
- ✅ **Análisis Estadístico Completo** por área de conocimiento
- ✅ **Visualizaciones Interactivas** con Plotly
- ✅ **Rankings y Clasificaciones** de estudiantes
- ✅ **Comparación Temporal** 2024 vs 2025
- ✅ **Análisis de Correlaciones** entre áreas
- ✅ **Identificación de Estudiantes** que requieren apoyo
- ✅ **Exportación de Datos** a CSV
- ✅ **Diseño Responsivo** para móviles y tablets
- ✅ **Modo Demostración** con datos de ejemplo

### 📊 Análisis Disponibles

1. **Resumen General**: Métricas globales y distribución de puntajes
2. **Análisis por Área**: Estadísticas detalladas de cada área de conocimiento
3. **Rankings**: Top 10 y clasificación por puntaje global
4. **Comparación 2024-2025**: Evolución temporal de resultados
5. **Correlaciones**: Relaciones entre diferentes áreas

### 🔐 Seguridad y Privacidad

- ⚠️ **IMPORTANTE**: Este repositorio contiene datos reales de 43 estudiantes del ITC
- ⚠️ **Datos públicos**: El archivo `ITC-RESULTADOS-ICFES-2025-ADAPTADO.xlsx` está en el repositorio público
- ✅ **Otros datos protegidos** con `.gitignore`
- ✅ **Aplicación usa datos reales ITC** en producción
- ✅ **Fallback a datos de ejemplo** si no encuentra datos reales

### 📊 Archivos de Datos

La aplicación busca archivos en este orden de prioridad:

1. **`ITC-RESULTADOS-ICFES-2025-ADAPTADO.xlsx`** (43 estudiantes reales del ITC)
   - ⚠️ Incluido en el repositorio público
   - Contiene nombres completos y puntajes reales

2. **`RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx`** (otros datos reales)
   - Solo disponible localmente (protegido por `.gitignore`)

3. **`RESULTADOS-ICFES-EJEMPLO.xlsx`** (datos ficticios)
   - Incluido en el repositorio para pruebas

---

## 📋 Requisitos

### Software Necesario

- **Python 3.11 o superior**
- **Git** (para clonar el repositorio)
- **Navegador web moderno** (Chrome, Firefox, Safari, Edge)

### Librerías Python

Las siguientes librerías están incluidas en `requirements.txt`:

- `streamlit` - Framework para aplicaciones web
- `pandas` - Análisis y manipulación de datos
- `plotly` - Visualizaciones interactivas
- `openpyxl` - Lectura de archivos Excel
- `numpy` - Cálculos numéricos
- `scipy` - Estadísticas avanzadas

---

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/alvarettosky/itc-analisis-resultados-icfes-2025.git
cd itc-analisis-resultados-icfes-2025
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
pip install -r requirements.txt
```

### 4. Generar datos de ejemplo (opcional)

```bash
python generar_datos_ejemplo.py
```

Esto creará el archivo `RESULTADOS-ICFES-EJEMPLO.xlsx` con datos ficticios para demostración.

---

## 📖 Uso

### 🚀 Ejecutar la Aplicación Localmente

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar la aplicación
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### 📊 Estructura del Archivo Excel

Si deseas usar tus propios datos, el archivo Excel debe contener las siguientes columnas:

- **Grupo**: Identificador del grupo (ej: 11A, 11B)
- **Primer Apellido**
- **Segundo Apellido**
- **Primer Nombre**
- **Segundo Nombre**
- **Tipo documento**: TI o CC
- **Número de documento**
- **Lectura Crítica**: Puntaje (0-100)
- **Matemáticas**: Puntaje (0-100)
- **Sociales y Ciudadanas**: Puntaje (0-100)
- **Ciencias Naturales**: Puntaje (0-100)
- **Inglés**: Puntaje (0-100)
- **Puntaje Global**: Puntaje total (0-500)

Guarda el archivo como `RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx` en la raíz del proyecto.

---

## 📁 Estructura del Proyecto

```
itc-analisis-resultados-icfes-2025/
│
├── app.py                                🚀 Aplicación Streamlit principal ⭐
├── app_resultados_icfes.py              📊 Aplicación alternativa (completa)
├── generar_datos_ejemplo.py             🔧 Generador de datos de ejemplo
│
├── requirements.txt                      📦 Dependencias Python
├── requirements-webapp.txt               📦 Dependencias para Streamlit Cloud
├── runtime.txt                           🐍 Versión de Python
│
├── .streamlit/                           ⚙️ Configuración de Streamlit
│   └── config.toml
│
├── ITC-RESULTADOS-ICFES-2025-ADAPTADO.xlsx  📊 Datos reales ITC (43 estudiantes)
├── RESULTADOS-ICFES-EJEMPLO.xlsx        📊 Datos de ejemplo (ficticios)
├── RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx  📊 Otros datos reales (no en Git)
│
├── README.md                             📚 Este archivo
├── README-WEBAPP.md                      📚 Documentación de la webapp
├── GUIA-DESPLIEGUE.md                   📚 Guía de despliegue
├── INSTRUCCIONES-STREAMLIT-CLOUD.md     📚 Instrucciones para Streamlit Cloud
│
├── venv/                                 🐍 Entorno virtual (no en Git)
├── logs/                                 📝 Logs de ejecución
└── pdfs_descargados/                    📄 PDFs (no en Git)
```

---

## 🚀 Despliegue en Streamlit Cloud

### Pasos para Desplegar

1. **Asegúrate de que el código esté en GitHub**
   ```bash
   git add .
   git commit -m "Preparar para despliegue"
   git push origin main
   ```

2. **Ve a Streamlit Cloud**
   - Visita: https://share.streamlit.io/
   - Inicia sesión con tu cuenta de GitHub

3. **Crea una nueva app**
   - Repository: `alvarettosky/itc-analisis-resultados-icfes-2025`
   - Branch: `main`
   - Main file: `app.py`

4. **Despliega**
   - Click en "Deploy!"
   - Espera 2-3 minutos
   - ¡Tu app estará en línea!

Para más detalles, consulta `INSTRUCCIONES-STREAMLIT-CLOUD.md`

---

## ⚠️ Notas Importantes

### Privacidad y Seguridad

1. **Datos ITC públicos**: El archivo `ITC-RESULTADOS-ICFES-2025-ADAPTADO.xlsx` con 43 estudiantes reales está en el repositorio público
2. **Otros datos protegidos**: Otros archivos Excel con datos sensibles NO se suben a GitHub
3. **Aplicación en producción**: Usa los datos reales del ITC (43 estudiantes)
4. **Uso local**: Para analizar otros datos reales, ejecuta la aplicación localmente
5. **Archivos protegidos**: `.gitignore` protege otros archivos sensibles

### Uso de la Aplicación

1. **Navegación**: Usa las pestañas superiores para cambiar entre análisis
2. **Interactividad**: Los gráficos son interactivos (zoom, pan, hover)
3. **Exportación**: Puedes exportar datos filtrados a CSV
4. **Actualización**: Recarga la página (F5) si actualizas el archivo Excel

---

## 🎯 Casos de Uso

### Para Docentes
- Identificar estudiantes que requieren apoyo
- Analizar fortalezas y debilidades por área
- Generar reportes para reuniones

### Para Coordinadores
- Evaluar desempeño general del grupo
- Identificar áreas que requieren refuerzo
- Tomar decisiones basadas en datos

### Para Estudiantes
- Ver perfil individual de competencias
- Compararse con el promedio del grupo
- Identificar áreas de mejora

---

## 🔄 Sincronización con GitHub

Este proyecto está sincronizado con GitHub para respaldo y colaboración.

### Sincronizar cambios

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

### Ver el repositorio

🌐 https://github.com/alvarettosky/itc-analisis-resultados-icfes-2025

---

## 📞 Soporte y Documentación

Si encuentras problemas:

1. Consulta la documentación:
   - `README.md` - Este archivo
   - `README-WEBAPP.md` - Documentación de la aplicación web
   - `GUIA-DESPLIEGUE.md` - Guía de despliegue
   - `INSTRUCCIONES-STREAMLIT-CLOUD.md` - Instrucciones para Streamlit Cloud
2. Verifica que el archivo Excel tenga el formato correcto
3. Limpia la caché de Streamlit: Menú > Clear cache

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+** - Lenguaje de programación
- **Streamlit 1.29+** - Framework para aplicaciones web
- **Pandas 2.0+** - Análisis de datos
- **Plotly 5.18+** - Visualizaciones interactivas
- **NumPy & SciPy** - Cálculos estadísticos
- **Git/GitHub** - Control de versiones

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Álvaro Ángel Molina** ([@alvarettosky](https://github.com/alvarettosky))

---

## 🙏 Agradecimientos

- Comunidad de Streamlit por el excelente framework
- Comunidad de Plotly por las visualizaciones interactivas
- Todos los que contribuyen a mejorar este proyecto

---

## 📅 Historial de Versiones

### Versión 3.0 (15 de octubre de 2025)
- ✅ Aplicación web Streamlit completamente funcional
- ✅ Análisis estadístico completo implementado
- ✅ Visualizaciones interactivas con Plotly
- ✅ Modo demostración con datos de ejemplo
- ✅ Preparado para despliegue en Streamlit Cloud
- ✅ Documentación actualizada
- ✅ Repositorio migrado a nueva ubicación

### Versión 2.0 (14 de octubre de 2025)
- ✅ Sistema de descarga funcional (scripts de desarrollo)
- ✅ Procesamiento de datos de estudiantes
- ✅ Generación de reportes

Ver historial completo en: `17-CHANGELOG.md`

---

**Desarrollado con ❤️ para facilitar el análisis educativo**

**Última actualización**: 15 de octubre de 2025
**Versión**: 3.0 (Aplicación Web Streamlit)
**Repositorio**: https://github.com/alvarettosky/itc-analisis-resultados-icfes-2025

