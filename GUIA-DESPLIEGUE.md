# 🚀 Guía de Despliegue - Aplicación Web ICFES Saber 11

Esta guía te ayudará a publicar tu aplicación web de análisis ICFES en plataformas gratuitas open source.

---

## 📋 Opciones de Despliegue Gratuitas

### ✅ OPCIÓN 1: Streamlit Community Cloud (RECOMENDADA)

**Ventajas:**
- ✅ 100% Gratuita
- ✅ Específicamente diseñada para Streamlit
- ✅ Despliegue automático desde GitHub
- ✅ SSL/HTTPS incluido
- ✅ Actualizaciones automáticas al hacer push
- ✅ Sin configuración de servidor

**Limitaciones:**
- Repositorio debe ser público (o cuenta GitHub Pro para privados)
- 1 GB de recursos por app
- Apps inactivas se duermen después de 7 días

**Pasos para desplegar:**

#### 1. Preparar el repositorio

```bash
# Asegúrate de que todos los archivos necesarios estén en el repo
git add app_resultados_icfes.py
git add requirements-webapp.txt
git add RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx
git add .streamlit/config.toml
git add runtime.txt
git commit -m "🚀 Preparar aplicación para despliegue en Streamlit Cloud"
git push origin main
```

#### 2. Crear cuenta en Streamlit Community Cloud

1. Ve a: https://streamlit.io/cloud
2. Haz clic en "Sign up" o "Get started"
3. Inicia sesión con tu cuenta de GitHub (alvaretto)

#### 3. Desplegar la aplicación

1. En el dashboard de Streamlit Cloud, haz clic en "New app"
2. Selecciona tu repositorio: `alvaretto/resultados-icfes`
3. Selecciona la rama: `main`
4. Selecciona el archivo principal: `app_resultados_icfes.py`
5. Haz clic en "Deploy!"

#### 4. Configuración avanzada (opcional)

Si necesitas variables de entorno o secretos:
- En el dashboard, ve a "Settings" → "Secrets"
- Agrega cualquier configuración sensible

**URL final:** `https://[tu-app-name].streamlit.app`

---

### ✅ OPCIÓN 2: Hugging Face Spaces

**Ventajas:**
- ✅ Gratuita
- ✅ Comunidad de ML/AI
- ✅ Repositorios públicos y privados
- ✅ GPU gratuita disponible (no necesaria para esta app)

**Pasos:**

1. Crea cuenta en: https://huggingface.co/join
2. Ve a: https://huggingface.co/spaces
3. Clic en "Create new Space"
4. Selecciona "Streamlit" como SDK
5. Sube tus archivos o conecta con GitHub

**Archivos necesarios:**
- `app_resultados_icfes.py` (renombrar a `app.py`)
- `requirements-webapp.txt` (renombrar a `requirements.txt`)
- `RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx`

---

### ✅ OPCIÓN 3: Render

**Ventajas:**
- ✅ Gratuita (plan free)
- ✅ Soporta múltiples frameworks
- ✅ Despliegue desde GitHub

**Limitaciones:**
- Apps gratuitas se duermen después de 15 minutos de inactividad
- 750 horas/mes en plan gratuito

**Pasos:**

1. Crea cuenta en: https://render.com
2. Conecta tu cuenta de GitHub
3. Clic en "New +" → "Web Service"
4. Selecciona tu repositorio
5. Configura:
   - **Build Command:** `pip install -r requirements-webapp.txt`
   - **Start Command:** `streamlit run app_resultados_icfes.py --server.port=$PORT --server.address=0.0.0.0`

---

### ✅ OPCIÓN 4: Railway

**Ventajas:**
- ✅ $5 de crédito gratuito mensual
- ✅ Despliegue automático desde GitHub
- ✅ Fácil configuración

**Pasos:**

1. Crea cuenta en: https://railway.app
2. Conecta GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detectará automáticamente que es una app Python

---

## 📁 Archivos Necesarios para el Despliegue

### ✅ Archivos ya creados:

1. **`app_resultados_icfes.py`** - Aplicación principal ✅
2. **`requirements-webapp.txt`** - Dependencias ✅
3. **`.streamlit/config.toml`** - Configuración de Streamlit ✅
4. **`runtime.txt`** - Versión de Python ✅
5. **`RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx`** - Datos reales ✅

### ⚠️ Consideraciones de Privacidad

**IMPORTANTE:** El archivo Excel contiene datos reales de estudiantes (nombres, documentos, puntajes).

**Opciones:**

