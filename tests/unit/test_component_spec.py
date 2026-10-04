import pytest
import tempfile
import os
from pipecatapp.workflow.component_spec import load_component_from_text, ComponentSpec

def test_load_component_from_text():
    yaml_text = """
name: test-component
description: A test component
inputs:
  - {name: input1, type: String}
outputs:
  - {name: output1, type: String}
implementation:
  container:
    image: test-image
    command: [python, -c, "print('hello')"]
"""
    spec = load_component_from_text(yaml_text)
    assert isinstance(spec, ComponentSpec)
    assert spec.name == "test-component"
    assert len(spec.inputs) == 1
    assert spec.inputs[0].name == "input1"
    assert spec.implementation.container.image == "test-image"


def test_component_dump_and_load():
    yaml_text = """
name: test-component
description: A test component
inputs:
  - name: input1
    type: String
outputs:
  - name: output1
    type: String
implementation:
  container:
    image: test-image
    command:
      - python
      - -c
      - "print('hello')"
"""
    spec = load_component_from_text(yaml_text)

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, 'component.yaml')
        from pipecatapp.workflow.component_spec import dump_component_to_file, load_component_from_file, dump_component_to_text, load_component_from_dict, dump_component_to_dict

        # Test text dump/load
        dumped_text = dump_component_to_text(spec)
        assert "name: test-component" in dumped_text
        spec_from_text = load_component_from_text(dumped_text)
        assert spec_from_text.name == spec.name

        # Test dict dump/load
        d = dump_component_to_dict(spec)
        assert isinstance(d, dict)
        assert d['name'] == "test-component"
        spec_from_dict = load_component_from_dict(d)
        assert spec_from_dict.name == spec.name

        # Test file dump/load
        dump_component_to_file(spec, filepath)
        spec_from_file = load_component_from_file(filepath)
        assert spec_from_file.name == "test-component"
        assert spec_from_file.implementation.container.image == "test-image"
