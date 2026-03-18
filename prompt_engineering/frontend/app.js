// Frontend logic for Campaign Analysis UI

// Helper: Determine node color based on fitness score
function getColorForFitness(fitness) {
    if (fitness >= 0.9) return "#a1d99b"; // Light Green
    if (fitness >= 0.5) return "#fee08b"; // Light Yellow
    return "#fc8d59";                     // Light Red
}

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("graph-container");
    const detailsPanel = document.getElementById("node-details");

    // Fetch the evolutionary tree data from the API
    fetch("/api/tree")
        .then(response => response.json())
        .then(data => {
            if (data.nodes.length === 0) {
                container.innerHTML = "<p>Archive is empty. No evolutionary tree to display.</p>";
                return;
            }

            // Process node colors
            data.nodes.forEach(node => {
                node.color = {
                    background: getColorForFitness(node.fitness),
                    border: "#333",
                    highlight: { background: "#fff", border: "#000" }
                };
                node.shape = "box";
                node.font = { multi: "html" }; // Allow basic formatting in labels
            });

            // Create vis.js Dataset
            const nodesDataset = new vis.DataSet(data.nodes);
            const edgesDataset = new vis.DataSet(data.edges);

            // Network Configuration
            const options = {
                layout: {
                    hierarchical: {
                        direction: "UD", // Top to Bottom
                        sortMethod: "directed",
                        levelSeparation: 150,
                        nodeSpacing: 200
                    }
                },
                physics: false, // Hierarchical layout usually turns this off anyway
                edges: {
                    arrows: "to",
                    color: "#666",
                    smooth: {
                        type: "cubicBezier",
                        forceDirection: "vertical",
                        roundness: 0.4
                    }
                },
                interaction: {
                    hover: true
                }
            };

            const networkData = { nodes: nodesDataset, edges: edgesDataset };
            const network = new vis.Network(container, networkData, options);

            // Expose network to global for testing
            window.__NETWORK__ = network;

            // Handle Node Click to Display Details
            network.on("selectNode", function (params) {
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    const nodeData = nodesDataset.get(nodeId);

                    renderNodeDetails(nodeData);
                }
            });

            // Handle Deselect to clear details
            network.on("deselectNode", function () {
                detailsPanel.innerHTML = "<p>Select a node to view its details.</p>";
            });

        })
        .catch(err => {
            console.error("Error fetching tree data:", err);
            container.innerHTML = "<p>Error loading tree data. Is the server running?</p>";
        });

    function renderNodeDetails(node) {
        // Sanitize code blocks for HTML display
        let safeCode = escapeHtml(node.code || "No code available.");

        detailsPanel.innerHTML = `
            <div class="detail-item">
                <span class="detail-label">ID:</span>
                <span class="detail-value">${node.id}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Fitness:</span>
                <span class="detail-value">${node.fitness.toFixed(4)}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Rationale:</span>
                <div class="detail-box">${escapeHtml(node.rationale || "N/A")}</div>
            </div>
            <div class="detail-item">
                <span class="detail-label">Code:</span>
                <pre><code class="language-python">${safeCode}</code></pre>
            </div>
        `;

        // Re-run highlighting for the newly inserted block
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }

    function escapeHtml(unsafe) {
        return (unsafe || "")
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
});
