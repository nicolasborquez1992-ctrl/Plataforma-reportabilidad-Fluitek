import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==========================================
st.set_page_config(
    page_title="CBM Expert - Plataforma Integrada de Monitoreo",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# MOTOR DE DATOS CBM & GENERACIÓN SINTÉTICA
# ==========================================
@st.cache_data
def load_cbm_data():
    np.random.seed(42)
    activos = [
        {"id": "MOL-001", "nombre": "Molino SAG 01", "area": "Molienda", "crit": "Alta"},
        {"id": "MOL-002", "nombre": "Molino Bolas 01", "area": "Molienda", "crit": "Alta"},
        {"id": "BOM-101", "nombre": "Bomba Slurry A", "area": "Flotación", "crit": "Media"},
        {"id": "BOM-102", "nombre": "Bomba Slurry B", "area": "Flotación", "crit": "Media"},
        {"id": "CHA-001", "nombre": "Chancador Primario", "area": "Chancado", "crit": "Alta"},
        {"id": "CEN-201", "nombre": "Centrífuga 01", "area": "Lixiviación", "crit": "Baja"},
    ]
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    records = []
    
    for eq in activos:
        base_vib = np.random.uniform(1.2, 2.5) if eq["crit"] != "Alta" else np.random.uniform(2.5, 4.5)
        base_temp = np.random.uniform(45, 60)
        base_fe = np.random.uniform(10, 25)
        
        for i, dt in enumerate(dates):
            factor = (i / 30) ** 2 if eq["id"] in ["MOL-001", "BOM-101"] else 0.1
            vib = base_vib + (factor * 4.5) + np.random.normal(0, 0.2)
            temp = base_temp + (factor * 25) + np.random.normal(0, 1.0)
            delta_t = (temp - 25.0) + np.random.normal(0, 0.5)
            fe_ppm = base_fe + (factor * 60) + np.random.normal(0, 2.0)
            viscosidad = 150 - (factor * 30) + np.random.normal(0, 1.5)
            
            records.append({
                "fecha": dt,
                "id_activo": eq["id"],
                "nombre": eq["nombre"],
                "area": eq["area"],
                "criticidad_base": eq["crit"],
                "vibracion_rms": round(max(0.5, vib), 2),
                "temperatura_max": round(max(20.0, temp), 1),
                "delta_t": round(max(0.0, delta_t), 1),
                "aceite_fe_ppm": round(max(5.0, fe_ppm), 1),
                "aceite_viscosidad": round(viscosidad, 1)
            })
            
    return pd.DataFrame(records)

df_cbm = load_cbm_data()

# Base de datos de Avisos en Session State
if 'avisos_db' not in st.session_state:
    st.session_state['avisos_db'] = pd.DataFrame([
        {
            "id_aviso": "AV-2026-001",
            "fecha_creacion": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "id_activo": "MOL-001",
            "componente": "Rodamiento Lado Acople",
            "disciplina": "Vibraciones",
            "severidad": "Crítica",
            "prioridad": "P1 - Inmediato",
            "descripcion": "Exceso de velocidad RMS. Transición a Zona D (ISO 10816).",
            "estado": "Abierto",
            "responsable": "Analista CBM"
        },
        {
            "id_aviso": "AV-2026-002",
            "fecha_creacion": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "id_activo": "BOM-101",
            "componente": "Caja Reductora",
            "disciplina": "Aceites",
            "severidad": "Media",
            "prioridad": "P2 - Programado",
            "descripcion": "Incremento de partículas de desgaste (Fe > 70 ppm). Viscosidad fuera de rango.",
            "estado": "En Proceso",
            "responsable": "Técnico Tribología"
        }
    ])

# ==========================================
# BARRA LATERAL - NAVEGACIÓN Y FILTROS
# ==========================================
st.sidebar.title("⚡ CBM Expert")
st.sidebar.caption("Plataforma de Monitoreo Basado en la Condición")

modulo = st.sidebar.radio(
    "Módulos del Sistema:",
    [
        "🗺️ Mapa de Calor 3D & Salud",
        "📈 Vibraciones & Espectro FFT",
        "🌡️ Termografía (Delta T)",
        "🧪 Control de Tribología",
        "🚨 Matriz de Riesgo y Avisos",
        "📄 Generación de Reportes"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### Filtros Operacionales")
area_selected = st.sidebar.multiselect(
    "Filtrar por Área:",
    options=df_cbm["area"].unique(),
    default=df_cbm["area"].unique()
)

df_filtered = df_cbm[df_cbm["area"].isin(area_selected)]

# ==========================================
# MÓDULO 1: MAPA DE CALOR 3D & SALUD
# ==========================================
if modulo == "🗺️ Mapa de Calor 3D & Salud":
    st.title("🗺️️ Mapa de Calor 3D y Salud Operacional")
    st.markdown("Diagnóstico matricial tridimensional del estado de salud de activos planta.")
    
    latest_df = df_filtered.sort_values('fecha').groupby('id_activo').last().reset_index()
    
    def calc_estado(row):
        if row['vibracion_rms'] > 7.1 or row['temperatura_max'] > 80 or row['aceite_fe_ppm'] > 70:
            return 3  # Crítico
        elif row['vibracion_rms'] > 4.5 or row['temperatura_max'] > 70 or row['aceite_fe_ppm'] > 45:
            return 2  # Alerta
        else:
            return 1  # Normal
            
    latest_df['estado_num'] = latest_df.apply(calc_estado, axis=1)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Activos Monitoreados", len(latest_df))
    c2.metric("Condición Normal", len(latest_df[latest_df['estado_num'] == 1]))
    c3.metric("En Alerta", len(latest_df[latest_df['estado_num'] == 2]), delta_color="inverse")
    c4.metric("Estado Crítico", len(latest_df[latest_df['estado_num'] == 3]), delta_color="inverse")
    
    st.divider()
    
    st.subheader("🌐 Matriz 3D de Severidad CBM (Vibración vs Temp vs Aceite)")
    fig_3d = px.scatter_3d(
        latest_df,
        x='vibracion_rms',
        y='temperatura_max',
        z='aceite_fe_ppm',
        color='estado_num',
        size='vibracion_rms',
        hover_name='nombre',
        text='id_activo',
        color_continuous_scale=[[0, '#2ECC71'], [0.5, '#F39C12'], [1, '#E74C3C']],
        labels={'vibracion_rms': 'Vibración RMS (mm/s)', 'temperatura_max': 'Temp Max (°C)', 'aceite_fe_ppm': 'Hierro Fe (ppm)'}
    )
    fig_3d.update_layout(height=600, coloraxis_showscale=False)
    st.plotly_chart(fig_3d, use_container_width=True)

# ==========================================
# MÓDULO 2: VIBRACIONES & FFT
# ==========================================
elif modulo == "📈 Vibraciones & Espectro FFT":
    st.title("📈 Análisis de Vibraciones y Espectro FFT")
    st.markdown("Evaluación conforme a norma *ISO 10816-3* y diagnóstico frecuencial.")
    
    equipo_sel = st.selectbox("Seleccionar Activo:", df_filtered["nombre"].unique())
    df_eq = df_filtered[df_filtered["nombre"] == equipo_sel].sort_values("fecha")
    
    fig_vib = go.Figure()
    fig_vib.add_trace(go.Scatter(x=df_eq['fecha'], y=df_eq['vibracion_rms'], mode='lines+markers', name='RMS (mm/s)', line=dict(color='#2980B9', width=3)))
    fig_vib.add_hline(y=2.8, line_dash="dot", line_color="#F39C12", annotation_text="Alerta (Zona B/C)")
    fig_vib.add_hline(y=4.5, line_dash="dash", line_color="#E67E22", annotation_text="Restringido (Zona C/D)")
    fig_vib.add_hline(y=7.1, line_dash="solid", line_color="#C0392B", annotation_text="Inadmisible (Zona D)")
    fig_vib.update_layout(title=f"Evolución RMS Global - {equipo_sel}", xaxis_title="Fecha", yaxis_title="Velocidad RMS (mm/s)", height=400)
    st.plotly_chart(fig_vib, use_container_width=True)
    
    st.subheader("📊 Análisis Espectral FFT (Simulación en Tiempo Real)")
    freqs = np.linspace(0, 500, 250)
    amps = np.random.exponential(scale=0.2, size=250)
    amps[25] += 3.5  # Armónico 1X
    amps[50] += 2.1  # Armónico 2X
    amps[120] += 1.8 # Paso de álabes/ BPF
    
    fig_fft = px.line(x=freqs, y=amps, labels={'x': 'Frecuencia (Hz)', 'y': 'Amplitud (mm/s PK)'}, title=f"Espectro FFT de Velocidad - {equipo_sel}")
    fig_fft.update_traces(line_color='#8E44AD')
    st.plotly_chart(fig_fft, use_container_width=True)

# ==========================================
# MÓDULO 3: TERMOGRAFÍA (DELTA T)
# ==========================================
elif modulo == "🌡️ Termografía (Delta T)":
    st.title("🌡️ Diagnóstico Termográfico por Delta T")
    st.markdown("Severidad analizada según el diferencial de temperatura sobre la temperatura ambiente ($\Delta T$).")
    
    equipo_sel = st.selectbox("Seleccionar Activo:", df_filtered["nombre"].unique())
    df_eq = df_filtered[df_filtered["nombre"] == equipo_sel].sort_values("fecha")
    
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Bar(x=df_eq['fecha'], y=df_eq['delta_t'], name='Delta T (°C)', marker_color='#E67E22'))
    fig_temp.add_hline(y=10, line_dash="dot", line_color="yellow", annotation_text="Etapa 1 (Ligero)")
    fig_temp.add_hline(y=25, line_dash="dash", line_color="orange", annotation_text="Etapa 2 (Moderado)")
    fig_temp.add_hline(y=40, line_dash="solid", line_color="red", annotation_text="Etapa 3 (Crítico)")
    fig_temp.update_layout(title=f"Diferencial de Temperatura (Delta T) - {equipo_sel}", xaxis_title="Fecha", yaxis_title="Delta T (°C)", height=400)
    st.plotly_chart(fig_temp, use_container_width=True)

# ==========================================
# MÓDULO 4: CONTROL DE TRIBOLOGÍA
# ==========================================
elif modulo == "🧪 Control de Tribología":
    st.title("🧪 Módulo de Control de Tribología")
    st.markdown("Monitoreo de desgaste metálico por espectrometría y estabilidad del lubricante.")
    
    equipo_sel = st.selectbox("Seleccionar Activo:", df_filtered["nombre"].unique())
    df_eq = df_filtered[df_filtered["nombre"] == equipo_sel].sort_values("fecha")
    
    c1, c2 = st.columns(2)
    with c1:
        fig_fe = px.line(df_eq, x='fecha', y='aceite_fe_ppm', title="Contaminación por Hierro (Fe PPM)", markers=True)
        fig_fe.add_hline(y=50, line_dash="dash", line_color="orange")
        fig_fe.update_traces(line_color='#27AE60')
        st.plotly_chart(fig_fe, use_container_width=True)
    with c2:
        fig_visc = px.line(df_eq, x='fecha', y='aceite_viscosidad', title="Viscosidad Cinemática @ 40°C (cSt)", markers=True)
        fig_visc.add_hline(y=120, line_dash="dash", line_color="red")
        fig_visc.update_traces(line_color='#2980B9')
        st.plotly_chart(fig_visc, use_container_width=True)

# ==========================================
# MÓDULO 5: MATRIZ DE RIESGO Y AVISOS
# ==========================================
elif modulo == "🚨 Matriz de Riesgo y Avisos":
    st.title("🚨 Matriz de Riesgo y Gestión de Avisos")
    st.markdown("Gestión centralizada de órdenes de inspección y matriz operacional de riesgo.")
    
    st.subheader("Matriz de Riesgo CBM (Severidad vs Probabilidad)")
    matriz_data = np.array([[1, 2, 3], [2, 4, 6], [3, 6, 9]])
    fig_matriz = px.imshow(
        matriz_data,
        labels=dict(x="Probabilidad de Falla", y="Severidad del Impacto", color="Nivel de Riesgo"),
        x=['Baja', 'Media', 'Alta'],
        y=['Menor', 'Mayor', 'Crítico'],
        color_continuous_scale='Reds'
    )
    fig_matriz.update_layout(height=350)
    st.plotly_chart(fig_matriz, use_container_width=True)
    
    st.subheader("Avisos CBM Registrados")
    st.dataframe(st.session_state['avisos_db'], use_container_width=True)

# ==========================================
# MÓDULO 6: GENERACIÓN DE REPORTES
# ==========================================
elif modulo == "📄 Generación de Reportes":
    st.title("📄 Motor de Generación de Reportes CBM")
    st.markdown("Exportación de matrices de datos y resúmenes ejecutivos.")
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, sheet_name='Lecturas_CBM', index=False)
        st.session_state['avisos_db'].to_excel(writer, sheet_name='Avisos_Activos', index=False)
        
    st.download_button(
        label="📥 Descargar Reporte Ejecutivo Completo (.xlsx)",
        data=buffer.getvalue(),
        file_name=f"Reporte_Ejecutivo_CBM_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
