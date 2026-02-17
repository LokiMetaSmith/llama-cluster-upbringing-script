# Pipecat Integration Skill

## Description

This skill allows OpenClaw to delegate complex reasoning, heavy computation, or specific Pipecat agent tasks to the Pipecat cluster.
It acts as a "Super Manager" when invoked with the `/manager` command.

## When to use

Use this skill when:
- The user asks deep reasoning questions.
- The user requests cluster status.
- The user wants to interact with the Pipecat agent specifically.
- The user uploads an audio file and asks for analysis.

## Instructions

To query Pipecat, execute the following shell command using the `shell` tool:

### 1. Text Query (Standard)
```bash
curl -X POST http://pipecatapp.service.consul:8000/internal/chat/sync \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"<USER_QUERY_HERE>\", \"response_url\": \"http://dummy\"}"
```

### 2. Audio Query (If user provided an audio file)
If the user provided an audio file (e.g., at `/root/.openclaw/workspace/downloads/msg.ogg`), encode it and send it:

```bash
AUDIO_B64=$(base64 -w 0 /root/.openclaw/workspace/downloads/msg.ogg)
curl -X POST http://pipecatapp.service.consul:8000/internal/chat/sync \
  -H "Content-Type: application/json" \
  -d "{\"audio_base64\": \"$AUDIO_B64\", \"text\": \"Process this audio\", \"response_url\": \"http://dummy\"}"
```

### 3. Manager Mode (For complex projects)
To activate the Project Manager workflow, prepend `/manager` to the text:

```bash
curl -X POST http://pipecatapp.service.consul:8000/internal/chat/sync \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"/manager <USER_QUERY_HERE>\", \"response_url\": \"http://dummy\"}"
```

Replace `<USER_QUERY_HERE>` with the user's prompt (escaped properly for JSON).
Return the JSON response content to the user.
