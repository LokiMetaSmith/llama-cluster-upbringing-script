import paramiko
import os

class SSH_Tool:
    def __init__(self):
        self.description = "Execute a command on a remote machine via SSH."
        self.name = "ssh_tool"

    def run_command(self, host, username, command, key_filename=None, password=None):
        """
        Executes a command on a remote machine via SSH.
        It is highly recommended to use key-based authentication.
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

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

        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            client.close()
