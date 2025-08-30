import subprocess
import os

class Ansible_Tool:
    def __init__(self):
        self.description = "Run an Ansible playbook to configure and manage the cluster."
        self.name = "ansible_tool"
        # The main playbook synchronizes the repo to /opt/cluster-infra on all nodes.
        self.project_root = "/opt/cluster-infra"

    def run_playbook(self, playbook='playbook.yaml', limit=None, tags=None, extra_vars=None):
        """
        Runs an Ansible playbook to provision or manage nodes in the cluster.

        :param playbook: The name of the playbook file to run, relative to the project root. Defaults to 'playbook.yaml'.
        :param limit: A host pattern to limit the playbook run to. For example, 'new_node_hostname'.
        :param tags: A comma-separated list of tags to run, to execute specific parts of the playbook.
        :param extra_vars: A dictionary of extra variables to pass to the playbook.
        :return: A string containing the output of the playbook run, or an error message.
        """
        playbook_path = os.path.join(self.project_root, playbook)
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
            process = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=900  # 15 minute timeout for long playbook runs
            )

            if process.returncode == 0:
                return f"Playbook run completed successfully.\nOutput:\n{process.stdout}"
            else:
                return f"Playbook run failed with return code {process.returncode}.\nSTDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}"

        except subprocess.TimeoutExpired as e:
            return f"Error: Ansible playbook run timed out after 15 minutes.\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        except Exception as e:
            return f"An unexpected error occurred while trying to run Ansible: {e}"
