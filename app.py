import streamlit as st

import streamlit.components.v1 as components



# Configuración de la página en Streamlit

st.set_page_config(

    page_title="Fluitek - Reportes Técnicos",

    page_icon="⚙️",

    layout="wide",

    initial_sidebar_state="collapsed"

)



# Código HTML, CSS y JavaScript encapsulado en una cadena multilínea de Python

fluitek_app_html = """

<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Fluitek - Sistema de Reportes Técnicos y Monitoreo</title>

    <!-- Tailwind CSS -->

    <script src="https://cdn.tailwindcss.com"></script>

    <!-- FontAwesome Icons -->

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <script>

        tailwind.config = {

            theme: {

                extend: {

                    colors: {

                        fluitek: {

                            50: '#f0f9ff',

                            100: '#e0f2fe',

                            500: '#0284c7',

                            600: '#0369a1',

                            700: '#075985',

                            800: '#0c4a6e',

                            900: '#0a3651',

                        }

                    }

                }

            }

        }

    </script>

    <style>

        @media print {

            .no-print { display: none !important; }

            .print-only { display: block !important; }

            body { background: white; color: black; }

            .print-card { border: 1px solid #ccc; box-shadow: none !important; }

        }

        .print-only { display: none; }

        /* Estilo distintivo para marca Fluitek */

        .fluitek-logo-badge {

            background-color: #000000;

            color: #ffffff;

            font-weight: 900;

            letter-spacing: 0.05em;

            display: inline-block;

        }

    </style>

</head>

<body class="bg-slate-100 font-sans text-slate-800 min-h-screen flex flex-col">



    <!-- Top Navigation Bar -->

    <header class="bg-slate-900 text-white shadow-lg no-print sticky top-0 z-50 border-b border-slate-800">

        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">

            <div class="flex items-center space-x-3">

                <!-- Logo Fluitek: Letras Blancas con Fondo Negro -->

                <div class="fluitek-logo-badge text-xl px-3.5 py-1 rounded shadow-md border border-slate-700">

                    FLUITEK

                </div>

                <div>

                    <h1 class="text-lg font-bold leading-tight text-white">Field & Technical Reports</h1>

                    <p class="text-xs text-slate-400">Gestión de Inspecciones, Fluidos & Monitoreo de Condición</p>

                </div>

            </div>

            <div class="flex items-center space-x-3">

                <button onclick="openNewReportModal()" class="bg-amber-500 hover:bg-amber-600 text-slate-900 font-semibold px-4 py-2 rounded-lg text-sm transition flex items-center shadow">

                    <i class="fa-solid fa-plus-circle mr-2"></i> Nuevo Reporte / OT

                </button>

                <button onclick="exportDataCSV()" class="bg-slate-800 hover:bg-slate-700 text-white border border-slate-600 px-3 py-2 rounded-lg text-sm transition flex items-center">

                    <i class="fa-solid fa-file-excel mr-2"></i> CSV

                </button>

            </div>

        </div>

    </header>



    <!-- Main Content Container -->

    <main class="max-w-7xl mx-auto px-4 py-6 flex-grow w-full">



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

                <select id="filterType" onchange="renderReports()" class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none">

                    <option value="ALL">Todos los Tipos</option>

                    <option value="Monitoreo de Condición">Monitoreo de Condición</option>

                    <option value="Análisis de Aceite / Fluidos">Análisis de Aceite / Fluidos</option>

                    <option value="Mantenimiento Hidráulico">Mantenimiento Hidráulico</option>

                    <option value="Inspección General">Inspección General</option>

                </select>

            </div>

            <button onclick="loadSampleData()" class="text-xs text-slate-600 hover:text-black underline font-medium">

                <i class="fa-solid fa-rotate-left mr-1"></i> Cargar Datos de Ejemplo

            </button>

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

            <div id="emptyState" class="p-8 text-center text-slate-500 hidden">

                <i class="fa-solid fa-folder-open text-4xl mb-2 text-slate-300"></i>

                <p>No se encontraron reportes con los filtros seleccionados.</p>

            </div>

        </div>



        <!-- Printable Official Report View -->

        <div id="printPreviewContainer" class="hidden bg-white p-8 rounded-xl shadow-lg border my-6 print-card">

            <div class="flex justify-between items-start border-b pb-4 mb-6">

                <div>

                    <!-- Logo Fluitek en Informe: Letras Blancas sobre Fondo Negro -->

                    <div class="fluitek-logo-badge text-2xl px-4 py-1.5 rounded tracking-wider shadow">

                        FLUITEK CHILE

                    </div>

                    <p class="text-xs text-slate-500 mt-2">Servicios de Ingeniería, Fluidos y Mantenimiento Predictivo</p>

                </div>

                <div class="text-right">

                    <span id="previewFolio" class="text-lg font-bold text-slate-800">FOLIO: FLT-2026-001</span>

                    <p id="previewFecha" class="text-xs text-slate-500">Fecha: 06/09/2026</p>

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



    <!-- Modal Form: Dynamic New/Edit Report with OT -->

    <div id="reportModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4 no-print">

        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">

            <div class="bg-slate-900 text-white px-6 py-4 flex justify-between items-center sticky top-0 z-10 border-b border-slate-800">

                <h3 class="font-bold text-lg flex items-center">

                    <span class="fluitek-logo-badge text-xs px-2 py-0.5 rounded mr-2">FLUITEK</span> 

                    <span id="modalTitle">Nuevo Reporte - Orden de Trabajo</span>

                </h3>

                <button onclick="closeReportModal()" class="text-slate-300 hover:text-white text-xl">

                    <i class="fa-solid fa-xmark"></i>

                </button>

            </div>



            <form id="reportForm" onsubmit="saveReport(event)" class="p-6 space-y-4">

                <input type="hidden" id="reportId">



                <!-- Orden de Trabajo y Datos Principales -->

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">

                    <div>

                        <label class="block text-xs font-bold text-slate-700 mb-1">Orden de Trabajo (OT) *</label>

                        <input type="text" id="inputOT" required placeholder="Ej: OT-10492" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none font-semibold text-amber-700">

                    </div>

                    <div>

                        <label class="block text-xs font-bold text-slate-700 mb-1">Cliente *</label>

                        <input type="text" id="inputCliente" required placeholder="Ej: Minera Candelaria" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none">

                    </div>

                    <div>

                        <label class="block text-xs font-bold text-slate-700 mb-1">Faena / Planta *</label>

                        <input type="text" id="inputFaena" required placeholder="Ej: Planta Concentradora" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none">

                    </div>

                    <div>

                        <label class="block text-xs font-bold text-slate-700 mb-1">Equipo / Tag ID *</label>

                        <input type="text" id="inputTag" required placeholder="Ej: RED-9000-A" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none">

                    </div>

                </div>



                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

                    <div>

                        <label class="block text-xs font-bold text-slate-700 mb-1">Tipo de Servicio</label>

                        <select id="inputTipo" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none">

                            <option value="Monitoreo de Condición">Monitoreo de Condición</option>

                            <option value="Análisis de Aceite / Fluidos">Análisis de Aceite / Fluidos</option>

                            <option value="Mantenimiento Hidráulico">Mantenimiento Hidráulico</option>

                            <option value="Inspección General">Inspección General</option>

                        </select>

                    </div>

                    <div>

                        <label class="block text-xs font-bold text-slate-700 mb-1">Nivel de Criticidad</label>

                        <select id="inputCriticidad" class="w-full p-2 border rounded-lg text-sm font-bold focus:ring-2 focus:ring-slate-800 focus:outline-none">

                            <option value="NORMAL" class="text-emerald-600 font-bold">🟢 Normal</option>

                            <option value="MEDIA" class="text-amber-600 font-bold">🟡 Advertencia</option>

                            <option value="ALTA" class="text-red-600 font-bold">🔴 Critica / Alarma</option>

                        </select>

                    </div>

                    <div>

                        <label class="block text-xs font-bold text-slate-700 mb-1">Inspector Responsable *</label>

                        <input type="text" id="inputInspector" required placeholder="Nombre del Técnico" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none">

                    </div>

                </div>



                <!-- Parameters Grid -->

                <div class="bg-slate-50 p-3 rounded-lg border">

                    <span class="text-xs font-bold text-slate-600 uppercase tracking-wider block mb-2">Mediciones y Parámetros Rápidos</span>

                    <div class="grid grid-cols-3 gap-3">

                        <div>

                            <label class="block text-[11px] text-slate-500">Temp. (°C)</label>

                            <input type="number" id="inputTemp" placeholder="65" class="w-full p-1.5 border rounded text-xs">

                        </div>

                        <div>

                            <label class="block text-[11px] text-slate-500">Presión (PSI)</label>

                            <input type="number" id="inputPresion" placeholder="1800" class="w-full p-1.5 border rounded text-xs">

                        </div>

                        <div>

                            <label class="block text-[11px] text-slate-500">Código ISO 4406</label>

                            <input type="text" id="inputISO" placeholder="18/16/13" class="w-full p-1.5 border rounded text-xs">

                        </div>

                    </div>

                </div>



                <div>

                    <label class="block text-xs font-bold text-slate-700 mb-1">Diagnóstico Técnico y Hallazgos *</label>

                    <textarea id="inputDiagnostico" rows="3" required placeholder="Describa el estado actual del equipo, nivel de contaminantes, ruidos anómalos o fugas detectadas..." class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none"></textarea>

                </div>



                <div>

                    <label class="block text-xs font-bold text-slate-700 mb-1">Recomendaciones y Acciones Correctivas</label>

                    <textarea id="inputRecomendaciones" rows="2" placeholder="Ej: Realizar cambio de elementos filtrantes en la próxima parada de mantenimiento..." class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-slate-800 focus:outline-none"></textarea>

                </div>



                <div class="flex justify-end space-x-3 pt-4 border-t">

                    <button type="button" onclick="closeReportModal()" class="px-4 py-2 border rounded-lg text-sm font-semibold text-slate-600 hover:bg-slate-100">

                        Cancelar

                    </button>

                    <button type="submit" class="px-5 py-2 bg-slate-900 text-white rounded-lg text-sm font-semibold hover:bg-black shadow flex items-center">

                        <i class="fa-solid fa-floppy-disk mr-2"></i> Guardar Reporte

                    </button>

                </div>

            </form>

        </div>

    </div>



    <!-- JavaScript Application Logic -->

    <script>

        let reports = [];



        const sampleReports = [

            {

                id: "FLT-2026-001",

                ot: "OT-88412",

                fecha: "2026-09-05 14:30",

                cliente: "Minera Pelambres",

                faena: "Planta Concentradora",

                tag: "BOMBA-HYD-04",

                tipo: "Monitoreo de Condición",

                criticidad: "ALTA",

                inspector: "Carlos Mendoza",

                temp: 78,

                presion: 2100,

                iso: "21/19/16",

                diagnostico: "Presencia de partículas metálicas en la muestra de drenaje. Elevada temperatura de funcionamiento en el bloque hidráulico principal.",

                recomendaciones: "Reemplazo inmediato de filtros de retorno y programación de diálisis de fluido lubricante dentro de 48 horas."

            },

            {

                id: "FLT-2026-002",

                ot: "OT-88413",

                fecha: "2026-09-06 09:15",

                cliente: "Atacama Minerals",

                faena: "Mina Subterránea",

                tag: "RED-PARAMAX-9000",

                tipo: "Análisis de Aceite / Fluidos",

                criticidad: "MEDIA",

                inspector: "Andrea Rojas",

                temp: 62,

                presion: 1450,

                iso: "18/16/13",

                diagnostico: "Viscosidad del aceite ligeramente fuera de rango óptimo por degradación térmica moderada.",

                recomendaciones: "Tomar nueva muestra de seguimiento en 15 días y verificar sellos de respiradero."

            },

            {

                id: "FLT-2026-003",

                ot: "OT-88414",

                fecha: "2026-09-06 11:00",

                cliente: "Candelaria",

                faena: "Área Chancado",

                tag: "CH-01-LUB-02",

                tipo: "Mantenimiento Hidráulico",

                criticidad: "NORMAL",

                inspector: "Carlos Mendoza",

                temp: 45,

                presion: 1200,

                iso: "15/13/10",

                diagnostico: "Inspección de rutina. Sistema hidráulico operando de manera limpia y silenciosa. Niveles dentro de norma ISO.",

                recomendaciones: "Continuar con plan estándar de lubricación preventiva."

            }

        ];



        window.addEventListener('DOMContentLoaded', () => {

            const saved = localStorage.getItem('fluitek_reports');

            if (saved) {

                try {

                    reports = JSON.parse(saved);

                } catch(e) {

                    reports = sampleReports;

                }

            } else {

                reports = sampleReports;

                saveToStorage();

            }

            renderReports();

        });



        function saveToStorage() {

            localStorage.setItem('fluitek_reports', JSON.stringify(reports));

        }



        function loadSampleData() {

            reports = [...sampleReports];

            saveToStorage();

            renderReports();

        }



        function renderReports() {

            const tbody = document.getElementById('reportsTableBody');

            const search = document.getElementById('searchInput').value.toLowerCase();

            const severity = document.getElementById('filterSeverity').value;

            const type = document.getElementById('filterType').value;



            tbody.innerHTML = '';



            let filtered = reports.filter(r => {

                const matchesSearch = r.cliente.toLowerCase().includes(search) || 

                                     r.tag.toLowerCase().includes(search) || 

                                     r.inspector.toLowerCase().includes(search) ||

                                     r.id.toLowerCase().includes(search) ||

                                     (r.ot && r.ot.toLowerCase().includes(search));

                const matchesSeverity = (severity === 'ALL') || (r.criticidad === severity);

                const matchesType = (type === 'ALL') || (r.tipo === type);

                return matchesSearch && matchesSeverity && matchesType;

            });



            document.getElementById('kpi-total').innerText = reports.length;

            document.getElementById('kpi-critical').innerText = reports.filter(r => r.criticidad === 'ALTA').length;

            document.getElementById('kpi-warning').innerText = reports.filter(r => r.criticidad === 'MEDIA').length;

            document.getElementById('kpi-normal').innerText = reports.filter(r => r.criticidad === 'NORMAL').length;



            if (filtered.length === 0) {

                document.getElementById('emptyState').classList.remove('hidden');

            } else {

                document.getElementById('emptyState').classList.add('hidden');

                

                filtered.forEach(r => {

                    const tr = document.createElement('tr');

                    tr.className = "hover:bg-slate-50 transition border-b";



                    let badgeClass = "bg-emerald-100 text-emerald-800 border-emerald-300";

                    let badgeIcon = "fa-circle-check";

                    if (r.criticidad === 'ALTA') {

                        badgeClass = "bg-red-100 text-red-800 border-red-300";

                        badgeIcon = "fa-triangle-exclamation";

                    } else if (r.criticidad === 'MEDIA') {

                        badgeClass = "bg-amber-100 text-amber-800 border-amber-300";

                        badgeIcon = "fa-circle-exclamation";

                    }



                    tr.innerHTML = `

                        <td class="p-4">

                            <span class="font-bold text-slate-900">${r.id}</span>

                            <div class="text-xs font-semibold text-amber-600"><i class="fa-solid fa-hashtag mr-0.5"></i>OT: ${r.ot || 'N/A'}</div>

                            <div class="text-xs text-slate-400">${r.fecha}</div>

                        </td>

                        <td class="p-4">

                            <div class="font-semibold text-slate-800">${r.cliente}</div>

                            <div class="text-xs text-slate-500">${r.faena}</div>

                        </td>

                        <td class="p-4">

                            <span class="font-mono bg-slate-100 px-2 py-1 rounded text-xs border font-semibold text-slate-700">${r.tag}</span>

                        </td>

                        <td class="p-4 text-xs font-medium text-slate-600">${r.tipo}</td>

                        <td class="p-4">

                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border ${badgeClass}">

                                <i class="fa-solid ${badgeIcon} mr-1.5 text-[10px]"></i> ${r.criticidad}

                            </span>

                        </td>

                        <td class="p-4 text-xs text-slate-600">${r.inspector}</td>

                        <td class="p-4 text-center">

                            <div class="flex items-center justify-center space-x-2">

                                <button onclick="previewReport('${r.id}')" title="Ver / Imprimir Informe" class="p-2 text-slate-800 hover:bg-slate-100 rounded-lg transition">

                                    <i class="fa-solid fa-file-pdf text-base"></i>

                                </button>

                                <button onclick="editReport('${r.id}')" title="Editar" class="p-2 text-slate-500 hover:bg-slate-100 rounded-lg transition">

                                    <i class="fa-solid fa-pen-to-square"></i>

                                </button>

                                <button onclick="deleteReport('${r.id}')" title="Eliminar" class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition">

                                    <i class="fa-solid fa-trash-can"></i>

                                </button>

                            </div>

                        </td>

                    `;

                    tbody.appendChild(tr);

                });

            }

        }



        function openNewReportModal() {

            document.getElementById('reportForm').reset();

            document.getElementById('reportId').value = '';

            document.getElementById('modalTitle').innerText = 'Nuevo Reporte - Orden de Trabajo';

            document.getElementById('reportModal').classList.remove('hidden');

        }



        function closeReportModal() {

            document.getElementById('reportModal').classList.add('hidden');

        }



        function saveReport(e) {

            e.preventDefault();

            const idInput = document.getElementById('reportId').value;

            const now = new Date();

            const dateStr = now.toISOString().slice(0, 10) + ' ' + now.toTimeString().slice(0, 5);



            const reportData = {

                ot: document.getElementById('inputOT').value,

                cliente: document.getElementById('inputCliente').value,

                faena: document.getElementById('inputFaena').value,

                tag: document.getElementById('inputTag').value,

                tipo: document.getElementById('inputTipo').value,

                criticidad: document.getElementById('inputCriticidad').value,

                inspector: document.getElementById('inputInspector').value,

                temp: document.getElementById('inputTemp').value || '-',

                presion: document.getElementById('inputPresion').value || '-',

                iso: document.getElementById('inputISO').value || '-',

                diagnostico: document.getElementById('inputDiagnostico').value,

                recomendaciones: document.getElementById('inputRecomendaciones').value || 'Sin recomendaciones.'

            };



            if (idInput) {

                const index = reports.findIndex(r => r.id === idInput);

                if (index !== -1) {

                    reports[index] = {

                        ...reports[index],

                        ...reportData

                    };

                }

            } else {

                const newFolioNumber = reports.length + 1;

                const newFolio = `FLT-2026-${Strin
