import argparse
import tracemalloc
import sys
import os
import json
import uuid
import time
import requests
import asyncio
import subprocess
import psutil

# Ensure the project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ElsaBot:
    def __init__(self):
        self.knowledge = "I am Elsa, a simple simulated bot testing multi-turn conversational capabilities. I generate random context."

    def generate_reply(self, incoming_msg):
        turn_id = uuid.uuid4().hex[:4]
        return f"Elsa-Response-{turn_id}: The weather is cold but the context is vast. Received: '{incoming_msg[:20]}...'"

def wait_for_server(base_url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{base_url}/health", timeout=1)
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False

def run_local_benchmark(turns):
    """
    Spins up the actual pipecatapp Uvicorn server locally as a subprocess,
    and runs the Elsa bot against it, measuring the subprocess's RSS memory usage.
    """
    print(f"Starting local benchmark simulation for {turns} turns...")

    env = os.environ.copy()
    env["TOOL_EXECUTION_MODE"] = "local"
    env["RAG_BASE_DIR"] = "/tmp/dummy"

    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "pipecatapp.web_server:app", "--port", "8007"],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    base_url = "http://127.0.0.1:8007"

    try:
        if not wait_for_server(base_url):
            print("Server failed to start within timeout.")
            return 0

        process = psutil.Process(server_process.pid)
        initial_mem = process.memory_info().rss / 10**6
        print(f"Initial Server RSS: {initial_mem:.2f} MB")

        bot = ElsaBot()
        bot_message = "Hello! Let's chat."
        headers = {}

        max_mem = initial_mem

        for i in range(turns):
            payload = {"message": bot_message}
            try:
                # Assuming /api/chat is the endpoint
                resp = requests.post(f"{base_url}/api/chat", json=payload, headers=headers, timeout=10)
                if resp.status_code == 200:
                    agent_reply = resp.json().get("response", "No response")
                else:
                    agent_reply = f"Error {resp.status_code}"
                bot_message = bot.generate_reply(agent_reply)
            except Exception as e:
                print(f"Turn {i} request failed: {e}")

            current_mem = process.memory_info().rss / 10**6
            max_mem = max(max_mem, current_mem)

            if i % max(1, turns // 5) == 0:
                print(f"Turn {i} RSS: {current_mem:.2f} MB")

        print(f"Local Benchmark Complete.")
        print(f"Peak Server RSS memory usage: {max_mem:.2f} MB")
        return max_mem

    finally:
        server_process.terminate()
        server_process.wait()

def run_remote_benchmark(turns, base_url="http://127.0.0.1:8007", api_key="dummy"):
    """
    Hits a live cluster running pipecatapp.
    """
    print(f"Starting remote benchmark against {base_url} for {turns} turns...")
    headers = {"Authorization": f"Bearer {api_key}"}
    bot = ElsaBot()
    bot_message = "Hello! Let's chat."

    try:
        health = requests.get(f"{base_url}/health", headers=headers, timeout=5)
        health.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to cluster {base_url}: {e}")
        return 0

    for i in range(turns):
        payload = {"message": bot_message}
        try:
            resp = requests.post(f"{base_url}/api/chat", json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            agent_reply = resp.json().get("response", "No response")
            bot_message = bot.generate_reply(agent_reply)
        except requests.exceptions.RequestException as e:
            print(f"Turn {i} failed: {e}")
            break

    print("Remote benchmark simulation complete.")
    return 1

def run_benchmark(mode, turns):
    if mode == "local":
        return run_local_benchmark(turns)
    elif mode == "remote":
        return run_remote_benchmark(turns)
    else:
        raise ValueError("Invalid mode")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark memory consumption of pipecatapp under multi-turn conversations.")
    parser.add_argument("--mode", type=str, choices=["local", "remote"], default="local", help="Mode to run the benchmark")
    parser.add_argument("--turns", type=int, default=10, help="Number of conversation turns to simulate")

    args = parser.parse_args()
    run_benchmark(args.mode, args.turns)
