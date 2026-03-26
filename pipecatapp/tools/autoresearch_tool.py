import json
import os
import time
import logging
import asyncio
import shutil
import tempfile
import subprocess
import shlex
import docker
from typing import List, Dict, Any, Optional

class AutoresearchTool:
    """
    A tool that performs an iterative, autonomous code optimization loop (Autoresearch).
    It continuously hypothesizes, edits a specific target file, runs a test/evaluation command
    in an isolated sandbox, and commits or reverts the change based on the evaluation outcome.
    """
    def __init__(self, llm_client: Any = None):
        self.logger = logging.getLogger(__name__)
        # The LLM client to be used for generating code mutations
        self.llm_client = llm_client
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            self.logger.warning(f"Could not initialize Docker client for AutoresearchTool: {e}")
            self.docker_client = None

    async def run(self,
                  target_file: str,
                  test_command: str,
                  program_instructions: str,
                  max_iterations: int = 5,
                  eval_metric: str = "exit_code") -> str:
        """
        Runs the Autoresearch loop.

        Args:
            target_file (str): The specific file to mutate in each iteration (e.g. 'train.py').
            test_command (str): Shell command to verify the solution (e.g., 'pytest tests/').
            program_instructions (str): The constraints, phases, or goals for the LLM to follow (e.g. contents of 'program.md').
            max_iterations (int): Maximum number of hypothesize -> edit -> eval loops to run.
            eval_metric (str): How to evaluate success. Defaults to "exit_code" (0 = pass). Future extensions could parse a float metric from stdout.

        Returns:
            str: JSON summary of the autoresearch results, including the final scratchpad and best code artifact.
        """
        self.logger.info(f"Starting Autoresearch on {target_file} for {max_iterations} iterations.")

        # Read the current target file content
        if not os.path.exists(target_file):
            return json.dumps({"error": f"Target file {target_file} does not exist."})

        with open(target_file, 'r') as f:
            original_code = f.read()

        current_best_code = original_code

        # Initialize the scratchpad
        scratchpad = []
        scratchpad.append(f"Goal: {program_instructions}")
        scratchpad.append(f"Target File: {target_file}")
        scratchpad.append(f"Evaluation Command: {test_command}")

        # Setup the source directory based on where target_file lives to ensure proper context
        # Determine the root directory. This is tricky, but often it's the current working directory,
        # or the root of the project where `target_file` resides.
        # We will use the current working directory as the sandbox root unless target_file is absolute,
        # in which case we might need to find a suitable project root (like where .git is).
        # For simplicity and security, we'll snapshot the current working directory, and expect target_file
        # to be relative to it. If it's absolute, we try to make it relative.

        target_file_abs = os.path.realpath(target_file)
        src_dir = os.getcwd()

        # Optimization: Create a source snapshot once to avoid repeatedly copying thousands of files.
        snapshot_path = self._create_snapshot(src_dir)

        # Make target_file relative to src_dir for the sandbox mapping
        if os.path.isabs(target_file):
            try:
                rel_target_file = os.path.relpath(target_file_abs, src_dir)
            except ValueError:
                # If it's on a different drive or impossible to make relative, just use the basename
                rel_target_file = os.path.basename(target_file_abs)
        else:
            rel_target_file = target_file

        experiment_history = []

        try:
            for iteration in range(1, max_iterations + 1):
                self.logger.info(f"Autoresearch Iteration {iteration}/{max_iterations}")

                # 1. Hypothesize / Edit (Call LLM to generate new code)
                # Build the prompt with instructions and history
                history_text = "\n".join(scratchpad[-10:]) # Keep context manageable
                prompt = f"""
You are an AI research assistant running an Autoresearch loop.
Your task is to modify the source code of `{target_file}` to improve it based on the following instructions:
{program_instructions}

Here is the history of previous experiments (Scratchpad):
{history_text}

Here is the current best version of `{target_file}`:
```python
{current_best_code}
```

Please provide the ENTIRE updated content for `{target_file}` that implements your next hypothesis.
Do not wrap it in markdown block quotes, just output the raw code. Or if you do, I will extract it.
Think step-by-step first, then provide the final file content under a `<final_code>` tag.
"""

                # Simulated LLM Call (In a real scenario we'd use self.llm_client.generate(prompt))
                # For this tool implementation, we assume we have a simple function to call an LLM.
                try:
                    llm_response = await self._call_llm(prompt)
                    new_code = self._extract_code(llm_response)

                    if not new_code:
                        scratchpad.append(f"Iteration {iteration}: Failed to extract code from LLM response. Reverting.")
                        experiment_history.append({"iteration": iteration, "status": "failed_extraction"})
                        continue

                except Exception as e:
                    self.logger.error(f"LLM Generation failed: {e}")
                    scratchpad.append(f"Iteration {iteration}: LLM Generation Error: {e}")
                    experiment_history.append({"iteration": iteration, "status": "llm_error"})
                    continue

                # 2. Evaluate (Run in sandbox)
                artifact = {
                    "file_path": rel_target_file,
                    "content": new_code
                }

                eval_result = await asyncio.to_thread(self._run_sandbox_eval, artifact, test_command, snapshot_path)

                # 3. Commit or Revert
                passed = eval_result["passed"]
                output = eval_result["output"]

                # Truncate output for scratchpad if too long
                short_output = output[:500] + ("..." if len(output) > 500 else "")

                if passed:
                    self.logger.info(f"Iteration {iteration}: Success! Committing changes.")
                    current_best_code = new_code
                    scratchpad.append(f"Iteration {iteration}: SUCCESS. Code committed. Output:\n{short_output}")
                    experiment_history.append({
                        "iteration": iteration,
                        "status": "committed",
                        "output": short_output
                    })
                else:
                    self.logger.info(f"Iteration {iteration}: Failed. Reverting changes.")
                    scratchpad.append(f"Iteration {iteration}: FAILED. Code reverted. Output:\n{short_output}")
                    experiment_history.append({
                        "iteration": iteration,
                        "status": "reverted",
                        "output": short_output
                    })

        finally:
            if snapshot_path and os.path.exists(snapshot_path):
                os.remove(snapshot_path)

        # Output the best code to the actual file if it changed
        if current_best_code != original_code:
            try:
                with open(target_file, 'w') as f:
                    f.write(current_best_code)
                self.logger.info(f"Successfully wrote best code back to {target_file}")
            except Exception as e:
                self.logger.error(f"Failed to write final code to {target_file}: {e}")

        summary = {
            "target_file": target_file,
            "total_iterations": max_iterations,
            "history": experiment_history,
            "final_scratchpad": scratchpad,
            "code_changed": current_best_code != original_code
        }

        return json.dumps(summary, indent=2)

    async def _call_llm(self, prompt: str) -> str:
        """
        Calls the LLM to generate the next iteration.
        In the Pipecat context, this would typically use a configured LLM node/service.
        For the standalone tool, we use the global configuration or a basic prompt.
        """
        # We need a generic way to call the LLM. If an LLM client was provided during init, use it.
        if self.llm_client and hasattr(self.llm_client, "generate"):
             # Adapting to typical async LLM clients
             if asyncio.iscoroutinefunction(self.llm_client.generate):
                 return await self.llm_client.generate(prompt)
             else:
                 return self.llm_client.generate(prompt)

        # Fallback to invoking a standard local endpoint if no client injected
        # In this ecosystem, often tools run locally and talk to an OpenAI-compatible endpoint
        # or the TwinService handles the LLM.
        # For simplicity, if no client, we raise an error requesting one, or return a stub.
        raise ValueError("No LLM client provided to AutoresearchTool. Please provide an LLM client capable of text generation.")

    def _extract_code(self, response: str) -> Optional[str]:
        """Extracts the code block from the LLM response."""
        # Try to find <final_code> tags
        if "<final_code>" in response and "</final_code>" in response:
            start = response.find("<final_code>") + len("<final_code>")
            end = response.find("</final_code>")
            return response[start:end].strip()

        # Fallback to standard markdown python code block
        if "```python" in response:
            parts = response.split("```python")
            if len(parts) > 1:
                code_part = parts[1].split("```")[0]
                return code_part.strip()

        # If no tags, assume the whole response is the code (risky, but sometimes happens)
        if "def " in response or "import " in response:
             return response.strip()

        return None

    def _validate_path(self, root_dir: str, filepath: str) -> str:
        """Ensures the filepath is within the root directory."""
        root_dir = os.path.realpath(root_dir)

        # Handle absolute paths by stripping leading slash
        if os.path.isabs(filepath):
            filepath = filepath.lstrip(os.sep)

        full_path = os.path.join(root_dir, filepath)
        full_path = os.path.realpath(full_path)

        try:
            common = os.path.commonpath([root_dir, full_path])
        except ValueError:
            common = ""

        if common != root_dir:
            raise ValueError(f"Access denied: {filepath} is outside the sandbox.")

        return full_path

    def _create_snapshot(self, src_dir: str) -> Optional[str]:
        """Creates a tar snapshot of the source directory to speed up sandbox creation."""
        if not os.path.exists(src_dir):
            return None

        try:
            fd, archive_path = tempfile.mkstemp(suffix=".tar")
            os.close(fd)

            cmd = [
                "tar",
                "-cf", archive_path,
                "-C", src_dir,
                "--exclude", ".git",
                "--exclude", "__pycache__",
                "--exclude", "node_modules",
                "--exclude", "*.pyc",
                "."
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return archive_path
        except Exception as e:
            self.logger.error(f"Failed to create snapshot: {e}")
            if 'archive_path' in locals() and os.path.exists(archive_path):
                os.remove(archive_path)
            return None

    def _run_sandbox_eval(self, artifact: Dict, test_command: str, snapshot_path: Optional[str] = None) -> Dict:
        """Runs the artifact in a Docker container sandbox against the test command."""
        if not self.docker_client:
            # Fallback to local subprocess if docker is unavailable
            return self._run_sandbox_eval_local(artifact, test_command, snapshot_path)

        temp_dir = tempfile.mkdtemp(prefix="pipecat_autoresearch_")

        try:
            # Populate Temp Directory Host-Side
            if snapshot_path and os.path.exists(snapshot_path):
                 cmd = ["tar", "-xf", snapshot_path, "-C", temp_dir]
                 subprocess.run(cmd, check=True, capture_output=True)
            else:
                 src_dir = os.getcwd() # Fallback to current working dir
                 shutil.copytree(src_dir, temp_dir, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns('.git', '__pycache__', 'node_modules', '*.pyc'))

            # Apply Artifact (The modified file)
            file_path = artifact.get("file_path", "target.py")
            try:
                full_path = self._validate_path(temp_dir, file_path)
            except ValueError as e:
                return {"passed": False, "output": f"Security Error: {e}"}

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            content = artifact.get("content", "")

            # Security Fix: Sentinel - Prevent DoS via large file
            if len(content) > 1024 * 1024:
                return {"passed": False, "output": "Security Error: Artifact too large (>1MB)."}

            with open(full_path, 'w') as f:
                f.write(content)

            # Run Command in Docker
            container_workdir = "/workspace"
            volumes = {
                os.path.abspath(temp_dir): {
                    'bind': container_workdir,
                    'mode': 'rw'
                }
            }

            # Using python:3.12-slim as a safe base image
            try:
                # Wrap test command in a timeout directly in the shell
                # Use shlex to safely pass the test_command into bash
                safe_command = ["timeout", "60s", "bash", "-c", test_command]

                result = self.docker_client.containers.run(
                    "python:3.12-slim",
                    command=safe_command,
                    volumes=volumes,
                    working_dir=container_workdir,
                    environment={"PYTHONPATH": container_workdir},
                    remove=True,
                    stderr=True,
                    stdout=True
                )
                output = result.decode('utf-8')
                return {
                    "passed": True,
                    "output": output
                }
            except docker.errors.ContainerError as e:
                output = e.stderr.decode('utf-8') if e.stderr else ""
                if "Terminated" in output or "Killed" in output or e.exit_status == 124: # timeout exit code
                    output = "Execution timed out after 60 seconds."
                return {
                    "passed": False,
                    "output": output
                }
            except Exception as e:
                 return {"passed": False, "output": f"Docker execution error: {str(e)}"}

        except Exception as e:
            return {"passed": False, "output": f"Error setting up sandbox: {e}"}
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _run_sandbox_eval_local(self, artifact: Dict, test_command: str, snapshot_path: Optional[str] = None) -> Dict:
        """Fallback for running the artifact locally without docker."""
        temp_dir = tempfile.mkdtemp(prefix="pipecat_autoresearch_")

        try:
            # Populate Sandbox
            if snapshot_path and os.path.exists(snapshot_path):
                 cmd = ["tar", "-xf", snapshot_path, "-C", temp_dir]
                 subprocess.run(cmd, check=True, capture_output=True)
            else:
                 src_dir = os.getcwd() # Fallback to current working dir
                 shutil.copytree(src_dir, temp_dir, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns('.git', '__pycache__', 'node_modules', '*.pyc'))

            # Apply Artifact (The modified file)
            file_path = artifact.get("file_path", "target.py")
            try:
                full_path = self._validate_path(temp_dir, file_path)
            except ValueError as e:
                return {"passed": False, "output": f"Security Error: {e}"}

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            content = artifact.get("content", "")

            # Security Fix: Sentinel - Prevent DoS via large file
            if len(content) > 1024 * 1024:
                return {"passed": False, "output": "Security Error: Artifact too large (>1MB)."}

            with open(full_path, 'w') as f:
                f.write(content)

            # Run Command
            env = os.environ.copy()
            env["PYTHONPATH"] = temp_dir

            cmd_args = shlex.split(test_command)

            result = subprocess.run(
                cmd_args,
                cwd=temp_dir,
                shell=False,
                capture_output=True,
                text=True,
                timeout=60,
                env=env
            )

            passed = (result.returncode == 0)
            return {
                "passed": passed,
                "output": result.stdout + "\n" + result.stderr
            }

        except Exception as e:
            return {"passed": False, "output": f"Sandbox error: {str(e)}"}
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    # Simple self-test mock
    class MockLLM:
        def generate(self, prompt):
            return "<final_code>\nprint('Hello Autoresearch')\n</final_code>"

    async def main():
        tool = AutoresearchTool(llm_client=MockLLM())
        # create dummy target
        with open("dummy_target.py", "w") as f:
            f.write("print('Hello World')")

        res = await tool.run(
            target_file="dummy_target.py",
            test_command="python dummy_target.py",
            program_instructions="Make it say Hello Autoresearch",
            max_iterations=1
        )
        print(res)
        os.remove("dummy_target.py")

    asyncio.run(main())
