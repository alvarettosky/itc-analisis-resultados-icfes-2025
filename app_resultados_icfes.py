#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Web Interactiva para Visualización y Análisis de Resultados ICFES Saber 11
Autor: Sistema de Análisis ICFES
Fecha: 2025-10-14
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Análisis Resultados ICFES Saber 11 - 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Constantes
ARCHIVO_EXCEL = 'RESULTADOS-ICFES-AULA-REGULAR-2025.xlsx'
AREAS = ['Lectura Crítica', 'Matemáticas', 'Sociales y Ciudadanas', 'Ciencias Naturales', 'Inglés']
COLORES = {
    'Lectura Crítica': '#1f77b4',
    'Matemáticas': '#ff7f0e',
    'Sociales y Ciudadanas': '#2ca02c',
    'Ciencias Naturales': '#d62728',
    'Inglés': '#9467bd',
    'Puntaje Global': '#8c564b'
}

@st.cache_data
def cargar_datos():
    """Carga y preprocesa los datos del Excel"""
    try:
        df = pd.read_excel(ARCHIVO_EXCEL)
        
        # Limpiar datos
        df = df.dropna(subset=['Número de documento'])
        
        # Crear nombre completo
        df['Nombre Completo'] = (
            df['Primer Nombre'].fillna('') + ' ' + 
            df['Segundo Nombre'].fillna('') + ' ' + 
            df['Primer Apellido'].fillna('') + ' ' + 
            df['Segundo Apellido'].fillna('')
        ).str.strip().str.replace(r'\s+', ' ', regex=True)
        
        # Convertir puntajes a numérico
        for area in AREAS + ['Puntaje Global']:
            df[area] = pd.to_numeric(df[area], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

def calcular_estadisticas(df, columna):
    """Calcula estadísticas descriptivas para una columna"""
    datos = df[columna].dropna()
    
    return {
        'Promedio': datos.mean(),
        'Mediana': datos.median(),
        'Moda': datos.mode()[0] if len(datos.mode()) > 0 else None,
        'Desv. Estándar': datos.std(),
        'Mínimo': datos.min(),
        'Máximo': datos.max(),
        'Percentil 25': datos.quantile(0.25),
        'Percentil 50': datos.quantile(0.50),
        'Percentil 75': datos.quantile(0.75),
        'Rango': datos.max() - datos.min(),
        'Coef. Variación': (datos.std() / datos.mean() * 100) if datos.mean() != 0 else 0
    }

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
    st.markdown('<div class="main-header">📊 Análisis de Resultados ICFES Saber 11 - 2025</div>', unsafe_allow_html=True)
    
    # Cargar datos
    df = cargar_datos()
    
    if df is None or len(df) == 0:
        st.error("No se pudieron cargar los datos. Verifica que el archivo Excel exista.")
        return
    
    # Sidebar con información general
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=ICFES+2025", use_container_width=True)
        st.markdown("### 📋 Información General")
        st.metric("Total de Estudiantes", len(df))
        st.metric("Promedio Global", f"{df['Puntaje Global'].mean():.1f}")
        st.metric("Puntaje Máximo", f"{df['Puntaje Global'].max():.1f}")
        st.metric("Puntaje Mínimo", f"{df['Puntaje Global'].min():.1f}")
        
        st.markdown("---")
        st.markdown("### 🎯 Navegación")
        st.markdown("""
        - **Vista General**: Resumen y estadísticas
        - **Por Estudiante**: Análisis individual
        - **Por Área**: Análisis por materia
        - **Comparativo**: Rankings y correlaciones
        - **Segmentación**: Clasificación por rangos
        """)
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Vista General",
        "👤 Por Estudiante",
        "📚 Por Área",
        "🏆 Comparativo",
        "📈 Segmentación"
    ])
    
    # TAB 1: Vista General
    with tab1:
        st.header("📊 Resumen General de Resultados")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Estudiantes Analizados",
                len(df),
                help="Total de estudiantes con resultados"
            )
        
        with col2:
            promedio_global = df['Puntaje Global'].mean()
            st.metric(
                "Promedio Global",
                f"{promedio_global:.1f}",
                help="Promedio del puntaje global (0-500)"
            )
        
        with col3:
            mejor_area = df[AREAS].mean().idxmax()
            st.metric(
                "Área Más Fuerte",
                mejor_area,
                f"{df[mejor_area].mean():.1f}",
                help="Área con mejor promedio"
            )
        
        with col4:
            peor_area = df[AREAS].mean().idxmin()
            st.metric(
                "Área a Mejorar",
                peor_area,
                f"{df[peor_area].mean():.1f}",
                help="Área con menor promedio"
            )
        
        st.markdown("---")
        
        # Gráfico de promedios por área
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Promedios por Área de Conocimiento")
            promedios = df[AREAS].mean().sort_values(ascending=True)
            
            fig = px.bar(
                x=promedios.values,
                y=promedios.index,
                orientation='h',
                labels={'x': 'Promedio', 'y': 'Área'},
                color=promedios.values,
                color_continuous_scale='Blues',
                text=promedios.values.round(1)
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_range=[0, 100]
            )
            st.plotly_chart(fig, use_container_width=True)
        
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
                annotation_text=f"Promedio: {df['Puntaje Global'].mean():.1f}"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Box plots de todas las áreas
        st.subheader("📦 Distribución y Dispersión por Área")
        
        fig = go.Figure()
        for area in AREAS:
            fig.add_trace(go.Box(
                y=df[area],
                name=area,
                marker_color=COLORES[area],
                boxmean='sd'
            ))
        
        fig.update_layout(
            yaxis_title="Puntaje",
            height=500,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: Por Estudiante
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
                    st.metric("Puntaje Total", f"{puntaje_global:.1f}/500")
                    clasificacion = clasificar_por_rango(puntaje_global)
                    st.write(f"**Clasificación:** {clasificacion}")
                
                with col3:
                    st.markdown("### 📊 Posición")
                    ranking = (df['Puntaje Global'] > puntaje_global).sum() + 1
                    st.metric("Ranking General", f"{ranking}° de {len(df)}")
                    percentil = ((len(df) - ranking + 1) / len(df)) * 100
                    st.write(f"**Percentil:** {percentil:.1f}%")
                
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
                            st.write(f"{puntaje:.1f}/100")
                        with col_c:
                            if diferencia > 0:
                                st.write(f"🟢 +{diferencia:.1f}")
                            else:
                                st.write(f"🔴 {diferencia:.1f}")
                
                with col2:
                    st.markdown("### 🎯 Perfil de Competencias")
                    fig_radar = crear_radar_chart(estudiante, AREAS)
                    st.plotly_chart(fig_radar, use_container_width=True)

    # TAB 3: Por Área
    with tab3:
        st.header("📚 Análisis por Área de Conocimiento")

        # Selector de área
        area_seleccionada = st.selectbox(
            "Selecciona un área para análisis detallado:",
            AREAS + ['Puntaje Global']
        )

        st.markdown("---")

        # Estadísticas del área
        st.subheader(f"📊 Estadísticas de {area_seleccionada}")

        stats_area = calcular_estadisticas(df, area_seleccionada)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Promedio", f"{stats_area['Promedio']:.2f}")
        with col2:
            st.metric("Mediana", f"{stats_area['Mediana']:.2f}")
        with col3:
            st.metric("Desv. Estándar", f"{stats_area['Desv. Estándar']:.2f}")
        with col4:
            st.metric("Mínimo", f"{stats_area['Mínimo']:.2f}")
        with col5:
            st.metric("Máximo", f"{stats_area['Máximo']:.2f}")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            # Histograma de distribución
            st.subheader("📈 Distribución de Puntajes")
            fig = px.histogram(
                df,
                x=area_seleccionada,
                nbins=15,
                labels={area_seleccionada: 'Puntaje', 'count': 'Frecuencia'},
                color_discrete_sequence=[COLORES.get(area_seleccionada, '#1f77b4')]
            )
            fig.add_vline(
                x=stats_area['Promedio'],
                line_dash="dash",
                line_color="red",
                annotation_text=f"Promedio: {stats_area['Promedio']:.1f}"
            )
            fig.add_vline(
                x=stats_area['Mediana'],
                line_dash="dot",
                line_color="green",
                annotation_text=f"Mediana: {stats_area['Mediana']:.1f}"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Box plot detallado
            st.subheader("📦 Análisis de Dispersión")
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=df[area_seleccionada],
                name=area_seleccionada,
                marker_color=COLORES.get(area_seleccionada, '#1f77b4'),
                boxmean='sd',
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8
            ))
            fig.update_layout(
                yaxis_title="Puntaje",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Tabla de percentiles
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Percentiles")
            percentiles_df = pd.DataFrame({
                'Percentil': ['25%', '50%', '75%'],
                'Puntaje': [
                    f"{stats_area['Percentil 25']:.2f}",
                    f"{stats_area['Percentil 50']:.2f}",
                    f"{stats_area['Percentil 75']:.2f}"
                ]
            })
            st.dataframe(percentiles_df, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("📈 Métricas Adicionales")
            metricas_df = pd.DataFrame({
                'Métrica': ['Rango', 'Coef. Variación', 'Moda'],
                'Valor': [
                    f"{stats_area['Rango']:.2f}",
                    f"{stats_area['Coef. Variación']:.2f}%",
                    f"{stats_area['Moda']:.2f}" if stats_area['Moda'] is not None else 'N/A'
                ]
            })
            st.dataframe(metricas_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Top 10 y Bottom 10
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"🏆 Top 10 en {area_seleccionada}")
            top_10 = df.nlargest(10, area_seleccionada)[['Nombre Completo', area_seleccionada]].reset_index(drop=True)
            top_10.index = top_10.index + 1
            st.dataframe(top_10, use_container_width=True)

        with col2:
            st.subheader(f"📉 Estudiantes que Requieren Apoyo")
            bottom_10 = df.nsmallest(10, area_seleccionada)[['Nombre Completo', area_seleccionada]].reset_index(drop=True)
            bottom_10.index = bottom_10.index + 1
            st.dataframe(bottom_10, use_container_width=True)

    # TAB 4: Comparativo
    with tab4:
        st.header("🏆 Análisis Comparativo y Rankings")

        # Ranking general
        st.subheader("🥇 Ranking General por Puntaje Global")

        df_ranking = df[['Nombre Completo', 'Puntaje Global'] + AREAS].copy()
        df_ranking = df_ranking.sort_values('Puntaje Global', ascending=False).reset_index(drop=True)
        df_ranking.index = df_ranking.index + 1
        df_ranking.index.name = 'Posición'

        # Mostrar top 10 por defecto
        mostrar_completo = st.checkbox("Mostrar ranking completo", value=False)

        if mostrar_completo:
            st.dataframe(df_ranking, use_container_width=True)
        else:
            st.dataframe(df_ranking.head(10), use_container_width=True)

        st.markdown("---")

        # Comparación entre áreas
        st.subheader("📊 Comparación de Promedios entre Áreas")

        promedios_areas = df[AREAS].mean().sort_values(ascending=False)

        fig = px.bar(
            x=promedios_areas.index,
            y=promedios_areas.values,
            labels={'x': 'Área', 'y': 'Promedio'},
            color=promedios_areas.values,
            color_continuous_scale='RdYlGn',
            text=promedios_areas.values.round(1)
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis_range=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Matriz de correlación
        st.subheader("🔗 Matriz de Correlación entre Áreas")

        col1, col2 = st.columns([2, 1])

        with col1:
            correlacion = df[AREAS + ['Puntaje Global']].corr()

            fig = px.imshow(
                correlacion,
                labels=dict(color="Correlación"),
                x=correlacion.columns,
                y=correlacion.columns,
                color_continuous_scale='RdBu_r',
                aspect="auto",
                text_auto='.2f'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 📖 Interpretación")
            st.markdown("""
            **Valores de correlación:**
            - **1.0**: Correlación perfecta positiva
            - **0.7 - 0.9**: Correlación fuerte
            - **0.4 - 0.7**: Correlación moderada
            - **0.1 - 0.4**: Correlación débil
            - **0.0**: Sin correlación
            - **Negativo**: Correlación inversa

            Una correlación alta entre dos áreas indica que los estudiantes que obtienen buenos puntajes en una tienden a obtener buenos puntajes en la otra.
            """)

        st.markdown("---")

        # Scatter plots de correlaciones
        st.subheader("📈 Análisis de Correlaciones entre Áreas")

        col1, col2 = st.columns(2)

        with col1:
            area_x = st.selectbox("Selecciona área X:", AREAS, key='area_x')

        with col2:
            area_y = st.selectbox("Selecciona área Y:", AREAS, index=1, key='area_y')

        if area_x != area_y:
            fig = px.scatter(
                df,
                x=area_x,
                y=area_y,
                hover_data=['Nombre Completo'],
                labels={area_x: area_x, area_y: area_y},
                trendline="ols",
                color_discrete_sequence=['#1f77b4']
            )

            # Calcular correlación
            corr_value = df[[area_x, area_y]].corr().iloc[0, 1]

            fig.update_layout(
                title=f"Correlación: {corr_value:.3f}",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Selecciona dos áreas diferentes para comparar.")

        st.markdown("---")

        # Identificar estudiantes destacados
        st.subheader("⭐ Estudiantes Destacados (Top 10%)")

        percentil_90 = df['Puntaje Global'].quantile(0.90)
        destacados = df[df['Puntaje Global'] >= percentil_90][['Nombre Completo', 'Puntaje Global'] + AREAS]
        destacados = destacados.sort_values('Puntaje Global', ascending=False).reset_index(drop=True)
        destacados.index = destacados.index + 1

        st.info(f"Estudiantes con puntaje global ≥ {percentil_90:.1f} (Top 10%)")
        st.dataframe(destacados, use_container_width=True)

    # TAB 5: Segmentación
    with tab5:
        st.header("📈 Segmentación y Categorización")

        # Clasificar estudiantes por rango
        df['Clasificación'] = df['Puntaje Global'].apply(clasificar_por_rango)

        # Distribución por clasificación
        st.subheader("📊 Distribución por Rango de Puntaje")

        col1, col2 = st.columns(2)

        with col1:
            clasificacion_counts = df['Clasificación'].value_counts()

            fig = px.pie(
                values=clasificacion_counts.values,
                names=clasificacion_counts.index,
                title="Distribución de Estudiantes por Clasificación",
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 📋 Resumen por Clasificación")
            resumen_df = pd.DataFrame({
                'Clasificación': clasificacion_counts.index,
                'Cantidad': clasificacion_counts.values,
                'Porcentaje': (clasificacion_counts.values / len(df) * 100).round(1)
            })
            st.dataframe(resumen_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Estudiantes que requieren apoyo
        st.subheader("🎯 Estudiantes que Requieren Apoyo (Bottom 20%)")

        percentil_20 = df['Puntaje Global'].quantile(0.20)
        apoyo = df[df['Puntaje Global'] <= percentil_20][['Nombre Completo', 'Puntaje Global'] + AREAS]
        apoyo = apoyo.sort_values('Puntaje Global').reset_index(drop=True)
        apoyo.index = apoyo.index + 1

        st.warning(f"Estudiantes con puntaje global ≤ {percentil_20:.1f} (Bottom 20%)")
        st.dataframe(apoyo, use_container_width=True)

        st.markdown("---")

        # Análisis de consistencia
        st.subheader("🎯 Análisis de Consistencia de Desempeño")

        # Calcular desviación estándar de puntajes por estudiante
        df['Desv_Puntajes'] = df[AREAS].std(axis=1)
        df['Consistencia'] = df['Desv_Puntajes'].apply(
            lambda x: 'Alta' if x < 5 else ('Media' if x < 10 else 'Baja')
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 Estudiantes con Desempeño Consistente")
            st.markdown("*Puntajes similares en todas las áreas (Desv. Std < 5)*")
            consistentes = df[df['Consistencia'] == 'Alta'][['Nombre Completo', 'Puntaje Global', 'Desv_Puntajes']]
            consistentes = consistentes.sort_values('Puntaje Global', ascending=False).reset_index(drop=True)
            consistentes.index = consistentes.index + 1
            st.dataframe(consistentes, use_container_width=True)

        with col2:
            st.markdown("### 📊 Estudiantes con Desempeño Dispar")
            st.markdown("*Puntajes muy variables entre áreas (Desv. Std > 10)*")
            dispares = df[df['Consistencia'] == 'Baja'][['Nombre Completo', 'Puntaje Global', 'Desv_Puntajes']]
            dispares = dispares.sort_values('Desv_Puntajes', ascending=False).reset_index(drop=True)
            dispares.index = dispares.index + 1
            st.dataframe(dispares, use_container_width=True)

        st.markdown("---")

        # Tabla completa con filtros
        st.subheader("📋 Tabla Completa de Resultados")

        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            filtro_clasificacion = st.multiselect(
                "Filtrar por clasificación:",
                options=df['Clasificación'].unique(),
                default=df['Clasificación'].unique()
            )

        with col2:
            filtro_consistencia = st.multiselect(
                "Filtrar por consistencia:",
                options=df['Consistencia'].unique(),
                default=df['Consistencia'].unique()
            )

        with col3:
            rango_puntaje = st.slider(
                "Rango de puntaje global:",
                float(df['Puntaje Global'].min()),
                float(df['Puntaje Global'].max()),
                (float(df['Puntaje Global'].min()), float(df['Puntaje Global'].max()))
            )

        # Aplicar filtros
        df_filtrado = df[
            (df['Clasificación'].isin(filtro_clasificacion)) &
            (df['Consistencia'].isin(filtro_consistencia)) &
            (df['Puntaje Global'] >= rango_puntaje[0]) &
            (df['Puntaje Global'] <= rango_puntaje[1])
        ]

        st.info(f"Mostrando {len(df_filtrado)} de {len(df)} estudiantes")

        # Mostrar tabla
        columnas_mostrar = ['Nombre Completo', 'Puntaje Global'] + AREAS + ['Clasificación', 'Consistencia']
        df_mostrar = df_filtrado[columnas_mostrar].sort_values('Puntaje Global', ascending=False).reset_index(drop=True)
        df_mostrar.index = df_mostrar.index + 1

        st.dataframe(df_mostrar, use_container_width=True, height=400)

        # Botón de descarga
        csv = df_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv,
            file_name=f"resultados_icfes_filtrados_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()

