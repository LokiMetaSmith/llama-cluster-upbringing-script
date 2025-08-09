import docker
import os
import tempfile

class CodeRunnerTool:
    def __init__(self):
        self.description = "Execute Python code in a sandboxed Docker container."
        self.name = "code_runner"
        self.client = docker.from_env()
        self.image = "python:3.9-slim"

    def run_python_code(self, code: str):
        """
        Runs a string of Python code in a secure, ephemeral Docker container and returns the output.
        """
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_file:
                tmp_file.write(code)
                tmp_file_path = tmp_file.name

            container_path = f"/tmp/{os.path.basename(tmp_file_path)}"

            container = self.client.containers.run(
                self.image,
                command=["python", container_path],
                volumes={os.path.dirname(tmp_file_path): {'bind': '/tmp', 'mode': 'ro'}},
                remove=True,
                stderr=True,
                stdout=True
            )

            output = container.decode('utf-8')
            return output

        except docker.errors.ImageNotFound:
            return f"Error: The Docker image '{self.image}' was not found. Please pull it first."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
