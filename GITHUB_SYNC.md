# 🔄 Guía de Sincronización con GitHub

## 📍 Información del Repositorio

- **URL**: https://github.com/alvaretto/resultados-icfes
- **Usuario**: alvaretto
- **Rama principal**: main
- **Estado**: ✅ Configurado y sincronizado

---

## 🚀 Sincronización Rápida

### Opción 1: Usar el Script Automático (Recomendado)

```bash
# Con mensaje de commit
./sincronizar_github.sh "Descripción de los cambios"

# Sin mensaje (te pedirá uno)
./sincronizar_github.sh
```

### Opción 2: Comandos Git Manuales

```bash
# 1. Ver cambios
git status

# 2. Agregar archivos
git add .

# 3. Hacer commit
git commit -m "Descripción de los cambios"

# 4. Subir a GitHub
git push origin main
```

---

## 📥 Descargar Cambios del Repositorio

Si trabajas desde múltiples computadoras o con otras personas:

```bash
# Descargar cambios del repositorio remoto
git pull origin main
```

---

## 🔍 Comandos Útiles

### Ver el estado del repositorio
```bash
git status
```

### Ver el historial de commits
```bash
git log --oneline --graph --all
```

### Ver diferencias antes de hacer commit
```bash
git diff
```

### Ver archivos modificados
```bash
git status -s
```

### Ver información del repositorio remoto
```bash
git remote -v
```

### Ver la rama actual
```bash
git branch
```

---

## 📋 Flujo de Trabajo Recomendado

### 1. Antes de Empezar a Trabajar

```bash
# Descargar últimos cambios
git pull origin main
```

### 2. Mientras Trabajas

Haz cambios en los archivos normalmente.

### 3. Después de Hacer Cambios

```bash
# Opción A: Usar el script
./sincronizar_github.sh "Descripción de los cambios"

# Opción B: Comandos manuales
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

---

## 🛡️ Archivos Protegidos (No se suben a GitHub)

El archivo `.gitignore` está configurado para **NO subir** los siguientes archivos sensibles:

### ❌ Archivos Excluidos:
- ✅ `pdfs_descargados/*.pdf` - PDFs con información de estudiantes
- ✅ `logs/*.txt` - Logs con información sensible
- ✅ `*.xls` y `*.xlsx` - Archivos Excel con datos de estudiantes
- ✅ `venv/` - Entorno virtual de Python
- ✅ `*.html` - Archivos HTML temporales
- ✅ `__pycache__/` - Archivos compilados de Python

### ✅ Archivos Incluidos:
- ✅ Scripts Python (`.py`)
- ✅ Documentación (`.md`, `.txt`)
- ✅ Configuración (`.gitignore`)
- ✅ Imágenes de capturas de pantalla (`.png`)
- ✅ Carpetas vacías (`logs/.gitkeep`, `pdfs_descargados/.gitkeep`)

---

## 🔐 Seguridad y Privacidad

### ⚠️ IMPORTANTE:

1. **NUNCA subas archivos con información personal de estudiantes**
   - PDFs de resultados
   - Archivos Excel con datos
   - Logs con información sensible

2. **Verifica antes de hacer push**
   ```bash
   git status
   ```
   Asegúrate de que no aparezcan archivos sensibles.

3. **Si accidentalmente agregaste un archivo sensible**
   ```bash
   # Quitar del staging
   git reset HEAD nombre_archivo.pdf
   
   # O deshacer el último commit (sin perder cambios)
   git reset --soft HEAD~1
   ```

---

## 🌐 Ver el Repositorio en GitHub

Abre en tu navegador:
```
https://github.com/alvaretto/resultados-icfes
```

---

## 📊 Estadísticas del Proyecto

### Primer Commit
- **Fecha**: 14 de octubre de 2025
- **Versión**: 2.0
- **Archivos**: 23 archivos
- **Líneas de código**: ~3,920 líneas

### Estado Actual
- **Rama**: main
- **Remote**: origin (https://github.com/alvaretto/resultados-icfes.git)
- **Tracking**: Configurado automáticamente

---

## 🆘 Solución de Problemas

### Problema: "Updates were rejected"

**Causa**: Hay cambios en el repositorio remoto que no tienes localmente.

**Solución**:
```bash
git pull origin main
# Resolver conflictos si los hay
git push origin main
```

### Problema: "Merge conflict"

**Causa**: Cambios en el mismo archivo tanto local como remotamente.

**Solución**:
```bash
# 1. Ver archivos en conflicto
git status

# 2. Editar los archivos y resolver conflictos manualmente
# Busca las marcas: <<<<<<< HEAD, =======, >>>>>>>

# 3. Agregar archivos resueltos
git add archivo_resuelto.py

# 4. Completar el merge
git commit -m "Resuelto conflicto en archivo_resuelto.py"

# 5. Subir cambios
git push origin main
```

### Problema: "Permission denied"

**Causa**: No tienes permisos o no estás autenticado.

**Solución**:
```bash
# Verificar configuración de usuario
git config user.name
git config user.email

# Configurar si es necesario
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### Problema: "fatal: not a git repository"

**Causa**: No estás en el directorio del proyecto.

**Solución**:
```bash
cd /home/proyectos/Escritorio/Resultados-ICFES-2025
```

---

## 📚 Recursos Adicionales

### Documentación de Git
- [Git - Guía Sencilla](https://rogerdudler.github.io/git-guide/index.es.html)
- [Git Book en Español](https://git-scm.com/book/es/v2)

### GitHub
- [GitHub Docs](https://docs.github.com/es)
- [GitHub Desktop](https://desktop.github.com/) - Interfaz gráfica para Git

---

## ✅ Verificación de Configuración

Para verificar que todo está configurado correctamente:

```bash
# 1. Verificar repositorio remoto
git remote -v

# 2. Verificar rama actual
git branch

# 3. Verificar estado
git status

# 4. Verificar último commit
git log -1
```

**Salida esperada**:
```
origin  https://github.com/alvaretto/resultados-icfes.git (fetch)
origin  https://github.com/alvaretto/resultados-icfes.git (push)

* main

En la rama main
Tu rama está actualizada con 'origin/main'.
```

---

## 🎯 Comandos Más Usados

```bash
# Ver cambios
git status

# Sincronizar (script automático)
./sincronizar_github.sh "mensaje"

# Descargar cambios
git pull origin main

# Ver historial
git log --oneline

# Ver repositorio en GitHub
xdg-open https://github.com/alvaretto/resultados-icfes
```

---

**Configurado el**: 14 de octubre de 2025  
**Repositorio**: https://github.com/alvaretto/resultados-icfes  
**Estado**: ✅ Completamente configurado y funcional

