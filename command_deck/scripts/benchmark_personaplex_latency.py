import asyncio
import websockets
import json
import binascii
import time
import statistics
import argparse

class LatencyBenchmarker:
    def __init__(self, uri="ws://localhost:8080/stream", iterations=10, timeout=5.0):
        self.uri = uri
        self.iterations = iterations
        self.timeout = timeout
        self.latencies = []

    async def run_benchmark(self):
        print(f"Starting latency benchmark to {self.uri} for {self.iterations} iterations...")

        # Simulated audio payload (e.g., 20ms of silence at 48kHz, 1 channel, 16-bit)
        # 960 frames * 2 bytes = 1920 bytes of zeros. We hex encode it.
        pcm_data = b'\x00' * 1920
        hex_data = binascii.hexlify(pcm_data).decode('utf-8')
        payload = json.dumps({"type": "audio", "data": hex_data})

        try:
            async with websockets.connect(self.uri) as websocket:
                for i in range(self.iterations):
                    start_time = time.perf_counter()

                    await websocket.send(payload)

                    # Wait for response
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=self.timeout)
                        end_time = time.perf_counter()
                        data = json.loads(response)
                        if data.get("type") == "audio":
                            latency_ms = (end_time - start_time) * 1000
                            self.latencies.append(latency_ms)
                            print(f"Iteration {i+1}: {latency_ms:.2f} ms")
                        else:
                            print(f"Iteration {i+1}: Received non-audio response")
                    except asyncio.TimeoutError:
                        print(f"Iteration {i+1}: Timeout after {self.timeout}s")

                    # Wait a bit before next iteration
                    await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Connection failed: {e}")
            return

        self.print_statistics()

    def print_statistics(self):
        if not self.latencies:
            print("No successful iterations to calculate statistics.")
            return

        min_lat = min(self.latencies)
        max_lat = max(self.latencies)
        avg_lat = statistics.mean(self.latencies)

        # Calculate p95
        sorted_lats = sorted(self.latencies)
        idx = int(0.95 * len(sorted_lats))
        p95_lat = sorted_lats[idx] if idx < len(sorted_lats) else sorted_lats[-1]

        print("\n--- Latency Benchmark Results ---")
        print(f"Iterations: {len(self.latencies)}/{self.iterations}")
        print(f"Min: {min_lat:.2f} ms")
        print(f"Max: {max_lat:.2f} ms")
        print(f"Avg: {avg_lat:.2f} ms")
        print(f"p95: {p95_lat:.2f} ms")

        if p95_lat <= 200.0:
            print("Status: PASS (p95 latency is within the 200ms budget)")
        else:
            print("Status: FAIL (p95 latency exceeds the 200ms budget)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark PersonaPlex Streaming Latency")
    parser.add_argument("--uri", type=str, default="ws://localhost:8080/stream", help="WebSocket URI")
    parser.add_argument("--iterations", type=int, default=10, help="Number of benchmark iterations")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout per request in seconds")
    args = parser.parse_args()

    benchmarker = LatencyBenchmarker(uri=args.uri, iterations=args.iterations, timeout=args.timeout)
    asyncio.run(benchmarker.run_benchmark())
