# 📊 Aplicación Web de Análisis de Resultados ICFES Saber 11 - 2025

Aplicación web interactiva desarrollada con **Streamlit** para visualización y análisis estadístico de resultados del examen ICFES Saber 11.

---

## 🎯 Características Principales

### 1. **Vista General**
- Resumen estadístico completo
- Promedios por área de conocimiento
- Distribución del puntaje global
- Box plots de dispersión por área
- Identificación de áreas fuertes y débiles

### 2. **Análisis por Estudiante**
- Búsqueda por nombre o documento
- Perfil individual detallado
- Radar chart de competencias
- Comparación con promedios del grupo
- Ranking y percentil individual

### 3. **Análisis por Área**
- Estadísticas descriptivas completas (promedio, mediana, moda, desviación estándar)
- Histogramas de distribución
- Box plots con outliers
- Percentiles (25, 50, 75)
- Top 10 y estudiantes que requieren apoyo por área

### 4. **Análisis Comparativo**
- Ranking general por puntaje global
- Comparación de promedios entre áreas
- Matriz de correlación entre áreas
- Scatter plots de correlaciones
- Identificación de estudiantes destacados (Top 10%)

### 5. **Segmentación**
- Clasificación por rangos de puntaje (Bajo, Medio, Alto, Superior)
- Estudiantes que requieren apoyo (Bottom 20%)
- Análisis de consistencia de desempeño
- Tabla completa con filtros dinámicos
- Exportación de datos filtrados a CSV

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Instalar Dependencias

```bash
# Activar el entorno virtual (si existe)
source venv/bin/activate

# Instalar las dependencias
pip install -r requirements-webapp.txt
```

### Paso 2: Verificar el Archivo de Datos

Asegúrate de que el archivo Excel esté en la ubicación correcta:
```
/home/proyectos/Escritorio/Resultados-ICFES-2025/RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx
```

### Paso 3: Ejecutar la Aplicación

```bash
# Desde el directorio del proyecto
streamlit run app_resultados_icfes.py
```

La aplicación se abrirá automáticamente en tu navegador en:
```
http://localhost:8501
```

---

## 📁 Estructura de Archivos

```
Resultados-ICFES-2025/
├── app_resultados_icfes.py          # Aplicación principal
├── requirements-webapp.txt           # Dependencias Python
├── README-WEBAPP.md                  # Este archivo
└── RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx  # Datos de entrada
```

---

## 📊 Estructura del Archivo Excel

El archivo debe contener las siguientes columnas:

| Columna | Tipo | Descripción |
|---------|------|-------------|
| Grupo | Texto | Grupo del estudiante (11A, 11B, etc.) |
| Primer Apellido | Texto | Primer apellido del estudiante |
| Segundo Apellido | Texto | Segundo apellido del estudiante |
| Primer Nombre | Texto | Primer nombre del estudiante |
| Segundo Nombre | Texto | Segundo nombre del estudiante (opcional) |
| Tipo documento | Texto | Tipo de documento (TI, CC) |
| Número de documento | Número | Número de documento de identidad |
| Lectura Crítica | Número | Puntaje en Lectura Crítica (0-100) |
| Matemáticas | Número | Puntaje en Matemáticas (0-100) |
| Sociales y Ciudadanas | Número | Puntaje en Sociales y Ciudadanas (0-100) |
| Ciencias Naturales | Número | Puntaje en Ciencias Naturales (0-100) |
| Inglés | Número | Puntaje en Inglés (0-100) |
| Puntaje Global | Número | Puntaje global (0-500) |

---

## 🎨 Funcionalidades Interactivas

### Filtros Dinámicos
- Búsqueda en tiempo real de estudiantes
- Filtros por clasificación de puntaje
- Filtros por consistencia de desempeño
- Slider de rango de puntajes

### Visualizaciones
- **Gráficos de barras**: Comparación de promedios
- **Histogramas**: Distribución de puntajes
- **Box plots**: Análisis de dispersión y outliers
- **Scatter plots**: Correlaciones entre áreas
- **Heatmap**: Matriz de correlación
- **Radar charts**: Perfiles individuales de competencias
- **Gráficos de torta**: Distribución por clasificación

