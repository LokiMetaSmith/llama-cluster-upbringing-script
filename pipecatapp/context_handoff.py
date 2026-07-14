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

from typing import Optional

def inject_context_handoff(messages: list, new_expert: str, goal_lineage: Optional[str] = None) -> list:
    """
    Injects a compact system prompt into the message history for context handoff,
    and broadcasts the handoff transition state to the Keystone Polyphony Swarm.
    """
    logging.info(f"Injecting context handoff system prompt for expert: {new_expert}")

    # Build the share thought for Polyphony broadcast
    thought = f"Swarm Context Handoff triggered. Active model switched to: {new_expert}"
    if goal_lineage:
        thought = f"Goal Ancestry: {goal_lineage} | {thought}"

    # Broadcast to Keystone Polyphony
    try:
        polyphony = PolyphonyTool()
        polyphony.execute("share", thought=thought)
    except Exception as e:
        logging.error(f"Failed to broadcast handoff state to Polyphony: {e}")

    # Construct the final system prompt with optional Goal Ancestry context
    prompt_text = CONTEXT_HANDOFF_PROMPT.format(new_expert=new_expert).strip()
    if goal_lineage:
        prompt_text = f"Goal Ancestry (Contextual Lineage): {goal_lineage}\n\n{prompt_text}"

    # Inject handoff prompt as a system message at the beginning of the messages list
    handoff_message = {
        "role": "system",
        "content": prompt_text
    }

    # Return updated messages
    return [handoff_message] + messages
