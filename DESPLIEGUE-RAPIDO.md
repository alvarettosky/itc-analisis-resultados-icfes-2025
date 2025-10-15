# 🚀 Despliegue Rápido - 5 Minutos

## ⚠️ IMPORTANTE: Proteger Datos Sensibles

Tu aplicación contiene **datos reales de estudiantes**. Antes de hacer push a GitHub:

### 🔒 PASO 1: Hacer el Repositorio Privado

```bash
# Ve a GitHub:
# https://github.com/alvaretto/resultados-icfes/settings

# Scroll hasta "Danger Zone"
# Click en "Change visibility"
# Selecciona "Make private"
# Confirma escribiendo el nombre del repositorio
```

**¿Por qué?** Para proteger los datos personales de los estudiantes (nombres, documentos, puntajes).

---

## 🚀 PASO 2: Push a GitHub

```bash
# Desde tu terminal:
cd /home/proyectos/Escritorio/Resultados-ICFES-2025

# Push de los commits pendientes
git push origin main
```

---

## 🌐 PASO 3: Desplegar en Streamlit Cloud

### 3.1 Crear cuenta (si no tienes)

1. Ve a: **https://streamlit.io/cloud**
2. Click en **"Sign up"** o **"Get started"**
3. Selecciona **"Continue with GitHub"**
4. Autoriza Streamlit a acceder a tu cuenta de GitHub

### 3.2 Desplegar la app

1. En el dashboard de Streamlit Cloud, click en **"New app"**
2. Completa el formulario:
   - **Repository:** `alvaretto/resultados-icfes`
   - **Branch:** `main`
   - **Main file path:** `app_resultados_icfes.py`
3. Click en **"Deploy!"**

### 3.3 Esperar el despliegue

- El proceso toma 2-3 minutos
- Verás logs en tiempo real
- Cuando termine, verás: "Your app is live! 🎉"

---

## ✅ PASO 4: Verificar la Aplicación

Tu app estará disponible en:
```
https://[nombre-generado].streamlit.app
```

**Prueba:**
- ✅ Verifica que cargue los 36 estudiantes
- ✅ Navega por todos los tabs
- ✅ Verifica que los datos sean correctos

---

## 🔗 PASO 5: Compartir la URL

**Para uso interno:**
- Comparte la URL solo con personal autorizado
- La app es privada si tu repo es privado (requiere GitHub Pro)

**Para uso público:**
- Si el repo es público, cualquiera puede acceder
- Considera usar datos de ejemplo en lugar de datos reales

---

## 🔧 Configuración Adicional (Opcional)

### Cambiar el nombre de la app

1. En Streamlit Cloud, ve a tu app
2. Click en **"Settings"** (⚙️)
3. En "General", cambia el nombre
4. Ejemplo: `analisis-icfes-2025`

### Configurar dominio personalizado

1. En "Settings" → "General"
2. Scroll hasta "Custom subdomain"
3. Ingresa tu subdominio preferido
4. Tu app estará en: `https://tu-nombre.streamlit.app`

---

## 📊 Actualizaciones Automáticas

Cada vez que hagas `git push` a la rama `main`, la app se actualizará automáticamente:

```bash
# Hacer cambios en el código
nano app_resultados_icfes.py

# Commit y push
git add app_resultados_icfes.py
git commit -m "Actualizar funcionalidad X"
git push origin main

# La app se actualizará automáticamente en 1-2 minutos
```

---

## ⚠️ Solución de Problemas Comunes

### Error: "Repository not found"
**Causa:** El repo es privado y Streamlit no tiene acceso  
**Solución:** Necesitas GitHub Pro para repos privados en Streamlit Cloud

### Error: "ModuleNotFoundError"
**Causa:** Falta una dependencia en requirements-webapp.txt  
**Solución:** Agrega la dependencia y haz push

### Error: "File not found: RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx"
**Causa:** El archivo no está en el repositorio  
**Solución:** Ya está agregado con `git add -f`

### App muy lenta
**Causa:** Primera carga o muchos datos  
**Solución:** Normal, usa `@st.cache_data` (ya implementado)

---

## 🎯 Resumen de Comandos

```bash
# 1. Hacer repo privado (en GitHub web)

# 2. Push a GitHub
git push origin main

# 3. Desplegar en Streamlit Cloud (en web)
# https://streamlit.io/cloud → New app

# 4. Compartir URL
# https://[tu-app].streamlit.app
```

---

## 📞 ¿Necesitas Ayuda?

- **Documentación Streamlit:** https://docs.streamlit.io/streamlit-community-cloud
- **Guía completa:** Ver `GUIA-DESPLIEGUE.md`
- **Soporte Streamlit:** https://discuss.streamlit.io

---

## 🎉 ¡Listo!

Tu aplicación de análisis ICFES estará disponible en línea, accesible desde cualquier dispositivo con internet.

**Tiempo total:** ~5 minutos  
**Costo:** $0 (100% gratuito)  
**Mantenimiento:** Automático