### Exportación
- Descarga de datos filtrados en formato CSV
- Todos los gráficos son interactivos (zoom, pan, hover)

---

## 📈 Métricas y Análisis

### Estadísticas Descriptivas
- **Promedio**: Media aritmética de los puntajes
- **Mediana**: Valor central de la distribución
- **Moda**: Valor más frecuente
- **Desviación Estándar**: Medida de dispersión
- **Percentiles**: Valores que dividen la distribución (25%, 50%, 75%)
- **Coeficiente de Variación**: Dispersión relativa (%)

### Clasificación por Rangos
- **Bajo**: 0-200 puntos
- **Medio**: 201-300 puntos
- **Alto**: 301-400 puntos
- **Superior**: 401-500 puntos

### Análisis de Consistencia
- **Alta**: Desviación estándar < 5 (puntajes similares en todas las áreas)
- **Media**: Desviación estándar 5-10
- **Baja**: Desviación estándar > 10 (puntajes muy variables)

---

## 🛠️ Tecnologías Utilizadas

- **Streamlit 1.29.0**: Framework para aplicaciones web de datos
- **Pandas 2.1.4**: Manipulación y análisis de datos
- **Plotly 5.18.0**: Visualizaciones interactivas
- **NumPy 1.26.2**: Cálculos numéricos
- **SciPy 1.11.4**: Estadísticas avanzadas
- **Openpyxl 3.1.2**: Lectura de archivos Excel

---

## 🎯 Casos de Uso

### Para Docentes
- Identificar estudiantes que requieren apoyo adicional
- Analizar fortalezas y debilidades por área
- Comparar desempeño entre estudiantes
- Generar reportes para reuniones de padres

### Para Coordinadores Académicos
- Evaluar el desempeño general del grupo
- Identificar áreas que requieren refuerzo
- Analizar correlaciones entre áreas de conocimiento
- Tomar decisiones basadas en datos

### Para Estudiantes
- Ver su perfil individual de competencias
- Compararse con el promedio del grupo
- Identificar áreas de mejora
- Visualizar su posición en el ranking

---

## 🔧 Solución de Problemas

### Error: "No se pudieron cargar los datos"
- Verifica que el archivo Excel exista en la ruta correcta
- Asegúrate de que el archivo tenga las columnas requeridas
- Verifica que el archivo no esté abierto en otra aplicación

### Error: "ModuleNotFoundError"
- Ejecuta: `pip install -r requirements-webapp.txt`
- Verifica que el entorno virtual esté activado

### La aplicación no se abre en el navegador
- Abre manualmente: http://localhost:8501
- Verifica que el puerto 8501 no esté en uso
- Usa: `streamlit run app_resultados_icfes.py --server.port 8502`

### Gráficos no se muestran correctamente
- Actualiza el navegador (Ctrl + F5)
- Limpia la caché de Streamlit: Menú > Clear cache

---

## 📝 Notas Importantes

1. **Privacidad**: La aplicación se ejecuta localmente, los datos no se envían a ningún servidor externo
2. **Rendimiento**: La aplicación usa caché para mejorar el rendimiento
3. **Actualización de datos**: Si actualizas el archivo Excel, recarga la página (F5)
4. **Navegadores compatibles**: Chrome, Firefox, Safari, Edge (últimas versiones)

---

## 🚀 Comandos Rápidos

```bash
# Instalar dependencias
pip install -r requirements-webapp.txt

# Ejecutar aplicación
streamlit run app_resultados_icfes.py

# Ejecutar en puerto diferente
streamlit run app_resultados_icfes.py --server.port 8502

# Ejecutar sin abrir navegador automáticamente
streamlit run app_resultados_icfes.py --server.headless true
```

---

## 📧 Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

---

**Fecha de creación**: 14 de octubre de 2025  
**Versión**: 1.0.0  
**Autor**: Sistema de Análisis ICFES

