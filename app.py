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
    
    # TAB 3: Análisis por Área de Conocimiento
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
            st.metric("Desv. Estándar", f"{stats_area['Desv. Estándar']:.0f}")
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
                    f"{stats_area['Percentil 25']:.0f}",
                    f"{stats_area['Percentil 50']:.0f}",
                    f"{stats_area['Percentil 75']:.0f}"
                ]
            })
            st.dataframe(percentiles_df, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("📈 Métricas Adicionales")
            metricas_df = pd.DataFrame({
                'Métrica': ['Rango', 'Coef. Variación', 'Moda'],
                'Valor': [
                    f"{stats_area['Rango']:.0f}",
                    f"{stats_area['Coef. Variación']:.0f}%",
                    f"{stats_area['Moda']:.0f}" if stats_area['Moda'] is not None else 'N/A'
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

if __name__ == "__main__":
    main()

