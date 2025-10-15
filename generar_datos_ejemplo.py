#!/usr/bin/env python3
"""
Script para generar datos de ejemplo para la aplicación web ICFES
Los datos son ficticios y no contienen información real de estudiantes
"""

import pandas as pd
import numpy as np
import random

# Configurar semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

# Listas de nombres ficticios
nombres = [
    "Juan", "María", "Carlos", "Ana", "Luis", "Laura", "Pedro", "Sofía",
    "Diego", "Valentina", "Andrés", "Camila", "Santiago", "Isabella", "Mateo",
    "Daniela", "Sebastián", "Gabriela", "Felipe", "Natalia", "Alejandro", "Paula",
    "David", "Carolina", "Miguel", "Andrea", "Daniel", "Juliana", "Nicolás", "Mariana",
    "Samuel", "Catalina", "Tomás", "Melissa", "Martín", "Alejandra"
]

apellidos = [
    "García", "Rodríguez", "Martínez", "López", "González", "Pérez", "Sánchez",
    "Ramírez", "Torres", "Flores", "Rivera", "Gómez", "Díaz", "Cruz", "Morales",
    "Reyes", "Gutiérrez", "Ortiz", "Chávez", "Ruiz", "Hernández", "Jiménez",
    "Mendoza", "Vargas", "Castro", "Romero", "Álvarez", "Medina", "Rojas", "Silva",
    "Moreno", "Delgado", "Castillo", "Vega", "León", "Herrera"
]

# Generar 36 estudiantes
estudiantes = []

for i in range(36):
    # Generar puntajes con distribución realista
    # Puntajes individuales (0-100)
    lectura = np.random.normal(60, 15)
    matematicas = np.random.normal(55, 18)
    sociales = np.random.normal(58, 16)
    ciencias = np.random.normal(57, 17)
    ingles = np.random.normal(62, 20)
    
    # Limitar a rango 0-100
    lectura = max(0, min(100, lectura))
    matematicas = max(0, min(100, matematicas))
    sociales = max(0, min(100, sociales))
    ciencias = max(0, min(100, ciencias))
    ingles = max(0, min(100, ingles))
    
    # Calcular puntaje global (aproximado, 0-500)
    puntaje_global = (lectura + matematicas + sociales + ciencias + ingles) * 1.0
    puntaje_global = max(0, min(500, puntaje_global))
    
    estudiante = {
        'Grupo': '11A' if i < 18 else '11B',
        'Primer Apellido': random.choice(apellidos),
        'Segundo Apellido': random.choice(apellidos),
        'Primer Nombre': nombres[i],
        'Segundo Nombre': random.choice(nombres),
        'Tipo documento': 'TI' if i < 5 else 'CC',
        'Número de documento': 1000000000 + i * 1000 + random.randint(100, 999),
        'Lectura Crítica': round(lectura, 1),
        'Matemáticas': round(matematicas, 1),
        'Sociales y Ciudadanas': round(sociales, 1),
        'Ciencias Naturales': round(ciencias, 1),
        'Inglés': round(ingles, 1),
        'Puntaje Global': round(puntaje_global, 1)
    }
    
    estudiantes.append(estudiante)

# Crear DataFrame
df = pd.DataFrame(estudiantes)

# Guardar a Excel
df.to_excel('RESULTADOS-ICFES-EJEMPLO.xlsx', index=False)

print("✅ Archivo de ejemplo creado: RESULTADOS-ICFES-EJEMPLO.xlsx")
print(f"📊 Total de estudiantes: {len(df)}")
print(f"📈 Promedio Global: {df['Puntaje Global'].mean():.1f}")
print(f"📊 Rango: {df['Puntaje Global'].min():.1f} - {df['Puntaje Global'].max():.1f}")

