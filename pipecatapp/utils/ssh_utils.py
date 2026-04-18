import os
import subprocess

def ensure_ssh_keys_initialized() -> None:
    """
    Ensures that an SSH key pair exists for the current user.
    If it doesn't exist, generates a new RSA key pair.
    """
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True, mode=0o700)
    key_path = os.path.join(ssh_dir, "id_rsa")

    if not os.path.exists(key_path):
        try:
            subprocess.run(
                ["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", key_path, "-N", "", "-q"],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            # We log or print it; for now, print is fine if logger isn't injected.
            print(f"Error generating SSH key: {e.stderr.decode()}")
