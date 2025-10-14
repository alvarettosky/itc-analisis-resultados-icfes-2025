#!/usr/bin/env python3
"""
Script de ayuda para mostrar información útil sobre el proyecto
"""

def mostrar_banner():
    """Muestra el banner del proyecto"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   🎓  DESCARGADOR AUTOMÁTICO DE RESULTADOS ICFES SABER 11  🎓            ║
║                                                                           ║
║   Sistema de automatización para descarga masiva de resultados           ║
║   desde el portal oficial del ICFES                                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

def mostrar_menu():
    """Muestra el menú de opciones"""
    print("""
📋 MENÚ DE OPCIONES:

1️⃣  Verificar configuración
    Verifica que todo esté instalado y configurado correctamente
    Comando: python3 verificar_configuracion.py

2️⃣  Analizar archivo Excel
    Muestra información sobre los estudiantes en el archivo Excel
    Comando: python3 analizar_excel.py

3️⃣  Ejecutar descarga (MODO PRUEBA - 1 estudiante)
    Procesa solo 1 estudiante para verificar que todo funciona
    Comando: python3 descargar_resultados_icfes.py
    (Selecciona opción 1 cuando se te pregunte)

4️⃣  Ejecutar descarga (MODO COMPLETO - todos los estudiantes)
    Procesa todos los estudiantes del archivo Excel
    Comando: python3 descargar_resultados_icfes.py
    (Selecciona opción 2 cuando se te pregunte)

5️⃣  Ver documentación completa
    Lee el archivo README.md para más información
    Comando: cat README.md

6️⃣  Ver análisis técnico
    Lee el archivo RESUMEN_ANALISIS.md para detalles técnicos
    Comando: cat RESUMEN_ANALISIS.md
    """)

def mostrar_flujo():
    """Muestra el flujo del proceso"""
    print("""
🔄 FLUJO DEL PROCESO:

┌─────────────────────────────────────────────────────────────────┐
│ 1. INICIO                                                       │
│    - Leer archivo Excel con datos de estudiantes               │
│    - Iniciar navegador Firefox                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. PARA CADA ESTUDIANTE                                         │
│    a) Navegar al portal ICFES                                   │
│    b) Llenar formulario automáticamente                         │
│    c) ⚠️  PAUSA - Resolver CAPTCHA manualmente                 │
│    d) Presionar ENTER para continuar                            │
│    e) Hacer clic en "Ingresar"                                  │
│    f) Descargar PDF de resultados                               │
│    g) Renombrar PDF con nombre del estudiante                   │
│    h) Esperar 3 segundos antes del siguiente                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. FINALIZACIÓN                                                 │
│    - Cerrar navegador                                           │
│    - Generar logs de la ejecución                               │
│    - Mostrar resumen de resultados                              │
└─────────────────────────────────────────────────────────────────┘
    """)

def mostrar_estructura():
    """Muestra la estructura de archivos"""
    print("""
📁 ESTRUCTURA DE ARCHIVOS:

Resultados-ICFES-2025/
│
├── 📄 Scripts principales:
│   ├── descargar_resultados_icfes.py    ← Script principal de descarga
│   ├── verificar_configuracion.py      ← Verificar que todo esté OK
│   ├── analizar_excel.py               ← Analizar el archivo Excel
│   └── mostrar_ayuda.py                ← Este archivo de ayuda
│
├── 📚 Documentación:
│   ├── README.md                        ← Guía de uso completa
│   └── RESUMEN_ANALISIS.md              ← Análisis técnico detallado
│
├── 📊 Datos:
│   └── INSCRITOS_EXAMEN SABER 11 (36).xls  ← Archivo con estudiantes
│
├── 📦 Entorno virtual:
│   └── venv/                            ← Librerías de Python
│
├── 📥 Resultados (se crean automáticamente):
│   ├── pdfs_descargados/                ← PDFs descargados
│   │   ├── APELLIDO1_APELLIDO2_NOMBRE_DOC.pdf
│   │   └── ...
│   │
│   └── logs/                            ← Logs de ejecución
│       ├── exitosos_[timestamp].txt
│       ├── errores_[timestamp].txt
│       └── sin_resultados_[timestamp].txt
│
└── 🔧 Archivos temporales:
    ├── pagina_login.html
    ├── pagina_login_completa.html
    └── captura_login_firefox.png
    """)

def mostrar_consejos():
    """Muestra consejos útiles"""
    print("""
