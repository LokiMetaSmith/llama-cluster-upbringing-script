document.addEventListener("DOMContentLoaded", function() {
    const terminal = document.getElementById("terminal");
    const ws = new WebSocket(`ws://${window.location.host}/ws`);

    function logToTerminal(message, className = '') {
        const p = document.createElement('p');
        p.innerHTML = message;
        if (className) {
            p.className = className;
        }
        terminal.appendChild(p);
        terminal.scrollTop = terminal.scrollHeight;
    }

    const saveNameInput = document.getElementById("save-name-input");
    const saveStateBtn = document.getElementById("save-state-btn");
    const loadStateBtn = document.getElementById("load-state-btn");
    const clearTerminalBtn = document.getElementById("clear-terminal-btn");
    const statusLight = document.getElementById("status-light");
    const testAndEvaluationBtn = document.getElementById("test-and-evaluation-btn");
    const statusDisplay = document.getElementById("status-display");
    const messageInput = document.getElementById("message-input");

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            ws.send(JSON.stringify({ type: "user_message", data: message }));
            logToTerminal(`<strong>You:</strong> ${message}`, "user-message");
            messageInput.value = "";
            animateThinking();
        }
    }

    messageInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function updateStatus() {
        fetch("/api/status")
            .then(response => response.json())
            .then(data => {
                const statusText = data.status;

                if (!statusText || statusText === "No active pipelines." || statusText === "MCP tool or runner not available." || statusText.startsWith("Agent not fully initialized")) {
                     statusDisplay.innerHTML = `<p>${statusText}</p>`;
                     return;
                }

                // Parse the string based on "Task {name}: {status}" format
                // Expected format: "Current pipeline status:\n- Task {name}: {state}\n..."
                const lines = statusText.split('\n').filter(line => line.trim().startsWith('- Task '));

                if (lines.length === 0) {
                     // Fallback if parsing fails or format is unexpected
                     statusDisplay.innerHTML = `<pre>${statusText}</pre>`;
                     return;
                }

                let html = '<table class="status-table">';
                html += '<thead><tr><th>Task</th><th>State</th></tr></thead>';
                html += '<tbody>';

                lines.forEach(line => {
                    const match = line.match(/- Task (.+): (.+)/);
                    if (match) {
                        const taskName = match[1];
                        const taskState = match[2];
                        html += `<tr><td>${taskName}</td><td>${taskState}</td></tr>`;
                    }
                });

                html += '</tbody></table>';
                statusDisplay.innerHTML = html;
            })
            .catch(error => {
                statusDisplay.innerText = `Error fetching status: ${error}`;
                console.error("Error fetching status:", error);
            });
    }

    testAndEvaluationBtn.onclick = updateStatus;

    const robotArt = document.getElementById("robot-art");

    const idleFrames = ["(^_^)", "(-_-)"];
    const typingFrame = "(>_<)";
    const wanderingFrames = ["(o_o)", "(O_O)"];
    const thinkingFrames = ["(o.o?)", "(o.O?)", "(O.o?)", "(O.O!)"];

    let currentFrame = 0;
    let idleAnimation;
    let typingTimeout;
    let wanderTimeout;
    let thinkingAnimation;

    function animateIdle() {
        currentFrame = (currentFrame + 1) % idleFrames.length;
        robotArt.textContent = idleFrames[currentFrame];
    }

    function stopAllAnimations() {
        clearInterval(idleAnimation);
        clearTimeout(typingTimeout);
        clearTimeout(wanderTimeout);
        clearInterval(thinkingAnimation);
    }

    function triggerWander() {
        stopAllAnimations();
        robotArt.textContent = wanderingFrames[0]; // Look left

        setTimeout(() => {
            robotArt.textContent = wanderingFrames[1]; // Look right
            setTimeout(() => {
                startIdleAnimation(); // Return to idle state, which will schedule the next wander
            }, 1000);
        }, 1000);
    }

    function animateThinking() {
        stopAllAnimations();
        let frame = 0;
        thinkingAnimation = setInterval(() => {
            robotArt.textContent = thinkingFrames[frame];
            frame = (frame + 1) % thinkingFrames.length;
        }, 500);
    }

    function startIdleAnimation() {
        stopAllAnimations();
        robotArt.textContent = idleFrames[0];
        idleAnimation = setInterval(animateIdle, 2000);
        // After starting idle, schedule a wander
        wanderTimeout = setTimeout(triggerWander, 8000);
    }

    messageInput.addEventListener("input", () => {
        stopAllAnimations();
        robotArt.textContent = typingFrame;

        typingTimeout = setTimeout(() => {
            startIdleAnimation(); // After typing, go back to idle
        }, 1500);
    });

    ws.onopen = function() {
        logToTerminal("--- Connection established with Agent ---");
        statusLight.style.backgroundColor = "#0f0"; // Green
        statusLight.setAttribute("aria-label", "Connection Status: Connected");
        statusLight.setAttribute("title", "Connection Status: Connected");
        updateStatus();
        startIdleAnimation();
    };

    saveStateBtn.onclick = function() {
        const saveName = saveNameInput.value.trim();
        if (!saveName) {
            logToTerminal("Please enter a name for the save state.", "error");
            return;
        }
        fetch("/api/state/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ save_name: saveName })
        })
        .then(response => response.json())
        .then(data => logToTerminal(data.message))
        .catch(error => logToTerminal(`Error saving state: ${error}`, "error"));
    };

    loadStateBtn.onclick = function() {
        const saveName = saveNameInput.value.trim();
        if (!saveName) {
            logToTerminal("Please enter the name of the state to load.", "error");
            return;
        }
        fetch("/api/state/load", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ save_name: saveName })
        })
        .then(response => response.json())
        .then(data => {
            logToTerminal(data.message);
            logToTerminal("--- State loaded. You may need to refresh the page to see changes in memory. ---");
        })
        .catch(error => logToTerminal(`Error loading state: ${error}`, "error"));
    };

    clearTerminalBtn.onclick = function() {
        // Find the robot art element within the terminal
        const robotArt = document.getElementById("robot-art");

        // Clear all content of the terminal
        terminal.innerHTML = '';

        // Re-append the robot art if it was found
        if (robotArt) {
            terminal.appendChild(robotArt);
        }
    };

    ws.onmessage = function(event) {
        try {
            const msg = JSON.parse(event.data);
            handleMessage(msg);
        } catch (e) {
            logToTerminal(event.data);
        }
    };

    ws.onclose = function() {
        logToTerminal("--- Connection lost with Agent ---", "error");
        statusLight.style.backgroundColor = "#f00"; // Red
        statusLight.setAttribute("aria-label", "Connection Status: Disconnected");
        statusLight.setAttribute("title", "Connection Status: Disconnected");
        stopAllAnimations();
    };

    ws.onerror = function(error) {
        logToTerminal(`--- WebSocket Error: ${error} ---`, "error");
    };

    function handleMessage(msg) {
        const type = msg.type;
        const data = msg.data;

        if (type === "log") {
            logToTerminal(data);
        } else if (type === "user") {
            logToTerminal(`<strong>You:</strong> ${data}`, "user-message");
        } else if (type === "agent") {
            logToTerminal(`<strong>Agent:</strong> ${data}`, "agent-message breathing-shimmering");
            startIdleAnimation();
        } else if (type === "display") {
            renderEffect(data.text, data.effect);
        } else if (type === "approval_request") {
            renderApprovalPrompt(data);
        } else {
            logToTerminal(JSON.stringify(msg));
        }
    }

    function renderApprovalPrompt(data) {
        const requestId = data.request_id;
        const toolCall = data.tool_call;

        const container = document.createElement('div');
        container.className = 'approval-prompt';

        const promptText = document.createElement('p');
        promptText.innerHTML = `<strong>Action Required:</strong> Approve the following tool call?`;
        container.appendChild(promptText);

        const toolCallPre = document.createElement('pre');
        toolCallPre.textContent = JSON.stringify(toolCall, null, 2);
        container.appendChild(toolCallPre);

        const buttonContainer = document.createElement('div');

        const approveButton = document.createElement('button');
        approveButton.textContent = "Approve";
        approveButton.onclick = function() {
            sendApprovalResponse(requestId, true);
            container.innerHTML = `<p><strong>Approved.</strong></p>`;
        };
        buttonContainer.appendChild(approveButton);

        const denyButton = document.createElement('button');
        denyButton.textContent = "Deny";
        denyButton.onclick = function() {
            sendApprovalResponse(requestId, false);
            container.innerHTML = `<p><strong>Denied.</strong></p>`;
        };
        buttonContainer.appendChild(denyButton);

        container.appendChild(buttonContainer);
        terminal.appendChild(container);
        terminal.scrollTop = terminal.scrollHeight;
    }

    function sendApprovalResponse(requestId, approved) {
        const response = {
            type: "approval_response",
            data: {
                request_id: requestId,
                approved: approved
            }
        };
        ws.send(JSON.stringify(response));
    }

    function renderEffect(text, effect) {
        if (effect === "figlet-lolcat") {
            figlet.text(text, { font: 'slant' }, function(err, data) {
                if (err) {
                    logToTerminal(text); // fallback
                    return;
                }
                const pre = document.createElement('pre');
                pre.innerHTML = lolcat.rainbow(function(char, color) {
                    return `<span style="color: ${color};">${char}</span>`;
                }, data);
                terminal.appendChild(pre);
                terminal.scrollTop = terminal.scrollHeight;
            });
        } else {
            logToTerminal(text);
        }
    }
});
