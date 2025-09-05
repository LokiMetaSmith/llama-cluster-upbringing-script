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
    const statusLight = document.getElementById("status-light");

    function displayWelcomeArt() {
        const art = `
  ___
 / _ \\
| | | |
| |_| |
 \\___/
 [o o]
  \\_/
`;
        logToTerminal(`<pre>${art}</pre>`);
    }

    ws.onopen = function() {
        displayWelcomeArt();
        logToTerminal("--- Connection established with Agent ---");
        statusLight.style.backgroundColor = "#0f0"; // Green
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
            logToTerminal(`<strong>Agent:</strong> ${data}`, "agent-message");
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
