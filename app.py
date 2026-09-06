import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

# Configuración de la página en Streamlit
st.set_page_config(
    page_title="Fluitek - Reportes Técnicos",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Datos iniciales de ejemplo
DATOS_EJEMPLO = [
    {
        "id": "FLT-2026-001",
        "ot": "OT-88412",
        "fecha": "2026-09-05 14:30",
        "cliente": "Minera Pelambres",
        "faena": "Planta Concentradora",
        "tag": "BOMBA-HYD-04",
        "tipo": "Monitoreo de Condición",
        "criticidad": "ALTA",
        "inspector": "Carlos Mendoza",
        "temp": "78",
        "presion": "2100",
        "iso": "21/19/16",
        "foto": None,
        "diagnostico": "Presencia de partículas metálicas en la muestra de drenaje. Elevada temperatura de funcionamiento en el bloque hidráulico principal.",
        "recomendaciones": "Reemplazo inmediato de filtros de retorno y programación de diálisis de fluido lubricante dentro de 48 horas."
    },
    {
        "id": "FLT-2026-002",
        "ot": "OT-88413",
        "fecha": "2026-09-06 09:15",
        "cliente": "Atacama Minerals",
        "faena": "Mina Subterránea",
        "tag": "RED-PARAMAX-9000",
        "tipo": "Análisis de Aceite / Fluidos",
        "criticidad": "MEDIA",
        "inspector": "Andrea Rojas",
        "temp": "62",
        "presion": "1450",
        "iso": "18/16/13",
        "foto": None,
        "diagnostico": "Viscosidad del aceite ligeramente fuera de rango óptimo por degradación térmica moderada.",
        "recomendaciones": "Tomar nueva muestra de seguimiento en 15 días y verificar sellos de respiradero."
    }
]

# Inicialización de la sesión para los reportes
if "reports_data" not in st.session_state:
    st.session_state.reports_data = DATOS_EJEMPLO

# --- DIÁLOGO / MODAL NATIVO DE STREAMLIT ---
@st.dialog("📝 Nuevo Reporte / Orden de Trabajo", width="large")
def modal_nuevo_reporte():
    with st.form("form_nuevo_reporte", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            ot = st.text_input("Orden de Trabajo (OT) *", placeholder="Ej: OT-10492")
            cliente = st.text_input("Cliente *", placeholder="Ej: Minera Candelaria")
            faena = st.text_input("Faena / Planta *", placeholder="Ej: Concentradora")
            tag = st.text_input("Equipo / Tag ID *", placeholder="Ej: RED-9000-A")
        
        with col2:
            tipo = st.selectbox("Tipo de Servicio", [
                "Monitoreo de Condición", 
                "Análisis de Aceite / Fluidos", 
                "Mantenimiento Hidráulico", 
                "Inspección General"
            ])
            criticidad = st.selectbox("Nivel de Criticidad", ["NORMAL", "MEDIA", "ALTA"])
            inspector = st.text_input("Inspector Responsable *", placeholder="Nombre del Técnico")
        
        st.markdown("*Parámetros Operacionales (Opcional)*")
        cp1, cp2, cp3 = st.columns(3)
        with cp1:
            temp = st.text_input("Temp. (°C)", placeholder="65")
        with cp2:
            presion = st.text_input("Presión (PSI)", placeholder="1800")
        with cp3:
            iso = st.text_input("Código ISO 4406", placeholder="18/16/13")

        diagnostico = st.text_area("Diagnóstico Técnico y Hallazgos *", placeholder="Describa el estado actual del equipo...")
        recomendaciones = st.text_area("Recomendaciones / Acciones", placeholder="Acciones correctivas sugeridas...")

        submitted = st.form_submit_button("💾 Guardar Reporte", use_container_width=True, type="primary")
        
        if submitted:
            if not ot or not cliente or not tag or not inspector or not diagnostico:
                st.error("Por favor completa todos los campos obligatorios (*).")
            else:
                nuevo_folio = f"FLT-2026-{len(st.session_state.reports_data) + 1:03d}"
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                nuevo_registro = {
                    "id": nuevo_folio,
                    "ot": ot,
                    "fecha": fecha_actual,
                    "cliente": cliente,
                    "faena": faena,
                    "tag": tag,
                    "tipo": tipo,
                    "criticidad": criticidad,
                    "inspector": inspector,
                    "temp": temp if temp else "-",
                    "presion": presion if presion else "-",
                    "iso": iso if iso else "-",
                    "foto": None,
                    "diagnostico": diagnostico,
                    "recomendaciones": recomendaciones if recomendaciones else "Sin recomendaciones."
                }
                
                st.session_state.reports_data.insert(0, nuevo_registro)
                st.success(f"¡Reporte {nuevo_folio} guardado exitosamente!")
                st.rerun()

# --- BARRA SUPERIOR DE ACCIONES EN STREAMLIT ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("### ⚙️ *Fluitek Chile* - Gestión de Reportes de Campo")
with col_head2:
    if st.button("➕ Nuevo Reporte / OT", type="primary", use_container_width=True):
        modal_nuevo_reporte()

# Convertir los datos de la sesión a JSON para cargarlos dinámicamente en el HTML
json_reports = json.dumps(st.session_state.reports_data, ensure_ascii=False)

# Código HTML/JS con interfaz corporativa Fluitek
fluitek_app_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @media print {{
            .no-print {{ display: none !important; }}
            .print-only {{ display: block !important; }}
            body {{ background: white; color: black; }}
            .print-card {{ border: 1px solid #ccc; box-shadow: none !important; }}
        }}
        .print-only {{ display: none; }}
        .fluitek-logo-badge {{
            background-color: #000000;
            color: #ffffff;
            font-weight: 900;
            letter-spacing: 0.05em;
            display: inline-block;
        }}
    </style>
</head>
<body class="bg-slate-100 font-sans text-slate-800 min-h-screen flex flex-col p-2">

    <!-- Top Navigation Bar -->
    <header class="bg-slate-900 text-white shadow-lg no-print rounded-xl mb-4 border border-slate-800">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="fluitek-logo-badge text-xl px-3.5 py-1 rounded shadow-md border border-slate-700">
                    FLUITEK
                </div>
                <div>
                    <h1 class="text-lg font-bold leading-tight text-white">Field & Technical Reports</h1>
                    <p class="text-xs text-slate-400">Gestión de Inspecciones, Fluidos & Monitoreo de Condición</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button onclick="exportDataCSV()" class="bg-slate-800 hover:bg-slate-700 text-white border border-slate-600 px-3 py-2 rounded-lg text-sm transition flex items-center shadow">
                    <i class="fa-solid fa-file-excel mr-2 text-emerald-400"></i> Exportar CSV
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-1 flex-grow w-full">

        <!-- KPI Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6 no-print">
            <div class="bg-white rounded-xl shadow-sm p-4 border-l-4 border-slate-900 flex justify-between items-center">
                <div>
                    <p class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Total Reportes</p>
                    <h3 id="kpi-total" class="text-2xl font-bold text-slate-800">0</h3>
                </div>
                <div class="w-10 h-10 rounded-full bg-slate-100 text-slate-800 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-clipboard-list"></i>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-4 border-l-4 border-red-500 flex justify-between items-center">
                <div>
                    <p class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Criticidad Alta / Alarma</p>
                    <h3 id="kpi-critical" class="text-2xl font-bold text-red-600">0</h3>
                </div>
                <div class="w-10 h-10 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-4 border-l-4 border-amber-500 flex justify-between items-center">
                <div>
                    <p class="text-xs uppercase tracking-wider text-slate-500 font-semibold">En Advertencia</p>
                    <h3 id="kpi-warning" class="text-2xl font-bold text-amber-600">0</h3>
                </div>
                <div class="w-10 h-10 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-circle-exclamation"></i>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-4 border-l-4 border-emerald-500 flex justify-between items-center">
                <div>
                    <p class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Condición Normal</p>
                    <h3 id="kpi-normal" class="text-2xl font-bold text-emerald-600">0</h3>
                </div>
                <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-circle-check"></i>
                </div>
            </div>
        </div>

        <!-- Filter & Search Controls -->
        <div class="bg-white p-4 rounded-xl shadow-sm mb-6 flex flex-col md:flex-row gap-4 items-center justify-between no-print">
            <div class="flex flex-1 gap-3 w-full md:w-auto">
                <div class="relative flex-1">
                    <i class="fa-solid fa-search absolute left-3 top-3 text-slate-400"></i>
                    <input type="text" id="searchInput" oninput="renderReports()" placeholder="Buscar por OT, Cliente, Tag, Inspector..." class="w-full pl-9 pr-4 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none">
                </div>
                <select id="filterSeverity" onchange="renderReports()" class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none">
                    <option value="ALL">Todas las Criticidades</option>
                    <option value="ALTA">Alta / Alarma</option>
                    <option value="MEDIA">Advertencia</option>
                    <option value="NORMAL">Normal</option>
                </select>
            </div>
        </div>

        <!-- Reports Table View -->
        <div class="bg-white rounded-xl shadow-sm overflow-hidden no-print">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-50 text-slate-600 text-xs uppercase tracking-wider border-b">
                            <th class="p-4">Folio / OT / Fecha</th>
                            <th class="p-4">Cliente / Faena</th>
                            <th class="p-4">Equipo / Tag</th>
                            <th class="p-4">Tipo de Servicio</th>
                            <th class="p-4">Criticidad</th>
                            <th class="p-4">Inspector</th>
                            <th class="p-4 text-center">Acciones</th>
                        </tr>
                    </thead>
                    <tbody id="reportsTableBody" class="divide-y text-sm">
                        <!-- Dynamic Rows -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Printable Official Report View -->
        <div id="printPreviewContainer" class="hidden bg-white p-8 rounded-xl shadow-lg border my-6 print-card">
            <div class="flex justify-between items-start border-b pb-4 mb-6">
                <div>
                    <div class="fluitek-logo-badge text-2xl px-4 py-1.5 rounded tracking-wider shadow">
                        FLUITEK CHILE
                    </div>
                    <p class="text-xs text-slate-500 mt-2">Servicios de Ingeniería, Fluidos y Mantenimiento Predictivo</p>
                </div>
                <div class="text-right">
                    <span id="previewFolio" class="text-lg font-bold text-slate-800">FOLIO: FLT-2026-001</span>
                    <p id="previewFecha" class="text-xs text-slate-500">Fecha: -</p>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4 bg-slate-50 p-4 rounded-lg mb-6 border text-xs">
                <div>
                    <p><strong class="text-slate-700">Orden de Trabajo (OT):</strong> <span id="previewOT" class="font-bold text-amber-700">-</span></p>
                    <p><strong class="text-slate-700">Cliente:</strong> <span id="previewCliente">-</span></p>
                    <p><strong class="text-slate-700">Faena / Planta:</strong> <span id="previewFaena">-</span></p>
                </div>
                <div>
                    <p><strong class="text-slate-700">Equipo / Tag:</strong> <span id="previewTag">-</span></p>
                    <p><strong class="text-slate-700">Tipo Servicio:</strong> <span id="previewTipo">-</span></p>
                    <p><strong class="text-slate-700">Inspector Fluitek:</strong> <span id="previewInspector">-</span></p>
                </div>
            </div>

            <div class="mb-6">
                <h4 class="font-bold text-sm text-slate-800 mb-2 border-b pb-1">ESTADO & CRITICIDAD DEL EQUIPO</h4>
                <div id="previewBadgeCriticidad" class="inline-block px-4 py-2 rounded font-bold text-sm mb-2">
                    CRITICIDAD ALTA
                </div>
                <div class="grid grid-cols-3 gap-4 text-xs bg-slate-100 p-3 rounded mt-2">
                    <div><strong>Temp. Operación:</strong> <span id="previewTemp">-</span> °C</div>
                    <div><strong>Presión / Flujo:</strong> <span id="previewPresion">-</span> PSI</div>
                    <div><strong>Nivel ISO Contaminación:</strong> <span id="previewISO">-</span></div>
                </div>
            </div>

            <div class="mb-6">
                <h4 class="font-bold text-sm text-slate-800 mb-2 border-b pb-1">DIAGNÓSTICO TÉCNICO & HALLAZGOS</h4>
                <p id="previewDiagnostico" class="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-slate-50 p-3 rounded border">
                    Sin observaciones registradas.
                </p>
            </div>

            <div class="mb-6">
                <h4 class="font-bold text-sm text-slate-800 mb-2 border-b pb-1">RECOMENDACIONES DE ACCIÓN</h4>
                <p id="previewRecomendaciones" class="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-amber-50/50 p-3 rounded border border-amber-200">
                    Sin recomendaciones.
                </p>
            </div>

            <div class="grid grid-cols-2 gap-8 mt-12 pt-8 border-t text-center text-xs">
                <div>
                    <div class="border-b border-slate-400 mb-2 h-12 flex items-end justify-center pb-1 text-slate-600">Firma Inspector</div>
                    <p class="font-bold" id="previewFirmaTecnico">Técnico Fluitek</p>
                    <p class="text-slate-500">Especialista en Monitoreo de Condición</p>
                </div>
                <div>
                    <div class="border-b border-slate-400 mb-2 h-12 flex items-end justify-center pb-1 text-slate-600">Aprobación Cliente</div>
                    <p class="font-bold">Recepción Cliente / Supervisión</p>
                    <p class="text-slate-500">Conforme / Notificado</p>
                </div>
            </div>

            <div class="mt-8 flex justify-end gap-3 no-print">
                <button onclick="closePreview()" class="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold hover:bg-slate-300">
                    Cerrar Vista Previa
                </button>
                <button onclick="window.print()" class="px-4 py-2 bg-slate-900 text-white rounded-lg text-xs font-semibold hover:bg-black flex items-center shadow">
                    <i class="fa-solid fa-print mr-2"></i> Imprimir / Exportar PDF
                </button>
            </div>
        </div>

    </main>

    <script>
        const reports = {json_reports};

        window.addEventListener('DOMContentLoaded', () => {{
            renderReports();
        }});

        function renderReports() {{
            const tbody = document.getElementById('reportsTableBody');
            const search = document.getElementById('searchInput').value.toLowerCase();
            const severity = document.getElementById('filterSeverity').value;

            tbody.innerHTML = '';

            let filtered = reports.filter(r => {{
                const matchesSearch = r.cliente.toLowerCase().includes(search) || 
                                     r.tag.toLowerCase().includes(search) || 
                                     r.inspector.toLowerCase().includes(search) ||
                                     r.id.toLowerCase().includes(search) ||
                                     (r.ot && r.ot.toLowerCase().includes(search));
                const matchesSeverity = (severity === 'ALL') || (r.criticidad === severity);
                return matchesSearch && matchesSeverity;
            }});

            document.getElementById('kpi-total').innerText = reports.length;
            document.getElementById('kpi-critical').innerText = reports.filter(r => r.criticidad === 'ALTA').length;
            document.getElementById('kpi-warning').innerText = reports.filter(r => r.criticidad === 'MEDIA').length;
            document.getElementById('kpi-normal').innerText = reports.filter(r => r.criticidad === 'NORMAL').length;

            filtered.forEach(r => {{
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50 transition border-b";

                let badgeClass = "bg-emerald-100 text-emerald-800 border-emerald-300";
                let badgeIcon = "fa-circle-check";
                if (r.criticidad === 'ALTA') {{
                    badgeClass = "bg-red-100 text-red-800 border-red-300";
                    badgeIcon = "fa-triangle-exclamation";
                }} else if (r.criticidad === 'MEDIA') {{
                    badgeClass = "bg-amber-100 text-amber-800 border-amber-300";
                    badgeIcon = "fa-circle-exclamation";
                }}

                tr.innerHTML = `
                    <td class="p-4">
                        <span class="font-bold text-slate-900">${{r.id}}</span>
                        <div class="text-xs font-semibold text-amber-600"><i class="fa-solid fa-hashtag mr-0.5"></i>OT: ${{r.ot || 'N/A'}}</div>
                        <div class="text-xs text-slate-400">${{r.fecha}}</div>
                    </td>
                    <td class="p-4">
                        <div class="font-semibold text-slate-800">${{r.cliente}}</div>
                        <div class="text-xs text-slate-500">${{r.faena}}</div>
                    </td>
                    <td class="p-4">
                        <span class="font-mono bg-slate-100 px-2 py-1 rounded text-xs border font-semibold text-slate-700">${{r.tag}}</span>
                    </td>
                    <td class="p-4 text-xs font-medium text-slate-600">${{r.tipo}}</td>
                    <td class="p-4">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border ${{badgeClass}}">
                            <i class="fa-solid ${{badgeIcon}} mr-1.5 text-[10px]"></i> ${{r.criticidad}}
                        </span>
                    </td>
                    <td class="p-4 text-xs text-slate-600">${{r.inspector}}</td>
                    <td class="p-4 text-center">
                        <button onclick="previewReport('${{r.id}}')" title="Ver / Imprimir Informe PDF" class="p-2 text-slate-800 hover:bg-slate-100 rounded-lg transition">
                            <i class="fa-solid fa-file-pdf text-base text-red-600"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function previewReport(id) {{
            const r = reports.find(item => item.id === id);
            if (!r) return;

            document.getElementById('previewFolio').innerText = FOLIO: ${{r.id}};
            document.getElementById('previewFecha').innerText = Fecha: ${{r.fecha}};
            document.getElementById('previewOT').innerText = r.ot || 'N/A';
            document.getElementById('previewCliente').innerText = r.cliente;
            document.getElementById('previewFaena').innerText = r.faena;
            document.getElementById('previewTag').innerText = r.tag;
            document.getElementById('previewTipo').innerText = r.tipo;
            document.getElementById('previewInspector').innerText = r.inspector;
            document.getElementById('previewFirmaTecnico').innerText = r.inspector;

            document.getElementById('previewTemp').innerText = r.temp;
            document.getElementById('previewPresion').innerText = r.presion;
            document.getElementById('previewISO').innerText = r.iso;

            document.getElementById('previewDiagnostico').innerText = r.diagnostico || 'Sin observaciones.';
            document.getElementById('previewRecomendaciones').innerText = r.recomendaciones || 'Sin recomendaciones.';

            const badge = document.getElementById('previewBadgeCriticidad');
            if (r.criticidad === 'ALTA') {{
                badge.className = "inline-block px-4 py-2 rounded font-bold text-sm mb-2 bg-red-100 text-red-800 border border-red-300";
                badge.innerText = "CRITICIDAD ALTA / ALARMA";
            }} else if (r.criticidad === 'MEDIA') {{
                badge.className = "inline-block px-4 py-2 rounded font-bold text-sm mb-2 bg-amber-100 text-amber-800 border border-amber-300";
                badge.innerText = "CRITICIDAD MEDIA / ADVERTENCIA";
            }} else {{
                badge.className = "inline-block px-4 py-2 rounded font-bold text-sm mb-2 bg-emerald-100 text-emerald-800 border border-emerald-300";
                badge.innerText = "CONDICIÓN NORMAL";
            }}

            const container = document.getElementById('printPreviewContainer');
            container.classList.remove('hidden');
            container.scrollIntoView({{ behavior: 'smooth' }});
        }}

        function closePreview() {{
            document.getElementById('printPreviewContainer').classList.add('hidden');
        }}

        function exportDataCSV() {{
            if (reports.length === 0) {{
                alert('No hay datos para exportar.');
                return;
            }}
            const headers = ["Folio", "Fecha", "Orden de Trabajo", "Cliente", "Faena", "Tag", "Tipo Servicio", "Criticidad", "Inspector", "Temp (C)", "Presion (PSI)", "Codigo ISO", "Diagnostico", "Recomendaciones"];
            const rows = reports.map(r => [
                "${{r.id}}",
                "${{r.fecha}}",
                "${{r.ot || ''}}",
                "${{r.cliente}}",
                "${{r.faena}}",
                "${{r.tag}}",
                "${{r.tipo}}",
                "${{r.criticidad}}",
                "${{r.inspector}}",
                "${{r.temp}}",
                "${{r.presion}}",
                "${{r.iso}}",
                "${{(r.diagnostico || '').replace(/"/g, '""')}}",
                "${{(r.recomendaciones || '').replace(/"/g, '""')}}"
            ]);

            const csvContent = "data:text/csv;charset=utf-8,\\uFEFF" + [headers.join(","), ...rows.map(e => e.join(","))].join("\\n");
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", Reportes_Fluitek_${{new Date().toISOString().slice(0,10)}}.csv);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
    </script>
</body>
</html>
"""

# Renderizar componente de la interfaz
components.html(fluitek_app_html, height=850, scrolling=True)
