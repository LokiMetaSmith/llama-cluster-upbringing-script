// Editor logic using LiteGraph.js

const WorkflowEditor = {
    graph: null,
    canvas: null,
    nodeTypes: {},
    currentWorkflowName: 'default_agent_loop.yaml',

    // Dynamically derive the list of node types from nodeTypes object
    getRegisteredNodeTypes: function() {
        return Object.keys(this.nodeTypes).map(type => "agent/" + type);
    },

    init: function(containerId, options = {}) {
        this.options = options;
        this.graph = new LGraph();
        this.canvas = new LGraphCanvas(containerId, this.graph);
        this.canvas.allow_searchbox = true; // enable search box with double click

        // Register custom nodes
        this.registerNodeTypes();

        if (!options.skipResize) {
            // Adjust canvas on resize
            window.addEventListener("resize", () => {
                const parent = document.getElementById(containerId).parentNode;
                this.canvas.resize(parent.clientWidth, parent.clientHeight);
            });

            // Initial resize
            setTimeout(() => {
                 const parent = document.getElementById(containerId).parentNode;
                 this.canvas.resize(parent.clientWidth, parent.clientHeight);
            }, 100);
        }

        // Setup Drag and Drop
        this.setupDragAndDrop(containerId);
    },

    setupDragAndDrop: function(containerId) {
        const canvasElement = document.getElementById(containerId);

        canvasElement.addEventListener("dragover", (e) => {
            e.preventDefault();
        });

        canvasElement.addEventListener("drop", (e) => {
            e.preventDefault();
            const nodeType = e.dataTransfer.getData("nodeType");
            if (nodeType && this.nodeTypes[nodeType.replace("agent/", "")]) {
                const rect = canvasElement.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                // Convert screen coordinates to graph coordinates
                const pos = this.canvas.convertEventToCanvasOffset(e);

                const node = LiteGraph.createNode(nodeType);
                node.pos = [pos[0], pos[1]];
                this.graph.add(node);
            }
        });
    },

    registerNodeTypes: function() {
        // Generic function to create node classes based on our YAML types
        const createGenericNode = (type, title, inputs, outputs, properties) => {
            function GenericNode() {
                if (inputs) {
                    inputs.forEach(i => this.addInput(i.name, i.type));
                }
                if (outputs) {
                    outputs.forEach(o => this.addOutput(o.name, o.type));
                }
                if (properties) {
                    for (const [key, value] of Object.entries(properties)) {
                        this.addProperty(key, value);
                        // Add widgets for properties for easier editing
                        if (typeof value === 'boolean') {
                            this.addWidget("toggle", key, value, (v) => { this.properties[key] = v; });
                        } else {
                            this.addWidget("text", key, String(value), (v) => { this.properties[key] = v; });
                        }
                    }
                }
                this.size = this.computeSize();
                this.agentNodeType = type; // Store original type

                // Add a text widget to display output data if needed
                this.outputWidget = this.addWidget("text", "Output", "", null, { disabled: true });
                this.image = null; // Store image object for rendering
            }

            GenericNode.title = title;
            GenericNode.desc = type;

            // Custom serialize to ensure agentNodeType is preserved
            GenericNode.prototype.onSerialize = function(o) {
                o.agentNodeType = this.agentNodeType;
            };

            GenericNode.prototype.onConfigure = function(o) {
                this.agentNodeType = o.agentNodeType || type;
            };

            // Override onDrawForeground to render image
            GenericNode.prototype.onDrawForeground = function(ctx) {
                if (this.flags.collapsed) return;

                if (this.image) {
                    // Draw image scaled to fit node width, maintaining aspect ratio
                    const margin = 10;
                    const contentWidth = this.size[0] - margin * 2;
                    // Calculate height based on aspect ratio
                    const aspectRatio = this.image.height / this.image.width;
                    const contentHeight = contentWidth * aspectRatio;

                    // Center the image vertically in the available space below inputs/widgets?
                    // For simplicity, just draw it at the bottom of the node
                    // We might need to resize the node to fit it

                    const yOffset = this.size[1] - contentHeight - margin;

                    // Only draw if there is space, or if we resized the node
                    if (contentHeight > 0) {
                        ctx.drawImage(this.image, margin, yOffset > 40 ? yOffset : 40, contentWidth, contentHeight);
                    }
                }
            };

            // Allow setting status for visualization
            GenericNode.prototype.setExecutionStatus = function(status, outputData) {
                if (status === 'executed') {
                    this.boxcolor = "#28a745"; // Green
                } else if (status === 'failed') {
                    this.boxcolor = "#dc3545"; // Red
                } else {
                    this.boxcolor = "#666"; // Default
                }

                if (outputData) {
                    // Check for Image
                    let isImage = false;
                    let imageSrc = "";

                    if (typeof outputData === 'string') {
                         if (outputData.startsWith("data:image")) {
                             isImage = true;
                             imageSrc = outputData;
                         } else if (outputData.length > 500 && /^[A-Za-z0-9+/=]+$/.test(outputData)) {
                             // Assume raw base64 png if really long
                             isImage = true;
                             imageSrc = "data:image/png;base64," + outputData;
                         }
                    }

                    if (isImage) {
                        const img = new Image();
                        img.src = imageSrc;
                        img.onload = () => {
                            this.image = img;
                            // Resize node to fit image + standard height
                            const margin = 10;
                            const requiredWidth = 240; // min width
                            const aspectRatio = img.height / img.width;
                            const imageH = (requiredWidth - margin*2) * aspectRatio;

                            // Ensure node is at least large enough
                            if (this.size[0] < requiredWidth) this.size[0] = requiredWidth;
                            if (this.size[1] < imageH + 60) this.size[1] = imageH + 60; // 60 for header/widgets

                            this.setDirtyCanvas(true, true);
                        };

                        if (this.outputWidget) {
                            this.outputWidget.value = "[Image Data]";
                        }
                    } else {
                        // Standard Text Output
                        this.image = null;

                        // Update the widget or just properties
                        // Simplify object for display
                        let displayVal = "";
                        if (typeof outputData === 'object') {
                            displayVal = JSON.stringify(outputData).substring(0, 50) + "...";
                        } else {
                            displayVal = String(outputData);
                        }

                        if(this.outputWidget) {
                            this.outputWidget.value = displayVal;
                        }
                    }

                    this.properties._last_output = outputData; // Store full output
                }
            };

            LiteGraph.registerNodeType("agent/" + type, GenericNode);
            this.nodeTypes[type] = GenericNode;
        };

        // Define known node types from the backend
        createGenericNode("InputNode", "Input", [], [{name: "user_text", type: "string"}, {name: "tools_dict", type: "object"}, {name: "tool_result", type: "object"}, {name: "consul_http_addr", type: "string"}]);
        createGenericNode("ConsulServiceDiscoveryNode", "Service Discovery", [{name: "consul_http_addr", type: "string"}], [{name: "available_services", type: "object"}]);
        createGenericNode("SystemPromptNode", "System Prompt", [{name: "tools", type: "object"}, {name: "available_services", type: "object"}], [{name: "system_prompt", type: "string"}]);
        createGenericNode("ScreenshotNode", "Screenshot", [{name: "tools", type: "object"}], [{name: "screenshot_base64", type: "string"}]);
        createGenericNode("PromptBuilderNode", "Prompt Builder", [{name: "system_prompt", type: "string"}, {name: "user_text", type: "string"}, {name: "screenshot", type: "string"}, {name: "tool_result", type: "object"}], [{name: "messages", type: "array"}]);
        createGenericNode("SimpleLLMNode", "Simple LLM", [{name: "messages", type: "array"}, {name: "user_text", type: "string"}], [{name: "response", type: "string"}], {model_tier: "balanced", system_prompt: "You are a helpful assistant."});
        createGenericNode("VisionLLMNode", "Vision LLM", [{name: "messages", type: "array"}], [{name: "response_text", type: "string"}]);
        createGenericNode("ToolParserNode", "Tool Parser", [{name: "llm_response", type: "string"}], [{name: "tool_call_data", type: "object"}, {name: "final_response", type: "string"}]);
        createGenericNode("ConditionalBranchNode", "Branch", [{name: "input_value", type: "object"}], [{name: "output_true", type: "object"}, {name: "output_false", type: "object"}], {check_if_tool_is: ""});
        createGenericNode("GateNode", "Gate", [{name: "input_value", type: "object"}], [{name: "output", type: "object"}]);
        createGenericNode("ExpertRouterNode", "Expert Router", [{name: "expert_name", type: "string"}, {name: "query", type: "string"}], [{name: "expert_response", type: "string"}]);
        createGenericNode("ToolExecutorNode", "Tool Executor", [{name: "tool_call_data", type: "object"}], [{name: "tool_result", type: "object"}]);
        createGenericNode("MergeNode", "Merge", [{name: "in1", type: "object"}, {name: "in2", type: "object"}], [{name: "merged_output", type: "object"}]);
        createGenericNode("OutputNode", "Output", [{name: "final_output", type: "object"}], []);

    },

    importWorkflow: function(yamlData) {
        this.graph.clear();

        const nodesMap = {};
        const yamlNodes = yamlData.nodes;

        // 1. Create Nodes
        yamlNodes.forEach(n => {
            const nodeTypeString = "agent/" + n.type;
            const node = LiteGraph.createNode(nodeTypeString);

            if (!node) {
                console.error(`Unknown node type: ${n.type}`);
                return;
            }

            node.title = n.id; // Use ID as title for clarity
            node.properties.id = n.id; // Store ID in properties

            // Set properties from YAML
            if (n) {
                for (const key in n) {
                    if (key !== 'id' && key !== 'type' && key !== 'inputs' && key !== 'outputs') {
                        node.properties[key] = n[key];
                        // Update widgets if they exist
                        const widget = node.widgets?.find(w => w.name === key);
                        if (widget) {
                            widget.value = n[key];
                        }
                    }
                }
            }

            // Attempt to layout nodes roughly (Auto-layout would be better)
            // For now, place them randomly or in a grid
            node.pos = [Math.random() * 800 + 100, Math.random() * 600 + 100];

            this.graph.add(node);
            nodesMap[n.id] = node;
        });

        // 2. Connect Edges
        yamlNodes.forEach(n => {
            const sourceNode = nodesMap[n.id];
            if (!sourceNode) return;

            if (n.inputs) {
                n.inputs.forEach(inputDef => {
                    const inputName = inputDef.name;
                    const inputIndex = sourceNode.findInputSlot(inputName);

                    if (inputIndex === -1) {
                        console.warn(`Input slot '${inputName}' not found on node '${n.id}'`);
                        return;
                    }

                    // Handle connection object or nested value structure
                    let connections = [];

                    if (inputDef.connection) {
                        connections.push(inputDef.connection);
                    } else if (inputDef.value) {
                         // Traverse nested value to find connections (like OutputNode)
                         const findConnectionsRecursively = (obj) => {
                             if (obj && typeof obj === 'object') {
                                 if (obj.connection) {
                                     connections.push(obj.connection);
                                 } else {
                                     Object.values(obj).forEach(findConnectionsRecursively);
                                 }
                             }
                         };
                         findConnectionsRecursively(inputDef.value);
                    }

                    connections.forEach(conn => {
                        const targetNodeId = conn.from_node;
                        const targetOutputName = conn.from_output;

                        const targetNode = nodesMap[targetNodeId];
                        if (targetNode) {
                            const outputIndex = targetNode.findOutputSlot(targetOutputName);
                            if (outputIndex !== -1) {
                                targetNode.connect(outputIndex, sourceNode, inputIndex);
                            } else {
                                console.warn(`Output slot '${targetOutputName}' not found on node '${targetNodeId}'`);
                            }
                        }
                    });
                });
            }
        });

        // Simple auto-layout to untangle
        this.autoLayout();
    },

    autoLayout: function() {
        // A very basic layout algorithm
        const nodes = this.graph._nodes;
        const columns = {};

        // 1. Assign levels (topological sort approximation)
        const visited = new Set();
        const levelMap = {};

        const calcLevel = (node) => {
            if (visited.has(node.id)) return levelMap[node.id];
            visited.add(node.id);

            let maxParentLevel = -1;
            if (node.inputs) {
                for (let i = 0; i < node.inputs.length; i++) {
                    const linkId = node.inputs[i].link;
                    if (linkId !== null) {
                        const link = this.graph.links[linkId];
                        const parent = this.graph.getNodeById(link.origin_id);
                        if (parent) {
                            const parentLvl = calcLevel(parent);
                            if (parentLvl > maxParentLevel) maxParentLevel = parentLvl;
                        }
                    }
                }
            }
            const lvl = maxParentLevel + 1;
            levelMap[node.id] = lvl;
            return lvl;
        };

        nodes.forEach(n => calcLevel(n));

        // 2. Group by level
        nodes.forEach(n => {
            const lvl = levelMap[n.id] || 0;
            if (!columns[lvl]) columns[lvl] = [];
            columns[lvl].push(n);
        });

        // 3. Position
        const xSpacing = 250;
        const ySpacing = 150;

        Object.keys(columns).forEach(lvl => {
            const colNodes = columns[lvl];
            const startX = lvl * xSpacing + 100;
            let startY = 100;

            colNodes.forEach((node, idx) => {
                node.pos = [startX, startY + idx * ySpacing];
            });
        });

        this.graph.setDirtyCanvas(true, true);
    },

    exportWorkflow: function() {
        const nodes = this.graph._nodes;
        const yamlNodes = [];

        nodes.forEach(node => {
            const yamlNode = {
                id: node.title, // Assuming title is kept as ID
                type: node.agentNodeType.replace("agent/", "") // Strip prefix
            };

            // Properties
            for (const key in node.properties) {
                if (key !== 'id' && !key.startsWith('_')) { // Skip internal properties like _last_output
                    yamlNode[key] = node.properties[key];
                }
            }

            // Inputs
            if (node.inputs && node.inputs.length > 0) {
                yamlNode.inputs = [];
                node.inputs.forEach((input, index) => {
                    const linkId = input.link;
                    if (linkId !== null) {
                        const link = this.graph.links[linkId];
                        const originNode = this.graph.getNodeById(link.origin_id);

                        // Find the output name on the origin node
                        const originOutputName = originNode.outputs[link.origin_slot].name;

                        const inputDef = {
                            name: input.name,
                            connection: {
                                from_node: originNode.title, // ID
                                from_output: originOutputName
                            }
                        };
                        yamlNode.inputs.push(inputDef);
                    }
                });

                // Cleanup empty inputs array
                if (yamlNode.inputs.length === 0) delete yamlNode.inputs;
            }

            yamlNodes.push(yamlNode);
        });

        return { nodes: yamlNodes };
    },

    updateLiveStatus: function(activeState) {
       this.visualizeRun({ final_state: activeState });
    },

    visualizeRun: function(runData) {
        if (!runData || !runData.final_state) return;
        const context = runData.final_state;
        const nodeOutputs = context.node_outputs || {};

        // Reset all nodes first
        this.graph._nodes.forEach(n => n.setExecutionStatus('default'));

        // Loop through all nodes in the graph
        this.graph._nodes.forEach(node => {
            const nodeId = node.title; // Using title as ID per import logic
            if (nodeOutputs[nodeId]) {
                node.setExecutionStatus('executed', nodeOutputs[nodeId]);
            }
        });

        this.graph.setDirtyCanvas(true, true);
    },

    saveWorkflow: async function() {
        const workflowData = this.exportWorkflow();
        try {
            const response = await fetch('/api/workflows/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: this.currentWorkflowName,
                    definition: workflowData
                })
            });
            const res = await response.json();

            if (this.options && this.options.onStatusUpdate) {
                this.options.onStatusUpdate(res.message, 'success');
            } else {
                alert(res.message);
            }
        } catch (error) {
            console.error("Save failed", error);
            if (this.options && this.options.onStatusUpdate) {
                this.options.onStatusUpdate("Save failed: " + error, 'error');
            } else {
                alert("Save failed: " + error);
            }
        }
    }
};

window.WorkflowEditor = WorkflowEditor;
