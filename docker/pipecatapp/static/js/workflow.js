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
                    'line-color': '#28a745',
                    'target-arrow-color': '#28a745',
                    'color': '#fff'

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

    try {
        const response = await fetch('/api/workflows/definition/default_agent_loop.yaml');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const workflow = await response.json();

        // Add nodes to the graph
        workflow.nodes.forEach(node => {
            cy.add({
                group: 'nodes',
                data: { id: node.id }
            });
        });

        // Add edges based on connections
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

        // Start polling for active workflow state
        setInterval(async () => {
            try {
                const activeResponse = await fetch('/api/workflows/active');
                const activeWorkflows = await activeResponse.json();

                // For simplicity, we'll just look at the first active workflow
                const workflowIds = Object.keys(activeWorkflows);
                if (workflowIds.length > 0) {
                    const activeState = activeWorkflows[workflowIds[0]];
                    const executedNodeIds = Object.keys(activeState.node_outputs);

                    // Reset all nodes to default style
                    cy.nodes().removeClass('executed');

                    // Highlight executed nodes
                    executedNodeIds.forEach(nodeId => {
                        cy.getElementById(nodeId).addClass('executed');
                    });
                } else {
                    // No active workflows, reset all styles
                    cy.nodes().removeClass('executed');
                }
            } catch (error) {
                console.error('Error polling for active workflows:', error);
            }
        }, 2000); // Poll every 2 seconds

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
        console.error('Error fetching or rendering workflow:', error);
        document.getElementById('cy').textContent = 'Error loading workflow definition.';
    }
});
