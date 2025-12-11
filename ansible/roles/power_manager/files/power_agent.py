#!/usr/bin/env python3
"""Power management agent for sleeping and waking Nomad services.

This agent uses an eBPF program to monitor network traffic to specific service
ports. If a service is idle for a configurable amount of time, this agent will
stop the corresponding Nomad job to conserve resources. When new traffic is
detected for a sleeping service, the agent will restart the job.

It also runs a simple HTTP server to respond to health checks for services
that have been put to sleep, preventing service orchestrators from marking
them as failed.
"""
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from bcc import BPF
import json
import os
import subprocess
import sys
import ctypes as ct
import socket

# --- Dummy HTTP Server for Health Check Spoofing ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    """A simple HTTP request handler that always returns a 200 OK response.

    This server is used to "spoof" health checks for services that have been
    put to sleep by the power agent. When a service is sleeping, this server
    can be configured to listen on its port and respond to health checks,
    tricking the service orchestrator (like Nomad or Consul) into thinking
    the service is still healthy.
    """
    def do_GET(self):
        """Handles GET requests by sending a 200 OK response."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check_server(port: int = 8888):
    """Runs the dummy HTTP server for health check spoofing.

    Args:
        port (int, optional): The port on which the server should listen.
            Defaults to 8888.
    """
    server_address = ('', port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print(f"Health check spoofer running on port {port}...")
    httpd.serve_forever()

# --- Configuration Loading ---
CONFIG_PATH = "/opt/power_manager/config.json"
MONITORED_SERVICES = {}
last_config_mtime = 0

def load_config():
    """Loads and reloads the service monitoring configuration from a JSON file.

    This function checks if the configuration file has been modified since it
    was last read. If so, it reloads the file and updates the global
    `MONITORED_SERVICES` dictionary. This allows for dynamic updates to the
    agent's behavior without requiring a restart.
    """
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
def put_service_to_sleep(port: int):
    """Stops a Nomad job associated with an idle service.

    Args:
        port (int): The port of the idle service whose job should be stopped.
    """
    config = MONITORED_SERVICES[port]
    job_name = config["job_name"]
    print(f"Service on port {port} has been idle. Putting job '{job_name}' to sleep...")
    try:
        subprocess.run(["nomad", "job", "stop", job_name], check=True)
        config["status"] = "sleeping"
        print(f"Job '{job_name}' stopped successfully.")
    except Exception as e:
        print(f"Error stopping job '{job_name}': {e}")

def wake_service_up(port: int):
    """Starts a Nomad job for a service that has received new traffic.

    Args:
        port (int): The port of the sleeping service that needs to be woken up.
    """
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
    """The main entry point and loop for the power agent."""
    interface = os.environ.get("POWER_AGENT_INTERFACE")
    if not interface:
        print("Error: POWER_AGENT_INTERFACE environment variable not set.")
        sys.exit(1)

    # Start the health check spoofer in a separate thread
    health_server_thread = threading.Thread(target=run_health_check_server, daemon=True)
    health_server_thread.start()

    b = None
    try:
        print(f"Loading eBPF program and attaching to interface {interface}...")
        b = BPF(src_file="traffic_monitor.c")
        b.attach_xdp(dev=interface, fn=b.load_func("xdp_traffic_monitor", BPF.XDP))

        packet_counts = b.get_table("packet_counts")
        last_known_counts = {}

        print("Power agent started. Monitoring traffic...")
        print("Press Ctrl+C to exit.")

        while True:
            load_config()
            time.sleep(10)

            for port, config in MONITORED_SERVICES.items():
                if config["status"] == "running":
                    # Correctly handle ctypes instances from the BPF table
                    # Convert port to network byte order (Big Endian) to match BPF
                    # Note: BPF maps store keys in network byte order.
                    port_ns = socket.htons(port)
                    current_count_obj = packet_counts.get(ct.c_ushort(port_ns))
                    current_count = current_count_obj.value if current_count_obj else 0
                    last_count = last_known_counts.get(port, 0)

                    if current_count > last_count:
                        print(f"Traffic detected for port {port}. Resetting idle timer.")
                        config["last_traffic_time"] = time.time()
                        last_known_counts[port] = current_count
                    else:
                        idle_time = time.time() - config["last_traffic_time"]
                        if idle_time > config["idle_threshold_seconds"]:
                            put_service_to_sleep(port)

            for port, config in MONITORED_SERVICES.items():
                if config["status"] == "sleeping":
                    # Convert port to network byte order (Big Endian) to match BPF
                    # Note: BPF maps store keys in network byte order.
                    port_ns = socket.htons(port)
                    current_count_obj = packet_counts.get(ct.c_ushort(port_ns))
                    current_count = current_count_obj.value if current_count_obj else 0
                    last_count = last_known_counts.get(port, 0)
                    if current_count > last_count:
                        wake_service_up(port)
                        last_known_counts[port] = current_count

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        if b:
            print("Detaching eBPF program...")
            b.remove_xdp(dev=interface, flags=0)
        print("Power agent stopped.")

if __name__ == "__main__":
    main()
