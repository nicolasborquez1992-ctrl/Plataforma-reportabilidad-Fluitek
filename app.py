import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página en Streamlit
st.set_page_config(
    page_title="Reliability & Condition Monitoring - Planta Concentradora",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Código HTML, CSS y JavaScript encapsulado para la plataforma de Monitoreo de Condiciones
monitoring_app_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Condition Monitoring - Planta Concentradora</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        plant: {
                            50: '#f8fafc',
                            100: '#f1f5f9',
                            500: '#0ea5e9',
                            600: '#0284c7',
                            700: '#0369a1',
                            800: '#075985',
                            900: '#0f172a',
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
        .plant-logo-badge {
            background-color: #0f172a;
            color: #38bdf8;
            font-weight: 800;
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
                <div class="plant-logo-badge text-lg px-3 py-1.5 rounded-lg shadow-md border border-slate-700 flex items-center">
                    <i class="fa-solid fa-industry mr-2 text-sky-400"></i> COND-MONITOR
                </div>
                <div>
                    <h1 class="text-base font-bold leading-tight text-white">Planta Concentradora - Confiabilidad y Activos</h1>
                    <p class="text-xs text-slate-400">Monitoreo de Condición, Vibraciones, Termografía e Informes Técnicos</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button onclick="openNewAssetModal()" class="bg-sky-500 hover:bg-sky-600 text-slate-950 font-bold px-4 py-2 rounded-lg text-sm transition flex items-center shadow">
                    <i class="fa-solid fa-circle-plus mr-2"></i> Registrar Activo / Hallazgo
                </button>
                <button onclick="exportDataCSV()" class="bg-slate-800 hover:bg-slate-700 text-white border border-slate-600 px-3 py-2 rounded-lg text-sm transition flex items-center">
                    <i class="fa-solid fa-file-excel mr-2"></i> Exportar CSV
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
                    <p class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Total Activos Monitoreados</p>
                    <h3 id="kpi-total" class="text-2xl font-bold text-slate-800">0</h3>
                </div>
                <div class="w-10 h-10 rounded-full bg-slate-100 text-slate-800 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-cubes"></i>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-4 border-l-4 border-red-500 flex justify-between items-center">
                <div>
                    <p class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Alarma Crítica (Falla Inminente)</p>
                    <h3 id="kpi-critical" class="text-2xl font-bold text-red-600">0</h3>
                </div>
                <div class="w-10 h-10 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-4 border-l-4 border-amber-500 flex justify-between items-center">
                <div>
                    <p class="text-xs uppercase tracking-wider text-slate-500 font-semibold">En Advertencia (Seguimiento)</p>
                    <h3 id="kpi-warning" class="text-2xl font-bold text-amber-600">0</h3>
                </div>
                <div class="w-10 h-10 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-circle-exclamation"></i>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm p-4 border-l-4 border-emerald-500 flex justify-between items-center">
                <div>
                    <p class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Operativo / Normal</p>
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
                    <input type="text" id="searchInput" oninput="renderAssets()" placeholder="Buscar por TAG, Nombre del Equipo, Área, Analista..." class="w-full pl-9 pr-4 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:outline-none">
                </div>
                <select id="filterStatus" onchange="renderAssets()" class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-sky-500 focus:outline-none">
                    <option value="ALL">Todas las Criticidades</option>
                    <option value="CRITICA">Alarma Crítica</option>
                    <option value="ADVERTENCIA">Advertencia</option>
                    <option value="NORMAL">Normal / Operativo</option>
                </select>
                <select id="filterArea" onchange="renderAssets()" class="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-sky-500 focus:outline-none">
                    <option value="ALL">Todas las Áreas</option>
                    <option value="Conminución (Molinos)">Conminución (Molinos)</option>
                    <option value="Flotación y Reactivos">Flotación y Reactivos</option>
                    <option value="Bombeo de Pulpa">Bombeo de Pulpa</option>
                    <option value="Correas Transportadoras">Correas Transportadoras</option>
                    <option value="Filtrado y Espesamiento">Filtrado y Espesamiento</option>
                </select>
            </div>
            <button onclick="loadSampleAssets()" class="text-xs text-slate-600 hover:text-black underline font-medium">
                <i class="fa-solid fa-rotate-left mr-1"></i> Cargar Datos Planta Base
            </button>
        </div>

        <!-- Assets Table View -->
        <div class="bg-white rounded-xl shadow-sm overflow-hidden no-print">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-50 text-slate-600 text-xs uppercase tracking-wider border-b">
                            <th class="p-4">TAG / Equipo</th>
                            <th class="p-4">Área Planta</th>
                            <th class="p-4">Variables Clave (Vibración / Temp)</th>
                            <th class="p-4">Estado de Salud</th>
                            <th class="p-4">Informe Técnico</th>
                            <th class="p-4 text-center">Acciones / Descarga</th>
                        </tr>
                    </thead>
                    <tbody id="assetsTableBody" class="divide-y text-sm">
                        <!-- Dynamic Rows -->
                    </tbody>
                </table>
            </div>
            <div id="emptyState" class="p-8 text-center text-slate-500 hidden">
                <i class="fa-solid fa-folder-open text-4xl mb-2 text-slate-300"></i>
                <p>No se encontraron activos con los filtros seleccionados.</p>
            </div>
        </div>

        <!-- Printable Official Technical Report View -->
        <div id="printPreviewContainer" class="hidden bg-white p-8 rounded-xl shadow-lg border my-6 print-card">
            <div class="flex justify-between items-start border-b pb-4 mb-6">
                <div>
                    <div class="plant-logo-badge text-xl px-4 py-1.5 rounded-lg tracking-wider shadow">
                        <i class="fa-solid fa-industry mr-2"></i> PLANTA CONCENTRADORA - INFORME TÉCNICO
                    </div>
                    <p class="text-xs text-slate-500 mt-2">Departamento de Confiabilidad y Monitoreo de Condiciones</p>
                </div>
                <div class="text-right">
                    <span id="previewTagCode" class="text-lg font-bold text-slate-800 font-mono">TAG: MOLINO-SAG-01</span>
                    <p id="previewFecha" class="text-xs text-slate-500">Fecha de Evaluación: 29/09/2026</p>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4 bg-slate-50 p-4 rounded-lg mb-6 border text-xs">
                <div>
                    <p><strong class="text-slate-700">Nombre del Equipo:</strong> <span id="previewNombre" class="font-bold text-sky-700">-</span></p>
                    <p><strong class="text-slate-700">Área Operativa:</strong> <span id="previewArea">-</span></p>
                    <p><strong class="text-slate-700">Criticidad Activo:</strong> <span id="previewCriticidadTxt" class="font-bold">-</span></p>
                </div>
                <div>
                    <p><strong class="text-slate-700">Vibración Global:</strong> <span id="previewVib" class="font-mono font-bold">-</span></p>
                    <p><strong class="text-slate-700">Temperatura Rodamiento:</strong> <span id="previewTemp" class="font-mono font-bold">-</span></p>
                    <p><strong class="text-slate-700">Analista Responsable:</strong> <span id="previewAnalista">-</span></p>
                </div>
            </div>

            <div class="mb-6">
                <h4 class="font-bold text-sm text-slate-800 mb-2 border-b pb-1">DIAGNÓSTICO TÉCNICO DE CONDICIÓN</h4>
                <p id="previewDiagnostico" class="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-slate-50 p-3 rounded border">
                    Sin observaciones registradas.
                </p>
            </div>

            <div class="mb-6">
                <h4 class="font-bold text-sm text-slate-800 mb-2 border-b pb-1">RECOMENDACIONES ESTRATÉGICAS / INTERVENCIÓN</h4>
                <p id="previewRecomendaciones" class="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-sky-50/50 p-3 rounded border border-sky-200">
                    Sin recomendaciones.
                </p>
            </div>

            <div class="mb-6">
                <h4 class="font-bold text-sm text-slate-800 mb-2 border-b pb-1">DOCUMENTO ADJUNTO ASOCIADO</h4>
                <div class="flex items-center justify-between bg-slate-50 p-3 rounded border text-xs">
                    <span id="previewDocName" class="font-mono text-slate-700"><i class="fa-solid fa-file-pdf text-red-500 mr-2"></i> Reporte_Vibraciones_Tecnico.pdf</span>
                    <button onclick="alert('Descargando informe técnico adjunto del activo...')" class="bg-slate-900 text-white px-3 py-1.5 rounded font-semibold hover:bg-black">
                        <i class="fa-solid fa-download mr-1"></i> Descargar PDF
                    </button>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-8 mt-12 pt-8 border-t text-center text-xs">
                <div>
                    <div class="border-b border-slate-400 mb-2 h-12 flex items-end justify-center pb-1 text-slate-600">Firma Analista de Condición</div>
                    <p class="font-bold" id="previewFirmaAnalista">Especialista Predictivo</p>
                    <p class="text-slate-500">Monitoreo de Condición</p>
                </div>
                <div>
                    <div class="border-b border-slate-400 mb-2 h-12 flex items-end justify-center pb-1 text-slate-600">Aprobación Confiabilidad</div>
                    <p class="font-bold">Jefatura de Mantenimiento</p>
                    <p class="text-slate-500">Planta Concentradora</p>
                </div>
            </div>

            <div class="mt-8 flex justify-end gap-3 no-print">
                <button onclick="closePreview()" class="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold hover:bg-slate-300">
                    Cerrar Vista Previa
                </button>
                <button onclick="window.print()" class="px-4 py-2 bg-sky-600 text-white rounded-lg text-xs font-semibold hover:bg-sky-700 flex items-center shadow">
                    <i class="fa-solid fa-print mr-2"></i> Imprimir / Guardar PDF Oficial
                </button>
            </div>
        </div>

    </main>

    <!-- Modal Form: Add / Edit Asset -->
    <div id="assetModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4 no-print">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
            <div class="bg-slate-900 text-white px-6 py-4 flex justify-between items-center sticky top-0 z-10 border-b border-slate-800">
                <h3 class="font-bold text-lg flex items-center">
                    <i class="fa-solid fa-microchip text-sky-400 mr-2"></i>
                    <span id="modalTitle">Registrar / Editar Activo y Condición</span>
                </h3>
                <button onclick="closeAssetModal()" class="text-slate-300 hover:text-white text-xl">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <form id="assetForm" onsubmit="saveAsset(event)" class="p-6 space-y-4">
                <input type="hidden" id="assetId">

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">TAG del Equipo *</label>
                        <input type="text" id="inputTag" required placeholder="Ej: MOL-SAG-01" class="w-full p-2 border rounded-lg text-sm font-mono font-bold text-sky-700 focus:ring-2 focus:ring-sky-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Nombre del Activo *</label>
                        <input type="text" id="inputNombre" required placeholder="Ej: Molino SAG Principal" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Área de la Planta *</label>
                        <select id="inputArea" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:outline-none">
                            <option value="Conminución (Molinos)">Conminución (Molinos)</option>
                            <option value="Flotación y Reactivos">Flotación y Reactivos</option>
                            <option value="Bombeo de Pulpa">Bombeo de Pulpa</option>
                            <option value="Correas Transportadoras">Correas Transportadoras</option>
                            <option value="Filtrado y Espesamiento">Filtrado y Espesamiento</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Vibración Global (mm/s RMS)</label>
                        <input type="text" id="inputVib" placeholder="Ej: 4.8 mm/s" class="w-full p-2 border rounded-lg text-sm font-mono focus:ring-2 focus:ring-sky-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Temperatura (°C)</label>
                        <input type="text" id="inputTemp" placeholder="Ej: 68 °C" class="w-full p-2 border rounded-lg text-sm font-mono focus:ring-2 focus:ring-sky-500 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Estado / Criticidad</label>
                        <select id="inputCriticidad" class="w-full p-2 border rounded-lg text-sm font-bold focus:ring-2 focus:ring-sky-500 focus:outline-none">
                            <option value="NORMAL" class="text-emerald-600">🟢 Normal / Operativo</option>
                            <option value="ADVERTENCIA" class="text-amber-600">🟡 Advertencia</option>
                            <option value="CRITICA" class="text-red-600">🔴 Alarma Crítica</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1">Analista a Cargo *</label>
                        <input type="text" id="inputAnalista" required placeholder="Tu Nombre / Analista" class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:outline-none">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1">Diagnóstico Técnico y Hallazgos (Espectro / Termografía / Aceite)</label>
                    <textarea id="inputDiagnostico" rows="3" required placeholder="Describa el comportamiento dinámico, armónicos detectados o anomalías térmicas..." class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:outline-none"></textarea>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1">Recomendaciones de Confiabilidad</label>
                    <textarea id="inputRecomendaciones" rows="2" placeholder="Ej: Programar inspección estroboscópica y revisar lubricación de bancada..." class="w-full p-2 border rounded-lg text-sm focus:ring-2 focus:ring-sky-500 focus:outline-none"></textarea>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-700 mb-1">Nombre del Archivo de Informe Técnico (PDF)</label>
                    <input type="text" id="inputDocName" placeholder="Ej: Informe_Vibraciones_SAG01.pdf" class="w-full p-2 border rounded-lg text-sm font-mono text-slate-600 focus:ring-2 focus:ring-sky-500 focus:outline-none">
                </div>

                <div class="flex justify-end space-x-3 pt-4 border-t">
                    <button type="button" onclick="closeAssetModal()" class="px-4 py-2 border rounded-lg text-sm font-semibold text-slate-600 hover:bg-slate-100">
                        Cancelar
                    </button>
                    <button type="submit" class="px-5 py-2 bg-sky-600 text-white rounded-lg text-sm font-semibold hover:bg-sky-700 shadow flex items-center">
                        <i class="fa-solid fa-floppy-disk mr-2"></i> Guardar Activo
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- JavaScript Logic -->
    <script>
        let assets = [];

        const sampleAssets = [
            {
                id: "AST-001",
                tag: "MOL-SAG-01",
                nombre: "Molino SAG Principal 38x22",
                area: "Conminución (Molinos)",
                vib: "7.4 mm/s RMS (Alta)",
                temp: "78 °C",
                criticidad: "CRITICA",
                analista: "Carlos Mendoza",
                diagnostico: "Elevación notable en componente de 1x RPM con modulación lateral en frecuencia de engranaje. Indicios claros de desgaste en descanso de muñón de descarga.",
                recomendaciones: "Programar inspección boroscópica inmediata y reducir tasa de alimentación en un 15% hasta próxima ventana de mantenimiento.",
                docName: "Informe_Termografia_MolinoSAG01.pdf",
                fecha: "2026-09-28 10:30"
            },
            {
                id: "AST-002",
                tag: "BOMB-PULP-04",
                nombre: "Bomba de Pulpa Concentrado Cu",
                area: "Bombeo de Pulpa",
                vib: "4.2 mm/s RMS",
                temp: "62 °C",
                criticidad: "ADVERTENCIA",
                analista: "Andrea Rojas",
                diagnostico: "Presencia de cavitación incipiente y desbalance leve en impulsor debido a abrasión en álabes.",
                recomendaciones: "Monitorear nivel de succión de cajón de carga y programar cambio de revestimiento interior en próxima detención corta.",
                docName: "Analisis_Aceite_Bomba04.pdf",
                fecha: "2026-09-29 08:15"
            },
            {
                id: "AST-003",
                tag: "CORR-PRIN-02",
                nombre: "Correa Transportadora de Gruesos",
                area: "Correas Transportadoras",
                vib: "1.8 mm/s RMS",
                temp: "41 °C",
                criticidad: "NORMAL",
                analista: "Carlos Mendoza",
                diagnostico: "Polines de carga operando bajo parámetros normales de temperatura y vibración. Alineación de banda correcta.",
                recomendaciones: "Continuar con plan estándar de lubricación y revisión visual semanal.",
                docName: "Inspeccion_Mecanica_Correa02.pdf",
                fecha: "2026-09-29 11:00"
            }
        ];

        window.addEventListener('DOMContentLoaded', () => {
            const saved = localStorage.getItem('plant_monitoring_assets');
            if (saved) {
                try {
                    assets = JSON.parse(saved);
                } catch(e) {
                    assets = sampleAssets;
                }
            } else {
                assets = sampleAssets;
                saveToStorage();
            }
            renderAssets();
        });

        function saveToStorage() {
            localStorage.setItem('plant_monitoring_assets', JSON.stringify(assets));
        }

        function loadSampleAssets() {
            assets = [...sampleAssets];
            saveToStorage();
            renderAssets();
        }

        function renderAssets() {
            const tbody = document.getElementById('assetsTableBody');
            const search = document.getElementById('searchInput').value.toLowerCase();
            const status = document.getElementById('filterStatus').value;
            const area = document.getElementById('filterArea').value;

            tbody.innerHTML = '';

            let filtered = assets.filter(a => {
                const matchesSearch = a.tag.toLowerCase().includes(search) || 
                                     a.nombre.toLowerCase().includes(search) || 
                                     a.analista.toLowerCase().includes(search) ||
                                     a.area.toLowerCase().includes(search);
                const matchesStatus = (status === 'ALL') || (a.criticidad === status);
                const matchesArea = (area === 'ALL') || (a.area === area);
                return matchesSearch && matchesStatus && matchesArea;
            });

            document.getElementById('kpi-total').innerText = assets.length;
            document.getElementById('kpi-critical').innerText = assets.filter(a => a.criticidad === 'CRITICA').length;
            document.getElementById('kpi-warning').innerText = assets.filter(a => a.criticidad === 'ADVERTENCIA').length;
            document.getElementById('kpi-normal').innerText = assets.filter(a => a.criticidad === 'NORMAL').length;

            if (filtered.length === 0) {
                document.getElementById('emptyState').classList.remove('hidden');
            } else {
                document.getElementById('emptyState').classList.add('hidden');
                
                filtered.forEach(a => {
                    const tr = document.createElement('tr');
                    tr.className = "hover:bg-slate-50 transition border-b";

                    let badgeClass = "bg-emerald-100 text-emerald-800 border-emerald-300";
                    let badgeIcon = "fa-circle-check";
                    let badgeText = "Normal";
                    if (a.criticidad === 'CRITICA') {
                        badgeClass = "bg-red-100 text-red-800 border-red-300";
                        badgeIcon = "fa-triangle-exclamation";
                        badgeText = "Alarma Crítica";
                    } else if (a.criticidad === 'ADVERTENCIA') {
                        badgeClass = "bg-amber-100 text-amber-800 border-amber-300";
                        badgeIcon = "fa-circle-exclamation";
                        badgeText = "Advertencia";
                    }

                    tr.innerHTML = `
                        <td class="p-4">
                            <span class="font-mono font-bold text-sky-700 bg-sky-50 px-2 py-1 rounded border border-sky-200">${a.tag}</span>
                            <div class="font-semibold text-slate-800 mt-1">${a.nombre}</div>
                        </td>
                        <td class="p-4 text-xs font-medium text-slate-600">${a.area}</td>
                        <td class="p-4 text-xs">
                            <div class="font-mono text-slate-700"><i class="fa-solid fa-wave-square text-sky-500 mr-1"></i> ${a.vib || 'N/A'}</div>
                            <div class="font-mono text-slate-700"><i class="fa-solid fa-temperature-half text-amber-500 mr-1"></i> ${a.temp || 'N/A'}</div>
                        </td>
                        <td class="p-4">
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border ${badgeClass}">
                                <i class="fa-solid ${badgeIcon} mr-1.5 text-[10px]"></i> ${badgeText}
                            </span>
                        </td>
                        <td class="p-4 text-xs">
                            <span class="font-mono text-slate-600 truncate block max-w-[180px]" title="${a.docName}"><i class="fa-solid fa-file-pdf text-red-500 mr-1"></i> ${a.docName || 'Sin informe'}</span>
                        </td>
                        <td class="p-4 text-center">
                            <div class="flex items-center justify-center space-x-1.5">
                                <button onclick="previewReport('${a.id}')" title="Ver e Imprimir Reporte Técnico" class="p-2 text-slate-800 hover:bg-slate-100 rounded-lg transition">
                                    <i class="fa-solid fa-file-pdf text-base"></i>
                                </button>
                                <button onclick="downloadFile('${a.docName}')" title="Descargar Informe Técnico PDF" class="p-2 text-sky-600 hover:bg-sky-50 rounded-lg transition">
                                    <i class="fa-solid fa-download text-base"></i>
                                </button>
                                <button onclick="editAsset('${a.id}')" title="Editar Activo" class="p-2 text-slate-500 hover:bg-slate-100 rounded-lg transition">
                                    <i class="fa-solid fa-pen-to-square"></i>
                                </button>
                                <button onclick="deleteAsset('${a.id}')" title="Eliminar" class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </div>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        }

        function openNewAssetModal() {
            document.getElementById('assetForm').reset();
            document.getElementById('assetId').value = '';
            document.getElementById('modalTitle').innerText = 'Registrar Nuevo Activo y Condición';
            document.getElementById('assetModal').classList.remove('hidden');
        }

        function closeAssetModal() {
            document.getElementById('assetModal').classList.add('hidden');
        }

        function saveAsset(e) {
            e.preventDefault();
            const idInput = document.getElementById('assetId').value;
            const now = new Date();
            const dateStr = now.toISOString().slice(0, 10) + ' ' + now.toTimeString().slice(0, 5);

            const assetData = {
                tag: document.getElementById('inputTag').value.toUpperCase(),
                nombre: document.getElementById('inputNombre').value,
                area: document.getElementById('inputArea').value,
                vib: document.getElementById('inputVib').value || 'N/A',
                temp: document.getElementById('inputTemp').value || 'N/A',
                criticidad: document.getElementById('inputCriticidad').value,
                analista: document.getElementById('inputAnalista').value,
                diagnostico: document.getElementById('inputDiagnostico').value,
                recomendaciones: document.getElementById('inputRecomendaciones').value || 'Sin recomendaciones.',
                docName: document.getElementById('inputDocName').value || 'Informe_Tecnico_Monitoreo.pdf',
                fecha: dateStr
            };

            if (idInput) {
                const index = assets.findIndex(a => a.id === idInput);
                if (index !== -1) {
                    assets[index] = {
                        ...assets[index],
                        ...assetData
                    };
                }
            } else {
                const newIdNumber = assets.length + 1;
                const newId = `AST-${String(newIdNumber).padStart(3, '0')}`;
                assets.unshift({
                    id: newId,
                    ...assetData
                });
            }

            saveToStorage();
            renderAssets();
            closeAssetModal();
        }

        function editAsset(id) {
            const a = assets.find(item => item.id === id);
            if (!a) return;

            document.getElementById('assetId').value = a.id;
            document.getElementById('inputTag').value = a.tag;
            document.getElementById('inputNombre').value = a.nombre;
            document.getElementById('inputArea').value = a.area;
            document.getElementById('inputVib').value = a.vib;
            document.getElementById('inputTemp').value = a.temp;
            document.getElementById('inputCriticidad').value = a.criticidad;
            document.getElementById('inputAnalista').value = a.analista;
            document.getElementById('inputDiagnostico').value = a.diagnostico;
            document.getElementById('inputRecomendaciones').value = a.recomendaciones;
            document.getElementById('inputDocName').value = a.docName;

            document.getElementById('modalTitle').innerText = `Editar Activo ${a.tag}`;
            document.getElementById('assetModal').classList.remove('hidden');
        }

        function deleteAsset(id) {
            if (confirm(`¿Está seguro de eliminar el activo ${id} del sistema?`)) {
                assets = assets.filter(a => a.id !== id);
                saveToStorage();
                renderAssets();
            }
        }

        function previewReport(id) {
            const a = assets.find(item => item.id === id);
            if (!a) return;

            document.getElementById('previewTagCode').innerText = `TAG: ${a.tag}`;
            document.getElementById('previewFecha').innerText = `Fecha de Evaluación: ${a.fecha}`;
            document.getElementById('previewNombre').innerText = a.nombre;
            document.getElementById('previewArea').innerText = a.area;
            document.getElementById('previewVib').innerText = a.vib;
            document.getElementById('previewTemp').innerText = a.temp;
            document.getElementById('previewAnalista').innerText = a.analista;
            document.getElementById('previewFirmaAnalista').innerText = a.analista;

            document.getElementById('previewDiagnostico').innerText = a.diagnostico;
            document.getElementById('previewRecomendaciones').innerText = a.recomendaciones;
            document.getElementById('previewDocName').innerHTML = `<i class="fa-solid fa-file-pdf text-red-500 mr-2"></i> ${a.docName || 'Informe_Tecnico.pdf'}`;

            const critTxt = document.getElementById('previewCriticidadTxt');
            critTxt.innerText = a.criticidad;
            if (a.criticidad === 'CRITICA') {
                critTxt.className = "font-bold text-red-600";
            } else if (a.criticidad === 'ADVERTENCIA') {
                critTxt.className = "font-bold text-amber-600";
            } else {
                critTxt.className = "font-bold text-emerald-600";
            }

            document.getElementById('printPreviewContainer').classList.remove('hidden');
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }

        function closePreview() {
            document.getElementById('printPreviewContainer').classList.add('hidden');
        }

        function downloadFile(filename) {
            alert(`Iniciando descarga segura del informe técnico: "${filename}". El archivo PDF se descargará a su equipo.`);
        }

        function exportDataCSV() {
            let csv = 'ID,TAG,Nombre,Area,Vibracion,Temperatura,Criticidad,Analista,Fecha\\n';
            assets.forEach(a => {
                csv += `"${a.id}","${a.tag}","${a.nombre}","${a.area}","${a.vib}","${a.temp}","${a.criticidad}","${a.analista}","${a.fecha}"\\n`;
            });
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", "monitoreo_condicion_activos_planta.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
"""

# Renderizar el componente web dentro de Streamlit ocupando el ancho completo
components.html(monitoring_app_html, height=850, scrolling=True)
