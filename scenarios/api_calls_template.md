# API Call Scenario Template

This template provides a standardized structure for documenting API calls, ensuring consistency and clarity across our systems.

## Overview

* **API Name:** [Name of the API, e.g., "User Creation API"]
* **Description:** [A brief description of what this API call accomplishes]
* **Target System:** [e.g., Nomad, Consul, Pipecat Backend]

## Endpoint Details

* **Base URL:** `[e.g., https://api.example.com/v1]`
* **Endpoint Path:** `[e.g., /users]`
* **HTTP Method:** `[e.g., GET, POST, PUT, DELETE, PATCH]`
* **Authentication Required:** `[Yes/No]`
* **Authentication Type:** `[e.g., Bearer Token, API Key, mTLS]`

## Request Details

### Headers

| Header Name       | Type     | Required | Description                                      | Example Value                 |
| :---------------- | :------- | :------- | :----------------------------------------------- | :---------------------------- |
| `Content-Type`    | `string` | Yes      | Media type of the resource                       | `application/json`            |
| `Authorization`   | `string` | Yes      | Authentication token                             | `Bearer <token>`              |
| `X-Request-ID`    | `string` | No       | Unique identifier for tracing the request        | `123e4567-e89b-12d3-a456-...` |

### Path Parameters

| Parameter | Type     | Required | Description                     | Example Value |
| :-------- | :------- | :------- | :------------------------------ | :------------ |
| `user_id` | `string` | Yes      | Unique identifier for the user  | `usr_12345`   |

### Query Parameters

| Parameter | Type     | Required | Description                     | Example Value |
| :-------- | :------- | :------- | :------------------------------ | :------------ |
| `limit`   | `int`    | No       | Number of items to return       | `50`          |
| `offset`  | `int`    | No       | Number of items to skip         | `0`           |

### Request Body

* **Content-Type:** `application/json`

**JSON Schema / Example Payload:**

```json
{
  "username": "jdoe",
  "email": "jdoe@example.com",
  "roles": ["user", "editor"]
}
```

## Response Details

### Success Response

* **HTTP Status Code:** `200 OK` (or `201 Created`, etc.)
* **Content-Type:** `application/json`

**Expected JSON Response:**

```json
{
  "status": "success",
  "data": {
    "user_id": "usr_12345",
    "username": "jdoe",
    "created_at": "2023-10-27T10:00:00Z"
  }
}
```

### Error Responses

Refer to the standard `error_handling_template.md` for our general error structure. Specific errors for this API might include:

* **400 Bad Request:** Validation failed for the request body (e.g., invalid email format).
* **401 Unauthorized:** Missing or invalid authentication token.
* **403 Forbidden:** User lacks the necessary permissions to create a new user.
* **404 Not Found:** (If applicable, e.g., if a related resource was not found).
* **429 Too Many Requests:** Rate limit exceeded.

## Execution Example (cURL / Python)

**cURL:**

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"username": "jdoe", "email": "jdoe@example.com", "roles": ["user", "editor"]}'
```

**Python (httpx):**

```python
import httpx

url = "https://api.example.com/v1/users"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"
}
data = {
    "username": "jdoe",
    "email": "jdoe@example.com",
    "roles": ["user", "editor"]
}

with httpx.Client() as client:
    response = client.post(url, headers=headers, json=data)
    response.raise_for_status()
    print(response.json())
```
