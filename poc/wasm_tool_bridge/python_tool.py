import json
import sys
import tracemalloc
import time

def process_text(action, text):
    if action == "uppercase":
        return text.upper()
    elif action == "lowercase":
        return text.lower()
    elif action == "reverse":
        return text[::-1]
    else:
        return f"Unknown action: {action}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python python_tool.py <action> <text>")
        sys.exit(1)

    action = sys.argv[1]
    text = sys.argv[2]

    tracemalloc.start()
    start_time = time.time()

    result = process_text(action, text)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Result: {result}")
    print(f"Execution time: {(end_time - start_time) * 1000:.2f} ms")
    print(f"Peak memory usage: {peak / 10**6:.3f} MB")
