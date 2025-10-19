import os
import yaml
from jinja2 import Environment, FileSystemLoader

def test_home_assistant_template():
    """
    Tests that the home_assistant.nomad.j2 template renders correctly.
    """
    j2_env = Environment(loader=FileSystemLoader('ansible/roles/home_assistant/templates'), trim_blocks=True)
    template = j2_env.get_template('home_assistant.nomad.j2')
    result = template.render()

    assert 'MQTT_BROKER = "mqtt.service.consul"' in result