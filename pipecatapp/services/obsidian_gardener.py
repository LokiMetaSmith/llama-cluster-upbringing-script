import os
import time
import logging
import asyncio
import re
import json
import uuid
import aiofiles
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pipecatapp.workflow.canvas_converter import CanvasConverter

logger = logging.getLogger(__name__)

class ObsidianGardener(FileSystemEventHandler):
    def __init__(self, vault_path: str, workflow_runner_class=None):
        self.vault_path = vault_path
        self.observer = Observer()
        self._is_running = False
        self.workflow_runner_class = workflow_runner_class

        # Prevent processing the same file multiple times in quick succession
        self._last_processed = {}
        self._debounce_seconds = 2.0

    def _should_process(self, filepath: str) -> bool:
        now = time.time()
        last_time = self._last_processed.get(filepath, 0)
        if now - last_time > self._debounce_seconds:
            self._last_processed[filepath] = now
            return True
        return False

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md') or event.src_path.endswith('.canvas'):
            if self._should_process(event.src_path):
                logger.info(f"Detected modification in: {event.src_path}")
                # We offload to an asyncio task since watchdog events are sync
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(self._handle_file_change(event.src_path))
                except RuntimeError:
                    # In case there's no running loop in this thread
                    asyncio.run(self._handle_file_change(event.src_path))

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md') or event.src_path.endswith('.canvas'):
             if self._should_process(event.src_path):
                logger.info(f"Detected creation of: {event.src_path}")
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(self._handle_file_change(event.src_path))
                except RuntimeError:
                    asyncio.run(self._handle_file_change(event.src_path))

    async def _handle_file_change(self, filepath: str):
        """Parse file for directives and execute workflows if needed."""
        try:
            if filepath.endswith('.md'):
                await self._process_markdown(filepath)
            elif filepath.endswith('.canvas'):
                await self._process_canvas(filepath)
        except Exception as e:
            logger.error(f"Error processing file {filepath}: {e}")

    async def _process_markdown(self, filepath: str):
        """Process markdown file for seeds and directives."""
        try:
            async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
        except Exception as e:
            logger.error(f"Could not read {filepath}: {e}")
            return

        # Simple seed tag logic: #agent
        if "#agent" not in content:
            return

        # Find directives like <!-- run: my_workflow.yaml -->
        directive_pattern = r'<!--\s*run:\s*(.*?)\s*-->'
        matches = re.finditer(directive_pattern, content)

        for match in matches:
            workflow_name = match.group(1).strip()

            # To avoid infinite loops, check if we already processed this
            processed_marker = f"<!-- done: {workflow_name} -->"
            if processed_marker in content:
                continue

            logger.info(f"Found directive to run workflow: {workflow_name} in {filepath}")

            if self.workflow_runner_class:
                try:
                    # Execute the workflow
                    workflow_path = os.path.join(os.path.dirname(filepath), workflow_name)
                    if not os.path.exists(workflow_path):
                         # Fallback to default workflow dir if not relative to vault
                         workflow_path = os.path.join("workflows", workflow_name)

                    if os.path.exists(workflow_path):
                        runner = self.workflow_runner_class(workflow_path)
                        result = await runner.run({"filepath": filepath, "content": content})

                        # Append result back to file
                        await self._append_result_to_markdown(filepath, workflow_name, result)
                    else:
                        logger.error(f"Workflow not found: {workflow_path}")
                except Exception as e:
                    logger.error(f"Failed to execute workflow {workflow_name}: {e}")

    async def _append_result_to_markdown(self, filepath: str, workflow_name: str, result: dict):
        """Appends the workflow execution result back to the markdown file."""
        try:
             async with aiofiles.open(filepath, 'a', encoding='utf-8') as f:
                 await f.write(f"\n\n<!-- done: {workflow_name} -->\n")
                 await f.write(f"### Result from {workflow_name}\n")
                 await f.write(f"```json\n{result}\n```\n")
             logger.info(f"Appended results to {filepath}")
        except Exception as e:
             logger.error(f"Failed to write results to {filepath}: {e}")

    async def _process_canvas(self, filepath: str):
        """Process canvas file using CanvasConverter logic to execute active nodes."""
        try:
            async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
                canvas_data = json.loads(content)
        except Exception as e:
            logger.error(f"Could not read canvas {filepath}: {e}")
            return

        # Simple seed logic: Does any node mention "#agent" or a run directive?
        should_run = False
        workflow_name = None
        for node in canvas_data.get("nodes", []):
            if node.get("type") == "text":
                text = node.get("text", "")
                if "#agent" in text:
                    should_run = True

                # Check for run directive
                match = re.search(r'<!--\s*run:\s*(.*?)\s*-->', text)
                if match:
                    workflow_name = match.group(1).strip()
                    should_run = True

                # Check if it was already processed to avoid loops
                if "<!-- done: canvas -->" in text or (workflow_name and f"<!-- done: {workflow_name} -->" in text):
                    should_run = False
                    break

        if not should_run:
            return

        logger.info(f"Found active directive in canvas: {filepath}")

        result = None
        if workflow_name and self.workflow_runner_class:
            try:
                workflow_path = os.path.join(os.path.dirname(filepath), workflow_name)
                if not os.path.exists(workflow_path):
                    workflow_path = os.path.join("workflows", workflow_name)

                if os.path.exists(workflow_path):
                    runner = self.workflow_runner_class(workflow_path)
                    # Pass the canvas file path as input context
                    result = await runner.run({"filepath": filepath, "source_type": "canvas"})
                else:
                    logger.error(f"Workflow not found: {workflow_path}")
            except Exception as e:
                logger.error(f"Failed to execute workflow {workflow_name} from canvas: {e}")
        else:
            # Native Canvas Workflow Execution
            # Convert canvas to Pipecat Workflow Dictionary
            workflow_dict = CanvasConverter.canvas_to_workflow(filepath)
            if workflow_dict and self.workflow_runner_class:
                # To execute this dynamically, we can write it to a temporary yaml, or
                # since WorkflowRunner expects a file path, we'll serialize to a temp YAML file.
                import yaml
                import tempfile

                with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w") as tmp:
                    yaml.dump(workflow_dict, tmp)
                    tmp_path = tmp.name

                try:
                    runner = self.workflow_runner_class(tmp_path)
                    result = await runner.run({"filepath": filepath, "source_type": "canvas_native"})
                except Exception as e:
                    logger.error(f"Failed to execute native canvas workflow: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

        if result is not None:
            await self._append_result_to_canvas(filepath, workflow_name or "canvas", result)

    async def _append_result_to_canvas(self, filepath: str, workflow_name: str, result: dict):
        """Appends the workflow execution result back to the canvas file as a new node."""
        try:
            async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
                canvas_data = json.loads(content)

            # Create a new text node with the result
            new_node = {
                "id": str(uuid.uuid4()),
                "type": "text",
                "text": f"### Result from {workflow_name}\n<!-- done: {workflow_name} -->\n```json\n{json.dumps(result, indent=2)}\n```",
                "x": 100,
                "y": 100, # Ideally we calculate a good position, but top-left is ok for now
                "width": 600,
                "height": 400,
                "color": "3" # Greenish in Obsidian
            }

            # Find a good y position below existing nodes
            max_y = 0
            for node in canvas_data.get("nodes", []):
                y = node.get("y", 0) + node.get("height", 0)
                if y > max_y:
                    max_y = y

            new_node["y"] = max_y + 50
            new_node["x"] = 0

            canvas_data.setdefault("nodes", []).append(new_node)

            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(canvas_data, indent=2))

            logger.info(f"Appended results to canvas {filepath}")
        except Exception as e:
            logger.error(f"Failed to write results to canvas {filepath}: {e}")

    def start(self):
        if not os.path.exists(self.vault_path):
            logger.error(f"Vault path does not exist: {self.vault_path}")
            return

        self.observer.schedule(self, self.vault_path, recursive=True)
        self.observer.start()
        self._is_running = True
        logger.info(f"Started Obsidian Gardener monitoring: {self.vault_path}")

    def stop(self):
        if self._is_running:
            self.observer.stop()
            self.observer.join()
            self._is_running = False
            logger.info("Stopped Obsidian Gardener")
