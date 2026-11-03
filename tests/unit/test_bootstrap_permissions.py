import os
import subprocess
import tempfile
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def test_initial_setup_script_has_ownership_restoration():
    setup_sh_path = os.path.join(REPO_ROOT, "initial-setup", "setup.sh")
    assert os.path.exists(setup_sh_path), "initial-setup/setup.sh must exist"
    with open(setup_sh_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "chown -R \"$TARGET_REPO_USER\":\"$TARGET_REPO_USER\"" in content
    assert "TARGET_REPO_USER=\"${SUDO_USER:-${USERNAME:-}}\"" in content

def test_bootstrap_script_has_permission_remediation():
    bootstrap_sh_path = os.path.join(REPO_ROOT, "bootstrap.sh")
    assert os.path.exists(bootstrap_sh_path), "bootstrap.sh must exist"
    with open(bootstrap_sh_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Retrying OpenCode AI Agent Installation" in content
    assert "node_modules" in content
    assert "chown -R" in content

def test_shell_syntax_validation():
    for rel_path in ["bootstrap.sh", "initial-setup/setup.sh"]:
        full_path = os.path.join(REPO_ROOT, rel_path)
        res = subprocess.run(["bash", "-n", full_path], capture_output=True, text=True)
        assert res.returncode == 0, f"Syntax error in {rel_path}: {res.stderr}"
