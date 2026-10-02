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

def test_convert_json_schema_to_component_spec():
    from pipecatapp.workflow.component_spec import convert_json_schema_to_component_spec

    schema = {
        "type": "function",
        "function": {
            "name": "my_test_tool",
            "description": "Does a test thing",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {"type": "string"},
                    "arg2": {"type": "integer"}
                },
                "required": ["arg1"]
            }
        }
    }

    spec = convert_json_schema_to_component_spec(schema)
    assert spec.name == "my_test_tool"
    assert spec.description == "Does a test thing"
    assert len(spec.inputs) == 2
    assert spec.inputs[0].name == "arg1"
    assert spec.inputs[0].type == "String"
    assert spec.inputs[0].optional is False

    assert spec.inputs[1].name == "arg2"
    assert spec.inputs[1].type == "Integer"
    assert spec.inputs[1].optional is True

    assert len(spec.outputs) == 1
    assert spec.outputs[0].name == "result"

    assert spec.implementation.container.image == "pipecat-default-worker"
    args = spec.implementation.container.args
    assert "--arg1=" in args
    assert "--arg2=" in args

def test_node_get_component_spec():
    from pipecatapp.workflow.node import Node

    class TestNode(Node):
        def __init__(self):
            super().__init__({"id": "test_node_id"})
            self.expected_inputs = ["input_data"]
            self.expected_outputs = ["output_data"]

        async def execute(self, context):
            pass

    node = TestNode()
    spec = node.get_component_spec()
    assert spec.name == "test_node_id"
    assert len(spec.inputs) == 1
    assert spec.inputs[0].name == "input_data"
    assert len(spec.outputs) == 1
    assert spec.outputs[0].name == "output_data"
