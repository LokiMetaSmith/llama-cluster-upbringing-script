import subprocess
import os
try:
    from ..secret_manager import secret_manager
except ImportError:
    from secret_manager import secret_manager

class Ansible_Tool:
    """A tool for running Ansible playbooks to configure and manage the cluster.

    This class provides a method to execute `ansible-playbook` commands from
    within the agent's environment. It assumes that the Ansible project is
    located at a predefined path (`/opt/cluster-infra`).

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
        project_root (str): The absolute path to the Ansible project directory.
    """
    def __init__(self):
        """Initializes the Ansible_Tool."""
        self.description = "Run an Ansible playbook to configure and manage the cluster."
        self.name = "ansible_tool"
        # The main playbook synchronizes the repo to /opt/cluster-infra on all nodes.
        self.project_root = "/opt/cluster-infra"

    def run_playbook(self, playbook: str = 'playbook.yaml', limit: str = None, tags: str = None, extra_vars: dict = None) -> str:
        """Runs an Ansible playbook to provision or manage nodes in the cluster.

        Args:
            playbook (str, optional): The name of the playbook file to run,
                relative to the project root. Defaults to 'playbook.yaml'.
            limit (str, optional): A host pattern to limit the playbook run to.
                For example, 'new_node_hostname'. Defaults to None.
            tags (str, optional): A comma-separated list of tags to run, to
                execute specific parts of the playbook. Defaults to None.
            extra_vars (dict, optional): A dictionary of extra variables to
                pass to the playbook. Defaults to None.

        Returns:
            str: A string containing the output of the playbook run, or an
                error message if the run fails or times out.
        """
        playbook_path = os.path.abspath(os.path.join(self.project_root, playbook))
        project_root_abs = os.path.abspath(self.project_root)

        # Ensure strict directory containment to prevent partial path attacks
        # e.g., /opt/cluster-infra vs /opt/cluster-infra-secret
        if os.path.commonpath([playbook_path, project_root_abs]) != project_root_abs:
            return "Error: Invalid playbook path. Path traversal detected."

        if not os.path.exists(playbook_path):
            return f"Error: Playbook '{playbook_path}' not found."

        # The base command. Assumes ansible-playbook is in the system's PATH.
        command = ["ansible-playbook", playbook_path]

        if limit:
            command.extend(["--limit", limit])

        if tags:
            command.extend(["--tags", tags])

        if extra_vars:
            # Ansible's --extra-vars can take a JSON string, which is safer than building a key=value string.
            import json
            command.extend(["--extra-vars", json.dumps(extra_vars)])

        try:
            # Running the command from the project root is critical so that ansible.cfg,
            # inventory.yaml, and roles are all found correctly.

            # Security: Inject secrets back into the subprocess environment
            # This ensures Ansible has access to necessary API keys/tokens
            # that were scrubbed from the main process environment.
            env = os.environ.copy()
            env.update(secret_manager.get_all_secrets())

            process = subprocess.run(
                command,
                cwd=self.project_root,
                env=env,
                capture_output=True,
                text=True,
                timeout=900  # 15 minute timeout for long playbook runs
            )

            if process.returncode == 0:
                return f"Playbook run completed successfully.\nOutput:\n{process.stdout}"
            else:
                error_msg = f"Playbook run failed with return code {process.returncode}.\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"

                # Reinforcement: Add hints based on common errors
                hints = []
                combined_output = (process.stdout or "") + (process.stderr or "")

                if "UNREACHABLE" in combined_output:
                    hints.append("HINT: The target host is unreachable. Check your network connection, VPN, or SSH keys.")
                if "syntax error" in combined_output.lower() or "yaml" in combined_output.lower():
                    hints.append("HINT: There seems to be a syntax error in the playbook. Check for invalid YAML or Jinja2 syntax.")
                if "undefined variable" in combined_output.lower():
                    hints.append("HINT: A variable is undefined. Check group_vars, extra_vars, or default values.")
                if "permission denied" in combined_output.lower():
                    hints.append("HINT: Permission denied. Ensure you are using 'become: yes' if root privileges are needed.")
                if "apt" in combined_output.lower() and "lock" in combined_output.lower():
                    hints.append("HINT: Could not get lock /var/lib/dpkg/lock. Another process is using apt/dpkg. Wait a moment or kill the process.")

                if hints:
                    error_msg += "\n\n" + "\n".join(hints)

                return error_msg

        except subprocess.TimeoutExpired as e:
            return f"Error: Ansible playbook run timed out after 15 minutes.\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        except Exception as e:
            return f"An unexpected error occurred while trying to run Ansible: {e}"
