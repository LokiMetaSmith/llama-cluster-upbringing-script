from .registry import registry
from ..node import Node
from ..context import WorkflowContext
import os
import json
import inspect
import httpx
from pathlib import Path
from typing import Any, Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

# --- The Emperor's Tools (adapted for Node context) ---

def resolve_abs_path(path_str: str, root_dir: str = None) -> Path:
    """
    file.py -> /path/to/root/file.py
    Ensures path stays within root_dir for safety.
    """
    if root_dir is None:
        root_dir = os.getenv("EMPEROR_ROOT_DIR", os.getcwd())

    root = Path(root_dir).resolve()
    path = Path(path_str).expanduser()

    if not path.is_absolute():
        path = (root / path).resolve()
    else:
        path = path.resolve()

    # Security check
    try:
        path.relative_to(root)
    except ValueError:
        # If outside root, default to root or raise error.
        # For this PoC, we'll force it to be under root if it's not.
        # But to be safe and simple, let's just error or re-root.
        # Let's re-root relative paths correctly above.
        # If an absolute path is provided that is outside, we block it.
        raise ValueError(f"Path {path} is outside allowed root {root}")

    return path

def read_file_tool(filename: str) -> Dict[str, Any]:
    """
    Gets the full content of a file provided by the user.
    :param filename: The name of the file to read.
    :return: The full content of the file.
    """
    try:
        full_path = resolve_abs_path(filename)
        with open(str(full_path), "r") as f:
            content = f.read()
        return {
            "file_path": str(full_path),
            "content": content
        }
    except Exception as e:
        return {"error": str(e)}

def list_files_tool(path: str) -> Dict[str, Any]:
    """
    Lists the files in a directory provided by the user.
    :param path: The path to a directory to list files from.
    :return: A list of files in the directory.
    """
    try:
        full_path = resolve_abs_path(path)
        all_files = []
        if full_path.is_dir():
            for item in full_path.iterdir():
                all_files.append({
                    "filename": item.name,
                    "type": "file" if item.is_file() else "dir"
                })
        return {
            "path": str(full_path),
            "files": all_files
        }
    except Exception as e:
        return {"error": str(e)}

def edit_file_tool(path: str, old_str: str, new_str: str) -> Dict[str, Any]:
    """
    Replaces first occurrence of old_str with new_str in file. If old_str is empty,
    create/overwrite file with new_str.
    :param path: The path to the file to edit.
    :param old_str: The string to replace.
    :param new_str: The string to replace with.
    :return: A dictionary with the path to the file and the action taken.
    """
    try:
        full_path = resolve_abs_path(path)

        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)

        if old_str == "":
            full_path.write_text(new_str, encoding="utf-8")
            return {
                "path": str(full_path),
                "action": "created_file"
            }

        if not full_path.exists():
             return {"error": "File not found"}

        original = full_path.read_text(encoding="utf-8")
        if original.find(old_str) == -1:
            return {
                "path": str(full_path),
                "action": "old_str not found"
            }
        edited = original.replace(old_str, new_str, 1)
        full_path.write_text(edited, encoding="utf-8")
        return {
            "path": str(full_path),
            "action": "edited"
        }
    except Exception as e:
        return {"error": str(e)}

TOOL_REGISTRY = {
    "read_file": read_file_tool,
    "list_files": list_files_tool,
    "edit_file": edit_file_tool
}

SYSTEM_PROMPT_TEMPLATE = """
You are a coding assistant whose goal it is to help us solve coding tasks.
You have access to a series of tools you can execute. Here are the tools you can execute:

{tool_list_repr}

When you want to use a tool, reply with exactly one line in the format: 'tool: TOOL_NAME({{JSON_ARGS}})' and nothing else.
Use compact single-line JSON with double quotes. After receiving a tool_result(...) message, continue the task.
If no tool is needed, respond normally.
"""

def get_tool_str_representation(tool_name: str) -> str:
    tool = TOOL_REGISTRY[tool_name]
    sig = inspect.signature(tool)
    return f"""
    Name: {tool_name}
    Description: {tool.__doc__}
    Signature: {sig}
    """

