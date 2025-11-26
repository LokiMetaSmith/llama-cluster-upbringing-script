document.addEventListener('DOMContentLoaded', async function () {
    const cy = cytoscape({
        container: document.getElementById('cy'),
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': '#666',
                    'label': 'data(id)'
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
                }
            },
            {
                selector: '.gated',
                style: {
                    'background-color': '#ffc107', // Yellow for gated nodes
                    'border-color': '#ffc107',
                    'border-width': 2,
                    'border-style': 'solid'
                }
            }
        ],
        layout: {
            name: 'cose',
            idealEdgeLength: 100,
            nodeOverlap: 20,
            fit: true,
            padding: 30,
        }
    });

    const approvalContainer = document.getElementById('approval-container');

    try {
        const response = await fetch('/api/workflows/definition/default_agent_loop.yaml');
        const workflow = await response.json();

        // Render graph... (omitted for brevity, same as before)
        // ...

        // Polling for active workflow state
        setInterval(async () => {
            const activeResponse = await fetch('/api/workflows/active');
            const activeWorkflows = await activeResponse.json();

            const workflowIds = Object.keys(activeWorkflows);
            if (workflowIds.length > 0) {
                const requestId = workflowIds[0];
                const activeState = activeWorkflows[requestId];
                const executedNodeIds = Object.keys(activeState.node_outputs);

                cy.nodes().removeClass('executed gated');

                executedNodeIds.forEach(nodeId => cy.getElementById(nodeId).addClass('executed'));

                // Check for a gated node
                const lastNodeId = executedNodeIds[executedNodeIds.length - 1];
                const lastNodeDef = workflow.nodes.find(n => n.id === lastNodeId);

                if (lastNodeDef && lastNodeDef.type === 'GateNode') {
                    cy.getElementById(lastNodeId).addClass('gated');
                    approvalContainer.innerHTML = `<button id="approve-btn" data-request-id="${requestId}">Approve</button>`;

                    document.getElementById('approve-btn').addEventListener('click', async (e) => {
                        const reqId = e.target.dataset.requestId;
                        await fetch('/api/gate/approve', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({ request_id: reqId })
                        });
                        approvalContainer.innerHTML = ''; // Clear button
                    });
                } else {
                    approvalContainer.innerHTML = '';
                }
            } else {
                cy.nodes().removeClass('executed gated');
                approvalContainer.innerHTML = '';
            }
        }, 2000);

    } catch (error) {
        console.error('Error:', error);
    }
});
