# Workflow Node Scenario Template

This template documents the behavior, inputs, and outputs of custom nodes added to the Pipecat visual workflow engine.

## Node Overview

* **Node Name:** [The class name of the node, e.g., `LLMRouterNode`, `JSONParserNode`]
* **Category:** [Where it appears in the Flowise UI, e.g., "Agents", "Logic", "Tools"]
* **Purpose:** [What does this node do in the context of the larger graph?]

## Data Interfaces

Define the exact expected shape of the data entering and leaving this node. (Reference the `validation_format_template.md` if using complex Pydantic models).

### Inputs (Incoming Edges / Slots)

| Slot Name    | Data Type | Required | Description                                                    |
| :----------- | :-------- | :------- | :------------------------------------------------------------- |
| `state_dict` | `dict`    | Yes      | The global workflow state.                                     |
| `prompt`     | `string`  | Yes      | The text prompt to process.                                    |
| `model`      | `string`  | No       | Override the default model (defaults to `llama3-8b-instruct`). |

### Outputs (Outgoing Edges / Slots)

| Slot Name       | Data Type | Description                                                               |
| :-------------- | :-------- | :------------------------------------------------------------------------ |
| `success`       | `dict`    | The updated state dictionary containing the generated response.           |
| `error`         | `string`  | An error message string if the execution fails (for fallback routing).    |
| `next_node_id`  | `string`  | (Dynamic) ID of the next node based on conditional routing logic.         |

## Execution Logic

Describe the core internal logic executed by the node's `execute()` method.

1. **State Extraction:** Node extracts `messages` list from the incoming `state_dict`.
2. **Processing:** Node appends the incoming `prompt` to the `messages` list.
3. **External Call:** Node calls the Llama inference server endpoint with the provided `model` and `messages`.
4. **State Update:** The resulting text is parsed, appended to `messages`, and saved back to the `state_dict` under `last_response`.

## Conditional Routing

If this node has multiple outgoing edges based on logic, explain the conditions.

* **Condition 1 (Success):** If the LLM returns a valid 200 HTTP response, route execution through the `success` output slot.
* **Condition 2 (Failure):** If the HTTP request times out, populate the `error` output string and route execution through the `error` output slot.

## Example Configuration (YAML)

Provide an example of how this node would look in the YAML workflow definition.

```yaml
nodes:
  - id: my_llm_node
    type: LLMRouterNode
    config:
      model_name: "mixtral-8x7b"
      temperature: 0.7
    inputs:
      prompt: "{{ $vars.user_input }}"
    outputs:
      success: "next_node_in_chain"
      error: "error_handler_node"
```
