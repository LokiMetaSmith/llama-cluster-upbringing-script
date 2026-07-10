/**
 * ========================================================================
 *   COMMANDDECK FRONTEND SCRIPT — CODENAME: NERV
 *   Real-time system orchestration controller and sci-fi tactical clock
 * ========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    // Current log offset for API polling
    let logOffset = 0;
    let pollInterval = null;
    let isRunning = false;

    // --- DOM Elements ---
    const clockEl = document.getElementById('deck-clock');
    const dateEl = document.getElementById('deck-date');
    const sysStatusText = document.getElementById('system-status-text');
    const statusDot = document.querySelector('.system-status-indicator .pulsing-dot');

    const tabBtns = document.querySelectorAll('.tab-menu .tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    const nodeRoleSelect = document.getElementById('node-role');
    const controllerIpGroup = document.getElementById('controller-ip-group');
    const controllerIpInput = document.getElementById('controller-ip');
    const sshUserInput = document.getElementById('ssh-user');
    const ansibleTagsInput = document.getElementById('ansible-tags');

    const startBootstrapBtn = document.getElementById('start-bootstrap-btn');
    const runValidateBtn = document.getElementById('run-validate-btn');
    const runHealBtn = document.getElementById('run-heal-btn');
    const stopTaskBtn = document.getElementById('stop-task-btn');
    const exitDeckBtn = document.getElementById('exit-deck-btn');

    const terminalScreen = document.getElementById('terminal-screen');
    const activeTaskName = document.getElementById('active-task-name');
    const taskStatusBadge = document.getElementById('task-status-badge');
    const consoleHeader = document.getElementById('console-header');

    const edgeMidModelsList = document.getElementById('edge-mid-models-list');
    const coreModelsList = document.getElementById('core-models-list');
    const filterBtns = document.querySelectorAll('.model-filter-row .filter-btn');

    // --- 1. Real-Time Clock & Date ---
    function updateClock() {
        const now = new Date();
        const hrs = String(now.getHours()).padStart(2, '0');
        const mins = String(now.getMinutes()).padStart(2, '0');
        const secs = String(now.getSeconds()).padStart(2, '0');
        clockEl.textContent = `${hrs}:${mins}:${secs}`;

        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const date = String(now.getDate()).padStart(2, '0');
        dateEl.textContent = `${year}.${month}.${date}`;
    }
    setInterval(updateClock, 1000);
    updateClock();

    // --- 2. Inner Panel Tabs Switching ---
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetId).classList.add('active');
        });
    });

    // --- 3. Dynamic Node Role Inputs ---
    nodeRoleSelect.addEventListener('change', () => {
        if (nodeRoleSelect.value === 'worker') {
            controllerIpGroup.classList.remove('hidden');
        } else {
            controllerIpGroup.classList.add('hidden');
        }
    });

    // --- 4. Models Catalog Dynamic Rendering ---
    async function loadModels() {
        try {
            const response = await fetch('/api/models');
            if (!response.ok) throw new Error("API error");
            const data = await response.json();

            renderModelsList(edgeMidModelsList, data.edge_mid);
            renderModelsList(coreModelsList, data.core);
        } catch (e) {
            console.error("Failed to load models list:", e);
            edgeMidModelsList.innerHTML = `<div class="loading-placeholder error">Error loading models list.</div>`;
            coreModelsList.innerHTML = `<div class="loading-placeholder error">Error loading models list.</div>`;
        }
    }

    function renderModelsList(container, models) {
        container.innerHTML = '';
        if (models.length === 0) {
            container.innerHTML = `<div class="loading-placeholder">No models registered in this tier.</div>`;
            return;
        }

        models.forEach(model => {
            const card = document.createElement('div');
            card.className = 'model-card';

            const isHeavy = model.memory_mb >= 8192;
            const ramClass = isHeavy ? 'model-ram heavy-ram' : 'model-ram';
            const ramLabel = isHeavy ? 'CORE REQUIRED' : 'MID-TIER OK';

            card.innerHTML = `
                <div class="model-name" title="${model.name}">${model.name}</div>
                <div class="model-meta">
                    <span>CAT: ${model.category.toUpperCase()}</span>
                    <span class="${ramClass}">${model.memory_gb} GB VRAM [${ramLabel}]</span>
                </div>
                <button class="btn-deploy-model" data-category="${model.category}">
                    DEPLOY EXPERT (${model.category.toUpperCase()})
                </button>
            `;

            // Bind individual model button
            const deployBtn = card.querySelector('.btn-deploy-model');
            deployBtn.addEventListener('click', () => {
                triggerTask('deploy_model', { category: model.category }, `DEPLOY MODEL [${model.name}]`);
            });

            container.appendChild(card);
        });
    }

    // --- 5. Catalog Filters ---
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filterValue = btn.getAttribute('data-filter');
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const sections = document.querySelectorAll('.tier-section');
            sections.forEach(sec => {
                const tier = sec.getAttribute('data-tier');
                if (filterValue === 'all' || filterValue === tier) {
                    sec.classList.remove('hidden');
                } else {
                    sec.classList.add('hidden');
                }
            });
        });
    });

    // --- 6. API Task Run Gateway ---
    async function triggerTask(action, params = {}, displayName = '') {
        if (isRunning) return;

        writeToTerminal(`\n>>> INITIATING PROCESS: ${displayName || action.toUpperCase()}...\n`);

        try {
            const response = await fetch('/api/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action, params })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || "Execution failed");
            }

            // Reset log buffer offset & set status to active
            logOffset = 0;
            setSystemStatusActive(displayName || action.toUpperCase());
            startLogPolling();

        } catch (e) {
            writeToTerminal(`\n❌ ERROR STARTING TASK: ${e.message}\n`);
            setSystemStatusIdle();
        }
    }

    // --- 7. Real-Time Logs Polling ---
    function startLogPolling() {
        if (pollInterval) clearInterval(pollInterval);
        pollInterval = setInterval(pollLogsAndStatus, 500);
    }

    function stopLogPolling() {
        if (pollInterval) {
            clearInterval(pollInterval);
            pollInterval = null;
        }
    }

    async function pollLogsAndStatus() {
        try {
            // 1. Fetch incremental logs
            const logResponse = await fetch(`/api/logs?offset=${logOffset}`);
            if (logResponse.ok) {
                const logData = await logResponse.json();
                if (logData.lines && logData.lines.length > 0) {
                    logData.lines.forEach(line => writeToTerminal(line));
                    logOffset = logData.next_offset;
                }
            }

            // 2. Fetch process state
            const statusResponse = await fetch('/api/status');
            if (statusResponse.ok) {
                const statusData = await statusResponse.json();
                if (statusData.status !== 'running') {
                    // Task has completed
                    stopLogPolling();
                    setSystemStatusIdle(statusData.status, statusData.exit_code);

                    // Do a final logs fetch just to make sure we caught everything
                    const finalLogResponse = await fetch(`/api/logs?offset=${logOffset}`);
                    if (finalLogResponse.ok) {
                        const finalLogData = await finalLogResponse.json();
                        finalLogData.lines.forEach(line => writeToTerminal(line));
                    }
                }
            }
        } catch (e) {
            console.error("Error during log polling:", e);
        }
    }

    function writeToTerminal(text) {
        // Simple ANSI terminal clean handler (remove color markers if simple pre-wrap)
        // Basic clean for cleaner reading:
        let cleanText = text.replace(/\x1B\[[0-9;]*[a-zA-Z]/g, '');

        // Append text node
        const lineEl = document.createElement('span');
        lineEl.className = 'terminal-line';
        lineEl.textContent = cleanText;
        terminalScreen.appendChild(lineEl);

        // Scroll terminal to the bottom
        terminalScreen.scrollTop = terminalScreen.scrollHeight;
    }

    // --- 8. UI State Modifiers ---
    function setSystemStatusActive(taskName) {
        isRunning = true;
        sysStatusText.textContent = "ACTIVE OPERATION RUNNING";
        statusDot.className = 'pulsing-dot active-dot';

        activeTaskName.textContent = taskName;
        taskStatusBadge.textContent = "RUNNING";
        consoleHeader.className = 'panel-header alert-themed';

        // Disable execution actions
        startBootstrapBtn.disabled = true;
        runValidateBtn.disabled = true;
        runHealBtn.disabled = true;
        stopTaskBtn.classList.remove('hidden');

        document.querySelectorAll('.btn-deploy-model').forEach(b => b.disabled = true);
    }

    function setSystemStatusIdle(finalState = 'idle', exitCode = 0) {
        isRunning = false;

        if (finalState === 'finished') {
            sysStatusText.textContent = "SYSTEM NOMINAL";
            statusDot.className = 'pulsing-dot ok-dot';
            taskStatusBadge.textContent = "FINISHED";
            consoleHeader.className = 'panel-header';
            writeToTerminal(`\n[✓] TASK COMPLETED SUCCESSFULLY.\n`);
        } else if (finalState === 'error') {
            sysStatusText.textContent = "SYSTEM NOMINAL // PREVIOUS FAILURE";
            statusDot.className = 'pulsing-dot error-dot';
            taskStatusBadge.textContent = "FAILED";
            consoleHeader.className = 'panel-header alert-themed';
            writeToTerminal(`\n[✗] TASK TERMINATED WITH EXIT CODE: ${exitCode}\n`);
        } else {
            sysStatusText.textContent = "SYSTEM NOMINAL";
            statusDot.className = 'pulsing-dot ok-dot';
            taskStatusBadge.textContent = "CONSOLE IDLE";
            consoleHeader.className = 'panel-header';
        }

        activeTaskName.textContent = "NONE";
        startBootstrapBtn.disabled = false;
        runValidateBtn.disabled = false;
        runHealBtn.disabled = false;
        stopTaskBtn.classList.add('hidden');

        document.querySelectorAll('.btn-deploy-model').forEach(b => b.disabled = false);
    }

    // --- 9. Control Bindings ---
    startBootstrapBtn.addEventListener('click', () => {
        const role = nodeRoleSelect.value;
        const user = sshUserInput.value.trim() || 'pipecatapp';
        const controllerIp = controllerIpInput.value.trim();
        const tags = ansibleTagsInput.value.trim();

        if (role === 'worker' && !controllerIp) {
            writeToTerminal("\n[!] WORKER ROLE REQUIRES A VALID CONTROLLER IP ADDRESS. PROVISIONING HALTED.\n");
            return;
        }

        const params = { role, user, tags };
        if (role === 'worker') params.controller_ip = controllerIp;

        triggerTask('bootstrap', params, `BOOTSTRAP ROLE: ${role.toUpperCase()}`);
    });

    runValidateBtn.addEventListener('click', () => {
        triggerTask('validate', {}, 'CLUSTER VALIDATION');
    });

    runHealBtn.addEventListener('click', () => {
        triggerTask('heal', {}, 'CLUSTER SELF-HEALING');
    });

    stopTaskBtn.addEventListener('click', async () => {
        try {
            writeToTerminal("\n>>> SIGNAL SENT: TERMINATING CURRENT TASK...\n");
            const response = await fetch('/api/stop', { method: 'POST' });
            if (response.ok) {
                writeToTerminal("[!] Task stopped by user request.\n");
            }
        } catch (e) {
            writeToTerminal(`\nError stopping task: ${e.message}\n`);
        }
    });

    // --- 10. Switch to KDE Plasma Desktop (Exit Kiosk) ---
    exitDeckBtn.addEventListener('click', async () => {
        if (confirm("Are you sure you want to shut down CommandDeck and switch to the standard KDE Plasma Desktop?")) {
            // Apply visual fadeout effect to CRT screen
            document.body.style.transition = 'all 1s ease';
            document.body.style.opacity = '0';
            document.body.style.transform = 'scale(0.95)';

            writeToTerminal("\n>>> INITIATING DECK SHUTDOWN. SWAPPING compositors...\n");

            try {
                await fetch('/api/exit', { method: 'POST' });
            } catch (e) {
                console.error("Exit API request failed:", e);
                // Try immediate exit anyway
                window.close();
            }
        }
    });

    // --- 11. Initial On-Load Sequence ---
    loadModels();

    // Check initial status in case we page refreshed and something is running
    fetch('/api/status')
        .then(res => res.json())
        .then(statusData => {
            if (statusData.status === 'running') {
                setSystemStatusActive("RUNNING BACKGROUND TASK");
                startLogPolling();
            }
        })
        .catch(console.error);

    // --- 12. Dynamic Ouroboros Webring Resolution (Cross-Port) ---
    try {
        const host = window.location.hostname || '127.0.0.1';
        const base8000 = `http://${host}:8000`;
        const fromParam = encodeURIComponent(`http://${host}:8085/`);

        const prevBtn = document.getElementById('webring-prev-btn');
        const randomBtn = document.getElementById('webring-random-btn');
        const nextBtn = document.getElementById('webring-next-btn');

        if (prevBtn) prevBtn.href = `${base8000}/webring/prev?from=${fromParam}`;
        if (randomBtn) randomBtn.href = `${base8000}/webring/random`;
        if (nextBtn) nextBtn.href = `${base8000}/webring/next?from=${fromParam}`;
    } catch (e) {
        console.error("Error setting webring dynamic URLs:", e);
    }
});
