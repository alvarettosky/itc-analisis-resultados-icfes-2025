#!/bin/bash

# Script para renombrar archivos con prefijos numéricos según el orden del proceso

echo "🔄 Renombrando archivos según orden del proceso..."

# DOCUMENTACIÓN PRINCIPAL
mv README.md 01-README.md 2>/dev/null
mv INICIO_RAPIDO.txt 02-INICIO_RAPIDO.txt 2>/dev/null

# CONFIGURACIÓN Y VERIFICACIÓN INICIAL
mv verificar_configuracion.py 03-verificar_configuracion.py 2>/dev/null

# ANÁLISIS INICIAL
mv analizar_excel.py 04-analizar_excel.py 2>/dev/null
mv RESUMEN_ANALISIS.md 05-RESUMEN_ANALISIS.md 2>/dev/null

# SCRIPTS DE INSPECCIÓN (desarrollo)
mv inspeccionar_sitio_simple.py 06-inspeccionar_sitio_simple.py 2>/dev/null
mv inspeccionar_sitio.py 07-inspeccionar_sitio.py 2>/dev/null
mv inspeccionar_con_firefox.py 08-inspeccionar_con_firefox.py 2>/dev/null
mv inspeccionar_opciones_tipo_doc.py 09-inspeccionar_opciones_tipo_doc.py 2>/dev/null
mv probar_seleccion_tipo_doc.py 10-probar_seleccion_tipo_doc.py 2>/dev/null
mv inspeccionar_pagina_resultados.py 11-inspeccionar_pagina_resultados.py 2>/dev/null

# SCRIPT PRINCIPAL DE PRODUCCIÓN
mv descargar_resultados_icfes.py 12-descargar_resultados_icfes.py 2>/dev/null

# VERIFICACIÓN POST-DESCARGA
mv verificar_pdfs_completos.py 13-verificar_pdfs_completos.py 2>/dev/null

# DOCUMENTACIÓN TÉCNICA
mv NOTAS_TECNICAS.md 14-NOTAS_TECNICAS.md 2>/dev/null
mv SOLUCION_FINAL.md 15-SOLUCION_FINAL.md 2>/dev/null
mv RESUMEN_FINAL_DESCARGA.md 16-RESUMEN_FINAL_DESCARGA.md 2>/dev/null
mv CHANGELOG.md 17-CHANGELOG.md 2>/dev/null

# SINCRONIZACIÓN CON GITHUB
mv sincronizar_github.sh 18-sincronizar_github.sh 2>/dev/null
mv GITHUB_SYNC.md 19-GITHUB_SYNC.md 2>/dev/null

# UTILIDADES
mv mostrar_ayuda.py 20-mostrar_ayuda.py 2>/dev/null

echo "✅ Renombrado completado"
echo ""
echo "📋 Archivos renombrados:"
ls -1 [0-9][0-9]-* | nl
