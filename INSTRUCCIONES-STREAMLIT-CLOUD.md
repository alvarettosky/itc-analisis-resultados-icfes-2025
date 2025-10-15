# 🚀 Instrucciones para Desplegar en Streamlit Cloud

## ✅ TODO ESTÁ LISTO - Solo sigue estos pasos:

---

## PASO 1: Ir a Streamlit Cloud

Ya abrí la página en tu navegador. Si no la ves, ve a:
👉 **https://share.streamlit.io/**

---

## PASO 2: Iniciar Sesión

1. Click en **"Sign in"** (arriba a la derecha)
2. Selecciona **"Continue with GitHub"**
3. Autoriza a Streamlit a acceder a tu cuenta de GitHub
4. Deberías ver tu dashboard

---

## PASO 3: Crear Nueva App

1. Click en el botón **"New app"** o **"Create app"**
2. Te aparecerá un formulario

---

## PASO 4: Completar el Formulario

### Opción A: Formulario Simple (URL completa)

Si ves un campo que dice **"GitHub URL"**, pega esto:

```
https://github.com/alvarettosky/itc-analisis-resultados-icfes-2025/blob/main/app.py
```

### Opción B: Formulario Interactivo (Recomendado)

Si ves campos separados, completa así:

**Repository:**
```
alvarettosky/itc-analisis-resultados-icfes-2025
```

**Branch:**
```
main
```

**Main file path:**
```
app.py
```

**App URL (opcional):**
```
itc-resultados-icfes-2025
```

---

## PASO 5: Configuración Avanzada (Opcional)

Si hay un botón de **"Advanced settings"**, puedes:

- **Python version:** Dejar en automático (detectará 3.11 desde runtime.txt)
- **Secrets:** No necesario por ahora
- Dejar todo lo demás por defecto

---

## PASO 6: Desplegar

1. Click en el botón **"Deploy!"** (grande, azul)
2. Espera 2-3 minutos
3. Verás logs en tiempo real:
   ```
   ⏳ Installing dependencies...
   📦 Collecting streamlit==1.29.0
   📦 Collecting pandas==2.0.3
   📦 Collecting plotly==5.18.0
   ✅ Successfully installed all packages
   🚀 Starting app...
   ✅ Your app is live!
   ```

---

## PASO 7: Verificar que Funciona

Una vez que veas **"Your app is live!"**, verifica:

✅ Se carga la página principal  
✅ Dice "36 estudiantes"  
✅ Puedes navegar entre los 5 tabs  
✅ Los gráficos se muestran correctamente  

---

## 🎯 Tu URL Final Será:

```
https://itc-resultados-icfes-2025.streamlit.app
```

O algo similar si Streamlit genera un nombre automático.

---

## 🐛 Si Hay Errores

### Error: "ModuleNotFoundError"
**YA ESTÁ SOLUCIONADO** ✅ - Actualicé las dependencias con versiones exactas

### Error: "File not found"
**YA ESTÁ SOLUCIONADO** ✅ - El archivo Excel está en el repositorio

### Error: "Repository not found"
**Solución:** Verifica que hayas autorizado a Streamlit a acceder a tu cuenta de GitHub

### La app se queda "Installing dependencies" por más de 5 minutos
**Solución:** 
1. Refresca la página
2. O click en "Manage app" → "Reboot app"

---

## 📱 Después del Despliegue

### Compartir la app:
- Copia la URL y compártela con quien quieras
- ⚠️ **IMPORTANTE:** Tu repositorio es PÚBLICO, así que cualquiera con la URL puede ver la app
- Si quieres hacerla privada, necesitas GitHub Pro (gratis para educadores)

### Actualizar la app:
Cada vez que hagas cambios:
```bash
git add .
git commit -m "Descripción del cambio"
git push origin main
```
La app se actualizará automáticamente en 1-2 minutos.

### Ver logs:
1. En tu app, click en "⋮" (menú)
2. Click en "Manage app"
3. Ve a la pestaña "Logs"

### Reiniciar la app:
1. En tu app, click en "⋮" (menú)
2. Click en "Reboot app"

---

## ✅ Checklist Final

- [x] Código subido a GitHub ✅
- [x] Dependencias corregidas ✅
- [x] Archivo Excel incluido ✅
- [x] Configuración de Streamlit lista ✅
- [ ] Crear app en Streamlit Cloud 👈 **ESTE ES TU PASO**
- [ ] Verificar que funciona
- [ ] Compartir URL

---

## 🎉 ¡Eso es Todo!

Solo necesitas:
1. Ir a https://share.streamlit.io/
2. Sign in con GitHub
3. New app
4. Pegar: `alvarettosky/itc-analisis-resultados-icfes-2025` y `app.py`
5. Deploy!

**Tiempo total: 3 minutos** ⏱️

---

## 📞 Si Necesitas Ayuda

Dime en qué paso estás y te ayudo específicamente con ese paso.

Opciones:
- "Estoy en el paso 2, no veo el botón de Sign in"
- "Estoy en el paso 4, no sé qué poner en Repository"
- "Ya desplegué pero da error X"
- etc.

---

**¡Adelante! Todo está listo del lado del código. Solo falta hacer click en Deploy.** 🚀

