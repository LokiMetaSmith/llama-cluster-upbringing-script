import os
import sys
import tempfile
import shutil
import asyncio
import time
import json

# Add project root and pipecatapp to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pipecatapp')))

from pipecatapp.services.obsidian_gardener import ObsidianGardener

async def run_benchmark():
    print("--- Starting Obsidian Gardener I/O Benchmark ---")
    temp_dir = tempfile.mkdtemp()

    # Create sample files
    num_files = 100
    markdown_files = []
    canvas_files = []

    for i in range(num_files):
        # Create corresponding workflow dummy yaml
        wf_path = os.path.join(temp_dir, f"workflow_{i}.yaml")
        with open(wf_path, "w", encoding="utf-8") as f:
            f.write("dummy: test")

        # Markdown file
        md_path = os.path.join(temp_dir, f"test_{i}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"#agent\nThis is markdown document {i}. Here is a directive. <!-- run: workflow_{i}.yaml -->\n")
        markdown_files.append(md_path)

        # Canvas file
        canvas_path = os.path.join(temp_dir, f"canvas_{i}.canvas")
        canvas_data = {
            "nodes": [
                {"id": "node1", "type": "text", "text": f"Some text #agent <!-- run: workflow_{i}.yaml -->", "x": 0, "y": 0, "width": 200, "height": 100},
                {"id": "node2", "type": "text", "text": "Another node", "x": 0, "y": 200, "width": 200, "height": 100}
            ]
        }
        with open(canvas_path, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f)
        canvas_files.append(canvas_path)

    from unittest.mock import MagicMock, AsyncMock
    mock_runner_instance = MagicMock()
    mock_runner_instance.run = AsyncMock(return_value={"status": "success", "data": "benchmark_test_output"})
    mock_runner_class = MagicMock(return_value=mock_runner_instance)

    gardener = ObsidianGardener(vault_path=temp_dir, workflow_runner_class=mock_runner_class)

    # Measure total execution time for parallel handling
    start_time = time.perf_counter()

    # We will trigger the handling of all these files concurrently
    tasks = []
    for md_path in markdown_files:
        tasks.append(gardener._process_markdown(md_path))
    for canvas_path in canvas_files:
        tasks.append(gardener._process_canvas(canvas_path))

    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Processed {num_files * 2} files concurrently in: {duration:.4f} seconds")

    # Clean up
    shutil.rmtree(temp_dir)
    return duration

if __name__ == "__main__":
    asyncio.run(run_benchmark())
