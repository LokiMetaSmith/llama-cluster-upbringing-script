document.addEventListener('DOMContentLoaded', async function () {
    const cy = cytoscape({
        container: document.getElementById('cy'),
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': '#666',
                    'label': 'data(id)',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'color': '#fff',
                    'text-outline-width': 2,
                    'text-outline-color': '#666'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            },
            {
                selector: '.executed',
                style: {
                    'background-color': '#28a745', // Green for executed nodes
                    'line-color': '#28a745',
                    'target-arrow-color': '#28a745',
                    'text-outline-color': '#28a745'
                }
            },
            {
                selector: '.gated',
                style: {
                    'background-color': '#ffc107', // Yellow for gated nodes
                    'border-color': '#ffc107',
                    'border-width': 2,
                    'border-style': 'solid',
                    'text-outline-color': '#ffc107'
                }
            },
            {
                selector: '.failed',
                style: {
                    'background-color': '#dc3545', // Red for failed nodes (if we can detect them)
                    'line-color': '#dc3545',
                    'target-arrow-color': '#dc3545',
                    'text-outline-color': '#dc3545'
                }
            }
        ],
        layout: {
            name: 'cose',
            idealEdgeLength: 100,
            nodeOverlap: 20,
            refresh: 20,
            fit: true,
            padding: 30,
            randomize: false,
            componentSpacing: 100,
            nodeRepulsion: 400000,
            edgeElasticity: 100,
            nestingFactor: 5,
            gravity: 80,
            numIter: 1000,
            initialTemp: 200,
            coolingFactor: 0.95,
            minTemp: 1.0
        }
    });

    const approvalContainer = document.getElementById('approval-container');
    const historyList = document.getElementById('history-list');
    const viewTitle = document.getElementById('view-title');
    const nodeModal = document.getElementById('nodeModal');
    const nodeOutputContent = document.getElementById('node-output-content');
    const closeModalSpan = document.getElementsByClassName("close")[0];

    let isLive = true;
    let pollingInterval = null;
    let currentWorkflowDefinition = null;
    let currentNodeOutputs = {};
    let lastExecutedNodeIdsSignature = "";

    // --- Workflow Loading and Rendering ---

    async function loadWorkflowDefinition(workflowName) {
        if (currentWorkflowDefinition && currentWorkflowDefinition.name === workflowName) {
            return; // Already loaded
        }

        try {
            // Assuming workflowName corresponds to a file in workflows/ dir, accessible via API
            // The API might expect just the filename.
            const response = await fetch(`/api/workflows/definition/${workflowName}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const workflow = await response.json();
            currentWorkflowDefinition = { name: workflowName, ...workflow };
            renderGraph(workflow);
        } catch (error) {
            console.error('Error loading workflow definition:', error);
            // Fallback to default if not found
             if (workflowName !== 'default_agent_loop.yaml') {
                 console.log("Falling back to default_agent_loop.yaml");
                 await loadWorkflowDefinition('default_agent_loop.yaml');
             }
        }
    }

    function renderGraph(workflow) {
        lastExecutedNodeIdsSignature = ""; // Reset optimization cache
        cy.elements().remove(); // Clear existing graph

        // Add nodes
        workflow.nodes.forEach(node => {
            cy.add({
                group: 'nodes',
                data: { id: node.id }
            });
        });

        // Add edges
        workflow.nodes.forEach(node => {
            if (node.inputs) {
                node.inputs.forEach(input => {
                    if (input.connection) {
                        cy.add({
                            group: 'edges',
                            data: {
                                id: `${input.connection.from_node}->${node.id}`,
                                source: input.connection.from_node,
                                target: node.id
                            }
                        });
                    }
                     // Handle nested inputs
                    if (input.value && typeof input.value === 'object') {
                        const findConnections = (obj, targetNodeId) => {
                            for (const key in obj) {
                                if (obj.hasOwnProperty(key)) {
                                    const value = obj[key];
                                    if (value && typeof value === 'object') {
                                        if (value.connection) {
                                            cy.add({
                                                group: 'edges',
                                                data: {
                                                    id: `${value.connection.from_node}->${targetNodeId}`,
                                                    source: value.connection.from_node,
                                                    target: targetNodeId
                                                }
                                            });
                                        }
                                        findConnections(value, targetNodeId);
                                    }
                                }
                            }
                        };
                        findConnections(input.value, node.id);
                    }
                });
            }
        });

        cy.layout({ name: 'cose' }).run();
    }

    function updateGraphState(nodeOutputs) {
        currentNodeOutputs = nodeOutputs;
        const executedNodeIds = Object.keys(nodeOutputs);

        // Bolt ⚡ Optimization: Memoize graph updates to prevent unnecessary re-renders
        const signature = JSON.stringify(executedNodeIds.sort());
        if (signature === lastExecutedNodeIdsSignature) {
            return;
        }
        lastExecutedNodeIdsSignature = signature;

        cy.nodes().removeClass('executed gated failed');

        executedNodeIds.forEach(nodeId => {
            cy.getElementById(nodeId).addClass('executed');
        });

        // Handling gate nodes or failures would go here if specific metadata is available
    }

    // --- Modal Logic ---

    let lastFocusedElement = null;

    function openModal() {
        lastFocusedElement = document.activeElement;
        nodeModal.style.display = "block";
        // Focus the close button for accessibility
        closeModalSpan.focus();
    }

    function closeModal() {
        nodeModal.style.display = "none";
        if (lastFocusedElement) {
            lastFocusedElement.focus();
        }
    }

    cy.on('tap', 'node', function(evt){
        const node = evt.target;
        const nodeId = node.id();
        const output = currentNodeOutputs[nodeId];

        if (output !== undefined) {
             nodeOutputContent.textContent = JSON.stringify(output, null, 2);
             openModal();
        }
    });

    closeModalSpan.onclick = closeModal;

    window.onclick = function(event) {
        if (event.target == nodeModal) {
             closeModal();
        }
    }

    // Palette UX: Trap focus inside modal
    nodeModal.addEventListener('keydown', function(e) {
        if (nodeModal.style.display !== 'block') return;

        if (e.key === 'Escape') {
            closeModal();
        } else if (e.key === 'Tab') {
            // Focusable elements inside modal: close button and pre content
            const focusableElements = nodeModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];

            if (e.shiftKey) { /* Shift + Tab */
                if (document.activeElement === firstElement) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else { /* Tab */
                if (document.activeElement === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        }
    });

    // Palette UX: Copy to Clipboard
    const copyBtn = document.getElementById('copy-node-output');
    if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
            const text = nodeOutputContent.textContent;
            try {
                await navigator.clipboard.writeText(text);

                // Visual Feedback
                const originalHTML = copyBtn.innerHTML;
                copyBtn.classList.add('success');
                // Checkmark icon
                copyBtn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
                copyBtn.setAttribute('aria-label', 'Copied!');

                setTimeout(() => {
                    copyBtn.classList.remove('success');
                    copyBtn.innerHTML = originalHTML;
                    copyBtn.setAttribute('aria-label', 'Copy output to clipboard');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy!', err);
            }
        });
    }

    // --- History Logic ---

    async function fetchHistory() {
        const btn = document.getElementById('refresh-history-btn');
        // Store original content to restore later (includes SVG)
        // If we haven't stored it yet, do so.
        if (!btn.dataset.originalContent) {
            btn.dataset.originalContent = btn.innerHTML;
        }

        try {
            btn.disabled = true;
            btn.classList.add('loading');
            btn.innerHTML = '<span class="spinner"></span> Refreshing...';

            // Palette UX: Show loading state in the list
            historyList.innerHTML = '<div class="empty-state">Loading history...</div>';

            const response = await fetch('/api/workflows/history?limit=50');
            if (response.ok) {
                const history = await response.json();
                renderHistoryList(history);
            } else {
                 // Palette UX: Handle server errors (e.g. 500)
                 historyList.innerHTML = '<div class="error-state">Failed to load history.</div>';
            }
        } catch (error) {
            console.error('Error fetching history:', error);
            // Palette UX: Show error state in the list
            historyList.innerHTML = '<div class="error-state">Connection failed. Please try again.</div>';
        } finally {
            btn.disabled = false;
            btn.classList.remove('loading');
            if (btn.dataset.originalContent) {
                btn.innerHTML = btn.dataset.originalContent;
            }
        }
    }

    function renderHistoryList(history) {
        historyList.innerHTML = '';

        // Palette UX: Empty State
        if (history.length === 0) {
            historyList.innerHTML = '<div class="empty-state">No workflow runs found.</div>';
            return;
        }

        history.forEach(run => {
            const li = document.createElement('li');
            li.className = 'history-item';
            li.dataset.runId = run.id; // Add data attribute for easier selection
            li.tabIndex = 0; // Accessibility
            li.setAttribute('role', 'option'); // Accessibility
            li.setAttribute('aria-selected', 'false'); // Accessibility

            const date = new Date(run.start_time * 1000).toLocaleString();
            li.innerHTML = `
                <div><strong>${run.workflow_name}</strong></div>
                <div class="history-meta">
                    ${date}<br>
                    Status: <span class="status-${run.status.toLowerCase()}">${run.status}</span>
                </div>
            `;

            const handleLoad = () => loadHistoricalRun(run.id);
            li.onclick = handleLoad;

            // Accessibility: Keyboard support
            li.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    handleLoad();
                }
            });

            historyList.appendChild(li);
        });
    }

    async function loadHistoricalRun(runId) {
        stopPolling();
        isLive = false;
        viewTitle.textContent = `Workflow Visualization (Run: ${runId})`;
        document.querySelectorAll('.history-item').forEach(el => {
            el.classList.remove('active');
            el.setAttribute('aria-selected', 'false'); // Accessibility
            if (el.dataset.runId === runId) {
                el.classList.add('active');
                el.setAttribute('aria-selected', 'true'); // Accessibility
            }
        });

        try {
            const response = await fetch(`/api/workflows/history/${runId}`);
            if (response.ok) {
                const runData = await response.json();
                // Ensure correct workflow definition is loaded
                await loadWorkflowDefinition(runData.workflow_name);

                // Extract node outputs from final_state
                const nodeOutputs = runData.final_state.node_outputs || {};
                updateGraphState(nodeOutputs);
            }
        } catch (error) {
            console.error('Error loading historical run:', error);
        }
    }

    // --- Live Mode Logic ---

    async function pollActiveWorkflows() {
        try {
            const activeResponse = await fetch('/api/workflows/active');
            const activeWorkflows = await activeResponse.json();
            const workflowIds = Object.keys(activeWorkflows);

            if (workflowIds.length > 0) {
                // Focus on the first active workflow
                const requestId = workflowIds[0];
                const activeState = activeWorkflows[requestId];

                // Assuming default workflow for active ones for now, or fetch if state has name
                // Ideally activeState should include workflow_name
                // For now, assume default_agent_loop.yaml if not specified
                await loadWorkflowDefinition('default_agent_loop.yaml');

                updateGraphState(activeState.node_outputs);

                // Check for gates
                const executedNodeIds = Object.keys(activeState.node_outputs);
                const lastNodeId = executedNodeIds[executedNodeIds.length - 1];
                // Simple heuristic: if last executed node is a GateNode, it might be waiting
                // Better would be to have explicit "status" in activeState
                 const lastNodeDef = currentWorkflowDefinition.nodes.find(n => n.id === lastNodeId);

                if (lastNodeDef && lastNodeDef.type === 'GateNode') {
                     cy.getElementById(lastNodeId).addClass('gated');
                     if (approvalContainer.innerHTML === '') {
                        // Palette UX: Enhanced Approve Button with Icon and Accessibility
                        approvalContainer.innerHTML = `
                            <button id="approve-btn" data-request-id="${requestId}" aria-label="Approve pending request ${requestId}">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 5px; vertical-align: text-bottom;">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                Approve
                            </button>`;

                        document.getElementById('approve-btn').addEventListener('click', async (e) => {
                            const btn = e.currentTarget;
                            const reqId = btn.dataset.requestId;

                            // Palette UX: Loading State
                            btn.disabled = true;
                            const originalContent = btn.innerHTML;
                            btn.innerHTML = '<span class="spinner" style="margin-right: 5px; border-color: currentColor; border-right-color: transparent;"></span> Approving...';

                            try {
                                await fetch('/api/gate/approve', {
                                    method: 'POST',
                                    headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify({ request_id: reqId })
                                });
                            } catch (error) {
                                console.error('Approval failed:', error);
                                btn.disabled = false;
                                btn.innerHTML = originalContent; // Revert on error
                                return;
                            }
                            approvalContainer.innerHTML = '';
                        });
                     }
                } else {
                    approvalContainer.innerHTML = '';
                }

            } else {
                 // No active workflow
                 // Optionally clear graph or show empty state
            }
        } catch (error) {
            console.error('Error polling active workflows:', error);
        }
    }

    function togglePolling() {
        if (pollingInterval) {
            stopPolling();
        } else {
            startPolling();
        }
    }

    function startPolling() {
        if (!pollingInterval) {
            pollingInterval = setInterval(pollActiveWorkflows, 2000);
            viewTitle.textContent = "Workflow Visualization (Live)";

            const btn = document.getElementById('live-btn');
            if (btn) {
                btn.textContent = "Stop Live View";
                btn.setAttribute('aria-pressed', 'true');
                btn.classList.remove('live-paused');
                btn.classList.add('live-active');
            }

            isLive = true;
            approvalContainer.innerHTML = '';
            // Load default immediately
            loadWorkflowDefinition('default_agent_loop.yaml');
        }
    }

    function stopPolling() {
        if (pollingInterval) {
            clearInterval(pollingInterval);
            pollingInterval = null;

            const btn = document.getElementById('live-btn');
            if (btn) {
                btn.textContent = "Resume Live View";
                btn.setAttribute('aria-pressed', 'false');
                btn.classList.remove('live-active');
                btn.classList.add('live-paused');
            }
        }
    }

    // --- Initialization ---

    document.getElementById('live-btn').addEventListener('click', togglePolling);
    document.getElementById('refresh-history-btn').addEventListener('click', fetchHistory);

    // Initial load
    await loadWorkflowDefinition('default_agent_loop.yaml');
    startPolling();
    fetchHistory();
});