#### Opción A: Repositorio Privado (Recomendado para datos reales)
- Usa GitHub Pro (gratis para estudiantes/educadores)
- O usa Hugging Face Spaces (permite repos privados gratis)
- Los datos NO serán públicos

#### Opción B: Repositorio Público con datos de ejemplo
- Usa `RESULTADOS-ICFES-EJEMPLO.xlsx` (datos ficticios)
- Modifica la app para cargar datos de ejemplo
- Seguro para compartir públicamente

#### Opción C: Datos en archivo de secretos
- Sube el Excel a Streamlit Secrets
- La app lo descarga en tiempo de ejecución
- Más complejo pero más seguro

---

## 🔒 Recomendación de Seguridad

Para proteger los datos de los estudiantes, te recomiendo:

### Opción 1: Despliegue Privado (RECOMENDADO)

```bash
# 1. Hacer el repositorio privado en GitHub
# Ve a: Settings → Danger Zone → Change visibility → Make private

# 2. Desplegar en Streamlit Cloud con GitHub Pro
# O usar Hugging Face Spaces (permite privados gratis)
```

### Opción 2: Usar datos de ejemplo públicamente

```bash
# 1. Modificar .gitignore para excluir datos reales
echo "RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx" >> .gitignore

# 2. Usar solo datos de ejemplo
git rm --cached RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx
git add RESULTADOS-ICFES-EJEMPLO.xlsx
git commit -m "Usar datos de ejemplo para despliegue público"
git push origin main
```

---

## 🚀 Despliegue Rápido (Paso a Paso)

### Para Streamlit Community Cloud:

```bash
# 1. Verificar que todo está listo
git status

# 2. Commit final
git add .
git commit -m "🚀 Listo para despliegue en Streamlit Cloud"
git push origin main

# 3. Ve a https://streamlit.io/cloud
# 4. Sign in con GitHub
# 5. New app → Selecciona tu repo → Deploy!
```

### Configuración en Streamlit Cloud:

- **Repository:** `alvaretto/resultados-icfes`
- **Branch:** `main`
- **Main file path:** `app_resultados_icfes.py`
- **Python version:** 3.11 (detectado automáticamente desde runtime.txt)

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError"
**Solución:** Verifica que `requirements-webapp.txt` esté en la raíz del repo

### Error: "File not found: RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx"
**Solución:** Asegúrate de que el archivo Excel esté en el repo y no en .gitignore

### App muy lenta
**Solución:** Verifica que estés usando `@st.cache_data` en la función de carga

### App se duerme
**Solución:** Normal en planes gratuitos. Se reactiva al visitarla.

---

## 📊 Comparación de Plataformas

| Plataforma | Gratuita | Fácil | Privado | SSL | Auto-deploy |
|------------|----------|-------|---------|-----|-------------|
| **Streamlit Cloud** | ✅ | ✅✅✅ | ⚠️* | ✅ | ✅ |
| **Hugging Face** | ✅ | ✅✅ | ✅ | ✅ | ✅ |
| **Render** | ✅ | ✅✅ | ❌ | ✅ | ✅ |
| **Railway** | ⚠️** | ✅✅ | ❌ | ✅ | ✅ |

*Requiere GitHub Pro para repos privados  
**$5/mes de crédito gratuito

---

## 🎯 Mi Recomendación

### Para uso interno (colegio/institución):
**→ Streamlit Community Cloud + Repositorio Privado (GitHub Pro)**
- Solicita GitHub Pro (gratis para educadores)
- Datos protegidos
- Fácil de actualizar

### Para demostración pública:
**→ Streamlit Community Cloud + Datos de Ejemplo**
- Usa `RESULTADOS-ICFES-EJEMPLO.xlsx`
- Seguro para compartir
- Muestra las capacidades sin exponer datos reales

---

## 📞 Próximos Pasos

1. **Decide qué opción usar** (privado con datos reales o público con datos de ejemplo)
2. **Sigue los pasos de despliegue** de la plataforma elegida
3. **Prueba la aplicación** en la URL generada
4. **Comparte la URL** con tu equipo/institución

---

## 🔗 Enlaces Útiles

- **Streamlit Cloud:** https://streamlit.io/cloud
- **Documentación Streamlit:** https://docs.streamlit.io/streamlit-community-cloud
- **Hugging Face Spaces:** https://huggingface.co/spaces
- **Render:** https://render.com
- **Railway:** https://railway.app
- **GitHub Education:** https://education.github.com (para GitHub Pro gratis)

---

**¿Necesitas ayuda?** Dime qué opción prefieres y te ayudo con el despliegue paso a paso.

