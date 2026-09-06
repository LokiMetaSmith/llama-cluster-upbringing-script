import os
import json
import logging
from openai import AsyncOpenAI
import re

class ShuntTool:
    """A tool that shunts I/O-heavy work to cheaper, local 'trivial' tier models.

    This saves context tokens on the main agent. It delegates tasks like
    reading large files (bulk_read) and generating boilerplate code (code_write)
    to a lightweight worker model via the MoE Gateway.
    """
    def __init__(self, root_dir="/opt/pipecatapp", gateway_url="http://localhost:8081/v1"):
        self.name = "shunt"
        self.root_dir = os.path.realpath(root_dir)
        self.logger = logging.getLogger(__name__)
        self.gateway_url = gateway_url

        # Use a dummy API key since we're pointing to the local router/gateway
        self.client = AsyncOpenAI(base_url=self.gateway_url, api_key="dummy")

    def get_schema(self) -> dict:
        """Returns the schema for the shunt tool."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Delegates I/O-heavy file reading and code generation tasks to a cheaper worker model to save your context space.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["bulk_read", "code_write"],
                            "description": "The delegation action to perform."
                        },
                        "paths": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of file paths to read (for bulk_read action)."
                        },
                        "question": {
                            "type": "string",
                            "description": "The question to ask about the files (for bulk_read action)."
                        },
                        "spec": {
                            "type": "string",
                            "description": "Specification for the code to generate (for code_write action)."
                        },
                        "reference": {
                            "type": "string",
                            "description": "Path to a reference file to match patterns against (for code_write action)."
                        },
                        "target": {
                            "type": "string",
                            "description": "Path to write the generated code to (for code_write action)."
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def _validate_path(self, filepath: str) -> str:
        """Ensures the filepath is within the root directory."""
        if not os.path.isabs(filepath):
            full_path = os.path.join(self.root_dir, filepath)
        else:
            full_path = filepath
        real_path = os.path.realpath(full_path)
        if not real_path.startswith(os.path.realpath(self.root_dir)):
            raise ValueError(f"Path traversal detected: {filepath}")
        return real_path

    def _read_file_content(self, filepath: str) -> str:
        """Reads file content safely."""
        path = self._validate_path(filepath)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: File not found at {filepath}"
        except Exception as e:
            return f"Error reading {filepath}: {str(e)}"

    def _strip_markdown_fences(self, text: str) -> str:
        """Removes markdown code fences from generated code."""
        # Remove starting fences like ```python or ```
        text = re.sub(r'^```[a-zA-Z]*\n', '', text, flags=re.MULTILINE)
        # Remove ending fences
        text = re.sub(r'```$', '', text, flags=re.MULTILINE)
        return text.strip()

    async def execute(self, action: str, **kwargs) -> str:
        """Executes the shunt action."""
        if action == "bulk_read":
            paths = kwargs.get("paths", [])
            question = kwargs.get("question", "")

            if not paths or not question:
                return "Error: 'paths' and 'question' are required for bulk_read."

            return await self._bulk_read(paths, question)

        elif action == "code_write":
            spec = kwargs.get("spec", "")
            reference = kwargs.get("reference", "")
            target = kwargs.get("target", "")

            if not spec or not reference or not target:
                return "Error: 'spec', 'reference', and 'target' are required for code_write."

            return await self._code_write(spec, reference, target)

        else:
            return f"Error: Unknown action {action}"

    async def _bulk_read(self, paths: list, question: str) -> str:
        """Delegates file reading to a worker model."""
        file_contents = []
        for path in paths:
            content = self._read_file_content(path)
            if content.startswith("Error:"):
                return content # Fail fast if a file can't be read
            file_contents.append(f'<file path="{path}">\n{content}\n</file>')

        context = "\n\n".join(file_contents)

        system_prompt = (
            "You are a precise code analyst. Read the provided files and answer the question concisely. "
            "Output structured bullets only. No greetings, no prose, no preambles, no summaries. "
            "Lead every bullet with the exact name, type, or line number. Use nested bullets for details. "
            "Skip anything the caller did not ask for."
        )

        user_prompt = f"{context}\n\nQuestion: {question}"

        try:
            # We use a general model name here; our MoE gateway routes requests
            response = await self.client.chat.completions.create(
                model="openai/local/router",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                extra_body={"tier": "trivial"},
                temperature=0.2,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error in ShuntTool bulk_read: {e}")
            return f"Delegation failed: {str(e)}"

    async def _code_write(self, spec: str, reference_path: str, target_path: str) -> str:
        """Delegates boilerplate generation to a worker model and writes to disk."""
        ref_content = self._read_file_content(reference_path)
        if ref_content.startswith("Error:"):
            return ref_content

        system_prompt = (
            "You generate code files based on a spec and reference files. "
            "Match the existing patterns, conventions, naming, and style exactly. "
            "Output only the code — no explanations, no markdown fences unless asked. "
            "If the spec is ambiguous, make reasonable choices that match the patterns in the reference code."
        )

        user_prompt = (
            f"Reference file ({reference_path}):\n"
            f"<file path=\"{reference_path}\">\n{ref_content}\n</file>\n\n"
            f"Specification: {spec}\n\n"
            f"Generate the exact raw code for {target_path} based on this specification."
        )

        try:
            response = await self.client.chat.completions.create(
                model="openai/local/router",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                extra_body={"tier": "trivial"},
                temperature=0.2,
                max_tokens=8000
            )

            generated_code = response.choices[0].message.content
            clean_code = self._strip_markdown_fences(generated_code)

            # Write to disk
            path = self._validate_path(target_path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(clean_code)

            return f"Successfully generated code and wrote to {target_path}."
        except Exception as e:
            self.logger.error(f"Error in ShuntTool code_write: {e}")
            return f"Delegation failed: {str(e)}"
