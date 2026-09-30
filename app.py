import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(
    page_title="Plataforma Integrada CBM & Mantenibilidad",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Plataforma de Monitoreo de Condiciones y Gestión de Mantenimiento")

# Subida de datos o generación de demostración
st.sidebar.header("📂 Carga de Datos")
uploaded_file = st.sidebar.file_uploader("Cargar matriz de datos (Excel o CSV)", type=["xlsx", "csv"])

# --- FUNCION DE GENERACION DE DATOS SINTETICOS PARA PRUEBA ---
@st.cache_data
def generate_sample_data():
    equipos = [
        "CHANCADOR-01", "CHANCADOR-02", "CORREA-01", "CORREA-02", 
        "MOLINO-SAG-01", "MOLINO-BOLA-01", "BOMBA-SLURRY-01", "BOMBA-SLURRY-02"
    ]
    areas = ["Chancado", "Chancado", "Transporte", "Transporte", "Molienda", "Molienda", "Molienda", "Molienda"]
    
    data = []
    np.random.seed(42)
    for i, eq in enumerate(equipos):
        vibracion = round(np.random.uniform(1.2, 8.5), 2)
        temp = round(np.random.uniform(45.0, 95.0), 1)
        
        # Determinar estado de salud según umbrales ISO
        if vibracion > 7.1 or temp > 85:
            condicion = "PELIGRO"
            criticidad = "ALTA"
            prioridad = "1 - INMEDIATO"
        elif vibracion > 4.5 or temp > 70:
            condicion = "ALARMA"
            criticidad = "MEDIA ALTA"
            prioridad = "2 - CORRECTIVO"
        else:
            condicion = "NORMAL"
            criticidad = "MEDIA"
            prioridad = "3 - PLANIFICADO"
            
        data.append({
            "TAG_EQUIPO": eq,
            "AREA": areas[i],
            "VIBRACION_RMS_MMS": vibracion,
            "TEMPERATURA_C": temp,
            "ESTADO_CBM": condicion,
            "CRITICIDAD": criticidad,
            "PRIORIDAD_AVISO": prioridad,
            "STATUS_AVISO": np.random.choice(["APRO", "NUEV", "RECH"], p=[0.6, 0.3, 0.1]),
            "FECHA_MEDICION": pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 10))
        })
    return pd.DataFrame(data)

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    st.info("💡 Usando datos de demostración de Planta Concentradora. Puedes cargar tu archivo propio desde la barra lateral.")
    df = generate_sample_data()

# Tabs principales de la aplicación
tab1, tab2, tab3 = st.tabs([
    "🔥 Mapa de Calor y Salud de Planta", 
    "📈 Monitoreo de Condiciones (CBM)", 
    "📋 Gestión de Avisos y Backlog"
])

# ==========================================
# TAB 1: MAPA DE CALOR Y SALUD
# ==========================================
with tab1:
    st.subheader("🔥 Mapa de Calor: Salud Operacional por Área y Criticidad")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Equipos Monitoreados", len(df["TAG_EQUIPO"].unique()))
    with col2:
        peligro_cnt = len(df[df["ESTADO_CBM"] == "PELIGRO"])
        st.metric("Equipos en Peligro", peligro_cnt, delta_color="inverse")
    with col3:
        alarma_cnt = len(df[df["ESTADO_CBM"] == "ALARMA"])
        st.metric("Equipos en Alarma", alarma_cnt, delta_color="inverse")
    with col4:
        normal_cnt = len(df[df["ESTADO_CBM"] == "NORMAL"])
        st.metric("Equipos Normales", normal_cnt)

    st.markdown("---")
    
    # Heatmap 1: Area vs Estado CBM
    pivot_heatmap = pd.crosstab(df["AREA"], df["ESTADO_CBM"])
    fig_heat = px.imshow(
        pivot_heatmap,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=["#2ca02c", "#ff7f0e", "#d62728"],
        title="Distribución de Salud de Equipos por Área"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ==========================================
# TAB 2: MONITOREO DE CONDICIONES (CBM)
# ==========================================
with tab2:
    st.subheader("📊 Monitoreo de Condiciones Técnica de Activos")
    
    equipo_sel = st.selectbox("Seleccionar Equipo para Análisis Detallado:", df["TAG_EQUIPO"].unique())
    eq_data = df[df["TAG_EQUIPO"] == equipo_sel].iloc[0]
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Vibración Global (mm/s RMS)", f"{eq_data['VIBRACION_RMS_MMS']} mm/s")
    with c2:
        st.metric("Temperatura CBM (°C)", f"{eq_data['TEMPERATURA_C']} °C")
    with c3:
        st.metric("Estado Técnico", eq_data["ESTADO_CBM"])
        
    # Gráfico de Indicador de Calibración / Gauge para Vibración
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = eq_data['VIBRACION_RMS_MMS'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Vibración RMS - {equipo_sel} (Límites ISO)"},
        gauge = {
            'axis': {'range': [0, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 4.5], 'color': "green"},
                {'range': [4.5, 7.1], 'color': "yellow"},
                {'range': [7.1, 10], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': eq_data['VIBRACION_RMS_MMS']
            }
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

# ==========================================
# TAB 3: GESTION DE AVISOS Y BACKLOG
# ==========================================
with tab3:
    st.subheader("📋 Matriz de Avisos de Mantenimiento")
    
    # Filtros de tabla
    filtro_status = st.multiselect("Filtrar por Estado de Aprobación:", df["STATUS_AVISO"].unique(), default=df["STATUS_AVISO"].unique())
    df_filtered = df[df["STATUS_AVISO"].isin(filtro_status)]
    
    st.dataframe(df_filtered[[
        "TAG_EQUIPO", "AREA", "CRITICIDAD", "PRIORIDAD_AVISO", "ESTADO_CBM", "STATUS_AVISO", "FECHA_MEDICION"
    ]], use_container_width=True)
    
    # Botón para descargar reporte de gestión
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte de Avisos CBM",
        data=csv_data,
        file_name="reporte_cbm_mantenibilidad.csv",
        mime="text/csv"
    )
