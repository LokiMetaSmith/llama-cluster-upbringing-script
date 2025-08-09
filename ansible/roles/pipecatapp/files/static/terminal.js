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

    ws.onopen = function() {
        logToTerminal("--- Connection established with Agent ---");
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
        } else if (type === "display") {
            renderEffect(data.text, data.effect);
        } else {
            logToTerminal(JSON.stringify(msg));
        }
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
