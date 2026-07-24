#!/usr/bin/env python3
"""
CommandDeck Setup Platform Backend.
Serves static frontend files and acts as an API gateway for Ansible playbooks and cluster setups.
"""

import os
import sys
import json
import yaml  # type: ignore
import subprocess
import threading
import socket
import re
import time
import signal
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

# Set fixed port for CommandDeck Web UI
PORT = 8085

# Find project root (assumed to be repo root)
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR = os.path.join(REPO_ROOT, "command_deck", "frontend")
MODELS_YAML_PATH = os.path.join(REPO_ROOT, "group_vars", "models.yaml")

# Thread-safe status and logs
process_lock = threading.Lock()
active_process = None
process_log_buffer = []
process_status = "idle"  # idle, running, finished, error
process_exit_code = 0

try:
    import webview
except ImportError:
    webview = None


def log_reader_thread(proc):
    global process_status, process_exit_code
    # Read output line by line
    for line in iter(proc.stdout.readline, ''):
        if not line:
            break
        with process_lock:
            process_log_buffer.append(line)
            # Cap the buffer size to 5000 lines to avoid high memory usage
            if len(process_log_buffer) > 5000:
                process_log_buffer.pop(0)
    proc.stdout.close()
    proc.wait()
    with process_lock:
        process_exit_code = proc.returncode
        if process_exit_code == 0:
            process_status = "finished"
        else:
            process_status = "error"


def parse_models():
    """Reads models.yaml and returns list categorized into Edge/Mid and Core"""
    if not os.path.exists(MODELS_YAML_PATH):
        return {"edge_mid": [], "core": []}

    try:
        with open(MODELS_YAML_PATH, 'r') as f:
            data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error parsing models.yaml: {e}", file=sys.stderr)
        return {"edge_mid": [], "core": []}

    expert_models = data.get("expert_models", {})
    edge_mid_list = []
    core_list = []

    for category, models_list in expert_models.items():
        if not isinstance(models_list, list):
            continue
        for m in models_list:
            if not isinstance(m, dict) or "name" not in m:
                continue
            mem = m.get("memory_mb", 0)
            model_info = {
                "category": category,
                "name": m.get("name"),
                "url": m.get("url", ""),
                "filename": m.get("filename", ""),
                "memory_mb": mem,
                "memory_gb": round(mem / 1024, 1)
            }
            # Edge/Mid models have memory < 8GB (8192 MB)
            if mem < 8192:
                edge_mid_list.append(model_info)
            else:
                core_list.append(model_info)

    return {
        "edge_mid": edge_mid_list,
        "core": core_list
    }


class CommandDeckAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress spamming terminal console with HTTP logs
        pass

    def do_GET(self):
        url_path = self.path.split('?')[0]

        # 1. API Endpoints
        if url_path == "/api/models":
            models_data = parse_models()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(models_data).encode('utf-8'))
            return

        elif url_path == "/api/status":
            with process_lock:
                status_data = {
                    "status": process_status,
                    "exit_code": process_exit_code,
                    "log_count": len(process_log_buffer)
                }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(status_data).encode('utf-8'))
            return

        elif url_path == "/api/info":
            try:
                # Try to get the IP address of the node
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip_address = s.getsockname()[0]
                s.close()
            except Exception:
                ip_address = "127.0.0.1"

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ip_address": ip_address}).encode('utf-8'))
            return

        elif url_path == "/api/logs":
            # Support logs offset for simple long-polling
            query = self.path.split('?')[-1] if '?' in self.path else ""
            offset = 0
            if "offset=" in query:
                try:
                    offset = int(query.split("offset=")[-1].split("&")[0])
                except ValueError:
                    pass

            with process_lock:
                current_len = len(process_log_buffer)
                lines = process_log_buffer[offset:]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "lines": lines,
                "next_offset": current_len
            }).encode('utf-8'))
            return

        # 2. Serve Static Frontend Files
        if url_path == "/" or url_path == "":
            file_name = "index.html"
        else:
            file_name = url_path.lstrip('/')

        file_path = os.path.join(FRONTEND_DIR, file_name)

        # Security check: ensure path is inside FRONTEND_DIR
        real_frontend_dir = os.path.realpath(FRONTEND_DIR)
        real_file_path = os.path.realpath(file_path)
        if not real_file_path.startswith(real_frontend_dir):
            self.send_error(403, "Access Denied")
            return

        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            if file_name.endswith('.html'):
                self.send_header("Content-Type", "text/html")
            elif file_name.endswith('.css'):
                self.send_header("Content-Type", "text/css")
            elif file_name.endswith('.js'):
                self.send_header("Content-Type", "application/javascript")
            elif file_name.endswith('.png'):
                self.send_header("Content-Type", "image/png")
            elif file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
                self.send_header("Content-Type", "image/jpeg")
            elif file_name.endswith('.svg'):
                self.send_header("Content-Type", "image/svg+xml")
            else:
                self.send_header("Content-Type", "application/octet-stream")
            self.end_headers()

            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        url_path = self.path.split('?')[0]

        if url_path in ["/api/run", "/api/stop", "/api/exit"]:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
            try:
                payload = json.loads(post_data)
            except json.JSONDecodeError:
                payload = {}

            if url_path == "/api/run":
                global active_process, process_status, process_exit_code, process_log_buffer

                with process_lock:
                    if active_process is not None and active_process.poll() is None:
                        self.send_response(400)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": "A task is already running."}).encode('utf-8'))
                        return

                action = payload.get("action")
                params = payload.get("params", {})

                cmd = []
                if action == "bootstrap":
                    role = params.get("role", "all")
                    user = params.get("user", "pipecatapp")
                    controller_ip = params.get("controller_ip", "")
                    tags = params.get("tags", "")

                    cmd = ["./bootstrap.sh", "--role", role, "--user", user, "--yes"]
                    if role == "worker" and controller_ip:
                        cmd.extend(["--controller-ip", controller_ip])
                    if tags:
                        cmd.extend(["--tags", tags])

                elif action == "deploy_model":
                    category = params.get("category", "main")
                    cmd = [".venv/bin/ansible-playbook", "-i", "local_inventory.ini", "playbooks/deploy_expert.yaml", "-e", f"current_expert={category}"]

                elif action == "validate":
                    cmd = [".venv/bin/ansible-playbook", "-i", "local_inventory.ini", "playbooks/run_health_check.yaml"]

                elif action == "heal":
                    cmd = ["./scripts/heal_cluster.sh"]

                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Unknown action."}).encode('utf-8'))
                    return

                with process_lock:
                    process_log_buffer = [f"Executing: {' '.join(cmd)}\n\n"]
                    process_status = "running"
                    process_exit_code = 0

                    try:
                        # Launch the background process from REPO_ROOT
                        active_process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            text=True,
                            bufsize=1,
                            cwd=REPO_ROOT
                        )

                        # Start line-reader thread
                        t = threading.Thread(target=log_reader_thread, args=(active_process,))
                        t.daemon = True
                        t.start()

                    except Exception as e:
                        process_status = "error"
                        process_exit_code = -1
                        process_log_buffer.append(f"Failed to start process: {e}\n")
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                        return

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "started"}).encode('utf-8'))
                return

            elif url_path == "/api/stop":
                with process_lock:
                    if active_process is not None and active_process.poll() is None:
                        active_process.terminate()
                        process_log_buffer.append("\nProcess terminated by user.\n")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "terminated"}).encode('utf-8'))
                return

            elif url_path == "/api/exit":
                print("Exit signal received. Terminating CommandDeck.", flush=True)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "exiting"}).encode('utf-8'))

                # Terminate python process in a separate thread to allow response to client first
                def terminate_app():
                    try:
                        # Directly execute bash command to avoid insecure temporary files
                        subprocess.Popen(["sudo", "bash", "-c", "sed -i 's/Session=command-deck/Session=plasmawayland/' /etc/sddm.conf.d/autologin.conf && systemctl restart sddm"])
                    except Exception as e:
                        print(f"Error executing switch script: {e}")

                    time.sleep(1)

                    # Try to set SDDM autologin session to plasmawayland and restart SDDM
                    if os.path.exists('/etc/sddm.conf.d/autologin.conf'):
                        try:
                            subprocess.run(['sudo', 'sed', '-i', 's/Session=command-deck/Session=plasmawayland/g', '/etc/sddm.conf.d/autologin.conf'], check=True)
                            subprocess.run(['sudo', 'systemctl', 'restart', 'sddm'], check=True)
                        except Exception as e:
                            print(f"Failed to configure or restart SDDM: {e}", flush=True)

                    os.kill(os.getpid(), signal.SIGTERM)
                threading.Thread(target=terminate_app).start()
                return

        self.send_error(404, "Not Found")


def run_server():
    server = HTTPServer(('127.0.0.1', PORT), CommandDeckAPIHandler)
    print(f"CommandDeck server running at http://127.0.0.1:{PORT}/", flush=True)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="CommandDeck Setup Platform")
    parser.add_argument("--server-only", action="store_true", help="Run only the API and static web server, no GUI window")
    args = parser.parse_args()

    # Start HTTP API server in background thread
    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()

    # Wait for server to start
    time.sleep(1)

    if args.server_only or webview is None:
        if webview is None and not args.server_only:
            print("pywebview is not installed. Running in server-only mode.", flush=True)
        print("Point your browser to http://127.0.0.1:8085/ to access CommandDeck.", flush=True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting.")
    else:
        print("Launching CommandDeck GUI Window...", flush=True)
        webview.create_window(
            title="CommandDeck Setup Platform",
            url=f"http://127.0.0.1:{PORT}/index.html",
            width=1024,
            height=768,
            resizable=True
        )
        webview.start()


if __name__ == "__main__":
    main()
