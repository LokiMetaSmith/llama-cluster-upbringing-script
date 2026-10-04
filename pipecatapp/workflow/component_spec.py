import dataclasses
import yaml
from typing import Any, Dict, List, Mapping, Optional, Union

import pydantic
import pydantic.alias_generators

PrimitiveTypes = str

TypeSpecType = Union[str, Dict, List]

_default_pydantic_config = pydantic.ConfigDict(
    alias_generator=pydantic.alias_generators.to_camel,
    validate_assignment=True,
)


class _BaseModel:
    __pydantic_config__ = _default_pydantic_config

    def to_json_dict(self):
        return pydantic.TypeAdapter(type(self)).dump_python(
            self,
            mode="json",
            by_alias=True,
            exclude_defaults=True,
        )

    @classmethod
    def from_json_dict(cls, d: dict):
        return pydantic.TypeAdapter(cls).validate_python(d)


@dataclasses.dataclass
class InputSpec(_BaseModel):
    name: str
    type: Optional[TypeSpecType] = None
    description: Optional[str] = None
    default: Optional[PrimitiveTypes] = None
    optional: Optional[bool] = False
    annotations: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class OutputSpec(_BaseModel):
    name: str
    type: Optional[TypeSpecType] = None
    description: Optional[str] = None
    annotations: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class InputValuePlaceholder(_BaseModel):
    _serialized_names = {"input_name": "inputValue"}
    __pydantic_config__ = _default_pydantic_config | pydantic.ConfigDict(
        alias_generator=lambda s: (
            InputValuePlaceholder._serialized_names.get(s)
            or pydantic.alias_generators.to_camel(s)
        ),
    )
    input_name: str


@dataclasses.dataclass
class InputPathPlaceholder(_BaseModel):
    _serialized_names = {"input_name": "inputPath"}
    __pydantic_config__ = _default_pydantic_config | pydantic.ConfigDict(
        alias_generator=lambda s: (
            InputPathPlaceholder._serialized_names.get(s)
            or pydantic.alias_generators.to_camel(s)
        ),
    )
    input_name: str


@dataclasses.dataclass
class OutputPathPlaceholder(_BaseModel):
    _serialized_names = {"output_name": "outputPath"}
    __pydantic_config__ = _default_pydantic_config | pydantic.ConfigDict(
        alias_generator=lambda s: (
            OutputPathPlaceholder._serialized_names.get(s)
            or pydantic.alias_generators.to_camel(s)
        ),
    )
    output_name: str


CommandlineArgumentType = Union[
    str,
    InputValuePlaceholder,
    InputPathPlaceholder,
    OutputPathPlaceholder,
    "ConcatPlaceholder",
    "IfPlaceholder",
]


@dataclasses.dataclass
class ConcatPlaceholder(_BaseModel):
    concat: List[CommandlineArgumentType]


@dataclasses.dataclass
class IsPresentPlaceholder(_BaseModel):
    is_present: str


IfConditionArgumentType = Union[bool, str, IsPresentPlaceholder, InputValuePlaceholder]


@dataclasses.dataclass
class IfPlaceholderStructure(_BaseModel):
    _serialized_names = {
        "condition": "cond",
        "then_value": "then",
        "else_value": "else",
    }
    __pydantic_config__ = _default_pydantic_config | pydantic.ConfigDict(
        alias_generator=lambda s: (
            IfPlaceholderStructure._serialized_names.get(s)
            or pydantic.alias_generators.to_camel(s)
        ),
    )
    condition: IfConditionArgumentType
    then_value: List[CommandlineArgumentType]
    else_value: Optional[List[CommandlineArgumentType]] = None


@dataclasses.dataclass
class IfPlaceholder(_BaseModel):
    _serialized_names = {"if_structure": "if"}
    __pydantic_config__ = _default_pydantic_config | pydantic.ConfigDict(
        alias_generator=lambda s: (
            IfPlaceholder._serialized_names.get(s)
            or pydantic.alias_generators.to_camel(s)
        ),
    )
    if_structure: IfPlaceholderStructure


@dataclasses.dataclass
class ContainerSpec(_BaseModel):
    image: str
    command: Optional[List[CommandlineArgumentType]] = None
    args: Optional[List[CommandlineArgumentType]] = None
    env: Optional[Mapping[str, str]] = None


@dataclasses.dataclass
class ContainerImplementation(_BaseModel):
    container: ContainerSpec


ImplementationType = Union[ContainerImplementation, "GraphImplementation"]


@dataclasses.dataclass
class MetadataSpec(_BaseModel):
    annotations: Optional[Dict[str, str]] = None
    labels: Optional[Dict[str, str]] = None


