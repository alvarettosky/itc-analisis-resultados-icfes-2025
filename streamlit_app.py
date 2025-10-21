#!/usr/bin/env python3
"""
Punto de entrada para Streamlit Cloud
Este archivo ejecuta la aplicación principal desde app.py
"""

# Ejecutar el contenido de app.py
with open('app.py', 'r', encoding='utf-8') as f:
    exec(f.read())

