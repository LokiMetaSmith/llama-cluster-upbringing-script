/* ==========================================================================
   INTERACTIVE AGENT MANAGER (GEMINI API)
   ========================================================================== */

window.AgentManager = {
    ws: null,
    uiCallback: null,
    pendingTools: {}, // keep track of tool uses for UI

    connectWebSocket() {
        if (this.ws) return;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // Connect to the cluster WebSocket endpoint. Assuming standard root WS mount for the backend.
        // It relies on Traefik or local proxy to hit pipecatapp.
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log("Connected to Cluster WebSocket");
        };

        this.ws.onmessage = async (event) => {
            if (!this.uiCallback) return;
            try {
                const msg = JSON.parse(event.data);

                if (msg.type === "message" || msg.type === "chunk") {
                    this.uiCallback(msg.data, false);
                } else if (msg.type === "tool_call" || msg.type === "tool_start") {
                     // Need to format this to match the UI's expected format, e.g., "[tool_use: ...]"
                     const toolName = msg.tool_name || msg.name || "unknown_tool";
                     let argsStr = "{}";
                     try {
                         if (msg.arguments) {
                             argsStr = typeof msg.arguments === 'string' ? msg.arguments : JSON.stringify(msg.arguments);
                         }
                     } catch(e) {}

                     // Standardize for OpenGravity UI parser
                     if (toolName === "thinking") {
                         this.uiCallback(`[tool_use: thinking ${argsStr}]`, true, true);
                     } else if (toolName === "shell" || toolName === "run_command") {
                         this.uiCallback(`[tool_use: run_command ${argsStr}]`, true, true);
                     } else if (toolName === "file_editor" || toolName === "write_file") {
                         this.uiCallback(`[tool_use: write_to_file ${argsStr}]`, true, true);
                     } else {
                         this.uiCallback(`[tool_use: command_status {"text": "Running ${toolName}..."}]`, true, true);
                     }
                } else if (msg.type === "tool_result" || msg.type === "tool_end") {
                     this.uiCallback('', true, false); // clear pending status
                     if (msg.result) {
                         const escapedOutput = String(msg.result).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
                         this.uiCallback(`[tool_result: "${escapedOutput}"]`, true, false);
                     }
                } else if (msg.type === "error") {
                     this.uiCallback(`**Error:** ${msg.data || msg.message}`, false);
                } else if (msg.type === "status") {
                     // For things like typing indicator or status messages
                     // this.uiCallback(`[tool_use: command_status {"text": "${msg.data}"}]`, true, true);
                }
            } catch (e) {
                // If it's plain text fallback
                this.uiCallback(event.data, false);
            }
        };

        this.ws.onerror = (err) => {
            console.error("WebSocket Error:", err);
            if (this.uiCallback) this.uiCallback("**WebSocket Error**: Could not connect to cluster backend.", false);
        };

        this.ws.onclose = () => {
            console.log("WebSocket Disconnected");
            this.ws = null;
        };
    },

    async processUserQuery(query, uiCallback) {
        this.uiCallback = uiCallback;
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            this.connectWebSocket();
            // wait a tiny bit for connection to open, ideally this should be handled better
            let attempts = 0;
            while (this.ws && this.ws.readyState !== WebSocket.OPEN && attempts < 20) {
                await new Promise(resolve => setTimeout(resolve, 100));
                attempts++;
            }
        }

        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            // Send the user message payload
            const payload = {
                type: "message",
                data: query
            };
            this.ws.send(JSON.stringify(payload));
        } else {
             uiCallback("**Error:** WebSocket connection is not open.", false);
        }
    }
};