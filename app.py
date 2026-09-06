import streamlit as st
import pandas as pd
import json
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Fluitek - OT & Field GPS Platform",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fluitek Brand CSS Styling
st.markdown("""
<style>
    /* Fluitek Industrial Dark Theme Overrides */
    .main {
        background-color: #0b0f19;
    }
    .stMetric {
        background-color: #161f33;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #2a3859;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .stMetric label {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    .stMetric .number {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    .ot-card {
        background-color: #161f33;
        border: 1px solid #2a3859;
        border-left: 5px solid #0284c7;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
    .badge-pending {
        background-color: #f59e0b22;
        color: #f59e0b;
        border: 1px solid #f59e0b55;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-in-progress {
        background-color: #0284c722;
        color: #38bdf8;
        border: 1px solid #0284c755;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-completed {
        background-color: #10b98122;
        color: #34d399;
        border: 1px solid #10b98155;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-high {
        background-color: #ef444422;
        color: #f87171;
        border: 1px solid #ef444455;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. INITIALIZE SESSION STATE DATA
# ==========================================
if 'work_orders' not in st.session_state:
    st.session_state.work_orders = [
        {
            "ot_number": "OT-2026-0891",
            "client": "Minera Doña Inés",
            "facility": "Planta Concentradora Norte",
            "equipment": "Filtro Prensa FP-402",
            "service_type": "Mantenimiento Preventivo",
            "technician": "Carlos Mendoza",
            "priority": "Alta",
            "status": "En Proceso",
            "lat": -23.6509,
            "lng": -70.3975,
            "accuracy": "8m",
            "created_at": "2026-09-05 08:30",
            "description": "Cambio preventivo de placas de filtración y calibración de unidad hidráulica."
        },
        {
            "ot_number": "OT-2026-0892",
            "client": "Celulosa Arauco",
            "facility": "Planta Valdivia",
            "equipment": "Bomba Depuradora BD-12",
            "service_type": "Reparación Mecánica",
            "technician": "Andrea Torres",
            "priority": "Urgente",
            "status": "Pendiente",
            "lat": -39.8142,
            "lng": -73.2459,
            "accuracy": "12m",
            "created_at": "2026-09-05 10:15",
            "description": "Fuga de fluido hidráulico en prensa principal. Requiere recambio de sellos."
        },
        {
            "ot_number": "OT-2026-0893",
            "client": "Empresa Portuaria Bío Bío",
            "facility": "Terminal 2",
            "equipment": "Sistema Filtración Aire SF-01",
            "service_type": "Inspección Técnica",
            "technician": "Roberto Silva",
            "priority": "Normal",
            "status": "Completada",
            "lat": -36.7167,
            "lng": -73.1167,
            "accuracy": "5m",
            "created_at": "2026-09-04 14:00",
            "description": "Inspección de rutina de cartuchos de filtración y toma de muestras de aceite."
        }
    ]

if 'last_captured_gps' not in st.session_state:
    st.session_state.last_captured_gps = {
        "lat": -33.4489,
        "lng": -70.6693,
        "accuracy": "No capturado"
    }


# ==========================================
# 3. HEADER & SIDEBAR NAVIGATION
# ==========================================
st.title("⚙️ Fluitek — Gestión de Ordenes de Trabajo (OT)")
st.caption("Plataforma Integrada de Servicios en Terreno y Captura GPS en Tiempo Real")

st.sidebar.image("https://img.icons8.com/color/96/worker-with-roadblock.png", width=70)
st.sidebar.title("Fluitek Field Operations")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegación / Módulos",
    [
        "📊 Dashboard General",
        "🛰️ Captura GPS en Terreno",
        "➕ Crear Nueva Orden (OT)",
        "📋 Lista y Control de OTs",
        "🗺️ Mapa General de Terreno"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "*Estado del Sistema:*\n\n"
    "• Modulo GPS: *Activo* (HTML5 Geolocation)\n"
    "• Conexión: *En Línea*\n"
    f"• OTs Registradas: *{len(st.session_state.work_orders)}*"
)


# ==========================================
# 4. MODULE 1: DASHBOARD GENERAL
# ==========================================
if menu == "📊 Dashboard General":
    st.subheader("Resumen Operativo de Terreno")
    
    total_ots = len(st.session_state.work_orders)
    pending = len([o for o in st.session_state.work_orders if o['status'] == 'Pendiente'])
    in_progress = len([o for o in st.session_state.work_orders if o['status'] == 'En Proceso'])
    completed = len([o for o in st.session_state.work_orders if o['status'] == 'Completada'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Ordenes (OT)", total_ots)
    col2.metric("En Proceso", in_progress, delta="Activas")
    col3.metric("Pendientes", pending, delta_color="inverse")
    col4.metric("Completadas", completed, delta="Finalizadas")

    st.markdown("### ⚡ Órdenes Prioritarias y Recientes")
    
    df_ots = pd.DataFrame(st.session_state.work_orders)
    if not df_ots.empty:
        st.dataframe(
            df_ots[['ot_number', 'client', 'facility', 'equipment', 'technician', 'priority', 'status', 'created_at']],
            use_container_width=True,
            hide_index=True
        )

# ==========================================
# 5. MODULE 2: CAPTURA GPS EN TERRENO (EMBEDDED HTML/JS)
# ==========================================
elif menu == "🛰️ Captura GPS en Terreno":
    st.subheader("🛰️ Captura de Geolocalización GPS del Técnico")
    st.markdown("""
    Utiliza el chip GPS de tu dispositivo o navegador para obtener las coordenadas exactas 
    de tu ubicación en terreno e inspección de equipos Fluitek.
    """)

    # Embedded HTML5/JS Geolocation Capture Component with Leaflet Map
    gps_html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: #0f172a;
                color: #f8fafc;
                margin: 0;
                padding: 10px;
            }
            .gps-box {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 16px;
                margin-bottom: 12px;
            }
            .btn-gps {
                background: linear-gradient(135deg, #0284c7, #2563eb);
                color: white;
                border: none;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
                width: 100%;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
            }
            .btn-gps:hover {
                background: linear-gradient(135deg, #0369a1, #1d4ed8);
                transform: translateY(-1px);
            }
            .data-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin-top: 15px;
            }
            .data-card {
                background: #0f172a;
                border: 1px solid #334155;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
            }
            .data-title {
                font-size: 11px;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .data-val {
                font-size: 16px;
                font-weight: bold;
                color: #38bdf8;
                margin-top: 4px;
            }
            #map {
                height: 280px;
                width: 100%;
                border-radius: 10px;
                margin-top: 15px;
                border: 1px solid #334155;
            }
            .status-tag {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                margin-top: 8px;
            }
            .status-waiting { background: #334155; color: #cbd5e1; }
            .status-active { background: #065f46; color: #34d399; }
            .status-error { background: #991b1b; color: #fca5a5; }
        </style>
    </head>
    <body>

        <div class="gps-box">
            <button class="btn-gps" onclick="getLocation()">
                📍 Obtener Mi Ubicación GPS Actual
            </button>
            <div id="status-container">
                <span id="status-badge" class="status-tag status-waiting">Esperando orden de captura...</span>
            </div>

            <div class="data-grid">
                <div class="data-card">
                    <div class="data-title">Latitud</div>
                    <div class="data-val" id="lat-val">--.----</div>
                </div>
                <div class="data-card">
                    <div class="data-title">Longitud</div>
                    <div class="data-val" id="lng-val">--.----</div>
                </div>
                <div class="data-card">
                    <div class="data-title">Precisión</div>
                    <div class="data-val" id="acc-val">-- m</div>
                </div>
            </div>

            <div id="map"></div>
        </div>

        <script>
            var map = L.map('map').setView([-33.4489, -70.6693], 5);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);

            var marker;

            function getLocation() {
                var badge = document.getElementById('status-badge');
                badge.className = 'status-tag status-waiting';
                badge.innerText = 'Capturando posición satellite/GPS...';

                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition, showError, {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    });
                } else {
                    badge.className = 'status-tag status-error';
                    badge.innerText = 'Geolocalización no soportada en este navegador.';
                }
            }

            function showPosition(position) {
                var lat = position.coords.latitude;
                var lng = position.coords.longitude;
                var acc = Math.round(position.coords.accuracy);

                document.getElementById('lat-val').innerText = lat.toFixed(5);
                document.getElementById('lng-val').innerText = lng.toFixed(5);
                document.getElementById('acc-val').innerText = '±' + acc + 'm';

                var badge = document.getElementById('status-badge');
                badge.className = 'status-tag status-active';
                badge.innerText = '✅ Coordenadas Capturadas Exitosamente (' + new Date().toLocaleTimeString() + ')';

                var newLatLng = new L.LatLng(lat, lng);
                map.setView(newLatLng, 15);

                if (marker) {
                    marker.setLatLng(newLatLng);
                } else {
                    marker = L.marker(newLatLng).addTo(map);
                }
                marker.bindPopup("<b>Ubicación del Técnico</b><br>Lat: " + lat.toFixed(5) + "<br>Lng: " + lng.toFixed(5)).openPopup();
            }

            function showError(error) {
                var badge = document.getElementById('status-badge');
                badge.className = 'status-tag status-error';
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        badge.innerText = "❌ El usuario denegó la solicitud de Geolocalización.";
                        break;
                    case error.POSITION_UNAVAILABLE:
                        badge.innerText = "❌ La información de ubicación no está disponible.";
                        break;
                    case error.TIMEOUT:
                        badge.innerText = "❌ Se agotó el tiempo de espera para obtener la ubicación.";
                        break;
                    case error.UNKNOWN_ERROR:
                        badge.innerText = "❌ Error desconocido al obtener la posición.";
                        break;
                }
            }
        </script>
    </body>
    </html>
    """

    components.html(gps_html_code, height=480)

    st.markdown("### 📝 Ingresar Coordenadas a la Sesión Activa")
    st.info("Copia las coordenadas capturadas arriba para asociarlas manualmente o usa los accesos directos de instalaciones Fluitek.")

    col1, col2, col3 = st.columns(3)
    with col1:
        manual_lat = st.number_input("Latitud GPS", value=st.session_state.last_captured_gps['lat'], format="%.5f")
    with col2:
        manual_lng = st.number_input("Longitud GPS", value=st.session_state.last_captured_gps['lng'], format="%.5f")
    with col3:
        manual_acc = st.text_input("Precisión Estimada", value="±10m")

    if st.button("💾 Guardar Coordenadas como Referencia para Nueva OT"):
        st.session_state.last_captured_gps = {
            "lat": manual_lat,
            "lng": manual_lng,
            "accuracy": manual_acc
        }
        st.success("¡Coordenadas guardadas temporalmente para el formulario de OT!")

# ==========================================
# 6. MODULE 3: CREAR NUEVA OT
# ==========================================
elif menu == "➕ Crear Nueva Orden (OT)":
    st.subheader("➕ Registro de Nueva Orden de Trabajo (OT)")
    st.markdown("Genera una nueva solicitud de servicio en terreno indicando cliente, equipo y geolocalización.")

    with st.form("new_ot_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            ot_num = f"OT-2026-0{len(st.session_state.work_orders) + 894}"
            st.text_input("Número de OT", value=ot_num, disabled=True)
            client = st.text_input("Cliente / Empresa", placeholder="Ej: Minera Escondida")
            facility = st.text_input("Planta / Instalación", placeholder="Ej: Nave de Molienda 3")
            equipment = st.text_input("Tag o Nombre del Equipo", placeholder="Ej: Filtro Prensa FP-101")
            
        with c2:
            service_type = st.selectbox(
                "Tipo de Servicio",
                ["Mantenimiento Preventivo", "Mantenimiento Correctivo", "Reparación Mecánica", "Inspección Técnica", "Cambio de Cartuchos/Filtros", "Calibración"]
            )
            technician = st.text_input("Nombre del Técnico Asignado", placeholder="Ej: Juan Pérez")
            priority = st.select_slider("Prioridad del Trabajo", options=["Baja", "Normal", "Alta", "Urgente"], value="Normal")
            status = st.selectbox("Estado Inicial", ["Pendiente", "En Proceso", "Completada"])

        st.markdown("#### 📍 Posición GPS de la Instalación/Equipo")
        g1, g2, g3 = st.columns(3)
        with g1:
            lat = st.number_input("Latitud GPS", value=st.session_state.last_captured_gps['lat'], format="%.5f")
        with g2:
            lng = st.number_input("Longitud GPS", value=st.session_state.last_captured_gps['lng'], format="%.5f")
        with g3:
            acc = st.text_input("Precisión GPS", value=st.session_state.last_captured_gps['accuracy'])

        description = st.text_area("Descripción Detallada del Servicio", placeholder="Detalla las actividades a realizar o diagnóstico preliminar...")

        submitted = st.form_submit_button("🚀 Crear y Publicar Orden de Trabajo")

        if submitted:
            if not client or not equipment or not technician:
                st.error("Por favor completa los campos obligatorios (Cliente, Equipo y Técnico).")
            else:
                new_ot = {
                    "ot_number": ot_num,
                    "client": client,
                    "facility": facility if facility else "Sede Principal",
                    "equipment": equipment,
                    "service_type": service_type,
                    "technician": technician,
                    "priority": priority,
                    "status": status,
                    "lat": lat,
                    "lng": lng,
                    "accuracy": acc,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "description": description if description else "Sin descripción adicional."
                }
                st.session_state.work_orders.insert(0, new_ot)
                st.success(f"¡Orden de Trabajo *{ot_num}* registrada correctamente!")

# ==========================================
# 7. MODULE 4: LISTA Y CONTROL DE OTS
# ==========================================
elif menu == "📋 Lista y Control de OTs":
    st.subheader("📋 Control de Ordenes de Trabajo Registradas")

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_status = st.multiselect("Filtrar por Estado", ["Pendiente", "En Proceso", "Completada"], default=["Pendiente", "En Proceso", "Completada"])
    with col_f2:
        filter_priority = st.multiselect("Filtrar por Prioridad", ["Baja", "Normal", "Alta", "Urgente"], default=["Baja", "Normal", "Alta", "Urgente"])
    with col_f3:
        search_query = st.text_input("🔍 Buscar (Cliente/OT/Equipo)", "")

    # Apply filters
    filtered_ots = [
        o for o in st.session_state.work_orders
        if o['status'] in filter_status
        and o['priority'] in filter_priority
        and (
            search_query.lower() in o['ot_number'].lower()
            or search_query.lower() in o['client'].lower()
            or search_query.lower() in o['equipment'].lower()
            or search_query.lower() in o['technician'].lower()
        )
    ]

    st.markdown(f"*Mostrando {len(filtered_ots)} de {len(st.session_state.work_orders)} OTs*")

    for i, ot in enumerate(filtered_ots):
        badge_class = (
            "badge-completed" if ot['status'] == "Completada"
            else "badge-in-progress" if ot['status'] == "En Proceso"
            else "badge-pending"
        )
        prio_badge = "badge-high" if ot['priority'] in ["Alta", "Urgente"] else ""

        with st.expander(f"{ot['ot_number']} — {ot['client']} ({ot['equipment']})", expanded=(i==0)):
            st.markdown(f"""
            <div class="ot-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 1.1rem; font-weight: bold; color: #38bdf8;">{ot['ot_number']}</span>
                    <div>
                        <span class="{badge_class}">{ot['status']}</span>
                        <span class="{prio_badge}">{ot['priority']}</span>
                    </div>
                </div>
                <p style="margin: 4px 0; color: #e2e8f0;"><strong>Cliente:</strong> {ot['client']} | <strong>Instalación:</strong> {ot['facility']}</p>
                <p style="margin: 4px 0; color: #e2e8f0;"><strong>Equipo:</strong> {ot['equipment']} | <strong>Servicio:</strong> {ot['service_type']}</p>
                <p style="margin: 4px 0; color: #94a3b8;"><strong>Técnico Asignado:</strong> {ot['technician']} | <strong>Fecha:</strong> {ot['created_at']}</p>
                <p style="margin: 4px 0; color: #34d399;"><strong>📍 Ubicación GPS:</strong> Lat {ot['lat']:.5f}, Lng {ot['lng']:.5f} (Precisión: {ot['accuracy']})</p>
                <div style="background-color: #0f172a; padding: 10px; border-radius: 6px; margin-top: 8px; color: #cbd5e1; font-size: 0.9rem;">
                    {ot['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action to change status
            c_s1, c_s2 = st.columns([2, 1])
            with c_s1:
                new_st = st.selectbox(f"Actualizar Estado de {ot['ot_number']}", ["Pendiente", "En Proceso", "Completada"], index=["Pendiente", "En Proceso", "Completada"].index(ot['status']), key=f"sel_{ot['ot_number']}")
            with c_s2:
                st.write("")
                st.write("")
                if st.button("Guardar Estado", key=f"btn_{ot['ot_number']}"):
                    ot['status'] = new_st
                    st.success(f"Estado de {ot['ot_number']} actualizado a '{new_st}'")
                    st.rerun()

    # Export options
    st.markdown("---")
    st.markdown("### 📥 Exportar Datos")
    df_export = pd.DataFrame(st.session_state.work_orders)
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar Reporte de OTs en CSV",
        data=csv_data,
        file_name=f"fluitek_ots_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
