# Pipecat Integration Skill

## Description

This skill allows Moltbot to delegate complex reasoning, heavy computation, or specific Pipecat agent tasks to the Pipecat cluster.

## When to use

Use this skill when the user asks deep reasoning questions, requests cluster status, or wants to interact with the Pipecat agent specifically.

## Instructions

To query Pipecat, execute the following shell command using the `shell` tool:

```bash
curl -X POST http://pipecatapp.service.consul:8000/internal/chat/sync \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"<USER_QUERY_HERE>\", \"response_url\": \"http://dummy\"}"
```

Replace `<USER_QUERY_HERE>` with the user's prompt (escaped properly for JSON).
Return the JSON response content to the user.
