#!/usr/bin/env python3
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from bcc import BPF

# This is a placeholder for the power agent.
# It will be responsible for loading the eBPF program, monitoring the packet
# counts, and making decisions about when to sleep or wake services.

# --- Dummy HTTP Server for Health Check Spoofing ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check_server(port=8888):
    server_address = ('', port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print(f"Health check spoofer running on port {port}...")
    httpd.serve_forever()

import json
import os
import subprocess

# --- Configuration Loading ---
CONFIG_PATH = "/opt/power_manager/config.json"
MONITORED_SERVICES = {}
last_config_mtime = 0

def load_config():
    """Loads the configuration from the JSON file."""
    global MONITORED_SERVICES, last_config_mtime
    try:
        current_mtime = os.path.getmtime(CONFIG_PATH)
        if current_mtime == last_config_mtime:
            return # No changes

        print("Configuration file changed. Reloading...")
        with open(CONFIG_PATH, 'r') as f:
            config_data = json.load(f).get("monitored_services", {})

        # Update MONITORED_SERVICES with new data, preserving state
        for port, new_config in config_data.items():
            port_int = int(port)
            if port_int not in MONITORED_SERVICES:
                MONITORED_SERVICES[port_int] = {
                    "status": "running",
                    "last_traffic_time": time.time(),
                    **new_config
                }
            else:
                MONITORED_SERVICES[port_int].update(new_config)

        last_config_mtime = current_mtime
        print("Configuration reloaded.")
    except FileNotFoundError:
        print("Config file not found. Using empty configuration.")
        MONITORED_SERVICES = {}
    except Exception as e:
        print(f"Error loading configuration: {e}")


# --- Nomad Actions ---
def put_service_to_sleep(port):
    """Stops a Nomad job."""
    config = MONITORED_SERVICES[port]
    job_name = config["job_name"]
    print(f"Service on port {port} has been idle. Putting job '{job_name}' to sleep...")
    try:
        subprocess.run(["nomad", "job", "stop", job_name], check=True)
        config["status"] = "sleeping"
        print(f"Job '{job_name}' stopped successfully.")
    except Exception as e:
        print(f"Error stopping job '{job_name}': {e}")

def wake_service_up(port):
    """Starts a Nomad job."""
    config = MONITORED_SERVICES[port]
    job_file_path = config["job_file_path"]
    print(f"New traffic detected for sleeping service on port {port}. Waking up job...")
    try:
        subprocess.run(["nomad", "job", "run", job_file_path], check=True)
        config["status"] = "running"
        config["last_traffic_time"] = time.time()
        print(f"Job from file '{job_file_path}' started successfully.")
    except Exception as e:
        print(f"Error starting job from file '{job_file_path}': {e}")

def main():
    # Start the health check spoofer in a separate thread
    health_server_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_server_thread.start()

    # Load the eBPF program
    b = BPF(src_file="traffic_monitor.c")
    b.attach_xdp(dev="eth0", fn=b.load_func("xdp_traffic_monitor", BPF.XDP))

    packet_counts = b.get_table("packet_counts")
    last_known_counts = {}

    print("Power agent started. Monitoring traffic...")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            load_config() # Periodically check for and reload config changes
            time.sleep(10) # Check every 10 seconds

            # --- Sleep Logic ---
            for port, config in MONITORED_SERVICES.items():
                if config["status"] == "running":
                    current_count = packet_counts.get(port, 0)
                    last_count = last_known_counts.get(port, 0)

                    if current_count > last_count:
                        # Traffic detected
                        print(f"Traffic detected for port {port}. Resetting idle timer.")
                        config["last_traffic_time"] = time.time()
                        last_known_counts[port] = current_count
                    else:
                        # No new traffic
                        idle_time = time.time() - config["last_traffic_time"]
                        if idle_time > config["idle_threshold_seconds"]:
                            put_service_to_sleep(port)

            # --- Wake Logic (Placeholder) ---
            # In a real implementation, this would not be a polling loop.
            # Instead, the eBPF program would send a perf event when it sees
            # traffic for a *sleeping* service. This agent would listen for
            # that event and call wake_service_up() immediately.
            #
            # For demonstration, we'll simulate this by checking if a sleeping
            # service has new traffic.
            for port, config in MONITORED_SERVICES.items():
                 if config["status"] == "sleeping":
                    current_count = packet_counts.get(port, 0)
                    last_count = last_known_counts.get(port, 0)
                    if current_count > last_count:
                        wake_service_up(port)
                        last_known_counts[port] = current_count


    except KeyboardInterrupt:
        print("Power agent stopped.")
        b.remove_xdp(dev="eth0", flags=0)

if __name__ == "__main__":
    main()
