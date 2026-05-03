import extism
import json
import sys
import os
import tracemalloc
import time

def run_wasm(action, text):
    # Path to the compiled wasm file
    wasm_path = os.path.join(os.path.dirname(__file__), "text_processor/target/wasm32-wasip1/release/text_processor.wasm")

    # Create the Extism plugin using a manifest dictionary as expected by the SDK
    manifest = {"wasm": [{"path": wasm_path}]}
    plugin = extism.Plugin(manifest, wasi=True)

    # Prepare input data
    input_data = json.dumps({
        "action": action,
        "text": text
    })

    # Call the plugin function
    result = plugin.call("process_text", input_data)

    # Parse and return output
    return json.loads(result)["result"]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python host.py <action> <text>")
        sys.exit(1)

    action = sys.argv[1]
    text = sys.argv[2]

    tracemalloc.start()
    start_time = time.time()

    result = run_wasm(action, text)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Result: {result}")
    print(f"Execution time: {(end_time - start_time) * 1000:.2f} ms")
    print(f"Peak memory usage: {peak / 10**6:.3f} MB")