def get_full_system_prompt():
    tool_str_repr = ""
    for tool_name in TOOL_REGISTRY:
        tool_str_repr += "TOOL\n===" + get_tool_str_representation(tool_name)
        tool_str_repr += f"\n{'='*15}\n"
    return SYSTEM_PROMPT_TEMPLATE.format(tool_list_repr=tool_str_repr)

def extract_tool_invocations(text: str) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Return list of (tool_name, args) requested in 'tool: name({...})' lines.
    """
    invocations = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("tool:"):
            continue
        try:
            after = line[len("tool:"):].strip()
            if "(" not in after: continue
            name, rest = after.split("(", 1)
            name = name.strip()
            if not rest.endswith(")"):
                continue
            json_str = rest[:-1].strip()
            args = json.loads(json_str)
            invocations.append((name, args))
        except Exception:
            continue
    return invocations

@registry.register
class EmperorAgentNode(Node):
    """
    A self-contained agent node that implements the 'Emperor Has No Clothes'
    loop: simple tools, direct file manipulation, and an inner REPL.
    """
    async def execute(self, context: WorkflowContext):
        task = self.get_input(context, "task") or self.get_input(context, "user_text")
        if not task:
            self.set_output(context, "response", "No task provided.")
            return

        # Discovery logic reused from llm_nodes.py
        consul_http_addr = context.global_inputs.get("consul_http_addr") or os.getenv("CONSUL_HTTP_ADDR")
        base_url = "http://127.0.0.1:8081/v1" # Default fallback

        if consul_http_addr:
            try:
                # Try to find the router
                token = os.getenv("CONSUL_HTTP_TOKEN")
                headers = {"X-Consul-Token": token.strip()} if token else {}
                async with httpx.AsyncClient(headers=headers) as client:
                    response = await client.get(f"{consul_http_addr}/v1/health/service/router-api?passing")
                    if response.status_code == 200:
                        services = response.json()
                        if services:
                            svc = services[0]['Service']
                            base_url = f"http://{svc['Address']}:{svc['Port']}/v1"
            except Exception:
                pass # Fallback to default

        # The Agent Loop
        system_content = get_full_system_prompt()
        conversation = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": task}
        ]

        final_response = ""
        max_turns = 20 # Safety break
        turn = 0

        logger.info(f"Starting Emperor Agent Loop for task: {task}")

        async with httpx.AsyncClient(timeout=120.0) as client:
            while turn < max_turns:
                turn += 1

                # Call LLM
                try:
                    resp = await client.post(
                        f"{base_url}/chat/completions",
                        json={
                            "model": "gpt-4o", # Router ignores this often, but good to set
                            "messages": conversation,
                            "temperature": 0.0
                        }
                    )
                    resp.raise_for_status()
                    assistant_response = resp.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    final_response = f"LLM Error: {e}"
                    break

                # Parse Tools
                tool_invocations = extract_tool_invocations(assistant_response)

                if not tool_invocations:
                    # No tools called -> Final Answer
                    final_response = assistant_response
                    conversation.append({"role": "assistant", "content": assistant_response})
                    break

                # If tools called, add assistant msg and execute tools
                conversation.append({"role": "assistant", "content": assistant_response})

                for name, args in tool_invocations:
                    logger.info(f"Emperor invoking: {name} with {args}")
                    tool_func = TOOL_REGISTRY.get(name)
                    if not tool_func:
                        result = f"Error: Tool {name} not found."
                    else:
                        # Map args based on tool signature or just unpack?
                        # The article does: tool(args.get("filename", ".")) etc.
                        # We will just unpack safely using defaults as in the article
                        if name == "read_file":
                            result = tool_func(args.get("filename", "."))
                        elif name == "list_files":
                            result = tool_func(args.get("path", "."))
                        elif name == "edit_file":
                            result = tool_func(
                                args.get("path", "."),
                                args.get("old_str", ""),
                                args.get("new_str", "")
                            )
                        else:
                            result = "Unknown tool"

                    conversation.append({
                        "role": "user",
                        "content": f"tool_result({json.dumps(result)})"
                    })

        self.set_output(context, "response", final_response)
