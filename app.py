#!/usr/bin/env python3
"""
Aplicación Web de Análisis de Resultados ICFES Saber 11
Versión para despliegue público con datos de ejemplo
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from scipy import stats
import os

# Configuración de la página
st.set_page_config(
    page_title="Análisis ICFES Saber 11",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .institution-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 1rem 0.5rem 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px 10px 0 0;
        margin-bottom: 0;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 0.5rem 1rem 1rem 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 0 0 10px 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Constantes
AREAS = ['Lectura Crítica', 'Matemáticas', 'Sociales y Ciudadanas', 'Ciencias Naturales', 'Inglés']
COLORES = {
    'Lectura Crítica': '#1f77b4',
    'Matemáticas': '#ff7f0e',
    'Sociales y Ciudadanas': '#2ca02c',
    'Ciencias Naturales': '#d62728',
    'Inglés': '#9467bd'
}

# Determinar qué archivo usar
def obtener_archivo_datos():
    """Determina qué archivo de datos usar (real o ejemplo)"""
    # Prioridad 1: Archivo ITC adaptado (datos reales)
    archivo_itc = 'ITC-RESULTADOS-ICFES-2025-ADAPTADO.xlsx'
    # Prioridad 2: Archivo original
    archivo_real = 'RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx'
    # Prioridad 3: Archivo de ejemplo
    archivo_ejemplo = 'RESULTADOS-ICFES-EJEMPLO.xlsx'

    if os.path.exists(archivo_itc):
        return archivo_itc, False  # False = no es ejemplo (datos reales ITC)
    elif os.path.exists(archivo_real):
        return archivo_real, False  # False = no es ejemplo
    elif os.path.exists(archivo_ejemplo):
        return archivo_ejemplo, True  # True = es ejemplo
    else:
        return None, None

@st.cache_data
def cargar_datos():
    """Carga y preprocesa los datos del Excel"""
    archivo, es_ejemplo = obtener_archivo_datos()
    
    if archivo is None:
        return None, None
    
    try:
        df = pd.read_excel(archivo)
        
        # Filtrar solo las filas de estudiantes reales (con grupo asignado)
        df = df[df['Grupo'].notna()].copy()

        # Crear nombre completo
        df['Nombre Completo'] = (
            df['Primer Nombre'].fillna('') + ' ' +
            df['Segundo Nombre'].fillna('') + ' ' +
            df['Primer Apellido'].fillna('') + ' ' +
            df['Segundo Apellido'].fillna('')
        ).str.strip().str.replace(r'\s+', ' ', regex=True)
        
        # Clasificación por puntaje global
        def clasificar_puntaje(puntaje):
            if puntaje < 200:
                return 'Bajo'
            elif puntaje < 300:
                return 'Medio'
            elif puntaje < 400:
                return 'Alto'
            else:
                return 'Superior'
        
        df['Clasificación'] = df['Puntaje Global'].apply(clasificar_puntaje)
        
        return df, es_ejemplo
        
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None, None

def clasificar_por_rango(puntaje):
    """Clasifica un puntaje global en categorías"""
    if pd.isna(puntaje):
        return 'Sin datos'
    elif puntaje <= 200:
        return 'Bajo (0-200)'
    elif puntaje <= 300:
        return 'Medio (201-300)'
    elif puntaje <= 400:
        return 'Alto (301-400)'
    else:
        return 'Superior (401-500)'

def crear_radar_chart(estudiante_data, areas):
    """Crea un gráfico de radar para un estudiante"""
    valores = [estudiante_data[area] for area in areas]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=areas,
        fill='toself',
        name=estudiante_data['Nombre Completo'],
        line=dict(color='#1f77b4', width=2),
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title=f"Perfil de {estudiante_data['Nombre Completo']}",
        height=500
    )
    
    return fig

def main():
    """Función principal de la aplicación"""
    
    # Header
    st.markdown('<div class="institution-header">Instituto Tecnológico Calarcá</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">📊 Análisis de Resultados ICFES Saber 11 - 2025</div>', unsafe_allow_html=True)
    
    # Cargar datos
    df, es_ejemplo = cargar_datos()
    
    if df is None:
        st.error("❌ No se encontró el archivo de datos. Por favor, asegúrate de que existe 'RESULTADOS-ICFES-EJEMPLO.xlsx' o 'RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx'")
        st.info("💡 Para generar datos de ejemplo, ejecuta: `python generar_datos_ejemplo.py`")
        return
    
    # Advertencia si son datos de ejemplo
    if es_ejemplo:
        st.warning("⚠️ **MODO DEMOSTRACIÓN**: Esta aplicación está usando datos ficticios de ejemplo. Los nombres y puntajes no son reales.")
    

    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Vista General",
        "👤 Por Estudiante",
        "📚 Por Área",
        "🏆 Rankings",
        "📈 Segmentación"
    ])
    
    # TAB 1: Vista General
    with tab1:
        st.header("📊 Resumen General de Resultados")
        
        # Nota metodológica
        st.info("""
        **📚 Importante:** Las áreas del ICFES Saber 11 utilizan escalas y criterios de evaluación diferentes. 
        Por esta razón, **NO se comparan promedios entre áreas diferentes** en esta aplicación. 
        Los análisis se realizan por área individual.
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Estudiantes Analizados",
                len(df),
                help="Total de estudiantes con resultados ICFES Saber 11"
            )
        
        with col2:
            promedio_global = df['Puntaje Global'].mean()
            st.metric(
                "Promedio Global",
                f"{promedio_global:.0f}",
                help="Promedio del puntaje global (0-500)"
            )

        with col3:
            mediana_global = df['Puntaje Global'].median()
            st.metric(
                "Mediana Global",
                f"{mediana_global:.0f}",
                help="Mediana del puntaje global (0-500)"
            )
        
        st.markdown("---")
        
        # Estadísticas por área
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Estadísticas por Área")
            st.markdown("*Cada área se analiza de forma independiente*")
            
            stats_data = []
            for area in AREAS:
                stats_data.append({
                    'Área': area,
                    'Promedio': f"{df[area].mean():.0f}",
                    'Mediana': f"{df[area].median():.0f}",
                    'Desv. Std': f"{df[area].std():.0f}"
                })
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("📈 Distribución del Puntaje Global")
            fig = px.histogram(
                df,
                x='Puntaje Global',
                nbins=20,
                labels={'Puntaje Global': 'Puntaje Global', 'count': 'Frecuencia'},
                color_discrete_sequence=['#1f77b4']
            )
            fig.add_vline(
                x=df['Puntaje Global'].mean(),
                line_dash="dash",
                line_color="red",
                annotation_text=f"Promedio: {df['Puntaje Global'].mean():.0f}"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Información adicional
        st.subheader("📋 Información del Grupo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Puntaje Máximo",
                f"{df['Puntaje Global'].max():.0f}",
                help="Mejor puntaje global del grupo"
            )

        with col2:
            st.metric(
                "Puntaje Mínimo",
                f"{df['Puntaje Global'].min():.0f}",
                help="Menor puntaje global del grupo"
            )

        with col3:
            st.metric(
                "Rango",
                f"{df['Puntaje Global'].max() - df['Puntaje Global'].min():.0f}",
                help="Diferencia entre el máximo y mínimo"
            )
    
    # TAB 2: Análisis por Estudiante Individual
    with tab2:
        st.header("👤 Análisis por Estudiante Individual")

        # Búsqueda de estudiante
        col1, col2 = st.columns([3, 1])

        with col1:
            busqueda = st.text_input(
                "🔍 Buscar estudiante por nombre o documento",
                placeholder="Escribe el nombre o número de documento..."
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            mostrar_todos = st.checkbox("Mostrar todos", value=False)

        # Filtrar estudiantes
        if busqueda:
            df_filtrado = df[
                df['Nombre Completo'].str.contains(busqueda, case=False, na=False) |
                df['Número de documento'].astype(str).str.contains(busqueda, na=False)
            ]
        elif mostrar_todos:
            df_filtrado = df
        else:
            df_filtrado = df.head(5)

        if len(df_filtrado) == 0:
            st.warning("No se encontraron estudiantes con ese criterio de búsqueda.")
        else:
            st.info(f"Mostrando {len(df_filtrado)} estudiante(s)")

            # Selector de estudiante
            estudiante_seleccionado = st.selectbox(
                "Selecciona un estudiante para ver su perfil detallado:",
                df_filtrado['Nombre Completo'].tolist()
            )

            if estudiante_seleccionado:
                estudiante = df_filtrado[df_filtrado['Nombre Completo'] == estudiante_seleccionado].iloc[0]

                st.markdown("---")

                # Información del estudiante
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("### 📋 Datos Personales")
                    st.write(f"**Nombre:** {estudiante['Nombre Completo']}")
                    st.write(f"**Documento:** {estudiante['Tipo documento']} {estudiante['Número de documento']}")
                    if 'Grupo' in estudiante and pd.notna(estudiante['Grupo']):
                        st.write(f"**Grupo:** {estudiante['Grupo']}")

                with col2:
                    st.markdown("### 🎯 Puntaje Global")
                    puntaje_global = estudiante['Puntaje Global']
                    st.metric("Puntaje Total", f"{int(round(puntaje_global))}/500")
                    clasificacion = clasificar_por_rango(puntaje_global)
                    st.write(f"**Clasificación:** {clasificacion}")

                with col3:
                    st.markdown("### 📊 Posición")
                    ranking = (df['Puntaje Global'] > puntaje_global).sum() + 1
                    st.metric("Ranking General", f"{ranking}° de {len(df)}")
                    percentil = ((len(df) - ranking + 1) / len(df)) * 100
                    st.write(f"**Percentil:** {percentil:.0f}%")

                st.markdown("---")

                # Puntajes por área
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📚 Puntajes por Área")
                    for area in AREAS:
                        puntaje = estudiante[area]
                        promedio_area = df[area].mean()
                        diferencia = puntaje - promedio_area

                        col_a, col_b, col_c = st.columns([2, 1, 1])
                        with col_a:
                            st.write(f"**{area}:**")
                        with col_b:
                            st.write(f"{int(round(puntaje))}/100")
                        with col_c:
                            if diferencia > 0:
                                st.write(f"🟢 +{int(round(diferencia))}")
                            else:
                                st.write(f"🔴 {int(round(diferencia))}")

                with col2:
                    st.markdown("### 🎯 Perfil de Competencias")
                    fig_radar = crear_radar_chart(estudiante, AREAS)
                    st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab3:
        st.header("📚 Análisis por Área de Conocimiento")
        st.info("Selecciona un área para ver análisis detallado")
        # ... código del TAB 3 ...
    
    with tab4:
        st.header("🏆 Rankings")
        st.info("Rankings generales y por área")
        # ... código del TAB 4 ...
    
    with tab5:
        st.header("📈 Segmentación por Rangos")
        st.info("Clasificación de estudiantes por nivel de desempeño")
        # ... código del TAB 5 ...

if __name__ == "__main__":
    main()

