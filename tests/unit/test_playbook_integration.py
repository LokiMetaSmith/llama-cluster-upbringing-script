import subprocess
import pytest
import shutil

def test_playbook_integration_syntax_check():
    """
    Tests that the main playbook is syntactically correct and that all roles,
    including mqtt, can be found and parsed by Ansible.
    This uses `ansible-playbook --syntax-check`, which is a more direct
    validation of integration than linting.
    """
    # Find the ansible-playbook executable in the PATH
    ansible_playbook_path = shutil.which("ansible-playbook")
    if not ansible_playbook_path:
        # fallback to python -m ansible.cli.playbook
        ansible_playbook_path = "python3 -m ansible.cli.playbook"

    try:
        # Run ansible-playbook with --syntax-check
        # We need to provide an inventory and the target_user variable.

        # Determine the correct argument list
        if "python3" in ansible_playbook_path:
            cmd = ansible_playbook_path.split(" ") + [
                "playbook.yaml",
                "-i", "local_inventory.ini",
                "-e", "target_user=testuser",
                "--syntax-check"
            ]
        else:
            cmd = [
                ansible_playbook_path,
                "playbook.yaml",
                "-i", "local_inventory.ini",
                "-e", "target_user=testuser",
                "--syntax-check"
            ]

        result = subprocess.run(
            cmd,
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


def test_cluster_ip_and_nomad_url_resolution():
    """
    Tests that cluster_ip resolves properly with and without tailscale0 facts,
    and never produces an empty host for Nomad API URLs (https://:4646).
    """
    import yaml
    from jinja2 import Environment

    with open("group_vars/all.yaml", "r") as f:
        all_vars = yaml.safe_load(f)

    cluster_ip_expr = all_vars.get("cluster_ip")
    assert cluster_ip_expr is not None

    env = Environment()
    cluster_ip_template = env.from_string(cluster_ip_expr)

    # 1. When tailscale0 is present
    facts_with_tailscale = {"tailscale0": {"ipv4": {"address": "100.64.0.42"}}}
    res_with_ts = cluster_ip_template.render(ansible_facts=facts_with_tailscale, node_id="11")
    assert res_with_ts == "100.64.0.42"

    # 2. When tailscale0 is absent
    facts_without_tailscale = {}
    res_without_ts = cluster_ip_template.render(ansible_facts=facts_without_tailscale, node_id="11")
    assert res_without_ts == "10.0.0.11"

    # 3. Verify Nomad readiness URL formation never has an empty host
    nomad_url_template = env.from_string(
        "{{ nomad_protocol | default('https') }}://{{ cluster_ip | default('10.0.0.' + (node_id | default('10', true) | string), true) }}:{{ nomad_http_port | default(4646, true) }}/v1/agent/self"
    )

    url_with_ts = nomad_url_template.render(cluster_ip=res_with_ts, nomad_protocol="https", nomad_http_port=4646)
    assert url_with_ts == "https://100.64.0.42:4646/v1/agent/self"

    url_without_ts = nomad_url_template.render(cluster_ip=res_without_ts, nomad_protocol="https", nomad_http_port=4646)
    assert url_without_ts == "https://10.0.0.11:4646/v1/agent/self"

    # Even if cluster_ip is explicitly passed as empty string or None
    url_empty_ip = nomad_url_template.render(cluster_ip="", node_id="15", nomad_protocol="https")
    assert url_empty_ip == "https://10.0.0.15:4646/v1/agent/self"