@dataclasses.dataclass
class ComponentSpec(_BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[MetadataSpec] = None
    inputs: Optional[List[InputSpec]] = None
    outputs: Optional[List[OutputSpec]] = None
    implementation: Optional[ImplementationType] = None


@dataclasses.dataclass
class GraphInputReference(_BaseModel):
    input_name: str
    type: Optional[TypeSpecType] = None


@dataclasses.dataclass
class GraphInputArgument(_BaseModel):
    graph_input: GraphInputReference


@dataclasses.dataclass
class TaskOutputReference(_BaseModel):
    output_name: str
    task_id: str


@dataclasses.dataclass
class TaskOutputArgument(_BaseModel):
    task_output: TaskOutputReference


DynamicDataReference = Union[str, Dict[str, Any]]


@dataclasses.dataclass
class DynamicDataArgument(_BaseModel):
    dynamic_data: DynamicDataReference


ArgumentType = Union[
    PrimitiveTypes, GraphInputArgument, TaskOutputArgument, DynamicDataArgument
]


@dataclasses.dataclass
class RetryStrategySpec(_BaseModel):
    max_retries: int


@dataclasses.dataclass
class CachingStrategySpec(_BaseModel):
    max_cache_staleness: Optional[str] = None


@dataclasses.dataclass
class ExecutionOptionsSpec(_BaseModel):
    retry_strategy: Optional[RetryStrategySpec] = None
    caching_strategy: Optional[CachingStrategySpec] = None


@dataclasses.dataclass
class ComponentReference(_BaseModel):
    name: Optional[str] = None
    digest: Optional[str] = None
    tag: Optional[str] = None
    url: Optional[str] = None
    spec: Optional[ComponentSpec] = None
    text: Optional[str] = None


@dataclasses.dataclass
class TaskSpec(_BaseModel):
    component_ref: ComponentReference
    arguments: Optional[Mapping[str, ArgumentType]] = None
    is_enabled: Optional[ArgumentType] = None
    execution_options: Optional[ExecutionOptionsSpec] = None
    annotations: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class GraphSpec(_BaseModel):
    tasks: Mapping[str, TaskSpec]
    output_values: Optional[Mapping[str, ArgumentType]] = None


@dataclasses.dataclass
class GraphImplementation(_BaseModel):
    graph: GraphSpec


def convert_json_schema_to_component_spec(
    schema: dict,
    image: str = "pipecat-default-worker",
    command: Optional[List[CommandlineArgumentType]] = None,
    args: Optional[List[CommandlineArgumentType]] = None,
) -> ComponentSpec:
    """Converts a standard OpenAI-style JSON schema (from a Tool) to a KFP-style ComponentSpec."""
    function_def = schema.get(
        "function", schema
    )  # Handle if wrapped in "type": "function"
    name = function_def.get("name", "UnknownComponent")
    description = function_def.get("description", "")

    inputs: List[InputSpec] = []

    parameters = function_def.get("parameters", {})
    properties = parameters.get("properties", {})
    required = parameters.get("required", [])

    for prop_name, prop_details in properties.items():
        is_optional = prop_name not in required
        prop_type_str = prop_details.get("type", "String")
        # Map basic types
        if prop_type_str == "string":
            mapped_type = "String"
        elif prop_type_str == "integer":
            mapped_type = "Integer"
        elif prop_type_str == "boolean":
            mapped_type = "Boolean"
        elif prop_type_str == "number":
            mapped_type = "Float"
        else:
            mapped_type = "JsonObject"

        inputs.append(
            InputSpec(
                name=prop_name,
                type=mapped_type,
                description=prop_details.get("description"),
                optional=is_optional,
            )
        )

    # We create a generic output for the tool result
    outputs = [
        OutputSpec(
            name="result", type="JsonObject", description="Result of the tool execution"
        )
    ]

    # Auto-generate args if not provided
    if args is None:
        args = []
        for prop_name in properties.keys():
            args.extend(
                [f"--{prop_name}=", InputValuePlaceholder(input_name=prop_name)]
            )
        args.append(OutputPathPlaceholder(output_name="result"))

    implementation = ContainerImplementation(
        container=ContainerSpec(
            image=image,
            command=command or ["python", "-m", f"pipecatapp.tools.{name}"],
            args=args,
        )
    )

    return ComponentSpec(
        name=name,
        description=description,
        inputs=inputs,
        outputs=outputs,
        implementation=implementation,
    )


def load_component_from_dict(d: dict) -> ComponentSpec:
    """Loads a ComponentSpec from a dictionary."""
    return ComponentSpec.from_json_dict(d)

def load_component_from_text(text: str) -> ComponentSpec:
    """Loads a ComponentSpec from a YAML or JSON string."""
    d = yaml.safe_load(text)
    return load_component_from_dict(d)

def load_component_from_file(filepath: str) -> ComponentSpec:
    """Loads a ComponentSpec from a YAML or JSON file."""
    with open(filepath, 'r') as f:
        d = yaml.safe_load(f)
    return load_component_from_dict(d)

def dump_component_to_dict(component: ComponentSpec) -> dict:
    """Dumps a ComponentSpec to a dictionary."""
    return component.to_json_dict()

def dump_component_to_text(component: ComponentSpec) -> str:
    """Dumps a ComponentSpec to a YAML string."""
    d = dump_component_to_dict(component)
    return yaml.safe_dump(d, sort_keys=False)

def dump_component_to_file(component: ComponentSpec, filepath: str):
    """Dumps a ComponentSpec to a YAML file."""
    with open(filepath, 'w') as f:
        yaml.safe_dump(dump_component_to_dict(component), f, sort_keys=False)
