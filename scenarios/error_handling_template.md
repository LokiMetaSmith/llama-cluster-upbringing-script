# Error Handling Scenario Template

This template defines the standard strategies, HTTP status codes, and response structures for handling errors across the application APIs and backend services. Consistency in error reporting is critical for both internal debugging and external API consumers.

## General Strategy

1. **Fail Fast:** Validate inputs at the boundary (e.g., API Gateway, Controller level) before passing them to core business logic.
2. **Standardized Format:** All REST API errors must return a JSON response adhering to the `Standard Error Response JSON Structure` defined below.
3. **Meaningful Codes:** Use standard HTTP status codes to indicate the general *category* of the error. Use application-specific error codes (strings) to indicate the *specific* error.
4. **Actionable Messages:** Error messages should clearly explain *what* went wrong and, if possible, *how* the user can fix it. Do not expose internal stack traces to end-users in production.
5. **Logging:** All errors (especially 5xx server errors) must be logged centrally (e.g., via standard Python logging configured for structured JSON output) including relevant context like trace IDs.

## Standard HTTP Status Codes

| Code | Name                  | When to use                                                                                   |
| :--- | :-------------------- | :-------------------------------------------------------------------------------------------- |
| 400  | Bad Request           | Client sent invalid input (e.g., malformed JSON, missing required fields, validation errors). |
| 401  | Unauthorized          | Client is not authenticated (missing or invalid token).                                       |
| 403  | Forbidden             | Client is authenticated but lacks permission to access the resource or perform the action.    |
| 404  | Not Found             | The requested resource (URL path or specific ID) does not exist.                              |
| 409  | Conflict              | The request conflicts with the current state of the server (e.g., duplicate unique key).      |
| 422  | Unprocessable Entity  | Used specifically by Pydantic/FastAPI for validation errors (often interchangeable with 400). |
| 429  | Too Many Requests     | Client has exceeded rate limits.                                                              |
| 500  | Internal Server Error | Unhandled exception on the server side (e.g., database connection failed, code bug).          |
| 502  | Bad Gateway           | The server, while acting as a gateway or proxy, received an invalid response from upstream.   |
| 503  | Service Unavailable   | The server is temporarily unable to handle the request (e.g., maintenance, Nomad node down).  |

## Standard Error Response JSON Structure

All API error responses must adhere to this structure:

```json
{
  "error": {
    "code": "STRING_ERROR_CODE",
    "message": "A human-readable explanation of the error.",
    "details": [
      {
        "field": "optional_field_name",
        "issue": "Specific issue with this field"
      }
    ],
    "request_id": "req_12345abcde"
  }
}
```

### Fields

* **`code` (Required):** A standard string enum representing the error type (e.g., `VALIDATION_ERROR`, `RESOURCE_NOT_FOUND`, `INTERNAL_ERROR`).
* **`message` (Required):** A descriptive message.
* **`details` (Optional):** An array providing more granular information, particularly useful for form/payload validation (Code 400/422).
* **`request_id` (Optional but highly recommended):** The trace ID to correlate the error response with internal server logs.

## Examples

### Scenario 1: Validation Error (400 Bad Request)

A client tries to create an agent but provides an invalid temperature.

```json
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The provided configuration payload is invalid.",
    "details": [
      {
        "field": "temperature",
        "issue": "Value must be between 0.0 and 2.0."
      }
    ],
    "request_id": "req_a1b2c3d4"
  }
}
```

### Scenario 2: Resource Not Found (404 Not Found)

A client tries to retrieve a specific workflow that doesn't exist.

```json
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Workflow with ID 'wf_999' was not found.",
    "request_id": "req_e5f6g7h8"
  }
}
```

### Scenario 3: Internal Server Error (500 Internal Server Error)

The database goes offline while processing a request.

```json
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred while processing your request. Please try again later.",
    "request_id": "req_i9j0k1l2"
  }
}
```

*(Note: Internal details like "Database connection refused" are NOT exposed here, but they MUST be logged internally using the `request_id`.)*
