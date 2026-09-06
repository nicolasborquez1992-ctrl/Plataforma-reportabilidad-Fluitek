import streamlit as st
import streamlit.components.v1 as components

# Configuración de página en Streamlit
st.set_page_config(
    page_title="Fluitek - Reportes Técnicos",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo para eliminar márgenes extra de Streamlit
st.markdown("""
    <style>
        .block-container { padding-top: 0rem; padding-bottom: 0rem; padding-left: 0rem; padding-right: 0rem; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

fluitek_full_app = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fluitek - Field & Technical Reports</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @media print {
            .no-print { display: none !important; }
            .print-only { display: block !important; }
            body { background: white; color: black; }
        }
        .print-only { display: none; }
        
        /* Modal Backdrop Fix */
        .modal-active {
            display: flex !important;
        }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen p-3">

    <!-- CABECERA MADRE FLUITEK -->
    <header class="bg-slate-950 border border-slate-800 rounded-xl p-4 mb-4 shadow-xl flex justify-between items-center no-print">
        <div class="flex items-center space-x-3">
            <div class="bg-black text-white font-black text-xl px-4 py-1.5 rounded tracking-wider border border-slate-700">
                FLUITEK
            </div>
            <div>
                <h1 class="text-lg font-bold text-white tracking-wide">Field & Technical Reports</h1>
                <p class="text-xs text-slate-400">Gestión de Inspecciones, Fluidos & Monitoreo de Condición</p>
            </div>
        </div>
        
        <div class="flex items-center space-x-3">
            <!-- BOTÓN EN AMARILLO PEDIDO POR EL USUARIO -->
            <button onclick="openModal()" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-extrabold px-4 py-2 rounded-lg text-sm transition flex items-center shadow-lg border border-amber-400">
                <i class="fa-solid fa-plus-circle mr-2"></i> Nuevo Reporte / OT
            </button>
            <button onclick="exportCSV()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3.5 py-2 rounded-lg text-sm transition flex items-center shadow">
                <i class="fa-solid fa-file-excel mr-2 text-emerald-400"></i> Exportar CSV
            </button>
        </div>
    </header>

    <!-- TARJETAS KPIS -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6 no-print">
        <div class="bg-slate-950 rounded-xl p-4 border-l-4 border-slate-500 border-t border-r border-b border-slate-800 flex justify-between items-center shadow-md">
            <div>
                <p class="text-xs uppercase tracking-wider text-slate-400 font-medium">TOTAL REPORTES</p>
                <h3 id="kpi-total" class="text-2xl font-bold text-white">0</h3>
            </div>
            <div class="text-slate-500 text-xl"><i class="fa-solid fa-clipboard-list"></i></div>
        </div>

        <div class="bg-slate-950 rounded-xl p-4 border-l-4 border-red-500 border-t border-r border-b border-slate-800 flex justify-between items-center shadow-md">
            <div>
                <p class="text-xs uppercase tracking-wider text-slate-400 font-medium">CRITICIDAD ALTA / ALARMA</p>
                <h3 id="kpi-alta" class="text-2xl font-bold text-red-500">0</h3>
            </div>
            <div class="text-red-500 text-xl"><i class="fa-solid fa-triangle-exclamation"></i></div>
        </div>

        <div class="bg-slate-950 rounded-xl p-4 border-l-4 border-amber-500 border-t border-r border-b border-slate-800 flex justify-between items-center shadow-md">
            <div>
                <p class="text-xs uppercase tracking-wider text-slate-400 font-medium">EN ADVERTENCIA</p>
                <h3 id="kpi-media" class="text-2xl font-bold text-amber-500">0</h3>
            </div>
            <div class="text-amber-500 text-xl"><i class="fa-solid fa-circle-exclamation"></i></div>
        </div>

        <div class="bg-slate-950 rounded-xl p-4 border-l-4 border-emerald-500 border-t border-r border-b border-slate-800 flex justify-between items-center shadow-md">
            <div>
                <p class="text-xs uppercase tracking-wider text-slate-400 font-medium">CONDICIÓN NORMAL</p>
                <h3 id="kpi-normal" class="text-2xl font-bold text-emerald-500">0</h3>
            </div>
            <div class="text-emerald-500 text-xl"><i class="fa-solid fa-circle-check"></i></div>
        </div>
    </div>

    <!-- CONTROLES BÚSQUEDA Y FILTRO -->
    <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 mb-4 flex flex-col md:flex-row gap-3 justify-between items-center no-print">
        <div class="relative w-full md:w-96">
            <i class="fa-solid fa-search absolute left-3 top-3 text-slate-500"></i>
            <input type="text" id="searchInput" oninput="renderTable()" placeholder="Buscar por OT, Cliente, Tag, Inspector..." class="w-full pl-9 pr-4 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-amber-500">
        </div>
        <div class="flex items-center space-x-3 w-full md:w-auto">
            <select id="filterCriticidad" onchange="renderTable()" class="bg-slate-900 border border-slate-700 text-slate-200 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-amber-500">
                <option value="ALL">Todas las Criticidades</option>
                <option value="ALTA">Alta / Alarma</option>
                <option value="MEDIA">Advertencia</option>
                <option value="NORMAL">Normal</option>
            </select>
            <button onclick="cargarEjemplos()" class="text-xs text-amber-400 hover:text-amber-300 underline font-medium whitespace-nowrap">
                🔄 Cargar Datos de Ejemplo
            </button>
        </div>
    </div>

    <!-- TABLA DE REPORTES -->
    <div class="bg-slate-950 rounded-xl border border-slate-800 overflow-hidden shadow-lg no-print">
        <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-900 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
                        <th class="p-3">FOTO</th>
                        <th class="p-3">FOLIO / OT / FECHA</th>
                        <th class="p-3">CLIENTE / FAENA</th>
                        <th class="p-3">EQUIPO / TAG</th>
                        <th class="p-3">TIPO DE SERVICIO</th>
                        <th class="p-3">CRITICIDAD</th>
                        <th class="p-3">INSPECTOR</th>
                        <th class="p-3 text-center">ACCIONES</th>
                    </tr>
                </thead>
                <tbody id="tableBody" class="divide-y divide-slate-800/60 text-sm">
                    <!-- Registros dinámicos -->
                </tbody>
            </table>
        </div>
    </div>

    <!-- MODAL POPUP PARA NUEVO REPORTE -->
    <div id="reportModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm hidden justify-center items-center p-4 z-50">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3 mb-4">
                <h3 class="text-lg font-bold text-amber-400 flex items-center">
                    <i class="fa-solid fa-file-pen mr-2"></i> Nuevo Reporte / Orden de Trabajo
                </h3>
                <button onclick="closeModal()" class="text-slate-400 hover:text-white text-xl">&times;</button>
            </div>

            <form id="reportForm" onsubmit="saveReport(event)" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">Orden de Trabajo (OT) *</label>
                        <input type="text" id="inputOT" required placeholder="Ej: OT-88412" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">Tipo de Servicio</label>
                        <select id="inputTipo" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500">
                            <option value="Monitoreo de Condición">Monitoreo de Condición</option>
                            <option value="Análisis de Aceite / Fluidos">Análisis de Aceite / Fluidos</option>
                            <option value="Mantenimiento Hidráulico">Mantenimiento Hidráulico</option>
                            <option value="Inspección de Reductores">Inspección de Reductores</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">Cliente *</label>
                        <input type="text" id="inputCliente" required placeholder="Ej: Minera Los Pelambres" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">Nivel de Criticidad *</label>
                        <select id="inputCriticidad" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 font-bold focus:outline-none focus:border-amber-500">
                            <option value="NORMAL" class="text-emerald-500">NORMAL</option>
                            <option value="MEDIA" class="text-amber-500">MEDIA / ADVERTENCIA</option>
                            <option value="ALTA" class="text-red-500">ALTA / ALARMA</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">Faena / Planta *</label>
                        <input type="text" id="inputFaena" required placeholder="Ej: Planta Concentradora" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">Inspector Responsable *</label>
                        <input type="text" id="inputInspector" required placeholder="Nombre del Técnico" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">Equipo / Tag ID *</label>
                        <input type="text" id="inputTag" required placeholder="Ej: RED-PARAMAX-9000" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-300 mb-1">Adjuntar Foto (Opcional)</label>
                        <input type="file" id="inputFoto" accept="image/*" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-1.5 text-xs text-slate-400 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:bg-slate-800 file:text-slate-200">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Diagnóstico Técnico y Hallazgos *</label>
                    <textarea id="inputDiagnostico" required rows="3" placeholder="Describa la condición operacional o falla detectada..." class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500"></textarea>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-slate-300 mb-1">Recomendaciones / Acciones</label>
                    <textarea id="inputRecomendaciones" rows="2" placeholder="Acciones correctivas o preventivas..." class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-sm text-slate-100 focus:outline-none focus:border-amber-500"></textarea>
                </div>

                <div class="flex justify-end space-x-3 pt-3 border-t border-slate-800">
                    <button type="button" onclick="closeModal()" class="px-4 py-2 bg-slate-800 text-slate-300 hover:bg-slate-700 rounded-lg text-sm">Cancelar</button>
                    <button type="submit" class="px-5 py-2 bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold rounded-lg text-sm flex items-center shadow-lg">
                        <i class="fa-solid fa-floppy-disk mr-2"></i> Guardar Reporte
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- VISTA PREVIA FORMATO INFORME IMPRIMIBLE -->
    <div id="printPreview" class="hidden bg-white text-slate-900 p-8 rounded-xl shadow-2xl border border-slate-300 max-w-4xl mx-auto my-6 print-card">
        <div class="flex justify-between items-start border-b-2 border-slate-900 pb-4 mb-6">
            <div>
                <div class="bg-black text-white font-black text-2xl px-4 py-1.5 rounded tracking-wider inline-block">
                    FLUITEK CHILE
                </div>
                <p class="text-xs text-slate-600 mt-2">Servicios de Ingeniería, Fluidos & Mantenimiento Predictivo</p>
            </div>
            <div class="text-right">
                <span id="pvFolio" class="text-lg font-bold text-slate-900">FOLIO: FLT-2026-001</span>
                <p id="pvFecha" class="text-xs text-slate-500">Fecha: -</p>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4 bg-slate-50 p-4 rounded-lg mb-6 border border-slate-200 text-xs">
            <div>
                <p class="mb-1"><strong class="text-slate-800">Orden de Trabajo:</strong> <span id="pvOT" class="font-bold text-amber-700">-</span></p>
                <p class="mb-1"><strong class="text-slate-800">Cliente:</strong> <span id="pvCliente">-</span></p>
                <p><strong class="text-slate-800">Faena / Planta:</strong> <span id="pvFaena">-</span></p>
            </div>
            <div>
                <p class="mb-1"><strong class="text-slate-800">Equipo / Tag:</strong> <span id="pvTag">-</span></p>
                <p class="mb-1"><strong class="text-slate-800">Tipo Servicio:</strong> <span id="pvTipo">-</span></p>
                <p><strong class="text-slate-800">Inspector Responsable:</strong> <span id="pvInspector">-</span></p>
            </div>
        </div>

        <div class="mb-6">
            <h4 class="font-bold text-sm text-slate-900 mb-2 border-b border-slate-300 pb-1">ESTADO & CRITICIDAD</h4>
            <div id="pvBadgeCriticidad" class="inline-block px-3 py-1.5 rounded font-bold text-xs uppercase">
                NORMAL
            </div>
        </div>

        <div class="mb-6">
            <h4 class="font-bold text-sm text-slate-900 mb-2 border-b border-slate-300 pb-1">DIAGNÓSTICO TÉCNICO Y HALLAZGOS</h4>
            <p id="pvDiagnostico" class="text-xs text-slate-800 whitespace-pre-line leading-relaxed bg-slate-50 p-3 rounded border border-slate-200">
                -
            </p>
        </div>

        <div class="mb-6">
            <h4 class="font-bold text-sm text-slate-900 mb-2 border-b border-slate-300 pb-1">RECOMENDACIONES</h4>
            <p id="pvRecomendaciones" class="text-xs text-slate-800 whitespace-pre-line leading-relaxed bg-amber-50/50 p-3 rounded border border-amber-200">
                -
            </p>
        </div>

        <div class="grid grid-cols-2 gap-8 mt-12 pt-8 border-t border-slate-300 text-center text-xs">
            <div>
                <div class="border-b border-slate-400 mb-2 h-10 flex items-end justify-center pb-1 text-slate-500">Firma Técnico</div>
                <p class="font-bold" id="pvFirmaInspector">Técnico Fluitek</p>
            </div>
            <div>
                <div class="border-b border-slate-400 mb-2 h-10 flex items-end justify-center pb-1 text-slate-500">Recepción Cliente</div>
                <p class="font-bold">Supervisión / Operaciones</p>
            </div>
        </div>

        <div class="mt-8 flex justify-end gap-3 no-print">
            <button onclick="closePreview()" class="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold hover:bg-slate-300">Cerrar</button>
            <button onclick="window.print()" class="px-4 py-2 bg-slate-900 text-white rounded-lg text-xs font-semibold hover:bg-black flex items-center">
                <i class="fa-solid fa-print mr-2"></i> Imprimir Informe PDF
            </button>
        </div>
    </div>

    <script>
        let reportsData = [];

        function openModal() {
            document.getElementById('reportModal').classList.add('modal-active');
        }

        function closeModal() {
            document.getElementById('reportModal').classList.remove('modal-active');
            document.getElementById('reportForm').reset();
        }

        function saveReport(event) {
            event.preventDefault();

            const ot = document.getElementById('inputOT').value.trim();
            const cliente = document.getElementById('inputCliente').value.trim();
            const faena = document.getElementById('inputFaena').value.trim();
            const tag = document.getElementById('inputTag').value.trim();
            const tipo = document.getElementById('inputTipo').value;
            const criticidad = document.getElementById('inputCriticidad').value;
            const inspector = document.getElementById('inputInspector').value.trim();
            const diagnostico = document.getElementById('inputDiagnostico').value.trim();
            const recomendaciones = document.getElementById('inputRecomendaciones').value.trim();
            const fotoInput = document.getElementById('inputFoto');

            const folioNum = String(reportsData.length + 1).padStart(3, '0');
            const newFolio = FLT-2026-${folioNum};
            
            const now = new Date();
            const fechaStr = ${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')} ${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')};

            let imgUrl = null;
            if (fotoInput.files && fotoInput.files[0]) {
                imgUrl = URL.createObjectURL(fotoInput.files[0]);
            }

            const newRecord = {
                id: newFolio,
                ot: ot,
                fecha: fechaStr,
                cliente: cliente,
                faena: faena,
                tag: tag,
                tipo: tipo,
                criticidad: criticidad,
                inspector: inspector,
                diagnostico: diagnostico,
                recomendaciones: recomendaciones || 'Sin recomendaciones adicionales.',
                foto: imgUrl
            };

            reportsData.unshift(newRecord);
            closeModal();
            renderTable();
        }

        function renderTable() {
            const tbody = document.getElementById('tableBody');
            const search = document.getElementById('searchInput').value.toLowerCase();
            const filterCrit = document.getElementById('filterCriticidad').value;

            tbody.innerHTML = '';

            let filtered = reportsData.filter(r => {
                const matchSearch = r.cliente.toLowerCase().includes(search) ||
                                    r.tag.toLowerCase().includes(search) ||
                                    r.inspector.toLowerCase().includes(search) ||
                                    r.id.toLowerCase().includes(search) ||
                                    (r.ot && r.ot.toLowerCase().includes(search));
                const matchCrit = (filterCrit === 'ALL') || (r.criticidad === filterCrit);
                return matchSearch && matchCrit;
            });

            // Actualizar KPIs
            document.getElementById('kpi-total').innerText = reportsData.length;
            document.getElementById('kpi-alta').innerText = reportsData.filter(r => r.criticidad === 'ALTA').length;
            document.getElementById('kpi-media').innerText = reportsData.filter(r => r.criticidad === 'MEDIA').length;
            document.getElementById('kpi-normal').innerText = reportsData.filter(r => r.criticidad === 'NORMAL').length;

            if (filtered.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" class="p-8 text-center text-slate-500 font-medium">
                            <i class="fa-regular fa-folder-open text-2xl mb-2 block"></i>
                            No hay reportes ingresados. Haz clic en <span class="text-amber-400 font-bold">"Nuevo Reporte / OT"</span> para registrar uno.
                        </td>
                    </tr>
                `;
                return;
            }

            filtered.forEach(r => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-900/80 transition border-b border-slate-800/60";

                // ESTILOS DE COLORES PARA CRITICIDAD
                let badgeHTML = '';
                if (r.criticidad === 'ALTA') {
                    badgeHTML = `<span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-red-500/20 text-red-400 border border-red-500/40">
                                    <i class="fa-solid fa-triangle-exclamation mr-1.5"></i> ALTA / ALARMA
                                 </span>`;
                } else if (r.criticidad === 'MEDIA') {
                    badgeHTML = `<span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/40">
                                    <i class="fa-solid fa-circle-exclamation mr-1.5"></i> ADVERTENCIA
                                 </span>`;
                } else {
                    badgeHTML = `<span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
                                    <i class="fa-solid fa-circle-check mr-1.5"></i> NORMAL
                                 </span>`;
                }

                const photoHTML = r.foto 
                    ? <img src="${r.foto}" class="w-9 h-9 object-cover rounded-lg border border-slate-700">
                    : <div class="w-9 h-9 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-600 text-xs"><i class="fa-solid fa-image"></i></div>;

                tr.innerHTML = `
                    <td class="p-3">${photoHTML}</td>
                    <td class="p-3">
                        <div class="font-bold text-slate-100">${r.id}</div>
                        <div class="text-xs font-semibold text-amber-400"><i class="fa-solid fa-hashtag mr-0.5"></i>${r.ot}</div>
                        <div class="text-[11px] text-slate-500">${r.fecha}</div>
                    </td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-200">${r.cliente}</div>
                        <div class="text-xs text-slate-400">${r.faena}</div>
                    </td>
                    <td class="p-3">
                        <span class="font-mono bg-slate-900 border border-slate-700 px-2 py-0.5 rounded text-xs font-semibold text-slate-300">${r.tag}</span>
                    </td>
                    <td class="p-3 text-xs text-slate-300 font-medium">${r.tipo}</td>
                    <td class="p-3">${badgeHTML}</td>
                    <td class="p-3 text-xs text-slate-300">${r.inspector}</td>
                    <td class="p-3 text-center">
                        <button onclick="previewReport('${r.id}')" title="Ver / Imprimir Informe" class="p-2 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg transition">
                            <i class="fa-solid fa-file-pdf text-red-400 text-base"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function previewReport(id) {
            const r = reportsData.find(item => item.id === id);
            if (!r) return;

            document.getElementById('pvFolio').innerText = FOLIO: ${r.id};
            document.getElementById('pvFecha').innerText = Fecha: ${r.fecha};
            document.getElementById('pvOT').innerText = r.ot;
            document.getElementById('pvCliente').innerText = r.cliente;
            document.getElementById('pvFaena').innerText = r.faena;
            document.getElementById('pvTag').innerText = r.tag;
            document.getElementById('pvTipo').innerText = r.tipo;
            document.getElementById('pvInspector').innerText = r.inspector;
            document.getElementById('pvFirmaInspector').innerText = r.inspector;

            document.getElementById('pvDiagnostico').innerText = r.diagnostico;
            document.getElementById('pvRecomendaciones').innerText = r.recomendaciones;

            const badge = document.getElementById('pvBadgeCriticidad');
            if (r.criticidad === 'ALTA') {
                badge.className = "inline-block px-3 py-1 rounded font-bold text-xs bg-red-100 text-red-800 border border-red-300";
                badge.innerText = "CRITICIDAD ALTA / ALARMA";
            } else if (r.criticidad === 'MEDIA') {
                badge.className = "inline-block px-3 py-1 rounded font-bold text-xs bg-amber-100 text-amber-800 border border-amber-300";
                badge.innerText = "ADVERTENCIA / CRITICIDAD MEDIA";
            } else {
                badge.className = "inline-block px-3 py-1 rounded font-bold text-xs bg-emerald-100 text-emerald-800 border border-emerald-300";
                badge.innerText = "CONDICIÓN NORMAL";
            }

            const pv = document.getElementById('printPreview');
            pv.classList.remove('hidden');
            pv.scrollIntoView({ behavior: 'smooth' });
        }

        function closePreview() {
            document.getElementById('printPreview').classList.add('hidden');
        }

        function cargarEjemplos() {
            reportsData = [
                {
                    id: "FLT-2026-001",
                    ot: "OT-88412",
                    fecha: "2026-09-06 14:30",
                    cliente: "Minera Pelambres",
                    faena: "Planta Concentradora",
                    tag: "BOMBA-HYD-04",
                    tipo: "Monitoreo de Condición",
                    criticidad: "ALTA",
                    inspector: "Carlos Mendoza",
                    diagnostico: "Presencia de partículas metálicas en la muestra de drenaje. Elevada temperatura de funcionamiento en el bloque hidráulico.",
                    recomendaciones: "Reemplazo inmediato de filtros de retorno y diálisis de aceite.",
                    foto: null
                },
                {
                    id: "FLT-2026-002",
                    ot: "OT-88413",
                    fecha: "2026-09-06 16:15",
                    cliente: "Atacama Minerals",
                    faena: "Mina Subterránea",
                    tag: "RED-PARAMAX-9000",
                    tipo: "Análisis de Aceite / Fluidos",
                    criticidad: "MEDIA",
                    inspector: "Andrea Rojas",
                    diagnostico: "Viscosidad del fluido ligeramente fuera de rango operacional.",
                    recomendaciones: "Programar cambio de lubricante en próximo turno de mantenimiento.",
                    foto: null
                }
            ];
            renderTable();
        }

        // Render inicial
        renderTable();
    </script>
</body>
</html>
"""

# Renderizar toda la aplicación embebida
components.html(fluitek_full_app, height=920, scrolling=True)
