import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(
    page_title="Gestión de Mantenibilidad - Planta Concentradora",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Sistema de Gestión y Monitoreo de Mantenibilidad")
st.markdown("Análisis de avisos, criticidad y gestión de backlog operacional.")

# 1. Carga de datos
uploaded_file = st.sidebar.file_uploader("Cargar matriz de datos (Excel o CSV)", type=["xlsx", "csv"])

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    # Limpieza básica de columnas
    df.columns = [col.strip().upper() for col in df.columns]
    
    # Convertir fechas si existe columna de creación
    for col in df.columns:
        if "FECHA" in col or "CREADO" in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    # Sidebar: Filtros Globales
    st.sidebar.header("Filtros de Control")
    
    # Filtro por Área
    col_area = [c for c in df.columns if "AREA" in c or "SECTOR" in c or "PLANTA" in c]
    if col_area:
        areas = st.sidebar.multiselect("Seleccionar Área", options=df[col_area[0]].unique(), default=df[col_area[0]].unique())
        df = df[df[col_area[0]].isin(areas)]
        
    # Filtro por Status
    col_status = [c for c in df.columns if "STATUS" in c or "ESTADO" in c]
    if col_status:
        estados = st.sidebar.multiselect("Estado de Aprobación", options=df[col_status[0]].unique(), default=df[col_status[0]].unique())
        df = df[df[col_status[0]].isin(estados)]

    # --- KPIs PRINCIPALES ---
    col1, col2, col3, col4 = st.columns(4)
    
    col_prioridad = [c for c in df.columns if "PRIORIDAD" in c or "TIPO" in c]
    col_criticidad = [c for c in df.columns if "CRITICIDAD" in c or "RANGO" in c]
    
    with col1:
        st.metric("Total Avisos", len(df))
    with col2:
        if col_prioridad:
            inmediatos = len(df[df[col_prioridad[0]].astype(str).str.contains("1|INMEDIATO", case=False, na=False)])
            st.metric("Avisos Inmediatos (1)", inmediatos, delta_color="inverse")
    with col3:
        if col_criticidad:
            criticos = len(df[df[col_criticidad[0]].astype(str).str.contains("ALTA", case=False, na=False)])
            st.metric("Criticidad ALTA", criticos, delta_color="inverse")
    with col4:
        if col_status:
            rechazados = len(df[df[col_status[0]].astype(str).str.contains("RECH", case=False, na=False)])
            st.metric("Avisos Rechazados", rechazados)

    st.markdown("---")

    # --- MAPA DE CALOR (HEATMAP) DE CRITICIDAD VS PRIORIDAD ---
    if col_prioridad and col_criticidad:
        st.subheader("🔥 Matriz Heatmap: Criticidad vs Prioridad de Trabajo")
        
        pivot_table = pd.crosstab(df[col_criticidad[0]], df[col_prioridad[0]])
        
        fig_heatmap = px.imshow(
            pivot_table,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Reds",
            labels=dict(x="Prioridad / Tipo", y="Criticidad", color="Cantidad"),
            title="Distribución de Eventos por Riesgo Operacional"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # --- TABLAS DE ACCIÓN RÁPIDA ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("⚠️ Eventos Críticos Inmediatos (Prioridad 1 / Criticidad ALTA)")
        if col_prioridad and col_criticidad:
            crit_filter = (df[col_prioridad[0]].astype(str).str.contains("1|INMEDIATO", case=False, na=False)) & \
                          (df[col_criticidad[0]].astype(str).str.contains("ALTA", case=False, na=False))
            st.dataframe(df[crit_filter], use_container_width=True)

    with col_right:
        st.subheader("🛠️ Avisos Programados para Parada de Planta (P)")
        if col_prioridad:
            paradas_filter = df[col_prioridad[0]].astype(str).str.contains("P|PARADA", case=False, na=False)
            st.dataframe(df[paradas_filter], use_container_width=True)

else:
    st.info("💡 Sube una planilla en Excel o CSV desde la barra lateral izquierda para comenzar a analizar la matriz de mantenibilidad.")
