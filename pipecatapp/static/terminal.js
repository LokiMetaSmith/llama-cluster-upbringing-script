document.addEventListener("DOMContentLoaded", function() {
    const terminal = document.getElementById("terminal");
    const MAX_LOG_ENTRIES = 500; // Optimization: Limit terminal size to prevent DOM bloat
    const ws = new WebSocket(`ws://${window.location.host}/ws`);

    // Security Fix: Prevent XSS by escaping HTML special characters
    function escapeHtml(text) {
        if (!text) return text;
        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function logToTerminal(message, className = '') {
        const p = document.createElement('p');
        p.innerHTML = message;
        if (className) {
            p.className = className;
        }
        terminal.appendChild(p);

        // Bolt ⚡ Optimization: Limit the number of log entries to prevent DOM bloat
        // We preserve the robot-art element if it's the first child.
        const maxElements = MAX_LOG_ENTRIES + (document.getElementById("robot-art") ? 1 : 0);

        while (terminal.childElementCount > maxElements) {
            const first = terminal.firstElementChild;
            // If the first element is the robot art, we want to remove the *next* sibling (the oldest log)
            // If the first element is NOT robot art (maybe it was cleared?), we remove the first element.
            if (first && first.id === 'robot-art') {
                const second = first.nextElementSibling;
                if (second) {
                    terminal.removeChild(second);
                } else {
                    // Should not happen if count > maxElements, but safe break
                    break;
                }
            } else {
                if (first) {
                    terminal.removeChild(first);
                }
            }
        }

        terminal.scrollTop = terminal.scrollHeight;
    }

    const saveNameInput = document.getElementById("save-name-input");
    const saveStateBtn = document.getElementById("save-state-btn");
    const loadStateBtn = document.getElementById("load-state-btn");
    const clearTerminalBtn = document.getElementById("clear-terminal-btn");
    const statusLight = document.getElementById("connection-status");
    const systemStatusBtn = document.getElementById("system-status-btn");
    const statusDisplay = document.getElementById("status-display");
    const messageInput = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");
    const jumpToBottomBtn = document.getElementById("jump-to-bottom-btn");

    // Palette UX Improvement: Auto-focus input on load
    if (messageInput) {
        messageInput.focus();
    }

    // Palette UX Improvement: Jump to Bottom Logic
    if (jumpToBottomBtn) {
        jumpToBottomBtn.addEventListener('click', () => {
            terminal.scrollTop = terminal.scrollHeight;
        });

        terminal.addEventListener('scroll', () => {
            const isNearBottom = terminal.scrollHeight - terminal.scrollTop - terminal.clientHeight < 100;
            if (isNearBottom) {
                jumpToBottomBtn.style.display = 'none';
            } else {
                jumpToBottomBtn.style.display = 'block';
            }
        });
    }

    // Palette UX Improvement: Disable Save/Load buttons when input is empty
    function toggleStateButtons() {
        if (!saveStateBtn || !loadStateBtn || !saveNameInput) return;
        const isDisabled = !saveNameInput.value.trim();
        saveStateBtn.disabled = isDisabled;
        loadStateBtn.disabled = isDisabled;
    }

    if (saveNameInput) {
        saveNameInput.addEventListener("input", toggleStateButtons);
        saveNameInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                if (saveStateBtn && !saveStateBtn.disabled) {
                    saveStateBtn.click();
                }
            }
        });
        // Initialize state
        toggleStateButtons();
    }

    // Helper for loading state
    function setLoading(btn, isLoading, loadingText) {
        if (!btn) return;
        if (isLoading) {
             // Store original text if not already stored
             if (!btn.hasAttribute('data-original-text')) {
                 btn.setAttribute('data-original-text', btn.textContent);
             }
             btn.textContent = loadingText || "Loading...";
             btn.disabled = true;
             btn.setAttribute("aria-busy", "true");
        } else {
             const originalText = btn.getAttribute('data-original-text');
             if (originalText) {
                 btn.textContent = originalText;
                 btn.removeAttribute('data-original-text');
             }
             btn.disabled = false;
             btn.setAttribute("aria-busy", "false");
        }
    }

    // Dropdown Logic
    const adminUiBtn = document.getElementById("admin-ui-btn");
    const adminUiDropdown = document.getElementById("admin-ui-dropdown");

    if (adminUiBtn && adminUiDropdown) {
        adminUiBtn.addEventListener('click', function(event) {
            // Prevent event from bubbling to window (which would close it immediately)
            event.stopPropagation();
            adminUiDropdown.classList.toggle("show");
            const expanded = adminUiDropdown.classList.contains("show");
            adminUiBtn.setAttribute("aria-expanded", expanded);

            if (expanded && typeof window.refreshAdminUIs === 'function') {
                window.refreshAdminUIs();
            }
        });

        // Close dropdown when clicking outside
        window.addEventListener('click', function(event) {
            if (!event.target.matches('.dropbtn') && !event.target.matches('.dropdown-content') && !adminUiDropdown.contains(event.target)) {
                if (adminUiDropdown.classList.contains('show')) {
                    adminUiDropdown.classList.remove('show');
                    adminUiBtn.setAttribute("aria-expanded", "false");
                }
            }
        });

        // Handle Escape key to close dropdown and Arrow Keys for navigation
        adminUiDropdown.addEventListener('keydown', function(event) {
            const isExpanded = adminUiDropdown.classList.contains("show");

            // Close on Escape
            if (event.key === 'Escape') {
                if (isExpanded) {
                    adminUiDropdown.classList.remove('show');
                    adminUiBtn.setAttribute("aria-expanded", "false");
                    adminUiBtn.focus();
                }
                return;
            }

            // Open menu with ArrowDown if focused on button
            if (!isExpanded && document.activeElement === adminUiBtn && event.key === 'ArrowDown') {
                event.preventDefault();
                adminUiDropdown.classList.add("show");
                adminUiBtn.setAttribute("aria-expanded", "true");
                const firstLink = adminUiDropdown.querySelector('.dropdown-content a:not(.unhealthy)');
                if (firstLink) firstLink.focus();
                return;
            }

            // Navigate links if menu is open
            if (isExpanded) {
                const links = Array.from(adminUiDropdown.querySelectorAll('.dropdown-content a:not(.unhealthy)'));
                if (links.length === 0) return;

                const currentIndex = links.indexOf(document.activeElement);

                if (event.key === 'ArrowDown') {
                    event.preventDefault();
                    // If no link is focused (e.g. still on button), focus first. Otherwise next.
                    const nextIndex = currentIndex === -1 ? 0 : (currentIndex + 1) % links.length;
                    links[nextIndex].focus();
                } else if (event.key === 'ArrowUp') {
                    event.preventDefault();
                    // If no link is focused, focus last. Otherwise previous.
                    const prevIndex = currentIndex === -1 ? links.length - 1 : (currentIndex - 1 + links.length) % links.length;
                    links[prevIndex].focus();
                } else if (event.key === 'Home') {
                    event.preventDefault();
                    links[0].focus();
                } else if (event.key === 'End') {
                    event.preventDefault();
                    links[links.length - 1].focus();
                }
            } else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
                event.preventDefault();
                // Ensure dropdown is open
                if (!adminUiDropdown.classList.contains('show')) {
                    adminUiDropdown.classList.add('show');
                    adminUiBtn.setAttribute("aria-expanded", "true");
                }

                const links = Array.from(adminUiDropdown.querySelectorAll('a[href]')); // Only focusable links
                if (links.length === 0) return;

                const currentIndex = links.indexOf(document.activeElement);
                let nextIndex = 0;

                if (currentIndex !== -1) {
                     if (event.key === 'ArrowDown') {
                         nextIndex = (currentIndex + 1) % links.length;
                     } else {
                         nextIndex = (currentIndex - 1 + links.length) % links.length;
                     }
                } else if (event.key === 'ArrowUp') {
                    // If no link focused, ArrowUp goes to last
                    nextIndex = links.length - 1;
                }

                links[nextIndex].focus();
            }
        });
    }

    // Palette UX Improvement: Command History
    const messageHistory = [];
    const MAX_HISTORY = 50;
    let historyIndex = -1;
    let tempInput = "";

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            ws.send(JSON.stringify({ type: "user_message", data: message }));
            // Security Fix: Escape user input before rendering
            logToTerminal(`<strong>You:</strong> ${escapeHtml(message)}`, "user-message");

            // Add to history if unique or last entry is different
            if (messageHistory.length === 0 || messageHistory[messageHistory.length - 1] !== message) {
                messageHistory.push(message);
                if (messageHistory.length > MAX_HISTORY) messageHistory.shift();
            }
            historyIndex = -1;
            tempInput = "";

            messageInput.value = "";
            animateThinking();
        }
    }

    // Palette UX Improvement: Global Keyboard Shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl+K to clear terminal
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            if (clearTerminalBtn) clearTerminalBtn.click();
        }
        // Ctrl+L to focus input
        if ((event.ctrlKey || event.metaKey) && event.key === 'l') {
            event.preventDefault();
            if (messageInput) messageInput.focus();
        }
    });

    messageInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();
            event.preventDefault();
            return;
        }

        if (event.key === "ArrowUp") {
            if (messageHistory.length === 0) return;
            event.preventDefault();

            if (historyIndex === -1) {
                tempInput = messageInput.value;
                historyIndex = messageHistory.length - 1;
            } else if (historyIndex > 0) {
                historyIndex--;
            }
            messageInput.value = messageHistory[historyIndex];
            // Move cursor to end
            setTimeout(() => messageInput.setSelectionRange(messageInput.value.length, messageInput.value.length), 0);
        } else if (event.key === "ArrowDown") {
            if (historyIndex === -1) return;
            event.preventDefault();

            if (historyIndex < messageHistory.length - 1) {
                historyIndex++;
                messageInput.value = messageHistory[historyIndex];
            } else {
                historyIndex = -1;
                messageInput.value = tempInput;
            }
            // Move cursor to end
            setTimeout(() => messageInput.setSelectionRange(messageInput.value.length, messageInput.value.length), 0);
        }
    });

    if (sendBtn) {
        sendBtn.addEventListener("click", sendMessage);
    }

    function updateStatus(event) {
        // If triggered by event (button click), handle loading state
        const btn = (event instanceof Event) ? event.target : null;
        if (btn) setLoading(btn, true, "Checking...");

        fetch("/api/status")
            .then(response => response.json())
            .then(data => {
                const statusText = data.status;

                if (!statusText || statusText === "No active pipelines." || statusText === "MCP tool or runner not available." || statusText.startsWith("Agent not fully initialized")) {
                     // Security Fix: Escape status text
                     statusDisplay.innerHTML = `<p>${escapeHtml(statusText)}</p>`;
                     return;
                }

                // Parse the string based on "Task {name}: {status}" format
                // Expected format: "Current pipeline status:\n- Task {name}: {state}\n..."
                const lines = statusText.split('\n').filter(line => line.trim().startsWith('- Task '));

                if (lines.length === 0) {
                     // Fallback if parsing fails or format is unexpected
                     // Security Fix: Escape status text
                     statusDisplay.innerHTML = `<pre>${escapeHtml(statusText)}</pre>`;
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
                        // Security Fix: Escape task name and state
                        html += `<tr><td>${escapeHtml(taskName)}</td><td>${escapeHtml(taskState)}</td></tr>`;
                    }
                });

                html += '</tbody></table>';
                statusDisplay.innerHTML = html;
            })
            .catch(error => {
                statusDisplay.innerText = `Error fetching status: ${error}`;
                console.error("Error fetching status:", error);
            })
            .finally(() => {
                if (btn) setLoading(btn, false);
            });
    }

    if (systemStatusBtn) {
        systemStatusBtn.onclick = updateStatus;
    }

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

    // Accessibility Helper: Update aria-label and text content together
    function updateRobotState(text, stateLabel) {
        if (!robotArt) return;
        robotArt.textContent = text;
        if (stateLabel) {
            robotArt.setAttribute("aria-label", `Robot face: ${stateLabel}`);
        }
    }

    function animateIdle() {
        currentFrame = (currentFrame + 1) % idleFrames.length;
        // Don't update aria-label on every frame to avoid spamming the screen reader
        // Just update text content. The state "Idle" remains valid.
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
        updateRobotState(wanderingFrames[0], "Wandering"); // Look left

        setTimeout(() => {
            updateRobotState(wanderingFrames[1], "Wandering"); // Look right
            setTimeout(() => {
                startIdleAnimation(); // Return to idle state, which will schedule the next wander
            }, 1000);
        }, 1000);
    }

    function animateThinking() {
        stopAllAnimations();
        let frame = 0;
        // Set initial label
        updateRobotState(thinkingFrames[0], "Thinking");
        thinkingAnimation = setInterval(() => {
            robotArt.textContent = thinkingFrames[frame];
            frame = (frame + 1) % thinkingFrames.length;
        }, 500);
    }

    function startIdleAnimation() {
        stopAllAnimations();
        // Set initial label
        updateRobotState(idleFrames[0], "Idle");
        idleAnimation = setInterval(animateIdle, 2000);
        // After starting idle, schedule a wander
        wanderTimeout = setTimeout(triggerWander, 8000);
    }

    messageInput.addEventListener("input", () => {
        stopAllAnimations();
        updateRobotState(typingFrame, "Typing");

        typingTimeout = setTimeout(() => {
            startIdleAnimation(); // After typing, go back to idle
        }, 1500);
    });

    ws.onopen = function() {
        logToTerminal("--- Connection established with Agent ---");
        if (statusLight) {
            statusLight.classList.remove("disconnected");
            statusLight.classList.add("connected");
            const statusText = statusLight.querySelector(".status-text");
            if (statusText) statusText.textContent = "Connected";
            statusLight.setAttribute("aria-label", "Connection Status: Connected");
            statusLight.setAttribute("title", "Connection Status: Connected");
        }
        updateStatus();
        startIdleAnimation();
    };

    saveStateBtn.onclick = function() {
        const saveName = saveNameInput.value.trim();
        if (!saveName) {
            logToTerminal("Please enter a name for the save state.", "error");
            return;
        }
        setLoading(saveStateBtn, true, "Saving...");

        fetch("/api/state/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ save_name: saveName })
        })
        .then(response => response.json())
        .then(data => logToTerminal(escapeHtml(data.message))) // Security Fix: Escape response
        .catch(error => logToTerminal(`Error saving state: ${escapeHtml(error)}`, "error")) // Security Fix: Escape error
        .finally(() => setLoading(saveStateBtn, false));
    };

    loadStateBtn.onclick = function() {
        const saveName = saveNameInput.value.trim();
        if (!saveName) {
            logToTerminal("Please enter the name of the state to load.", "error");
            return;
        }
        setLoading(loadStateBtn, true, "Loading...");

        fetch("/api/state/load", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ save_name: saveName })
        })
        .then(response => response.json())
        .then(data => {
            logToTerminal(escapeHtml(data.message)); // Security Fix: Escape response
            logToTerminal("--- State loaded. You may need to refresh the page to see changes in memory. ---");
        })
        .catch(error => logToTerminal(`Error loading state: ${escapeHtml(error)}`, "error")) // Security Fix: Escape error
        .finally(() => setLoading(loadStateBtn, false));
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
            // Security Fix: Escape raw message
            logToTerminal(escapeHtml(event.data));
        }
    };

    ws.onclose = function() {
        logToTerminal("--- Connection lost with Agent ---", "error");
        if (statusLight) {
            statusLight.classList.remove("connected");
            statusLight.classList.add("disconnected");
            const statusText = statusLight.querySelector(".status-text");
            if (statusText) statusText.textContent = "Disconnected";
            statusLight.setAttribute("aria-label", "Connection Status: Disconnected");
            statusLight.setAttribute("title", "Connection Status: Disconnected");
        }
        stopAllAnimations();
    };

    ws.onerror = function(error) {
        logToTerminal(`--- WebSocket Error: ${escapeHtml(error)} ---`, "error");
    };

    function handleMessage(msg) {
        const type = msg.type;
        const data = msg.data;

        if (type === "log") {
            logToTerminal(escapeHtml(data));
        } else if (type === "user") {
            logToTerminal(`<strong>You:</strong> ${escapeHtml(data)}`, "user-message");
        } else if (type === "agent") {
            logToTerminal(`<strong>Agent:</strong> ${escapeHtml(data)}`, "agent-message breathing-shimmering");
            startIdleAnimation();
        } else if (type === "display") {
            // display type might expect HTML or specific rendering,
            // but renderEffect uses figlet/lolcat which generates HTML.
            // We trust renderEffect for now as it doesn't take raw HTML from user directly in this path?
            // Actually renderEffect takes 'text'. If text is safe...
            renderEffect(data.text, data.effect);
        } else if (type === "approval_request") {
            renderApprovalPrompt(data);
        } else {
            logToTerminal(escapeHtml(JSON.stringify(msg)));
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
        approveButton.className = "btn-approve";
        approveButton.setAttribute("aria-label", "Approve tool execution");
        approveButton.title = "Allow the agent to execute this tool";
        approveButton.onclick = function() {
            sendApprovalResponse(requestId, true);
            container.innerHTML = `<p><strong>Approved.</strong></p>`;
        };
        buttonContainer.appendChild(approveButton);

        const denyButton = document.createElement('button');
        denyButton.textContent = "Deny";
        denyButton.className = "btn-deny";
        denyButton.setAttribute("aria-label", "Deny tool execution");
        denyButton.title = "Block this tool execution";
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
            // figlet relies on text content, safe from HTML injection usually as it converts chars to ascii art
            figlet.text(text, { font: 'slant' }, function(err, data) {
                if (err) {
                    logToTerminal(escapeHtml(text)); // fallback
                    return;
                }
                const pre = document.createElement('pre');
                // lolcat.rainbow wraps chars in spans. data is ascii art.
                // We assume figlet output is safe.
                pre.innerHTML = lolcat.rainbow(function(char, color) {
                    return `<span style="color: ${color};">${char}</span>`;
                }, data);
                terminal.appendChild(pre);
                terminal.scrollTop = terminal.scrollHeight;
            });
        } else {
            logToTerminal(escapeHtml(text));
        }
    }
});
