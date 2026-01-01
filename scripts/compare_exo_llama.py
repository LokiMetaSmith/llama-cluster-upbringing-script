import argparse
import time
import requests
import json
import sys
from datetime import datetime

# Helper to print colored output
def print_color(text, color="white"):
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "bold": "\033[1m",
        "reset": "\033[0m"
    }
    sys.stdout.write(f"{colors.get(color, '')}{text}{colors['reset']}\n")

def check_health(url, name):
    print(f"Checking health of {name} at {url}...")
    try:
        # Exo and standard OpenAI compatible endpoints often have a /v1/models or similar
        # But a simple GET to root might not work.
        # Let's try listing models as a health check.
        response = requests.get(f"{url}/v1/models", timeout=5)
        if response.status_code == 200:
            print_color(f"✅ {name} is healthy.", "green")
            return True
        else:
            print_color(f"❌ {name} returned status {response.status_code}.", "red")
            return False
    except Exception as e:
        print_color(f"❌ {name} is unreachable: {e}", "red")
        return False

def run_inference(url, model, prompt, name):
    print(f"\nRunning inference on {name} ({url}) with model '{model}'...")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "max_tokens": 512
    }

    start_time = time.time()
    first_token_time = None
    token_count = 0
    full_response = ""

    try:
        response = requests.post(f"{url}/v1/chat/completions", json=payload, stream=True, timeout=120)

        if response.status_code != 200:
            print_color(f"❌ Inference failed with status {response.status_code}: {response.text}", "red")
            return None

        print_color("Streaming response...", "blue")
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                if first_token_time is None:
                                    first_token_time = time.time()
                                full_response += content
                                token_count += 1
                                sys.stdout.write(content)
                                sys.stdout.flush()
                    except json.JSONDecodeError:
                        pass

        end_time = time.time()
        print("\n")

        if first_token_time is None:
             first_token_time = end_time # Fallback if no tokens

        ttft = (first_token_time - start_time) * 1000 # ms
        total_time = end_time - start_time
        tps = token_count / total_time if total_time > 0 else 0

        metrics = {
            "name": name,
            "ttft_ms": ttft,
            "total_time_s": total_time,
            "tokens": token_count,
            "tps": tps
        }

        print_color(f"✅ Inference Complete:", "green")
        print(f"  - TTFT: {ttft:.2f} ms")
        print(f"  - TPS: {tps:.2f} tokens/sec")
        print(f"  - Total Tokens: {token_count}")

        return metrics

    except Exception as e:
        print_color(f"❌ Error during inference: {e}", "red")
        return None

def main():
    parser = argparse.ArgumentParser(description="Compare Exo vs Llama.cpp performance")
    parser.add_argument("--exo-url", default="http://localhost:52415", help="URL for Exo API")
    parser.add_argument("--llama-url", default="http://localhost:8081", help="URL for Llama.cpp API")
    parser.add_argument("--exo-model", default="llama-3.2-1b", help="Model name for Exo")
    parser.add_argument("--llama-model", default="main", help="Model name for Llama.cpp (expert name)")
    parser.add_argument("--prompt", default="Write a Python function to implement Bubble Sort.", help="Prompt to test")
    parser.add_argument("--runs", type=int, default=3, help="Number of runs to average")

    args = parser.parse_args()

    print_color("🚀 Starting Benchmark: Exo vs Llama.cpp", "bold")
    print(f"Exo URL: {args.exo_url} (Model: {args.exo_model})")
    print(f"Llama URL: {args.llama_url} (Model: {args.llama_model})")

    # 1. Health Checks
    exo_healthy = check_health(args.exo_url, "Exo")
    llama_healthy = check_health(args.llama_url, "Llama.cpp")

    results = []

    if exo_healthy:
        print_color("\n--- Testing Exo ---", "bold")
        for i in range(args.runs):
            print(f"Run {i+1}/{args.runs}")
            m = run_inference(args.exo_url, args.exo_model, args.prompt, "Exo")
            if m: results.append(m)
            time.sleep(1)

    if llama_healthy:
        print_color("\n--- Testing Llama.cpp ---", "bold")
        for i in range(args.runs):
             print(f"Run {i+1}/{args.runs}")
             m = run_inference(args.llama_url, args.llama_model, args.prompt, "Llama.cpp")
             if m: results.append(m)
             time.sleep(1)

    # Report
    print_color("\n📊 Benchmark Results", "bold")
    print(f"{'Service':<15} | {'Avg TTFT (ms)':<15} | {'Avg TPS':<15} | {'Total Runs':<10}")
    print("-" * 65)

    for name in ["Exo", "Llama.cpp"]:
        service_results = [r for r in results if r["name"] == name]
        if service_results:
            avg_ttft = sum(r["ttft_ms"] for r in service_results) / len(service_results)
            avg_tps = sum(r["tps"] for r in service_results) / len(service_results)
            print(f"{name:<15} | {avg_ttft:<15.2f} | {avg_tps:<15.2f} | {len(service_results):<10}")
        else:
             print(f"{name:<15} | {'N/A':<15} | {'N/A':<15} | 0")

    # Decision Matrix
    print_color("\n📝 Evaluation & Decision Matrix", "bold")
    print("Based on the observed performance:")

    exo_res = [r for r in results if r["name"] == "Exo"]
    llama_res = [r for r in results if r["name"] == "Llama.cpp"]

    if exo_res and llama_res:
        avg_exo_tps = sum(r["tps"] for r in exo_res) / len(exo_res)
        avg_llama_tps = sum(r["tps"] for r in llama_res) / len(llama_res)

        if avg_exo_tps > avg_llama_tps * 1.1:
             print_color("🚀 Exo is significantly faster (>10%) than Llama.cpp.", "green")
        elif avg_llama_tps > avg_exo_tps * 1.1:
             print_color("🐢 Exo is significantly slower (>10%) than Llama.cpp.", "yellow")
        else:
             print_color("⚖️ Performance is comparable (within 10%).", "blue")

    elif not exo_res:
        print_color("⚠️ Exo tests failed or service was unreachable.", "red")
    elif not llama_res:
         print_color("⚠️ Llama.cpp tests failed or service was unreachable.", "red")

if __name__ == "__main__":
    main()
