import subprocess
import pytest
import os

def test_playbook_integration_syntax_check():
    """
    Tests that the main playbook is syntactically correct and that all roles,
    including mqtt and home_assistant, can be found and parsed by Ansible.
    This uses `ansible-playbook --syntax-check`, which is a more direct
    validation of integration than linting.
    """
    # Construct the path to the ansible-playbook executable within the virtualenv
    ansible_playbook_path = ".venv/bin/ansible-playbook"

    if not os.path.exists(ansible_playbook_path):
        pytest.fail(f"ansible-playbook executable not found at {ansible_playbook_path}")

    try:
        # Run ansible-playbook with --syntax-check
        # We need to provide an inventory and the target_user variable.
        result = subprocess.run(
            [
                ansible_playbook_path,
                "playbook.yaml",
                "-i", "inventory.yaml",
                "-e", "target_user=testuser",
                "--syntax-check"
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        # If the command completes with a 0 exit code, the syntax is valid.
        assert result.returncode == 0
    except FileNotFoundError:
        pytest.fail(f"ansible-playbook executable not found at {ansible_playbook_path}")
    except subprocess.CalledProcessError as e:
        # If ansible-playbook finds a syntax error, fail the test and print the output
        pytest.fail(
            f"ansible-playbook --syntax-check failed with errors (exit code {e.returncode}):\n"
            f"STDOUT:\n{e.stdout}\n"
            f"STDERR:\n{e.stderr}"
        )