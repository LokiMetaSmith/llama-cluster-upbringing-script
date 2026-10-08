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

    _validationTimeout: null,
    validateGraph: function() {
        if (this._validationTimeout) clearTimeout(this._validationTimeout);
        this._validationTimeout = setTimeout(() => {
            this._runValidation();
        }, 500);
    },

    _runValidation: function() {
        if (!this.graph) return;
        const nodes = this.graph._nodes;
        let errors = [];
        let warnings = [];

        if (!nodes || nodes.length === 0) {
            this.showStatus("Empty canvas", "info");
            return;
        }

        nodes.forEach(node => {
            // 1. Check if node is missing required inputs
            if (node.inputs) {
                node.inputs.forEach(input => {
                    if (input.link === null || input.link === undefined) {
                        warnings.push(`'${node.title}' is missing input connection: '${input.name}'`);
                    }
                });
            }

            // 2. Check if properties are empty
            if (node.properties) {
                for (const [key, val] of Object.entries(node.properties)) {
                    if (val === "" || val === null || val === undefined) {
                        if (key !== '_last_output' && key !== 'id') {
                            warnings.push(`Node '${node.title}' has empty property: '${key}'`);
                        }
                    }
                }
            }
        });

        const statusEl = document.getElementById('status-text');
        if (!statusEl) return;

        if (errors.length > 0) {
            statusEl.textContent = "✗ Error: " + errors[0];
            statusEl.className = "status-error";
            statusEl.style.color = "#dc3545";
        } else if (warnings.length > 0) {
            statusEl.textContent = "⚠ Warning: " + warnings[0];
            statusEl.className = "status-info";
            statusEl.style.color = "#ff9900";
        } else {
            statusEl.textContent = "✓ Graph Valid";
            statusEl.className = "status-success";
            statusEl.style.color = "#28a745";
        }
    },

    showStatus: function(msg, type) {
        if (this.options && this.options.onStatusUpdate) {
            this.options.onStatusUpdate(msg, type);
        } else {
            const statusEl = document.getElementById('status-text');
            if (statusEl) {
                statusEl.textContent = msg;
                statusEl.className = "status-" + type;
            }
        }
    },

    init: async function(containerId, options = {}) {
        this.options = options;
        this.graph = new LGraph();
        const canvasElement = typeof containerId === "string"
            ? (document.getElementById(containerId) || document.querySelector(containerId) || document.querySelector("#" + containerId))
            : containerId;
        this.canvas = new LGraphCanvas(canvasElement, this.graph);
        this.canvas.allow_searchbox = true; // enable search box with double click

        // Register custom nodes
        await this.registerNodeTypes();

        // Strict Visual Edge Validation
        const originalIsValidConnection = LiteGraph.isValidConnection;
        LiteGraph.isValidConnection = function(type_a, type_b) {
            // Treat empty/wildcard types safely but enforce strict checks on known types
            const a = type_a === 0 ? "0" : String(type_a || "").toLowerCase();
            const b = type_b === 0 ? "0" : String(type_b || "").toLowerCase();

            const strictTypes = ["string", "object", "array", "dict"];

            // If both are strict types and they don't match, reject
            if (strictTypes.includes(a) && strictTypes.includes(b) && a !== b) {
                // Allow some specific exceptions if needed (e.g. object and dict could be considered same)
                if ((a === "object" && b === "dict") || (a === "dict" && b === "object")) {
                    // fall through to original
                } else {
                    return false;
                }
            }

            // Wildcards (0, "", "*", null) are generic and should be allowed to connect to any strict type.
            // Do not block connections involving wildcards.
            return originalIsValidConnection.apply(this, arguments);
        };

        if (!options.skipResize) {
            // Adjust canvas on resize
            window.addEventListener("resize", () => {
                if (canvasElement && canvasElement.parentNode && this.canvas) {
                    const parent = canvasElement.parentNode;
                    this.canvas.resize(parent.clientWidth, parent.clientHeight);
                }
            });

            // Initial resize
            setTimeout(() => {
                 if (canvasElement && canvasElement.parentNode && this.canvas) {
                     const parent = canvasElement.parentNode;
                     this.canvas.resize(parent.clientWidth, parent.clientHeight);
                 }
            }, 100);
        }

        // Setup validation triggers on graph changes
        this.graph.onNodeAdded = () => { this.validateGraph(); };
        this.graph.onNodeRemoved = () => { this.validateGraph(); };
        this.graph.onConnectionChange = () => { this.validateGraph(); };

        // Setup Drag and Drop
        this.setupDragAndDrop(canvasElement || containerId);
    },

    setupDragAndDrop: function(containerId) {
        const canvasElement = typeof containerId === "string"
            ? (document.getElementById(containerId) || document.querySelector(containerId) || document.querySelector("#" + containerId))
            : containerId;
        if (!canvasElement) return;

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

    registerNodeTypes: async function() {
        // Fetch node metadata and dynamic schemas from backend
        let backendMetadata = [];
        let backendSchemas = {};
        try {
            const headers = {};
            const apiKey = localStorage.getItem('api_key');
            if (apiKey) headers["Authorization"] = `Bearer ${apiKey}`;

            const response = await fetch('/api/workflows/node_schemas', { headers });
            if (response.ok) {
                const data = await response.json();
                if (data) {
                    backendMetadata = data.nodes || [];
                    backendSchemas = data.schemas || {};
                }
            } else {
                // Fallback to legacy metadata endpoint
                const legacyResp = await fetch('/api/workflows/nodes/metadata', { headers });
                if (legacyResp.ok) {
                    const legacyData = await legacyResp.json();
                    backendMetadata = legacyData.nodes || legacyData || [];
                }
            }
        } catch (error) {
            console.error("Error fetching node metadata/schemas:", error);
        }

        // Generic function to create node classes based on our YAML types
        const createGenericNode = (type, title, inputs, outputs, properties, desc) => {
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
                            this.addWidget("toggle", key, value, (v) => {
                                this.properties[key] = v;
                                WorkflowEditor.validateGraph();
                            });
                        } else {
                            this.addWidget("text", key, String(value), (v) => {
                                this.properties[key] = v;
                                WorkflowEditor.validateGraph();
                            });
                        }
                    }
                }
                this.size = this.computeSize();
                this.agentNodeType = type; // Store original type

                // Add a text widget to display output data if needed
                this.outputWidget = this.addWidget("text", "Output", "", (v) => {}, { disabled: true });
                this.image = null; // Store image object for rendering
            }

            GenericNode.title = title;
            GenericNode.desc = desc || type;

            // Custom serialize to ensure agentNodeType is preserved
            GenericNode.prototype.onSerialize = function(o) {
                o.agentNodeType = this.agentNodeType;
            };
            GenericNode.prototype.onConfigure = function(o) {
                this.agentNodeType = o.agentNodeType || type;
            };

            // NodeInputHandler - Manages incoming edges and input UI
            GenericNode.prototype.NodeInputHandler = {
                getPosition: function(slot_index) {
                    const y = 10 + (slot_index * LiteGraph.NODE_SLOT_HEIGHT);
                    return [0, y];
                },

                updateInternals: function() {
                    // Recalculate input anchor positions after config changes
                    if (this.inputs) {
                        this.setDirtyCanvas(true, true);
                    }
                },

                onConnect: function(slot_index, connected) {
                    // Handle input connection changes
                    this.setDirtyCanvas(true, true);
                }
            };

            // NodeOutputHandler - Manages outgoing edges and output UI
            GenericNode.prototype.NodeOutputHandler = {
                getPosition: function(slot_index) {
                    const inputsHeight = (this.inputs ? this.inputs.length : 0) * LiteGraph.NODE_SLOT_HEIGHT;
                    const widgetsHeight = this._getWidgetsHeight ? this._getWidgetsHeight() : 0;
                    const y = inputsHeight + widgetsHeight + 10 + (slot_index * LiteGraph.NODE_SLOT_HEIGHT);
                    return [this.size[0], y];
                },

                updateInternals: function() {
                    // Recalculate output anchor positions after config changes
                    if (this.outputs) {
                        this.setDirtyCanvas(true, true);
                    }
                },

                onConnect: function(slot_index, connected) {
                    // Handle output connection changes
                    this.setDirtyCanvas(true, true);
                }
            };

            // Helper to get widgets height
            GenericNode.prototype._getWidgetsHeight = function() {
                if (!this.widgets || !this.widgets.length) return 0;
                let widgetsHeight = 0;
                for (let i = 0; i < this.widgets.length; ++i) {
                    if (this.widgets[i].computeSize) {
                        widgetsHeight += this.widgets[i].computeSize(this.size[0])[1] + 4;
                    } else {
                        widgetsHeight += LiteGraph.NODE_WIDGET_HEIGHT + 4;
                    }
                }
                return widgetsHeight + 8;
            };

            // Exposed method to update node internals (like Flowise's useUpdateNodeInternals)
            GenericNode.prototype.updateNodeInternals = function() {
                this.NodeInputHandler.updateInternals.call(this);
                this.NodeOutputHandler.updateInternals.call(this);
                // Recompute size after config changes
                if (this.computeSize) {
                    const newSize = this.computeSize();
                    this.setSize(newSize);
                }
                this.setDirtyCanvas(true, true);
            };

            GenericNode.prototype.computeSize = function(out) {
                out = out || new Float32Array([0, 0]);
                // Call original first to get base width
                let size = LGraphNode.prototype.computeSize.call(this, out);

                const inputsHeight = (this.inputs ? this.inputs.length : 0) * LiteGraph.NODE_SLOT_HEIGHT;

                let widgetsHeight = 0;
                if (this.widgets && this.widgets.length) {
                    for (let i = 0; i < this.widgets.length; ++i) {
                        if (this.widgets[i].computeSize) {
                            widgetsHeight += this.widgets[i].computeSize(size[0])[1] + 4;
                        } else {
                            widgetsHeight += LiteGraph.NODE_WIDGET_HEIGHT + 4;
                        }
                    }
                    widgetsHeight += 8;
                }

                const outputsHeight = (this.outputs ? this.outputs.length : 0) * LiteGraph.NODE_SLOT_HEIGHT;

                // Inputs at top, then widgets, then outputs
                this.widgets_start_y = inputsHeight > 0 ? inputsHeight + 10 : 10;

                size[1] = this.widgets_start_y + widgetsHeight + outputsHeight + 10;

                if (this.image) {
                    const margin = 10;
                    const requiredWidth = 240;
                    const aspectRatio = this.image.height / this.image.width;
                    const imageH = (Math.max(size[0], requiredWidth) - margin*2) * aspectRatio;
                    size[1] += imageH + margin;
                }

                return size;
            };

            GenericNode.prototype.getConnectionPos = function(is_input, slot_number, out) {
                out = out || new Float32Array(2);
                const offset = LiteGraph.NODE_SLOT_HEIGHT * 0.5;

                if (this.flags.collapsed) {
                    return LiteGraph.LGraphNode.prototype.getConnectionPos.call(this, is_input, slot_number, out);
                }

                if (is_input) {
                    // Use NodeInputHandler for input positions
                    const inputPos = this.NodeInputHandler.getPosition(slot_number);
                    out[0] = this.pos[0] + offset + inputPos[0];
                    out[1] = this.pos[1] + offset + inputPos[1];
                } else {
                    // Use NodeOutputHandler for output positions
                    const outputPos = this.NodeOutputHandler.getPosition.call(this, slot_number);
                    out[0] = this.pos[0] + offset + outputPos[0] - this.size[0] + this.size[0] + 1 - offset * 2;
                    out[1] = this.pos[1] + offset + outputPos[1] - 10 + (this.constructor.slot_start_y || 0);
                }
                return out;
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

        // 1. Standard node specifications
        const standardNodes = {
            "InputNode": {
                title: "Input",
                inputs: [],
                outputs: [
                    {name: "user_text", type: "string"},
                    {name: "tools_dict", type: "object"},
                    {name: "tool_result", type: "object"},
                    {name: "consul_http_addr", type: "string"}
                ],
                properties: {},
                desc: "Initial inputs for the workflow."
            },
            "ConsulServiceDiscoveryNode": {
                title: "Service Discovery",
                inputs: [{name: "consul_http_addr", type: "string"}],
                outputs: [{name: "available_services", type: "object"}],
                properties: {},
                desc: "Discovers available services from Consul."
            },
            "SystemPromptNode": {
                title: "System Prompt",
                inputs: [
                    {name: "tools", type: "object"},
                    {name: "available_services", type: "object"},
                    {name: "custom_prompt", type: "string"}
                ],
                outputs: [{name: "system_prompt", type: "string"}],
                properties: {},
                desc: "Constructs the system prompt with tool definitions."
            },
            "ScreenshotNode": {
                title: "Screenshot",
                inputs: [{name: "tools", type: "object"}],
                outputs: [{name: "screenshot_base64", type: "string"}],
                properties: {},
                desc: "Captures desktop screenshot."
            },
            "PromptBuilderNode": {
                title: "Prompt Builder",
                inputs: [
                    {name: "system_prompt", type: "string"},
                    {name: "user_text", type: "string"},
                    {name: "screenshot", type: "string"},
                    {name: "tool_result", type: "object"}
                ],
                outputs: [{name: "messages", type: "array"}],
                properties: {},
                desc: "Builds messages array for LLM."
            },
            "SimpleLLMNode": {
                title: "Simple LLM",
                inputs: [
                    {name: "messages", type: "array"},
                    {name: "user_text", type: "string"},
                    {name: "system_prompt", type: "string"},
                    {name: "tool_result", type: "object"}
                ],
                outputs: [{name: "response", type: "string"}],
                properties: {model_tier: "balanced", system_prompt: "You are a helpful assistant."},
                desc: "Executes LLM inference."
            },
            "VisionLLMNode": {
                title: "Vision LLM",
                inputs: [{name: "messages", type: "array"}],
                outputs: [{name: "response_text", type: "string"}],
                properties: {},
                desc: "Vision-capable LLM inference."
            },
            "ToolParserNode": {
                title: "Tool Parser",
                inputs: [{name: "llm_response", type: "string"}],
                outputs: [
                    {name: "tool_call_data", type: "object"},
                    {name: "final_response", type: "string"}
                ],
                properties: {},
                desc: "Parses model output to determine tool call or response."
            },
            "ConditionalBranchNode": {
                title: "Branch",
                inputs: [{name: "input_value", type: "object"}],
                outputs: [
                    {name: "output_true", type: "object"},
                    {name: "output_false", type: "object"}
                ],
                properties: {check_if_tool_is: ""},
                desc: "Conditional branch based on predicate."
            },
            "GateNode": {
                title: "Gate",
                inputs: [{name: "input_value", type: "object"}],
                outputs: [{name: "output", type: "object"}],
                properties: {},
                desc: "Pause/approval gate."
            },
            "ExpertRouterNode": {
                title: "Expert Router",
                inputs: [
                    {name: "expert_name", type: "string"},
                    {name: "query", type: "string"}
                ],
                outputs: [{name: "expert_response", type: "string"}],
                properties: {},
                desc: "Routes task to specialized experts."
            },
            "ToolExecutorNode": {
                title: "Tool Executor",
                inputs: [
                    {name: "tool_call_data", type: "object"},
                    {name: "tools_dict", type: "object"}
                ],
                outputs: [{name: "tool_result", type: "object"}],
                properties: {},
                desc: "Executes tool calls and returns results."
            },
            "MergeNode": {
                title: "Merge",
                inputs: [
                    {name: "in1", type: "object"},
                    {name: "in2", type: "object"}
                ],
                outputs: [{name: "merged_output", type: "object"}],
                properties: {},
                desc: "Merges multiple upstream paths."
            },
            "OutputNode": {
                title: "Output",
                inputs: [
                    {name: "final_response", type: "string"},
                    {name: "tool_call", type: "object"},
                    {name: "tool_result", type: "object"},
                    {name: "final_output", type: "object"}
                ],
                outputs: [],
                properties: {},
                desc: "Collects output of workflow."
            },
            "PostProcessorNode": {
                title: "Post Processor",
                inputs: [
                    {name: "data", type: "object"},
                    {name: "expression", type: "string"}
                ],
                outputs: [{name: "processed_data", type: "object"}],
                properties: {expression: "data"},
                desc: "Processes data using expressions."
            }
        };

        // Register standard nodes
        for (const [nodeType, def] of Object.entries(standardNodes)) {
            createGenericNode(nodeType, def.title, def.inputs, def.outputs, def.properties, def.desc);
        }

        // Register additional dynamic nodes from backend
        if (backendMetadata && backendMetadata.length > 0) {
            backendMetadata.forEach(meta => {
                if (!standardNodes[meta.name]) {
                    createGenericNode(
                        meta.name,
                        meta.name.replace(/Node$/, '').replace(/([A-Z])/g, ' $1').trim(),
                        meta.inputs || [],
                        meta.outputs || [],
                        meta.properties || {},
                        meta.description
                    );
                }
            });
        }

    },

    importWorkflow: function(yamlData) {
        if (!yamlData) {
            console.warn("importWorkflow called with empty data");
            return;
        }
        this.graph.clear();

        const nodesMap = {};
        const yamlNodes = Array.isArray(yamlData.nodes) ? yamlData.nodes : [];

        // 1. Create Nodes
        yamlNodes.forEach(n => {
            if (n.type === "scope" || n.type === "group") {
                const group = new LiteGraph.LGraphGroup();
                group.title = n.id || n.name || "Group";

                if (n.position) {
                    group.pos = [n.position.x || 0, n.position.y || 0];
                } else {
                    group.pos = [Math.random() * 800 + 100, Math.random() * 600 + 100];
                }

                if (n.dimensions) {
                    group.size = [n.dimensions.width || 400, n.dimensions.height || 200];
                }

                if (n.style && n.style.color) {
                    group.color = n.style.color;
                }

                this.graph.add(group);
                return;
            }

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

            if (n.position) {
                node.pos = [n.position.x || 0, n.position.y || 0];
            } else {
                // Attempt to layout nodes roughly (Auto-layout would be better)
                // For now, place them randomly or in a grid
                node.pos = [Math.random() * 800 + 100, Math.random() * 600 + 100];
            }

            if (n.dimensions) {
                node.size = [n.dimensions.width || LiteGraph.NODE_WIDTH, n.dimensions.height || LiteGraph.NODE_SLOT_HEIGHT];
            }

            if (n.style && n.style.color) {
                node.color = n.style.color;
            }

            this.graph.add(node);
            nodesMap[n.id] = node;
        });

        // 2. Connect Edges
        yamlNodes.forEach(n => {
            const destNode = nodesMap[n.id];
            if (!destNode) return;

            if (n.inputs) {
                n.inputs.forEach(inputDef => {
                    const inputName = inputDef.name;
                    let inputIndex = destNode.findInputSlot(inputName);

                    if (inputIndex === -1) {
                        destNode.addInput(inputName, "any");
                        inputIndex = destNode.findInputSlot(inputName);
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
                        const fromNodeId = conn.from_node;
                        const fromOutputName = conn.from_output;

                        const fromNode = nodesMap[fromNodeId];
                        if (fromNode) {
                            let outputIndex = fromNode.findOutputSlot(fromOutputName);
                            if (outputIndex === -1) {
                                fromNode.addOutput(fromOutputName, "any");
                                outputIndex = fromNode.findOutputSlot(fromOutputName);
                            }
                            if (outputIndex !== -1 && inputIndex !== -1) {
                                fromNode.connect(outputIndex, destNode, inputIndex);
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
        if (typeof dagre === 'undefined') {
            console.warn("dagre.js not found. Using simple fallback layout.");
            this.fallbackAutoLayout();
            return;
        }

        const g = new dagre.graphlib.Graph();
        g.setGraph({
            rankdir: 'LR',
            nodesep: 50,
            edgesep: 10,
            ranksep: 100,
        });
        g.setDefaultEdgeLabel(function() { return {}; });

        const nodes = this.graph._nodes;

        nodes.forEach(n => {
            g.setNode(n.id, { width: n.size[0], height: n.size[1] });
        });

        nodes.forEach(n => {
            if (n.inputs) {
                for (let i = 0; i < n.inputs.length; i++) {
                    const linkId = n.inputs[i].link;
                    if (linkId !== null) {
                        const link = this.graph.links[linkId];
                        if (link && link.origin_id) {
                            g.setEdge(link.origin_id, n.id);
                        }
                    }
                }
            }
        });

        dagre.layout(g);

        nodes.forEach(n => {
            const dagreNode = g.node(n.id);
            if (dagreNode) {
                n.pos = [dagreNode.x - n.size[0] / 2, dagreNode.y - n.size[1] / 2];
            }
        });

        this.graph.setDirtyCanvas(true, true);
    },

    fallbackAutoLayout: function() {
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
        const groups = this.graph._groups || [];
        const yamlNodes = [];

        // Export groups (scopes)
        groups.forEach(group => {
            const yamlNode = {
                id: group.title || "Group",
                type: "scope",
                position: {
                    x: group._pos[0],
                    y: group._pos[1],
                    z: 0
                },
                dimensions: {
                    width: group._size[0],
                    height: group._size[1],
                    depth: 0
                },
                style: {
                    color: group.color || "#cccccc",
                    shape: "box"
                }
            };
            yamlNodes.push(yamlNode);
        });

        nodes.forEach(node => {
            const yamlNode = {
                id: node.title, // Assuming title is kept as ID
                type: node.agentNodeType.replace("agent/", ""), // Strip prefix
                position: {
                    x: node.pos[0],
                    y: node.pos[1],
                    z: 0
                },
                dimensions: {
                    width: node.size[0],
                    height: node.size[1],
                    depth: 0
                }
            };

            if (node.color) {
                yamlNode.style = { color: node.color };
            }

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
            const headers = { 'Content-Type': 'application/json' };
            const apiKey = localStorage.getItem('api_key');
            if (apiKey) headers["Authorization"] = `Bearer ${apiKey}`;
            const response = await fetch('/api/workflows/save', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({
                    name: this.currentWorkflowName,
                    definition: workflowData
                })
            });
            const res = await response.json();
            if (!response.ok) {
                throw new Error(res.detail || `HTTP ${response.status}`);
            }

            if (this.options && this.options.onStatusUpdate) {
                this.options.onStatusUpdate(res.message || "Workflow saved successfully", 'success');
            } else {
                alert(res.message || "Workflow saved successfully");
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
