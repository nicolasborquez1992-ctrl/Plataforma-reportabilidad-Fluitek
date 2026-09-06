import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image
import io

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="App de Reportes de Inspección",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para apariencia de App Móvil / Dashboard
st.markdown("""
    <style>
    /* Estilizar contenedor principal */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    /* Tarjetas personalizadas */
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #007bff;
    }
    /* Botones principales */
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "reportes.csv"
IMAGE_DIR = "uploaded_images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# -----------------------------------------------------------------------------
# 2. FUNCIONES DE MANEJO DE DATOS E IMÁGENES
# -----------------------------------------------------------------------------
def cargar_reportes():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "ID", "Fecha", "Título", "Categoría", "Área_Ubicación", 
            "Prioridad", "Estado", "Inspector", "Descripción", "Ruta_Foto"
        ])

def guardar_reportes_df(df):
    df.to_csv(DATA_FILE, index=False)

def guardar_nuevo_reporte(nuevo_registro):
    df = cargar_reportes()
    df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
    guardar_reportes_df(df)

def optimizar_y_guardar_imagen(imagen_bytes, nombre_base):
    """Redimensiona y comprime la imagen para optimizar espacio"""
    try:
        img = Image.open(imagen_bytes)
        # Convertir a RGB si viene en RGBA/PNG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Redimensionar si supera ancho máximo de 1200px
        max_size = (1200, 1200)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"foto_{timestamp}_{nombre_base}.jpg"
        ruta_completa = os.path.join(IMAGE_DIR, nombre_archivo)
        
        # Guardar comprimida al 80% de calidad
        img.save(ruta_completa, "JPEG", optimize=True, quality=80)
        return ruta_completa
    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")
        return ""

# -----------------------------------------------------------------------------
# 3. BARRA LATERAL (MENÚ DE NAVEGACIÓN)
# -----------------------------------------------------------------------------
st.sidebar.title("📱 Menú Principal")
opcion = st.sidebar.radio(
    "Seleccione una sección:",
    ["➕ Nuevo Reporte", "📋 Ver / Gestionar Reportes", "📊 Estadísticas"]
)

st.sidebar.markdown("---")
st.sidebar.caption("⚡ *Sistema de Inspección Móvil v2.0*")

# -----------------------------------------------------------------------------
# 4. MÓDULO 1: NUEVO REPORTE
# -----------------------------------------------------------------------------
if opcion == "➕ Nuevo Reporte":
    st.header("📝 Registrar Nuevo Reporte")
    st.write("Complete la información solicitada y adjunte o tome la fotografía de evidencia.")

    with st.form(key="form_nuevo_reporte", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            titulo = st.text_input("Título del Reporte *", placeholder="Ej: Anomalía en Reductor Paramax")
            categoria = st.selectbox(
                "Categoría / Clasificación *",
                ["Inspección Visual", "Mantenimiento Correctivo", "Falla Mecánica", "Fuga de Aceite / Fluido", "Seguridad / HSE", "Otro"]
            )
            area_ubicacion = st.text_input("Área / Ubicación del Equipo *", placeholder="Ej: Planta de Chancado - Cinta 3")

        with col2:
            prioridad = st.selectbox("Nivel de Prioridad", ["Baja", "Media", "Alta", "Crítica"])
            inspector = st.text_input("Nombre del Inspector / Operador *", placeholder="Ej: Juan Pérez")
            fecha_reporte = st.date_input("Fecha del Hallazgo", value=datetime.today())

        descripcion = st.text_area("Descripción detallada del problema / observación *", rows=3, placeholder="Detalle las condiciones detectadas...")

        st.subheader("📸 Evidencia Fotográfica")
        st.write("Elija cómo desea adjuntar la imagen:")

        tab_camara, tab_archivo = st.tabs(["📷 Tomar Foto con Cámara", "📁 Subir de la Galería"])

        foto_camara = None
        foto_archivo = None

        with tab_camara:
            foto_camara = st.camera_input("Capturar foto directamente")

        with tab_archivo:
            foto_archivo = st.file_uploader("Seleccionar archivo de imagen", type=["jpg", "jpeg", "png"])

        st.caption("* Campos obligatorios")
        btn_guardar = st.form_submit_button("💾 Guardar y Enviar Reporte", use_container_width=True)

        if btn_guardar:
            if not titulo or not area_ubicacion or not inspector or not descripcion:
                st.error("⚠️ Por favor, complete todos los campos obligatorios (*).")
            else:
                ruta_foto = ""
                # Determinar qué origen de imagen se usó
                imagen_para_guardar = foto_camara if foto_camara is not None else foto_archivo

                if imagen_para_guardar is not None:
                    nombre_origen = "camara" if foto_camara is not None else "galeria"
                    ruta_foto = optimizar_y_guardar_imagen(imagen_para_guardar, nombre_origen)

                # Generar ID consecutivo
                df_actual = cargar_reportes()
                nuevo_id = f"REP-{(len(df_actual) + 1):04d}"

                # Registro de datos
                nuevo_registro = {
                    "ID": nuevo_id,
                    "Fecha": fecha_reporte.strftime("%Y-%m-%d"),
                    "Título": titulo,
                    "Categoría": categoria,
                    "Área_Ubicación": area_ubicacion,
                    "Prioridad": prioridad,
                    "Estado": "Abierto",
                    "Inspector": inspector,
                    "Descripción": descripcion,
                    "Ruta_Foto": ruta_foto
                }

                guardar_nuevo_reporte(nuevo_registro)
                st.success(f"✅ ¡Reporte **{nuevo_id}** guardado con éxito!")
                st.balloons()

# -----------------------------------------------------------------------------
# 5. MÓDULO 2: GESTIÓN Y HISTORIAL DE REPORTES
# -----------------------------------------------------------------------------
elif opcion == "📋 Ver / Gestionar Reportes":
    st.header("📋 Historial y Gestión de Reportes")

    df_reportes = cargar_reportes()

    if df_reportes.empty:
        st.info("Aún no existen reportes registrados.")
    else:
        # Filtros de búsqueda rápidos
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            filtro_cat = st.multiselect("Categoría:", options=df_reportes["Categoría"].unique(), default=df_reportes["Categoría"].unique())
        with col_f2:
            filtro_prio = st.multiselect("Prioridad:", options=df_reportes["Prioridad"].unique(), default=df_reportes["Prioridad"].unique())
        with col_f3:
            filtro_est = st.multiselect("Estado:", options=df_reportes["Estado"].unique(), default=df_reportes["Estado"].unique())

        # Aplicar Filtros
        df_filtrado = df_reportes[
            (df_reportes["Categoría"].isin(filtro_cat)) & 
            (df_reportes["Prioridad"].isin(filtro_prio)) &
            (df_reportes["Estado"].isin(filtro_est))
        ]

        # Botón para descargar datos en CSV
        st.download_button(
            label="📥 Descargar todos los reportes (CSV)",
            data=df_filtrado.to_csv(index=False).encode("utf-8"),
            file_name=f"reportes_inspeccion_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        st.dataframe(
            df_filtrado[["ID", "Fecha", "Título", "Categoría", "Área_Ubicación", "Prioridad", "Estado", "Inspector"]],
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🔍 Detalle del Reporte y Actualización")

        lista_ids = df_filtrado["ID"].tolist()
        if lista_ids:
            id_sel = st.selectbox("Seleccione el ID del reporte a inspeccionar:", lista_ids)
            idx_reporte = df_reportes[df_reportes["ID"] == id_sel].index[0]
            reporte = df_reportes.loc[idx_reporte]

            col_det1, col_det2 = st.columns([2, 1])

            with col_det1:
                st.markdown(f"### {reporte['Título']} (`{reporte['ID']}`)")
                st.write(f"📅 **Fecha:** {reporte['Fecha']} | 👤 **Inspector:** {reporte['Inspector']}")
                st.write(f"📍 **Ubicación / Área:** {reporte['Área_Ubicación']}")
                st.write(f"🏷️ **Categoría:** {reporte['Categoría']} | 🚨 **Prioridad:** {reporte['Prioridad']}")
                
                st.write("**📝 Descripción del Hallazgo:**")
                st.info(reporte['Descripción'])

                # Cambio de estado dinámico
                st.markdown("#### ⚙️ Actualizar Estado del Reporte")
                nuevo_estado = st.selectbox(
                    "Estado Actual:", 
                    ["Abierto", "En Proceso", "Resuelto"], 
                    index=["Abierto", "En Proceso", "Resuelto"].index(reporte['Estado']) if reporte['Estado'] in ["Abierto", "En Proceso", "Resuelto"] else 0,
                    key=f"estado_{id_sel}"
                )

                if st.button("💾 Actualizar Estado"):
                    df_reportes.loc[idx_reporte, "Estado"] = nuevo_estado
                    guardar_reportes_df(df_reportes)
                    st.success(f"Estado del reporte {id_sel} cambiado a '{nuevo_estado}'")
                    st.rerun()

            with col_det2:
                ruta_img = reporte['Ruta_Foto']
                if pd.notna(ruta_img) and ruta_img != "" and os.path.exists(str(ruta_img)):
                    st.image(ruta_img, caption=f"Fotografía del Reporte - {reporte['ID']}", use_container_width=True)
                else:
                    st.warning("📷 Sin fotografía adjunta")

# -----------------------------------------------------------------------------
# 6. MÓDULO 3: ESTADÍSTICAS Y PANEL METRICAS
# -----------------------------------------------------------------------------
elif opcion == "📊 Estadísticas":
    st.header("📊 Métricas de Inspección")

    df_reportes = cargar_reportes()

    if df_reportes.empty:
        st.info("No hay datos disponibles para mostrar estadísticas.")
    else:
        # Métricas Clave (KPIs)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Reportes", len(df_reportes))
        kpi2.metric("Abiertos / Pendientes", len(df_reportes[df_reportes["Estado"] == "Abierto"]))
        kpi3.metric("En Proceso", len(df_reportes[df_reportes["Estado"] == "En Proceso"]))
        kpi4.metric("Resueltos", len(df_reportes[df_reportes["Estado"] == "Resuelto"]))

        st.markdown("---")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("Reportes por Categoría")
            st.bar_chart(df_reportes["Categoría"].value_counts())

        with col_g2:
            st.subheader("Reportes por Prioridad")
            st.bar_chart(df_reportes["Prioridad"].value_counts())
