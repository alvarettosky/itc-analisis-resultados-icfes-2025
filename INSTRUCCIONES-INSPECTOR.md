# 🔍 INSTRUCCIONES: Inspector de HTML de Resultados ICFES

## 📋 Objetivo

Ejecutar el script `inspeccionar_html_resultados.py` para analizar la estructura HTML de la página de resultados del ICFES y determinar cómo extraer los puntajes individuales.

---

## 🚀 Pasos para Ejecutar

### 1. Activar el entorno virtual

```bash
source venv/bin/activate
```

### 2. Ejecutar el script

```bash
python3 inspeccionar_html_resultados.py
```

### 3. Seguir las instrucciones en pantalla

El script hará lo siguiente:

1. **Abrirá Firefox** automáticamente
2. **Navegará** a la página del ICFES
3. **Ingresará los datos** del primer estudiante:
   - Tipo de documento
   - Número de documento

4. **Esperará** a que tú:
   - ✅ Resuelvas el CAPTCHA
   - ✅ Hagas clic en "Ingresar"
   - ✅ Esperes a que cargue la página de resultados
   - ✅ Presiones ENTER en la terminal

5. **Analizará** la página:
   - Guardará el HTML completo
   - Buscará el puntaje global
   - Buscará elementos con clases relacionadas a puntajes
   - Intentará hacer clic en cada área de prueba
   - Guardará el HTML de cada vista

6. **Esperará** a que presiones ENTER para cerrar el navegador

---

## 📊 Archivos que se Generarán

### 1. `html_resultados.html`
- HTML completo de la página principal de resultados
- Contiene toda la estructura de la página

### 2. `html_Lectura_Critica.html` (si se hace clic exitoso)
- HTML de la vista de Lectura Crítica
- Puede contener el puntaje individual de esta área

### 3. `html_Matematicas.html` (si se hace clic exitoso)
- HTML de la vista de Matemáticas

### 4. `html_Sociales_y_Ciudadanas.html` (si se hace clic exitoso)
- HTML de la vista de Sociales y Ciudadanas

### 5. `html_Ciencias_Naturales.html` (si se hace clic exitoso)
- HTML de la vista de Ciencias Naturales

### 6. `html_Ingles.html` (si se hace clic exitoso)
- HTML de la vista de Inglés

---

## 🔍 Información que Buscará el Script

### En la Terminal

El script mostrará:

1. **Puntaje Global**
   - Formato: XXX/500
   - Ejemplo: 171/500
   - Contexto HTML donde se encuentra

2. **Elementos con clases de puntajes**
   - Elementos con clases como: `puntaje`, `score`, `resultado`, etc.
   - Texto visible de cada elemento
   - Clase CSS y tag HTML

3. **Números encontrados**
   - Todos los números de 2-3 dígitos en la página
   - Contexto de cada número

4. **Palabras clave**
   - Contexto de: "Lectura Crítica", "Matemáticas", "Sociales", etc.

5. **Clics en áreas**
   - Si se puede hacer clic en cada área
   - Si el HTML cambia después del clic
   - Números visibles en la nueva vista

---

## 📝 Qué Hacer Después

### 1. Revisar la salida en la terminal

Busca información como:

```
✅ Puntaje Global encontrado: 171/500

Contexto HTML:
<div class="puntaje-global">171/500</div>

✅ Selector "[class*="puntaje"]" encontró 6 elementos:
   1. Texto: Lectura Crítica: 45
      Clase: puntaje-area
      Tag: div
```

### 2. Revisar los archivos HTML generados

Abre los archivos HTML en un editor de texto y busca:

- Elementos `<div>`, `<span>`, `<p>` que contengan números
- Clases CSS que contengan: `puntaje`, `score`, `resultado`, `prueba`
- Atributos `data-*` que puedan contener puntajes
- Estructura de la página (Angular components)

### 3. Identificar los selectores CSS/XPath

