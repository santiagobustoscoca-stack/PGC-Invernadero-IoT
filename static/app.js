document.addEventListener('DOMContentLoaded', () => {
    const navButtons = document.querySelectorAll('.nav-btn');
    const viewTitle = document.getElementById('view-title');
    const kpiSection = document.getElementById('kpi-section');
    const reportContainer = document.getElementById('report-container');
    const configSection = document.getElementById('config-section');
    
    const urlInput = document.getElementById('pbi-url-input');
    const saveUrlBtn = document.getElementById('save-url-btn');
    const pbiIframe = document.getElementById('pbi-iframe');
    const placeholderMsg = document.getElementById('placeholder-msg');
    const fullscreenBtn = document.getElementById('fullscreen-btn');

    // Consumir la API de KPIs del backend de Flask
    fetch('/api/kpis')
        .then(response => response.json())
        .then(data => {
            if(!data.error) {
                document.getElementById('kpi-registros').textContent = data.registros_procesados;
                document.getElementById('kpi-eficiencia').textContent = data.eficiencia_operativa;
                document.getElementById('kpi-alertas').textContent = data.alertas_activas;
                document.getElementById('kpi-estado').textContent = data.estado_sistema;
            }
        })
        .catch(err => console.error("Error cargando KPIs:", err));

    // Cargar URL guardada
    const savedUrl = localStorage.getItem('pbi_embed_url');
    if (savedUrl) {
        urlInput.value = savedUrl;
        loadReport(savedUrl);
    }

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.export?.() || navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const view = btn.getAttribute('data-view');
            if (view === 'general') {
                viewTitle.textContent = 'Resumen General de Operaciones';
                kpiSection.classList.remove('hidden');
                reportContainer.classList.remove('hidden');
                configSection.classList.add('hidden');
            } else if (view === 'config') {
                viewTitle.textContent = 'Configuración de Origen de Datos';
                kpiSection.classList.add('hidden');
                reportContainer.classList.add('hidden');
                configSection.classList.remove('hidden');
            }
        });
    });

    saveUrlBtn.addEventListener('click', () => {
        const url = urlInput.value.trim();
        if (url) {
            localStorage.setItem('pbi_embed_url', url);
            loadReport(url);
            document.querySelector('[data-view="general"]').click();
        }
    });

    function loadReport(url) {
        pbiIframe.src = url;
        placeholderMsg.classList.add('hidden');
        pbiIframe.classList.remove('hidden');
    }

    fullscreenBtn.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            reportContainer.requestFullscreen().catch(err => console.error(err));
        } else {
            document.exitFullscreen();
        }
    });
});