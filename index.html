<!DOCTYPE html>
<html lang="es" class="h-full bg-slate-950 text-slate-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APEX CBM Enterprise - Monitoreo de Condiciones</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- ECharts CDN para Gráficos Corporativos -->
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: { 50: '#f0f9ff', 500: '#0ea5e9', 600: '#0284c7', 900: '#0c4a6e' },
                        status: { ok: '#10b981', warn: '#f59e0b', danger: '#ef4444' }
                    }
                }
            }
        }
    </script>
</head>
<body class="h-full flex overflow-hidden font-sans antialiased selection:bg-brand-500 selection:text-white">

    <!-- SIDEBAR CORPORATIVO -->
    <aside class="w-72 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0">
        <div>
            <!-- Branding / Logo Area -->
            <div class="h-16 flex items-center px-6 border-b border-slate-800 gap-3">
                <div class="p-2 bg-brand-500/10 rounded-lg border border-brand-500/20 text-brand-500">
                    <i data-lucide="activity" class="w-6 h-6"></i>
                </div>
                <div>
                    <h1 class="font-bold text-base tracking-wide text-white">APEX <span class="text-brand-500">CBM</span></h1>
                    <p class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Reliability Suite v4.2</p>
                </div>
            </div>

            <!-- Navegación Principal -->
            <nav class="p-4 space-y-1">
                <div class="px-3 py-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">Monitoreo & Control</div>
                
                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-brand-500/10 text-brand-500 font-medium border border-brand-500/20 transition-all">
                    <i data-lucide="layout-dashboard" class="w-5 h-5"></i>
                    <span>Dashboard Operacional</span>
                </a>
                
                <a href="#" class="flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 font-medium transition-all group">
                    <div class="flex items-center gap-3">
                        <i data-lucide="waves" class="w-5 h-5 text-slate-500 group-hover:text-brand-500"></i>
                        <span>Análisis de Vibraciones</span>
                    </div>
                    <span class="text-xs bg-slate-800 px-2 py-0.5 rounded text-slate-400 border border-slate-700">ISO</span>
                </a>

                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 font-medium transition-all group">
                    <i data-lucide="thermometer" class="w-5 h-5 text-slate-500 group-hover:text-brand-500"></i>
                    <span>Termografía (Delta T)</span>
                </a>

                <a href="#" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 font-medium transition-all group">
                    <i data-lucide="droplet" class="w-5 h-5 text-slate-500 group-hover:text-brand-500"></i>
                    <span>Tribología & Aceites</span>
                </a>

                <div class="pt-4 px-3 py-2 text-[11px] font-bold text-slate-500 uppercase tracking-wider">Gestión & Avisos</div>

                <a href="#" class="flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 font-medium transition-all group">
                    <div class="flex items-center gap-3">
                        <i data-lucide="grid" class="w-5 h-5 text-slate-500 group-hover:text-brand-500"></i>
                        <span>Matriz de Criticidad</span>
                    </div>
                    <span class="w-2 h-2 rounded-full bg-status-danger"></span>
                </a>

                <a href="#" class="flex items-center justify-between px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 font-medium transition-all group">
                    <div class="flex items-center gap-3">
                        <i data-lucide="bell" class="w-5 h-5 text-slate-500 group-hover:text-brand-500"></i>
                        <span>Backlog de Avisos</span>
                    </div>
                    <span class="px-2 py-0.5 text-xs rounded-full bg-red-500/10 text-red-400 border border-red-500/20 font-bold">4 Críticos</span>
                </a>
            </nav>
        </div>

        <!-- Perfil Usuario / Planta -->
        <div class="p-4 border-t border-slate-800 bg-slate-900/50">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-sm text-brand-500">
                    NB
                </div>
                <div class="overflow-hidden">
                    <p class="text-xs font-semibold text-white truncate">Ing. Confiabilidad</p>
                    <p class="text-[11px] text-slate-400 truncate">Planta Concentradora</p>
                </div>
            </div>
        </div>
    </aside>

    <!-- ÁREA PRINCIPAL -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
        
        <!-- HEADER TOP BAR -->
        <header class="h-16 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 flex items-center justify-between px-8 z-10">
            <div class="flex items-center gap-4">
                <div class="flex items-center gap-2 text-xs text-slate-400">
                    <span>Planta Concentradora</span>
                    <i data-lucide="chevron-right" class="w-4 h-4"></i>
                    <span class="text-white font-medium">Área Molienda & Chancado</span>
                </div>
            </div>

            <!-- Acciones y Filtros Globales -->
            <div class="flex items-center gap-4">
                <div class="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800 text-xs">
                    <span class="w-2 h-2 rounded-full bg-status-ok animate-pulse"></span>
                    <span class="text-slate-300 font-mono">SCADA: ONLINE</span>
                </div>
                <button class="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-brand-600/20 flex items-center gap-2 transition-all">
                    <i data-lucide="file-down" class="w-4 h-4"></i>
                    <span>Exportar Reporte Ejecutivo</span>
                </button>
            </div>
        </header>

        <!-- CONTENIDO PRINCIPAL -->
        <main class="flex-1 overflow-y-auto p-8 space-y-6 bg-slate-950">
            
            <!-- TARJETAS DE KPIS PRINCIPALES -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
                    <div class="flex items-center justify-between text-slate-400">
                        <span class="text-xs font-semibold uppercase tracking-wider">Salud Global Planta</span>
                        <i data-lucide="shield-check" class="w-5 h-5 text-status-ok"></i>
                    </div>
                    <div class="flex items-baseline gap-2">
                        <span class="text-3xl font-extrabold text-white">91.4%</span>
                        <span class="text-xs font-bold text-status-ok flex items-center">+1.2%</span>
                    </div>
                    <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-status-ok h-full rounded-full" style="width: 91.4%"></div>
                    </div>
                </div>

                <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
                    <div class="flex items-center justify-between text-slate-400">
                        <span class="text-xs font-semibold uppercase tracking-wider">Equipos en Peligro</span>
                        <i data-lucide="alert-triangle" class="w-5 h-5 text-status-danger"></i>
                    </div>
                    <div class="flex items-baseline gap-2">
                        <span class="text-3xl font-extrabold text-white">3</span>
                        <span class="text-xs text-slate-400">de 42 activos</span>
                    </div>
                    <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-status-danger h-full rounded-full" style="width: 12%"></div>
                    </div>
                </div>

                <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
                    <div class="flex items-center justify-between text-slate-400">
                        <span class="text-xs font-semibold uppercase tracking-wider">Avisos Pendientes</span>
                        <i data-lucide="clock" class="w-5 h-5 text-status-warn"></i>
                    </div>
                    <div class="flex items-baseline gap-2">
                        <span class="text-3xl font-extrabold text-white">14</span>
                        <span class="text-xs text-status-warn font-semibold">8 Aprobados</span>
                    </div>
                    <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-status-warn h-full rounded-full" style="width: 45%"></div>
                    </div>
                </div>

                <div class="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-2">
                    <div class="flex items-center justify-between text-slate-400">
                        <span class="text-xs font-semibold uppercase tracking-wider">Cumplimiento CBM</span>
                        <i data-lucide="check-circle-2" class="w-5 h-5 text-brand-500"></i>
                    </div>
                    <div class="flex items-baseline gap-2">
                        <span class="text-3xl font-extrabold text-white">98.5%</span>
                        <span class="text-xs text-slate-400">Rondas al día</span>
                    </div>
                    <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div class="bg-brand-500 h-full rounded-full" style="width: 98.5%"></div>
                    </div>
                </div>
            </div>

            <!-- SECCIÓN CENTRAL DE GRÁFICOS INTERACTIVOS -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                <!-- MAPA DE CALOR OPERACIONAL -->
                <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="font-bold text-slate-100">Matriz de Salud Operacional (Heatmap)</h3>
                            <p class="text-xs text-slate-400">Estado técnico de activos cruzado por disciplina CBM</p>
                        </div>
                        <span class="text-xs font-semibold bg-slate-800 text-slate-300 px-3 py-1 rounded-lg border border-slate-700">
                            En Tiempo Real
                        </span>
                    </div>
                    <div id="heatmapChart" class="w-full h-80 flex-1"></div>
                </div>

                <!-- GAUGE ISO VIBRACIONES DE ACTIVO CRÍTICO -->
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-brand-500 uppercase">Activo Bajo Análisis</span>
                            <span class="text-xs px-2 py-0.5 bg-red-500/10 text-red-400 rounded border border-red-500/20 font-bold">ALTA CRITICIDAD</span>
                        </div>
                        <h3 class="font-bold text-lg text-white">Molino SAG 01 (MOL-001)</h3>
                        <p class="text-xs text-slate-400">Vibración Global RMS vs Norma ISO 10816</p>
                    </div>

                    <div id="gaugeChart" class="w-full h-56"></div>

                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800/80 flex items-center justify-between text-xs">
                        <span class="text-slate-400">Diagnóstico:</span>
                        <span class="font-bold text-status-danger">Transición a Zona D (Desbalance)</span>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <!-- SCRIPT DE CONFIGURACIÓN DE GRÁFICOS (ECHARTS) -->
    <script>
        lucide.createIcons();

        // 1. Gráfico Heatmap (Matriz de Salud)
        const heatmapDom = document.getElementById('heatmapChart');
        const heatmapChart = echarts.init(heatmapDom, 'dark');
        
        const hours = ['Molino SAG', 'Molino Bolas 1', 'Chancador Prim.', 'Bomba Slurry A', 'Bomba Slurry B'];
        const days = ['Vibraciones', 'Termografía', 'Tribología (Aceites)'];

        const data = [
            [0,0,3], [1,0,1], [2,0,2], [3,0,1], [4,0,2],
            [0,1,1], [1,1,2], [2,1,3], [3,1,1], [4,1,1],
            [0,2,2], [1,2,1], [2,2,1], [3,2,3], [4,2,1]
        ];

        const optionHeatmap = {
            backgroundColor: 'transparent',
            tooltip: { position: 'top' },
            grid: { top: '10%', bottom: '15%', left: '15%', right: '5%' },
            xAxis: { type: 'category', data: hours, splitArea: { show: true }, axisLabel: { color: '#94a3b8' } },
            yAxis: { type: 'category', data: days, splitArea: { show: true }, axisLabel: { color: '#94a3b8' } },
            visualMap: {
                min: 1, max: 3,
                calculable: false, orient: 'horizontal', left: 'center', bottom: '0%',
                inRange: { color: ['#10b981', '#f59e0b', '#ef4444'] },
                text: ['Crítico', 'Normal'], textStyle: { color: '#94a3b8' }
            },
            series: [{
                name: 'Estado CBM', type: 'heatmap', data: data,
                label: { show: true, formatter: (p) => p.data[2] === 3 ? 'CRÍTICO' : (p.data[2] === 2 ? 'ALERTA' : 'OK') },
                itemStyle: { borderRadius: 4, borderWidth: 2, borderColor: '#0f172a' }
            }]
        };
        heatmapChart.setOption(optionHeatmap);

        // 2. Gráfico Gauge ISO 10816
        const gaugeDom = document.getElementById('gaugeChart');
        const gaugeChart = echarts.init(gaugeDom, 'dark');

        const optionGauge = {
            backgroundColor: 'transparent',
            series: [{
                type: 'gauge',
                startAngle: 180, endAngle: 0,
                min: 0, max: 10,
                pointer: { icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z', width: 6, length: '60%', offsetCenter: [0, '8%'], itemStyle: { color: '#ffffff' } },
                axisLine: {
                    lineStyle: {
                        width: 18,
                        color: [[0.28, '#10b981'], [0.45, '#f59e0b'], [0.71, '#f97316'], [1, '#ef4444']]
                    }
                },
                axisTick: { distance: -18, length: 6, lineStyle: { color: '#0f172a', width: 2 } },
                splitLine: { distance: -18, length: 18, lineStyle: { color: '#0f172a', width: 3 } },
                axisLabel: { color: '#94a3b8', distance: -35, fontSize: 10 },
                detail: { valueAnimation: true, formatter: '{value} mm/s', color: '#ffffff', fontSize: 20, offsetCenter: [0, '35%'] },
                data: [{ value: 7.8 }]
            }]
        };
        gaugeChart.setOption(optionGauge);

        window.addEventListener('resize', () => {
            heatmapChart.resize();
            gaugeChart.resize();
        });
    </script>
</body>
</html>