Basándote en el análisis, identifica:

```python
# Ejemplo de selectores que podrías encontrar:
SELECTORES = {
    'puntaje_global': '.puntaje-global',
    'lectura_critica': '.area-lectura .puntaje',
    'matematicas': '.area-matematicas .puntaje',
    'sociales': '.area-sociales .puntaje',
    'ciencias': '.area-ciencias .puntaje',
    'ingles': '.area-ingles .puntaje'
}
```

### 4. Actualizar el script de extracción

Con los selectores identificados, actualiza la función `extraer_puntajes_de_pagina()` en `21-extraer_puntajes_desde_web.py`

---

## 🎯 Preguntas Clave a Responder

Después de ejecutar el inspector, deberías poder responder:

1. **¿Dónde está el puntaje global?**
   - ¿En qué elemento HTML?
   - ¿Qué clase CSS tiene?
   - ¿Qué selector usar?

2. **¿Están visibles los puntajes individuales en la página principal?**
   - ✅ SÍ → Identificar selectores para cada uno
   - ❌ NO → Necesitamos hacer clic en cada área

3. **¿Se puede hacer clic en cada área?**
   - ¿Qué elemento es clickeable?
   - ¿Cambia el HTML después del clic?
   - ¿Aparecen los puntajes individuales?

4. **¿Qué selectores usar para cada puntaje?**
   - CSS Selector o XPath
   - ¿Son consistentes entre estudiantes?

---

## 🐛 Posibles Problemas y Soluciones

### Problema 1: El script no encuentra elementos

**Solución**: 
- Aumenta los tiempos de espera (`time.sleep()`)
- Verifica que la página esté completamente cargada
- Revisa los selectores CSS

### Problema 2: No se puede hacer clic en las áreas

**Solución**:
- Los puntajes pueden estar en la página principal
- Busca en el HTML guardado
- Usa las herramientas de desarrollador del navegador (F12)

### Problema 3: El HTML es muy complejo

**Solución**:
- Usa las herramientas de desarrollador (F12)
- Inspecciona elementos manualmente
- Busca patrones en los nombres de clases
- Busca atributos `data-*` o `ng-*` (Angular)

---

## 💡 Consejos

1. **No cierres el navegador inmediatamente**
   - Inspecciona la página manualmente con F12
   - Busca los puntajes visualmente
   - Identifica los elementos en el inspector

2. **Toma capturas de pantalla**
   - De la página principal
   - De cada área si haces clic

3. **Anota los selectores**
   - Copia los selectores CSS que funcionen
   - Pruébalos en la consola del navegador:
     ```javascript
     document.querySelector('.selector-aqui')
     ```

4. **Busca patrones**
   - Angular usa componentes con nombres específicos
   - Busca clases como: `app-*`, `ng-*`, `mat-*`

---

## 📞 Siguiente Paso

Una vez que hayas ejecutado el inspector y revisado los resultados:

1. **Comparte los hallazgos**:
   - ¿Qué selectores encontraste?
   - ¿Los puntajes están visibles?
   - ¿Necesitas hacer clic en áreas?

2. **Actualizaremos el script**:
   - Agregaremos los selectores correctos
   - Implementaremos la lógica de navegación
   - Probaremos la extracción

3. **Ejecutaremos en modo prueba**:
   - 1 estudiante para validar
   - Verificar que todos los puntajes se extraen

---

## 🚀 Comando para Ejecutar

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar inspector
python3 inspeccionar_html_resultados.py

# Seguir las instrucciones en pantalla
# Resolver CAPTCHA
# Presionar ENTER cuando veas los resultados
# Revisar la salida en la terminal
# Revisar los archivos HTML generados
# Presionar ENTER para cerrar el navegador
```

---

**¡Buena suerte con la inspección!** 🔍

Una vez que tengas los resultados, podremos completar el script de extracción y generar el Excel consolidado.

