import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="Fluitek - Reportes Técnicos",
    page_icon="⚙️",
    layout="wide"
)

# Estilo personalizado para botones y encabezados
st.markdown("""
    <style>
    .main-title {
        color: #0c4a6e;
        font-weight: 800;
        font-size: 28px;
    }
    .sub-title {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 20px;
    }
    div.stButton > button:first-child {
        background-color: #f59e0b;
        color: #0f172a;
        font-weight: bold;
        border: none;
        border-radius: 8px;
    }
    div.stButton > button:first-child:hover {
        background-color: #d97706;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar la base de datos temporal en la sesión
if "reports" not in st.session_state:
    st.session_state.reports = [
        {
            "Folio": "FLT-2026-001",
            "OT": "OT-8840",
            "Fecha": "2026-09-05 14:30",
            "Cliente": "Minera Pelambres",
            "Faena": "Planta Concentradora",
            "Tag": "BOMBA-HYD-04",
            "Tipo": "Monitoreo de Condición",
            "Criticidad": "🔴 ALTA",
            "Inspector": "Carlos Mendoza",
            "Diagnostico": "Presencia de partículas metálicas en muestra de drenaje.",
            "Recomendaciones": "Reemplazo inmediato de filtros de retorno."
        },
        {
            "Folio": "FLT-2026-002",
            "OT": "OT-8841",
            "Fecha": "2026-09-06 09:15",
            "Cliente": "Atacama Minerals",
            "Faena": "Mina Subterránea",
            "Tag": "RED-PARAMAX-9000",
            "Tipo": "Análisis de Aceite / Fluidos",
            "Criticidad": "🟡 MEDIA",
            "Inspector": "Andrea Rojas",
            "Diagnostico": "Viscosidad ligeramente fuera de rango óptimo.",
            "Recomendaciones": "Tomar nueva muestra de seguimiento en 15 días."
        }
    ]

# Función modal para crear nuevo reporte
@st.dialog("📋 Nuevo Reporte de Campo - Fluitek")
def modal_nuevo_reporte():
    with st.form("form_reporte", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ot = st.text_input("Orden de Trabajo (OT) *", placeholder="Ej: OT-10452")
            cliente = st.text_input("Cliente *", placeholder="Ej: Minera Candelaria")
            faena = st.text_input("Faena / Planta *", placeholder="Ej: Planta Concentradora")
        with col2:
            tag = st.text_input("Equipo / Tag ID *", placeholder="Ej: RED-9000-A")
            tipo = st.selectbox("Tipo de Servicio", [
                "Monitoreo de Condición",
                "Análisis de Aceite / Fluidos",
                "Mantenimiento Hidráulico",
                "Inspección General"
            ])
            criticidad = st.selectbox("Nivel de Criticidad", [
                "🟢 NORMAL",
                "🟡 MEDIA",
                "🔴 ALTA"
            ])
        
        inspector = st.text_input("Inspector Responsable *", placeholder="Nombre del Técnico")
        diagnostico = st.text_area("Diagnóstico Técnico y Hallazgos *", placeholder="Escriba los hallazgos...")
        recomendaciones = st.text_area("Recomendaciones y Acciones Correctivas", placeholder="Escriba las recomendaciones...")
        
        submitted = st.form_submit_button("💾 Guardar Reporte", use_container_width=True)
        if submitted:
            if not ot or not cliente or not faena or not tag or not inspector or not diagnostico:
                st.error("Por favor completa los campos obligatorios (*).")
            else:
                folio_num = len(st.session_state.reports) + 1
                nuevo_registro = {
                    "Folio": f"FLT-2026-{folio_num:03d}",
                    "OT": ot,
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Cliente": cliente,
                    "Faena": faena,
                    "Tag": tag,
                    "Tipo": tipo,
                    "Criticidad": criticidad,
                    "Inspector": inspector,
                    "Diagnostico": diagnostico,
                    "Recomendaciones": recomendaciones
                }
                st.session_state.reports.insert(0, nuevo_registro)
                st.success("¡Reporte guardado con éxito!")
                st.rerun()

# --- ENCABEZADO Y BOTÓN PRINCIPAL ---
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown('<div class="main-title">FLUITEK - Field & Technical Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Gestión de Inspecciones, Fluidos & Monitoreo de Condición</div>', unsafe_allow_html=True)

with header_col2:
    if st.button("➕ Nuevo Reporte", use_container_width=True):
        modal_nuevo_reporte()

# --- TARJETAS KPI ---
df = pd.DataFrame(st.session_state.reports)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Reportes", len(df))
kpi2.metric("Criticidad Alta", len(df[df["Criticidad"] == "🔴 ALTA"]) if not df.empty else 0)
kpi3.metric("En Advertencia", len(df[df["Criticidad"] == "🟡 MEDIA"]) if not df.empty else 0)
kpi4.metric("Condición Normal", len(df[df["Criticidad"] == "🟢 NORMAL"]) if not df.empty else 0)

st.divider()

# --- FILTROS Y BÚSQUEDA ---
col_search, col_crit, col_tipo = st.columns([2, 1, 1])
with col_search:
    search_query = st.text_input("🔍 Buscar", placeholder="Buscar por OT, Cliente, Tag, Inspector...")
with col_crit:
    filter_crit = st.selectbox("Filtrar Criticidad", ["Todas", "🔴 ALTA", "🟡 MEDIA", "🟢 NORMAL"])
with col_tipo:
    filter_tipo = st.selectbox("Filtrar Tipo", ["Todos", "Monitoreo de Condición", "Análisis de Aceite / Fluidos", "Mantenimiento Hidráulico", "Inspección General"])

# Aplicar filtros al DataFrame
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[
        filtered_df["OT"].str.contains(search_query, case=False, na=False) |
        filtered_df["Cliente"].str.contains(search_query, case=False, na=False) |
        filtered_df["Tag"].str.contains(search_query, case=False, na=False) |
        filtered_df["Inspector"].str.contains(search_query, case=False, na=False)
    ]

if filter_crit != "Todas":
    filtered_df = filtered_df[filtered_df["Criticidad"] == filter_crit]

if filter_tipo != "Todos":
    filtered_df = filtered_df[filtered_df["Tipo"] == filter_tipo]

# --- TABLA DE REPORTES ---
st.subheader("Registros de Inspección")
if not filtered_df.empty:
    st.dataframe(
        filtered_df[["Folio", "OT", "Fecha", "Cliente", "Faena", "Tag", "Tipo", "Criticidad", "Inspector"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No hay reportes registrados o ninguno coincide con los filtros aplicados.")
