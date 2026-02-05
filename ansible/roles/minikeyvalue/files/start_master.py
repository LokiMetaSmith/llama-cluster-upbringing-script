#!/usr/bin/env python3
import os
import time
import requests
import subprocess
import sys

CONSUL_ADDR = os.environ.get("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")
SERVICE_NAME = "mkv-volume"
REQUIRED_VOLUMES = int(os.environ.get("MKV_REPLICAS", "1"))

def get_service_nodes():
    try:
        url = f"{CONSUL_ADDR}/v1/catalog/service/{SERVICE_NAME}"
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error querying Consul: {e}")
        return []

def main():
    print("Waiting for volume servers...")
    nodes = []
    while len(nodes) < REQUIRED_VOLUMES:
        nodes = get_service_nodes()
        print(f"Found {len(nodes)}/{REQUIRED_VOLUMES} volume servers.")
        if len(nodes) < REQUIRED_VOLUMES:
            time.sleep(2)

    # Construct volumes string
    # Format: host:port,host:port
    volume_list = []
    for node in nodes:
        # Prefer ServiceAddress, then Address
        addr = node.get("ServiceAddress") or node.get("Address")
        port = node.get("ServicePort")
        volume_list.append(f"{addr}:{port}")

    volumes_arg = ",".join(volume_list)
    print(f"Starting MKV Master with volumes: {volumes_arg}")

    cmd = [
        "/app/mkv",
        "-volumes", volumes_arg,
        "-db", "/data/indexdb",
        "-replicas", str(REQUIRED_VOLUMES),
        "server"
    ]

    # Execute replaces the current process
    os.execv(cmd[0], cmd)

if __name__ == "__main__":
    main()