💡 CONSEJOS ÚTILES:

✅ ANTES DE EMPEZAR:
   • Ejecuta primero: python3 verificar_configuracion.py
   • Prueba con 1 estudiante antes de procesar todos
   • Asegúrate de tener conexión a Internet estable
   • Ten paciencia: cada estudiante toma 5-10 minutos

⚠️  DURANTE LA EJECUCIÓN:
   • NO cierres el navegador Firefox manualmente
   • NO cierres la terminal mientras se ejecuta
   • Resuelve el CAPTCHA cuando se te solicite
   • Presiona ENTER después de resolver el CAPTCHA
   • Supervisa el proceso por si hay errores

📊 DESPUÉS DE LA EJECUCIÓN:
   • Revisa los logs en la carpeta logs/
   • Verifica que los PDFs se descargaron correctamente
   • Si hubo errores, puedes volver a ejecutar solo para esos estudiantes

⏱️  TIEMPO ESTIMADO:
   • 1 estudiante: ~5-10 minutos
   • 36 estudiantes: ~3-6 horas
   • Recomendación: Ejecutar en horarios de baja demanda

🔐 SEGURIDAD:
   • El script NO almacena contraseñas
   • Solo accede a datos públicos del portal
   • Respeta los términos de servicio del ICFES
   • Implementa delays para no sobrecargar el servidor
    """)

def mostrar_solucion_problemas():
    """Muestra soluciones a problemas comunes"""
    print("""
🐛 SOLUCIÓN DE PROBLEMAS COMUNES:

❌ Error: "ModuleNotFoundError"
   Solución: Activa el entorno virtual
   → source venv/bin/activate

❌ Error: "Firefox not found"
   Solución: Instala Firefox
   → sudo pacman -S firefox (Arch)
   → sudo apt install firefox (Ubuntu)

❌ El navegador no se abre
   Solución: Verifica la instalación de Firefox
   → firefox --version

❌ Los PDFs no se descargan
   Solución: Verifica permisos de la carpeta
   → ls -la pdfs_descargados/

❌ El CAPTCHA no aparece
   Solución: Verifica tu conexión a Internet
   → ping google.com

❌ Error al leer el Excel
   Solución: Verifica la ruta del archivo
   → ls -la "INSCRITOS_EXAMEN SABER 11 (36).xls"

📞 Si el problema persiste:
   • Revisa los logs en la carpeta logs/
   • Consulta el archivo RESUMEN_ANALISIS.md
   • Ejecuta: python3 verificar_configuracion.py
    """)

def main():
    """Función principal"""
    mostrar_banner()
    
    while True:
        print("\n" + "="*80)
        print("¿Qué información deseas ver?")
        print("="*80)
        print("\n1. Menú de opciones")
        print("2. Flujo del proceso")
        print("3. Estructura de archivos")
        print("4. Consejos útiles")
        print("5. Solución de problemas")
        print("6. Ver todo")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción (0-6): ").strip()
        
        if opcion == "1":
            mostrar_menu()
        elif opcion == "2":
            mostrar_flujo()
        elif opcion == "3":
            mostrar_estructura()
        elif opcion == "4":
            mostrar_consejos()
        elif opcion == "5":
            mostrar_solucion_problemas()
        elif opcion == "6":
            mostrar_menu()
            mostrar_flujo()
            mostrar_estructura()
            mostrar_consejos()
            mostrar_solucion_problemas()
        elif opcion == "0":
            print("\n👋 ¡Hasta luego! Buena suerte con la descarga de resultados.\n")
            break
        else:
            print("\n❌ Opción no válida. Por favor, selecciona un número del 0 al 6.")
        
        input("\nPresiona ENTER para continuar...")

if __name__ == '__main__':
    main()

