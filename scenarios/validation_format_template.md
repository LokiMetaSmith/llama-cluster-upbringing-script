# Validation Format Scenario Template

This template documents the expected data schemas and validation rules for different entities within the application, ensuring data integrity at boundaries (e.g., API requests, database inserts, workflow node configurations).

## Entity Overview

* **Entity Name:** [Name of the data structure, e.g., "AgentConfiguration", "UserProfile", "WorkflowEdge"]
* **Purpose:** [Briefly describe what this data represents and where it is used in the system.]
* **Validation Level:** [e.g., API Gateway Validation, Application Logic Validation (Pydantic), Database Constraints]

## Schema Definition

Provide the formal schema definition using the appropriate technology for the component (e.g., JSON Schema for REST APIs, Pydantic for Python backend, Zod/Yup for frontend).

### Example: JSON Schema (for API Contracts)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgentConfiguration",
  "type": "object",
  "properties": {
    "agent_id": {
      "type": "string",
      "description": "Unique identifier for the agent (UUID format)",
      "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    },
    "model_name": {
      "type": "string",
      "description": "The specific LLM model to use"
    },
    "temperature": {
      "type": "number",
      "description": "Sampling temperature",
      "minimum": 0.0,
      "maximum": 2.0,
      "default": 0.7
    },
    "tools_enabled": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "uniqueItems": true
    }
  },
  "required": ["agent_id", "model_name"]
}
```

### Example: Pydantic Model (for Python Backend)

```python
from pydantic import BaseModel, Field, conlist, validator
from typing import List, Optional
import uuid

class AgentConfiguration(BaseModel):
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique UUID")
    model_name: str = Field(..., min_length=1, description="The specific LLM model")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Sampling temperature")
    tools_enabled: Optional[List[str]] = Field(default_factory=list, description="List of enabled tools")

    @validator('model_name')
    def check_model_supported(cls, v):
        supported_models = ['llama3-8b', 'mixtral-8x7b']
        if v not in supported_models:
            raise ValueError(f"Model '{v}' is not supported.")
        return v
```

## Specific Validation Rules

Detail the specific business logic constraints that might not be easily expressed in standard schema definitions.

| Field Name      | Rule                                                                               | Error Message (if violated)                                         |
| :-------------- | :--------------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| `agent_id`      | Must be a valid UUIDv4 string.                                                     | "Invalid agent_id format. Must be a UUIDv4."                        |
| `model_name`    | Must be one of the currently deployed models in the cluster (dynamic check).       | "The specified model_name is not currently available."              |
| `temperature`   | Must be between 0.0 and 2.0 inclusive.                                             | "Temperature must be between 0.0 and 2.0."                          |
| `tools_enabled` | Cannot contain duplicate entries. Tools must exist in the `ToolRegistry`.          | "Duplicate tools found" or "Tool 'X' not found in registry."        |
| *Cross-field*   | If `model_name` is an embedding model, `temperature` must not be provided (or 0). | "Temperature is not applicable for embedding models."               |

## Example Payloads

### Valid Payload

```json
{
  "agent_id": "123e4567-e89b-12d3-a456-426614174000",
  "model_name": "llama3-8b",
  "temperature": 0.5,
  "tools_enabled": ["web_search", "calculator"]
}
```

### Invalid Payload (Example 1)

```json
{
  "agent_id": "not-a-uuid",
  "model_name": "unknown-model",
  "temperature": 5.0
}
```

*Expected Error Output (based on standard error handling template):*

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Payload validation failed",
    "details": [
      {"field": "agent_id", "issue": "Invalid agent_id format. Must be a UUIDv4."},
      {"field": "model_name", "issue": "Model 'unknown-model' is not supported."},
      {"field": "temperature", "issue": "Temperature must be between 0.0 and 2.0."}
    ]
  }
}
```
