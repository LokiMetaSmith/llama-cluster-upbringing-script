import os
import yaml
import pytest
from jinja2 import Environment, FileSystemLoader

def test_home_assistant_template():
    """
    Tests that the home_assistant.nomad.j2 template renders correctly.
    """
    # Adjust path to templates depending on where pytest is run from.
    # Assuming run from repo root.
    template_dir = 'ansible/roles/home_assistant/templates'
    if not os.path.isdir(template_dir):
        # Fallback if running from tests directory
        template_dir = '../../ansible/roles/home_assistant/templates'

    j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
    template = j2_env.get_template('home_assistant.nomad.j2')

    # Mock context variables
    context = {
        'home_assistant_debug_mode': False,
        'use_host_network': False,
        'home_assistant_token': 'test_token',
        'hostvars': {
            'controller_node_1': {
                'ansible_host': '192.168.1.100'
            }
        },
        'advertise_ip': '192.168.1.100',
        'mqtt_port': 1883,
        'home_assistant_port': 8123
    }

    result = template.render(context)

    # Verify key configuration injections
    assert 'MQTT_SERVER = "mqtt://192.168.1.100:1883"' in result
    assert 'HA_TOKEN = "test_token"' in result
    assert 'job "home-assistant"' in result
