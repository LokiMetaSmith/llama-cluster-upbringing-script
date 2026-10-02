from pipecatapp.workflow.component_spec import (
    ComponentSpec,
    InputSpec,
    OutputSpec,
    ContainerImplementation,
    ContainerSpec,
    InputValuePlaceholder,
    OutputPathPlaceholder,
)

def test_component_spec_parsing():
    json_dict = {
        "name": "Test Component",
        "description": "A test component",
        "inputs": [
            {"name": "input1", "type": "String", "description": "Input 1 description"}
        ],
        "outputs": [
            {"name": "output1", "type": "String", "description": "Output 1 description"}
        ],
        "implementation": {
            "container": {
                "image": "alpine",
                "command": [
                    "echo",
                    {"inputValue": "input1"},
                ],
                "args": [
                    {"outputPath": "output1"}
                ]
            }
        }
    }

    spec = ComponentSpec.from_json_dict(json_dict)

    assert spec.name == "Test Component"
    assert spec.description == "A test component"
    assert len(spec.inputs) == 1
    assert spec.inputs[0].name == "input1"
    assert len(spec.outputs) == 1
    assert spec.outputs[0].name == "output1"

    assert isinstance(spec.implementation, ContainerImplementation)
    assert spec.implementation.container.image == "alpine"
    assert spec.implementation.container.command[0] == "echo"
    assert isinstance(spec.implementation.container.command[1], InputValuePlaceholder)
    assert spec.implementation.container.command[1].input_name == "input1"

    assert isinstance(spec.implementation.container.args[0], OutputPathPlaceholder)
    assert spec.implementation.container.args[0].output_name == "output1"
