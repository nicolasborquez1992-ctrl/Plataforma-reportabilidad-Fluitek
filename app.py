import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import hashlib
from datetime import datetime
import json

# ==========================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Fluitek - Platform & Technical Reports",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .fluitek-badge {
        background-color: #000000;
        color: #ffffff;
        font-weight: 900;
        padding: 4px 12px;
        border-radius: 4px;
        letter-spacing: 1px;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0f172a;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOTOR DE BASE DE DATOS (SQLite)
# ==========================================
DB_FILE = "fluitek_reports.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Tabla Usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            rol TEXT NOT NULL -- Admin, Técnico, Cliente
        )
    ''')
    
    # Tabla Reportes / Ordenes de Trabajo
    c.execute('''
        CREATE TABLE IF NOT EXISTS reportes (
            id TEXT PRIMARY KEY,
            ot TEXT NOT NULL,
            cliente TEXT NOT NULL,
            faena TEXT NOT NULL,
            tag TEXT NOT NULL,
            tipo_servicio TEXT NOT NULL,
            criticidad TEXT NOT NULL,
            estado_seguimiento TEXT NOT NULL, -- Borrador, Pendiente, En Ejecucion, Cerrado
            inspector TEXT NOT NULL,
            lat REAL,
            lng REAL,
            temperatura REAL,
            presion REAL,
            iso_code TEXT,
            diagnostico TEXT,
            recomendaciones TEXT,
            fecha_creacion TEXT NOT NULL
        )
    ''')
    
    # Tabla Historial de Cambios (Audit Log)
    c.execute('''
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reporte_id TEXT NOT NULL,
            usuario TEXT NOT NULL,
            accion TEXT NOT NULL,
            detalles TEXT,
            fecha TEXT NOT NULL,
            FOREIGN KEY(reporte_id) REFERENCES reportes(id)
        )
    ''')

    # Crear usuario Admin inicial por defecto (admin / admin123)
    c.execute("SELECT COUNT(*) FROM usuarios")
    if c.fetchone()[0] == 0:
        pass_hash = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)",
                  ("admin", pass_hash, "Administrador Fluitek", "Admin"))
        
        pass_tec = hashlib.sha256("tec123".encode()).hexdigest()
        c.execute("INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)",
                  ("carlos.m", pass_tec, "Carlos Mendoza", "Técnico"))

        pass_cli = hashlib.sha256("cli123".encode()).hexdigest()
        c.execute("INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)",
                  ("supervision", pass_cli, "Supervisión Minera", "Cliente"))

    conn.commit()
    conn.close()

init_db()

# Funciones Auxiliares BD
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validar_login(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, nombre, rol FROM usuarios WHERE username = ? AND password = ?", (username, hash_pass(password)))
    user = c.fetchone()
    conn.close()
    return user

def registrar_historial(reporte_id, usuario, accion, detalles=""):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO historial (reporte_id, usuario, accion, detalles, fecha) VALUES (?, ?, ?, ?, ?)",
              (reporte_id, usuario, accion, detalles, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# ==========================================
# 3. AUTENTICACIÓN Y MANEJO DE SESIÓN
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None

def login_form():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <span class="fluitek-badge" style="font-size: 28px;">FLUITEK</span>
            <p style="color: #64748b; margin-top: 10px;">Sistema Integral de Gestión & Monitoreo de Campo</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_login"):
            st.subheader("🔐 Iniciar Sesión")
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submit = st.form_submit_button("Ingresar al Sistema", use_container_width=True)
            
            if submit:
                user = validar_login(username, password)
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['user_info'] = {"username": user[0], "nombre": user[1], "rol": user[2]}
                    st.success(f"Bienvenido, {user[1]}")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")

if not st.session_state['logged_in']:
    login_form()
    st.stop()

# ==========================================
# 4. BARRA LATERAL Y NAVEGACIÓN
# ==========================================
user = st.session_state['user_info']

with st.sidebar:
    st.markdown(f'<span class="fluitek-badge" style="font-size: 20px;">FLUITEK</span>', unsafe_allow_html=True)
    st.markdown(f"**Usuario:** {user['nombre']}")
    st.markdown(f"**Rol:** `{user['rol']}`")
    st.divider()
    
    opciones_menu = ["📊 Dashboard Executivo", "📝 Nueva Orden / Reporte", "📋 Gestión de Reportes", "📜 Historial de Cambios"]
    if user['rol'] == 'Admin':
        opciones_menu.append("👥 Gestión de Usuarios")
        
    menu = st.radio("Navegación", opciones_menu)
    
    st.divider()
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['user_info'] = None
        st.rerun()

# ==========================================
# 5. MÓDULO: DASHBOARD CON GRÁFICOS
# ==========================================
if menu == "📊 Dashboard Executivo":
    st.title("📊 Dashboard de Monitoreo & Operaciones")
    
    conn = sqlite3.connect(DB_FILE)
    df_reportes = pd.read_sql_query("SELECT * FROM reportes", conn)
    conn.close()
    
    if df_reportes.empty:
        st.info("Aún no hay reportes registrados en la base de datos para generar el dashboard.")
    else:
        # Métricas KPI Principales
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        col_kpi1.metric("Total Ordenes / Reportes", len(df_reportes))
        col_kpi2.metric("Alertas Críticas (Alta)", len(df_reportes[df_reportes['criticidad'] == 'ALTA']), delta_color="inverse")
        col_kpi3.metric("En Seguimiento / Ejecución", len(df_reportes[df_reportes['estado_seguimiento'] == 'En Ejecución']))
        col_kpi4.metric("Casos Cerrados", len(df_reportes[df_reportes['estado_seguimiento'] == 'Cerrado']))
        
        st.divider()
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Distribución por Nivel de Criticidad")
            fig_crit = px.pie(
                df_reportes, 
                names='criticidad', 
                color='criticidad',
                color_discrete_map={'NORMAL': '#10b981', 'MEDIA': '#f59e0b', 'ALTA': '#ef4444'},
                hole=0.4
            )
            st.plotly_chart(fig_crit, use_container_width=True)
            
        with col_chart2:
            st.subheader("Estado de Seguimiento de Órdenes")
            fig_estado = px.bar(
                df_reportes, 
                x='estado_seguimiento', 
                color='estado_seguimiento',
                labels={'estado_seguimiento': 'Estado', 'count': 'Cantidad'},
                color_discrete_sequence=px.colors.qualitative.Dark24
            )
            st.plotly_chart(fig_estado, use_container_width=True)
            
        # Mapa de Ubicaciones GPS
        df_gps = df_reportes.dropna(subset=['lat', 'lng'])
        if not df_gps.empty:
            st.subheader("🗺️ Geolocalización de Inspecciones en Campo")
            fig_map = px.scatter_mapbox(
                df_gps, 
                lat="lat", 
                lon="lng", 
                hover_name="ot", 
                hover_data=["cliente", "tag", "criticidad"],
                color="criticidad",
                color_discrete_map={'NORMAL': 'green', 'MEDIA': 'orange', 'ALTA': 'red'},
                zoom=8, 
                height=400
            )
            fig_map.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# 6. MÓDULO: NUEVA ORDEN / REPORTE
# ==========================================
elif menu == "📝 Nueva Orden / Reporte":
    st.title("📝 Registrar Orden de Trabajo / Campo")
    
    if user['rol'] == 'Cliente':
        st.warning("⚠️ Su rol actual (Cliente) solo permite la lectura e inspección de reportes.")
        st.stop()

    with st.form("form_nuevo_reporte", clear_on_submit=True):
        st.subheader("Datos de la Orden y Ubicación")
        col1, col2, col3 = st.columns(3)
        with col1:
            ot = st.text_input("Orden de Trabajo (OT) *", placeholder="Ej: OT-9941")
            cliente = st.text_input("Cliente *", placeholder="Ej: Minera Los Pelambres")
        with col2:
            faena = st.text_input("Faena / Planta *", placeholder="Ej: Concentradora")
            tag = st.text_input("Tag del Equipo *", placeholder="Ej: RED-PARAMAX-9000")
        with col3:
            tipo_servicio = st.selectbox("Tipo de Servicio", [
                "Monitoreo de Condición", 
                "Análisis de Aceite / Fluidos", 
                "Mantenimiento Hidráulico", 
                "Inspección General"
            ])
            criticidad = st.selectbox("Criticidad Inicial", ["NORMAL", "MEDIA", "ALTA"])

        st.subheader("📍 Captura GPS & Parámetros Operativos")
        col_gps1, col_gps2, col_p1, col_p2, col_p3 = st.columns(5)
        with col_gps1:
            lat = st.number_input("Latitud GPS", value=-30.015300, format="%.6f")
        with col_gps2:
            lng = st.number_input("Longitud GPS", value=-71.393200, format="%.6f")
        with col_p1:
            temp = st.number_input("Temp (°C)", value=55.0)
        with col_p2:
            presion = st.number_input("Presión (PSI)", value=1500.0)
        with col_p3:
            iso_code = st.text_input("Código ISO 4406", value="18/16/13")

        st.subheader("📋 Diagnóstico y Fotografía")
        diagnostico = st.text_area("Diagnóstico Técnico y Hallazgos")
        recomendaciones = st.text_area("Recomendaciones de Acción")
        
        fotos = st.file_uploader("Adjuntar Fotografías / Evidencias", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

        btn_guardar = st.form_submit_button("💾 Guardar y Crear Orden de Trabajo", use_container_width=True)

        if btn_guardar:
            if not ot or not cliente or not tag:
                st.error("Por favor complete los campos obligatorios (*)")
            else:
                folio = f"FLT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO reportes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (folio, ot, cliente, faena, tag, tipo_servicio, criticidad, "Pendiente", user['nombre'],
                      lat, lng, temp, presion, iso_code, diagnostico, recomendaciones, datetime.now().strftime("%Y-%m-%d %H:%M")))
                conn.commit()
                conn.close()

                registrar_historial(folio, user['username'], "Creación", f"Creación de Orden de Trabajo {ot}")
                st.success(f"Reporte/OT guardado con éxito con el Folio: **{folio}**")

# ==========================================
# 7. MÓDULO: GESTIÓN Y ESTADOS DE SEGUIMIENTO
# ==========================================
elif menu == "📋 Gestión de Reportes":
    st.title("📋 Gestión y Seguimiento de Reportes")
    
    conn = sqlite3.connect(DB_FILE)
    df_reportes = pd.read_sql_query("SELECT * FROM reportes ORDER BY fecha_creacion DESC", conn)
    conn.close()

    if df_reportes.empty:
        st.info("No hay reportes guardados.")
    else:
        # Filtros
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filtro_estado = st.multiselect("Filtrar por Estado", df_reportes['estado_seguimiento'].unique(), default=df_reportes['estado_seguimiento'].unique())
        with col_f2:
            filtro_crit = st.multiselect("Filtrar por Criticidad", df_reportes['criticidad'].unique(), default=df_reportes['criticidad'].unique())

        df_filtrado = df_reportes[
            (df_reportes['estado_seguimiento'].isin(filtro_estado)) & 
            (df_reportes['criticidad'].isin(filtro_crit))
        ]

        st.dataframe(df_filtrado[['id', 'ot', 'cliente', 'tag', 'tipo_servicio', 'criticidad', 'estado_seguimiento', 'inspector', 'fecha_creacion']], use_container_width=True)

        st.divider()
        st.subheader("🔄 Actualizar Estado de Seguimiento")
        
        col_sel, col_est, col_btn = st.columns([2, 2, 1])
        with col_sel:
            reporte_sel = st.selectbox("Seleccionar Folio / OT para actualizar", df_filtrado['id'].tolist())
        with col_est:
            nuevo_estado = st.selectbox("Nuevo Estado", ["Borrador", "Pendiente", "En Ejecución", "Cerrado / Aprobado"])
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Actualizar", use_container_width=True):
                if user['rol'] == 'Cliente' and nuevo_estado == "Cerrado / Aprobado":
                    st.error("Los clientes solo pueden visualizar el estado.")
                else:
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("UPDATE reportes SET estado_seguimiento = ? WHERE id = ?", (nuevo_estado, reporte_sel))
                    conn.commit()
                    conn.close()
                    
                    registrar_historial(reporte_sel, user['username'], "Cambio de Estado", f"Estado cambiado a: {nuevo_estado}")
                    st.success("Estado actualizado con éxito.")
                    st.rerun()

# ==========================================
# 8. MÓDULO: HISTORIAL DE CAMBIOS (AUDIT)
# ==========================================
elif menu == "📜 Historial de Cambios":
    st.title("📜 Trazabilidad e Historial de Cambios")
    
    conn = sqlite3.connect(DB_FILE)
    df_hist = pd.read_sql_query("SELECT * FROM historial ORDER BY fecha DESC", conn)
    conn.close()
    
    if df_hist.empty:
        st.info("Sin registros de cambios aún.")
    else:
        st.dataframe(df_hist, use_container_width=True)

# ==========================================
# 9. MÓDULO: GESTIÓN DE USUARIOS (ADMIN)
# ==========================================
elif menu == "👥 Gestión de Usuarios":
    st.title("👥 Control de Usuarios y Roles")
    
    with st.form("form_usuario"):
        st.subheader("Crear Nuevo Usuario")
        new_user = st.text_input("Nombre de Usuario")
        new_pass = st.text_input("Contraseña", type="password")
        new_nombre = st.text_input("Nombre Completo")
        new_rol = st.selectbox("Rol de Acceso", ["Técnico", "Cliente", "Admin"])
        
        btn_crear = st.form_submit_button("Crear Usuario")
        if btn_crear:
            if new_user and new_pass:
                try:
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("INSERT INTO usuarios (username, password, nombre, rol) VALUES (?, ?, ?, ?)",
                              (new_user, hash_pass(new_pass), new_nombre, new_rol))
                    conn.commit()
                    conn.close()
                    st.success("Usuario registrado con éxito.")
                except sqlite3.IntegrityError:
                    st.error("El nombre de usuario ya existe.")
            else:
                st.error("Complete todos los campos.")

    st.divider()
    conn = sqlite3.connect(DB_FILE)
    df_users = pd.read_sql_query("SELECT id, username, nombre, rol FROM usuarios", conn)
    conn.close()
    st.subheader("Usuarios Registrados")
    st.table(df_users)
