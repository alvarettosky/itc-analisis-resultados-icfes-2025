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
    initial_sidebar_state="collapsed"
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

        # ⚠️ CORRECCIÓN CRÍTICA: Filtrar solo las 36 filas de estudiantes reales
        # Las últimas 4 filas (36-39) contienen estadísticas agregadas:
        # - Fila 36: Vacía (separador)
        # - Fila 37: Promedios 2025
        # - Fila 38: Promedios 2024
        # - Fila 39: Avance (diferencia 2025-2024)
        # Estas filas NO deben incluirse en el análisis de estudiantes individuales

        # Filtrar solo filas con Grupo no nulo (estudiantes reales)
        df = df[df['Grupo'].notna()].copy()

        # Validación: debe haber exactamente 36 estudiantes
        if len(df) != 36:
            st.warning(f"⚠️ Advertencia: Se esperaban 36 estudiantes, se encontraron {len(df)}")

        # Limpiar datos adicionales
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

@st.cache_data
def cargar_datos_historicos():
    """Carga los datos históricos de comparación entre años"""
    try:
        df_completo = pd.read_excel(ARCHIVO_EXCEL)

        # Extraer las filas de datos históricos
        # Fila 37 (índice 37): Promedios 2025
        # Fila 38 (índice 38): Promedios 2024
        # Fila 39 (índice 39): Avance (diferencia)

        if len(df_completo) >= 40:
            datos_2025 = df_completo.iloc[37][AREAS + ['Puntaje Global']].to_dict()
            datos_2024 = df_completo.iloc[38][AREAS + ['Puntaje Global']].to_dict()
            avance = df_completo.iloc[39][AREAS + ['Puntaje Global']].to_dict()

            return {
                '2025': datos_2025,
                '2024': datos_2024,
                'Avance': avance
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error al cargar datos históricos: {e}")
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
    

    # Tabs principales
    tab6, tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Comparación 2024-2025",
        "📊 Vista General",
        "👤 Por Estudiante",
        "📚 Por Área",
        "🏆 Rankings",
        "📈 Segmentación"
    ])

    # TAB 1: Vista General
    with tab1:
        st.header("📊 Resumen General de Resultados")

        # ⚠️ NOTA METODOLÓGICA IMPORTANTE
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
                help="Total de estudiantes con resultados (36 estudiantes)"
            )

        with col2:
            promedio_global = df['Puntaje Global'].mean()
            st.metric(
                "Promedio Global",
                f"{int(round(promedio_global))}",
                help="Promedio del puntaje global (0-500)"
            )

        with col3:
            mediana_global = df['Puntaje Global'].median()
            st.metric(
                "Mediana Global",
                f"{int(round(mediana_global))}",
                help="Mediana del puntaje global (0-500)"
            )

        st.markdown("---")

        # Estadísticas por área (sin comparaciones)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Estadísticas por Área")
            st.markdown("*Cada área se analiza de forma independiente*")

            stats_data = []
            for area in AREAS:
                stats_data.append({
                    'Área': area,
                    'Promedio': f"{int(round(df[area].mean()))}",
                    'Mediana': f"{int(round(df[area].median()))}",
                    'Desv. Std': f"{df[area].std():.1f}"
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
                annotation_text=f"Promedio: {int(round(df['Puntaje Global'].mean()))}"
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
                f"{int(round(df['Puntaje Global'].max()))}",
                help="Mejor puntaje global del grupo"
            )

        with col2:
            st.metric(
                "Puntaje Mínimo",
                f"{int(round(df['Puntaje Global'].min()))}",
                help="Menor puntaje global del grupo"
            )

        with col3:
            st.metric(
                "Rango",
                f"{int(round(df['Puntaje Global'].max() - df['Puntaje Global'].min()))}",
                help="Diferencia entre el máximo y mínimo"
            )

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
                    st.metric("Puntaje Total", f"{int(round(puntaje_global))}/500")
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
            st.metric("Promedio", f"{int(round(stats_area['Promedio']))}")
        with col2:
            st.metric("Mediana", f"{int(round(stats_area['Mediana']))}")
        with col3:
            st.metric("Desv. Estándar", f"{stats_area['Desv. Estándar']:.2f}")
        with col4:
            st.metric("Mínimo", f"{int(round(stats_area['Mínimo']))}")
        with col5:
            st.metric("Máximo", f"{int(round(stats_area['Máximo']))}")

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
                annotation_text=f"Promedio: {int(round(stats_area['Promedio']))}"
            )
            fig.add_vline(
                x=stats_area['Mediana'],
                line_dash="dot",
                line_color="green",
                annotation_text=f"Mediana: {int(round(stats_area['Mediana']))}"
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
            top_10 = df.nlargest(10, area_seleccionada)[['Nombre Completo', area_seleccionada]].copy()
            # Redondear puntajes a enteros (manejar NaN)
            top_10[area_seleccionada] = top_10[area_seleccionada].fillna(0).round(0).astype(int)
            top_10 = top_10.reset_index(drop=True)
            top_10.index = top_10.index + 1
            st.dataframe(top_10, use_container_width=True)

        with col2:
            st.subheader(f"📉 Estudiantes que Requieren Apoyo")
            bottom_10 = df.nsmallest(10, area_seleccionada)[['Nombre Completo', area_seleccionada]].copy()
            # Redondear puntajes a enteros (manejar NaN)
            bottom_10[area_seleccionada] = bottom_10[area_seleccionada].fillna(0).round(0).astype(int)
            bottom_10 = bottom_10.reset_index(drop=True)
            bottom_10.index = bottom_10.index + 1
            st.dataframe(bottom_10, use_container_width=True)

    # TAB 4: Rankings y Estudiantes Destacados
    with tab4:
        st.header("🏆 Rankings y Estudiantes Destacados")

        # ⚠️ NOTA METODOLÓGICA IMPORTANTE
        st.info("""
        **📚 Nota Metodológica del ICFES:**

        Las áreas evaluadas en el ICFES Saber 11 (Lectura Crítica, Matemáticas, Sociales, Ciencias, Inglés)
        utilizan **escalas, ponderaciones y criterios de evaluación diferentes**. Por esta razón, **NO es
        metodológicamente válido comparar puntajes entre áreas diferentes** (por ejemplo, comparar Matemáticas
        vs Lectura Crítica).

        Los análisis válidos son:
        - ✅ Rankings de estudiantes por puntaje global
        - ✅ Rankings por área individual
        - ✅ Comparación de la MISMA área entre diferentes años
        - ✅ Análisis de desempeño individual por área
        """)

        # Ranking general
        st.subheader("🥇 Ranking General por Puntaje Global")

        df_ranking = df[['Nombre Completo', 'Puntaje Global'] + AREAS].copy()
        # Redondear puntajes a enteros (manejar NaN)
        for col in ['Puntaje Global'] + AREAS:
            df_ranking[col] = df_ranking[col].fillna(0).round(0).astype(int)
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

        # Rankings por área individual
        st.subheader("📊 Rankings por Área Individual")

        area_ranking = st.selectbox(
            "Selecciona un área para ver su ranking:",
            AREAS,
            key='area_ranking'
        )

        df_area_ranking = df[['Nombre Completo', area_ranking]].copy()
        # Redondear puntajes a enteros (manejar NaN)
        df_area_ranking[area_ranking] = df_area_ranking[area_ranking].fillna(0).round(0).astype(int)
        df_area_ranking = df_area_ranking.sort_values(area_ranking, ascending=False).reset_index(drop=True)
        df_area_ranking.index = df_area_ranking.index + 1
        df_area_ranking.index.name = 'Posición'

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 🥇 Top 10 en {area_ranking}")
            st.dataframe(df_area_ranking.head(10), use_container_width=True)

        with col2:
            st.markdown(f"### 📉 Últimos 10 en {area_ranking}")
            st.dataframe(df_area_ranking.tail(10), use_container_width=True)

        st.markdown("---")

        # Identificar estudiantes destacados
        st.subheader("⭐ Estudiantes Destacados (Top 10%)")

        percentil_90 = df['Puntaje Global'].quantile(0.90)
        destacados = df[df['Puntaje Global'] >= percentil_90][['Nombre Completo', 'Puntaje Global'] + AREAS].copy()
        # Redondear puntajes a enteros (manejar NaN)
        for col in ['Puntaje Global'] + AREAS:
            destacados[col] = destacados[col].fillna(0).round(0).astype(int)
        destacados = destacados.sort_values('Puntaje Global', ascending=False).reset_index(drop=True)
        destacados.index = destacados.index + 1

        st.info(f"Estudiantes con puntaje global ≥ {int(round(percentil_90))} (Top 10%)")
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
        apoyo = df[df['Puntaje Global'] <= percentil_20][['Nombre Completo', 'Puntaje Global'] + AREAS].copy()
        # Redondear puntajes a enteros (manejar NaN)
        for col in ['Puntaje Global'] + AREAS:
            apoyo[col] = apoyo[col].fillna(0).round(0).astype(int)
        apoyo = apoyo.sort_values('Puntaje Global').reset_index(drop=True)
        apoyo.index = apoyo.index + 1

        st.warning(f"Estudiantes con puntaje global ≤ {int(round(percentil_20))} (Bottom 20%)")
        st.dataframe(apoyo, use_container_width=True)

        st.markdown("---")

        # ⚠️ SECCIÓN ELIMINADA: Análisis de Consistencia
        # Esta sección calculaba la desviación estándar entre áreas diferentes,
        # lo cual NO es metodológicamente válido según el ICFES, ya que cada área
        # tiene escalas y criterios de evaluación diferentes.

        st.markdown("---")

        # Tabla completa con filtros
        st.subheader("📋 Tabla Completa de Resultados")

        # Filtros
        col1, col2 = st.columns(2)

        with col1:
            filtro_clasificacion = st.multiselect(
                "Filtrar por clasificación:",
                options=df['Clasificación'].unique(),
                default=df['Clasificación'].unique()
            )

        with col2:
            rango_puntaje = st.slider(
                "Rango de puntaje global:",
                float(df['Puntaje Global'].min()),
                float(df['Puntaje Global'].max()),
                (float(df['Puntaje Global'].min()), float(df['Puntaje Global'].max()))
            )

        # Aplicar filtros
        df_filtrado = df[
            (df['Clasificación'].isin(filtro_clasificacion)) &
            (df['Puntaje Global'] >= rango_puntaje[0]) &
            (df['Puntaje Global'] <= rango_puntaje[1])
        ]

        st.info(f"Mostrando {len(df_filtrado)} de {len(df)} estudiantes")

        # Mostrar tabla
        columnas_mostrar = ['Nombre Completo', 'Puntaje Global'] + AREAS + ['Clasificación']
        df_mostrar = df_filtrado[columnas_mostrar].copy()
        # Redondear puntajes a enteros (manejar NaN)
        for col in ['Puntaje Global'] + AREAS:
            df_mostrar[col] = df_mostrar[col].fillna(0).round(0).astype(int)
        df_mostrar = df_mostrar.sort_values('Puntaje Global', ascending=False).reset_index(drop=True)
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

    # TAB 6: Comparación 2024-2025
    with tab6:
        st.header("📅 Comparación de Resultados 2024 vs 2025")

        # Cargar datos históricos
        datos_historicos = cargar_datos_historicos()

        if datos_historicos is None:
            st.warning("⚠️ No se encontraron datos históricos de comparación en el archivo Excel.")
            st.info("Los datos históricos deben estar en las filas 37-39 del archivo Excel.")
        else:
            # Nota metodológica
            st.info("""
            **📚 Comparación Válida:** Esta sección compara los promedios de la MISMA área entre diferentes años.
            Esta es una comparación metodológicamente válida según las recomendaciones del ICFES.
            """)

            st.markdown("---")

            # Métricas principales
            st.subheader("📊 Resumen de Avance General")

            col1, col2, col3 = st.columns(3)

            with col1:
                puntaje_2025 = datos_historicos['2025']['Puntaje Global']
                st.metric(
                    "Puntaje Global 2025",
                    f"{int(round(puntaje_2025))}",
                    help="Promedio del puntaje global en 2025"
                )

            with col2:
                puntaje_2024 = datos_historicos['2024']['Puntaje Global']
                st.metric(
                    "Puntaje Global 2024",
                    f"{int(round(puntaje_2024))}",
                    help="Promedio del puntaje global en 2024"
                )

            with col3:
                avance_global = datos_historicos['Avance']['Puntaje Global']
                delta_color = "normal" if avance_global >= 0 else "inverse"
                st.metric(
                    "Avance",
                    f"{int(round(avance_global))}",
                    delta=f"{int(round(avance_global))} puntos",
                    help="Diferencia entre 2025 y 2024"
                )

            st.markdown("---")

            # Comparación por área
            st.subheader("📈 Comparación por Área de Conocimiento")

            # Crear DataFrame para comparación
            comparacion_data = []
            for area in AREAS:
                comparacion_data.append({
                    'Área': area,
                    '2024': datos_historicos['2024'][area],
                    '2025': datos_historicos['2025'][area],
                    'Avance': datos_historicos['Avance'][area],
                    'Avance %': (datos_historicos['Avance'][area] / datos_historicos['2024'][area] * 100) if datos_historicos['2024'][area] != 0 else 0
                })

            df_comparacion = pd.DataFrame(comparacion_data)

            # Gráfico de barras comparativo
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📊 Comparación de Promedios")

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    name='2024',
                    x=AREAS,
                    y=[datos_historicos['2024'][area] for area in AREAS],
                    marker_color='#ff7f0e',
                    text=[f"{int(round(datos_historicos['2024'][area]))}" for area in AREAS],
                    textposition='outside'
                ))

                fig.add_trace(go.Bar(
                    name='2025',
                    x=AREAS,
                    y=[datos_historicos['2025'][area] for area in AREAS],
                    marker_color='#1f77b4',
                    text=[f"{int(round(datos_historicos['2025'][area]))}" for area in AREAS],
                    textposition='outside'
                ))

                fig.update_layout(
                    barmode='group',
                    xaxis_title='Área',
                    yaxis_title='Puntaje Promedio',
                    yaxis=dict(range=[0, 100]),
                    height=500,
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### 📉 Avance por Área")

                # Crear gráfico de avance
                colores_avance = ['#2ca02c' if x >= 0 else '#d62728' for x in df_comparacion['Avance']]

                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=AREAS,
                    y=df_comparacion['Avance'],
                    marker_color=colores_avance,
                    text=[f"{int(round(x)):+d}" for x in df_comparacion['Avance']],
                    textposition='outside'
                ))

                fig.add_hline(y=0, line_dash="dash", line_color="gray")

                fig.update_layout(
                    xaxis_title='Área',
                    yaxis_title='Avance (puntos)',
                    height=500,
                    showlegend=False
                )

                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # Tabla detallada
            st.subheader("📋 Tabla Detallada de Comparación")

            # Formatear tabla
            df_tabla = df_comparacion.copy()
            df_tabla['2024'] = df_tabla['2024'].apply(lambda x: f"{int(round(x))}")
            df_tabla['2025'] = df_tabla['2025'].apply(lambda x: f"{int(round(x))}")
            df_tabla['Avance'] = df_tabla['Avance'].apply(lambda x: f"{int(round(x)):+d}")
            df_tabla['Avance %'] = df_tabla['Avance %'].apply(lambda x: f"{x:+.2f}%")

            st.dataframe(df_tabla, use_container_width=True, hide_index=True)

            st.markdown("---")

            # Análisis de tendencias
            st.subheader("🔍 Análisis de Tendencias")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Áreas con Mejor Desempeño")
                areas_mejora = df_comparacion.nlargest(3, 'Avance')[['Área', 'Avance', 'Avance %']]

                if areas_mejora['Avance'].iloc[0] > 0:
                    for idx, row in areas_mejora.iterrows():
                        st.success(f"**{row['Área']}**: {int(round(row['Avance'])):+d} puntos ({row['Avance %']:+.2f}%)")
                else:
                    st.warning("No hay áreas con avance positivo")

            with col2:
                st.markdown("### ⚠️ Áreas que Requieren Atención")
                areas_atencion = df_comparacion.nsmallest(3, 'Avance')[['Área', 'Avance', 'Avance %']]

                for idx, row in areas_atencion.iterrows():
                    if row['Avance'] < 0:
                        st.error(f"**{row['Área']}**: {int(round(row['Avance'])):+d} puntos ({row['Avance %']:+.2f}%)")
                    else:
                        st.info(f"**{row['Área']}**: {int(round(row['Avance'])):+d} puntos ({row['Avance %']:+.2f}%)")

            st.markdown("---")

            # Recomendaciones
            st.subheader("💡 Recomendaciones")

            avance_promedio = df_comparacion['Avance'].mean()

            if avance_promedio > 0:
                st.success(f"""
                **✅ Tendencia General Positiva**

                El avance promedio es de **{int(round(avance_promedio)):+d} puntos**. Se observa una mejora general en el desempeño.

                **Recomendaciones:**
                - Mantener las estrategias pedagógicas actuales
                - Reforzar las áreas con menor avance
                - Compartir buenas prácticas de las áreas con mayor mejora
                """)
            elif avance_promedio < 0:
                st.warning(f"""
                **⚠️ Tendencia General Negativa**

                El avance promedio es de **{int(round(avance_promedio)):+d} puntos**. Se observa una disminución en el desempeño.

                **Recomendaciones:**
                - Revisar las estrategias pedagógicas actuales
                - Implementar planes de mejoramiento específicos por área
                - Analizar factores externos que puedan estar afectando el rendimiento
                - Considerar refuerzo académico en las áreas más afectadas
                """)
            else:
                st.info("""
                **➡️ Desempeño Estable**

                El avance promedio es cercano a cero. El desempeño se mantiene estable.

                **Recomendaciones:**
                - Implementar estrategias de mejora continua
                - Establecer metas de crecimiento para el próximo año
                """)

            # Botón de descarga
            st.markdown("---")
            csv_comparacion = df_comparacion.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar comparación (CSV)",
                data=csv_comparacion,
                file_name=f"comparacion_2024_2025_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()

