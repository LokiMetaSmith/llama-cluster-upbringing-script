import os
import pytest
from jinja2 import Environment, FileSystemLoader

def test_mqtt_template():
    """
    Tests that the mqtt.nomad.j2 template renders correctly and follows best practices.
    """
    # Adjust path to the template
    # This file is in testing/unit_tests/
    # Template is in ansible/roles/mqtt/templates/
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.abspath(os.path.join(base_dir, '../../ansible/roles/mqtt/templates'))

    assert os.path.exists(template_dir), f"Template directory not found: {template_dir}"

    j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
    template = j2_env.get_template('mqtt.nomad.j2')

    # Render the template
    result = template.render({})

    # Check for absence of 'ports =' inside config block (docker driver)
    assert 'ports = ["mqtt", "ws"]' not in result, "ports definition should be removed from docker config when using host network"

    # Check for presence of check_restart
    assert 'check_restart' in result, "check_restart stanza is missing"

    # Check for restart policy
    assert 'restart {' in result, "restart stanza is missing"
