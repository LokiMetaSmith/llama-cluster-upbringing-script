import paramiko
import os
import logging

class SSH_Tool:
    """A tool for executing commands on a remote machine via SSH.

    This class wraps the `paramiko` library to provide a simple interface for
    the agent to connect to other machines and run commands. It supports both
    key-based and password-based authentication.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self):
        """Initializes the SSH_Tool."""
        self.description = "Execute a command on a remote machine via SSH."
        self.name = "ssh_tool"

    def run_command(self, host: str, username: str, command: str, key_filename: str = None, password: str = None) -> str:
        """Executes a command on a remote machine via SSH.

        It is highly recommended to use key-based authentication for security.
        Provide either `key_filename` or `password`, but not both.

        Args:
            host (str): The hostname or IP address of the remote machine.
            username (str): The username to connect with.
            command (str): The command to execute on the remote machine.
            key_filename (str, optional): The path to the private SSH key file.
                Defaults to None.
            password (str, optional): The password for authentication.
                Defaults to None.

        Returns:
            str: The standard output from the command, or an error message if
                 the command fails or an exception occurs.
        """
        client = paramiko.SSHClient()

        # Security Fix: Sentinel - Prevent MITM attacks
        # Load system host keys (e.g. from ~/.ssh/known_hosts)
        client.load_system_host_keys()

        # Use RejectPolicy to prevent connecting to unknown hosts automatically.
        # Users must add the host to known_hosts manually or verify it elsewhere.
        client.set_missing_host_key_policy(paramiko.RejectPolicy())

        try:
            if key_filename:
                key = paramiko.RSAKey.from_private_key_file(os.path.expanduser(key_filename))
                client.connect(host, username=username, pkey=key)
            elif password:
                client.connect(host, username=username, password=password)
            else:
                return "Error: No authentication method provided. Use key_filename or password."

            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                return f"Error executing command: {error}"
            return output

        except paramiko.SSHException as e:
            return f"SSH Error: {e}. If 'Server not found in known_hosts', please add the server's public key to your local known_hosts file."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            client.close()
