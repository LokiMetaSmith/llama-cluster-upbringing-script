import logging
from tools.polyphony_tool import PolyphonyTool

# Context handoff system prompt template
CONTEXT_HANDOFF_PROMPT = """
FreeLLMAPI context handoff:
You are taking over an ongoing conversation from another model (switching to {new_expert}).
Continue the user's task using the conversation context already provided in this request.
Do not restart the task, re-ask already answered setup questions, or discard prior tool results.
Respect the user's latest message as the highest-priority instruction.
"""

def inject_context_handoff(messages: list, new_expert: str) -> list:
    """
    Injects a compact system prompt into the message history for context handoff,
    and broadcasts the handoff transition state to the Keystone Polyphony Swarm.
    """
    logging.info(f"Injecting context handoff system prompt for expert: {new_expert}")

    # Broadcast to Keystone Polyphony
    try:
        polyphony = PolyphonyTool()
        polyphony.execute("share", thought=f"Swarm Context Handoff triggered. Active model switched to: {new_expert}")
    except Exception as e:
        logging.error(f"Failed to broadcast handoff state to Polyphony: {e}")

    # Inject handoff prompt as a system message at the beginning of the messages list
    handoff_message = {
        "role": "system",
        "content": CONTEXT_HANDOFF_PROMPT.format(new_expert=new_expert).strip()
    }

    # Return updated messages
    return [handoff_message] + messages
