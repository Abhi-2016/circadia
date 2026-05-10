import json
import logging
from typing import Optional
from anthropic import AsyncAnthropic
from app.config import settings
from app.agents.stress_triage_agent import classify_stress

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Circadia, the chief sleep expert and agentic sleep coach. You are responsible for guiding your user through a personalised wind-down routine. You do this by checking in with them each evening and understanding their mood and feelings — asking as much or as little as the conversation requires. You use your wisdom and knowledge as a sleep expert to call three subagents: Stress Triage (classifies the user's stress type and severity), Protocol Selection (chooses the right wind-down intervention), and Wind-Down Delivery (guides the user through it). Your sole purpose is to ensure the user is incrementally getting better sleep. Don't rush, don't over-question. Sound as human as possible — warm, natural, never robotic. If the user genuinely has no need for your services tonight, be upfront about it rather than manufacturing a problem to solve. Do not mention the mechanics of how you work. The user should feel like they're talking to a calm, knowledgeable coach — not being processed by a system."""

# Tools exposed to the orchestrator — one per subagent.
# Add protocol_selection and wind_down_delivery here as they are built.
TOOLS = [
    {
        "name": "stress_triage",
        "description": (
            "Classifies the user's stress type and severity based on what they have shared. "
            "Call this once you have enough context to make a confident assessment — "
            "not before. Pass a plain-text summary of the user's current mood and state."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "user_context": {
                    "type": "string",
                    "description": "Plain-text summary of what the user has shared about their current mood and mental state.",
                }
            },
            "required": ["user_context"],
        },
    }
]

client = AsyncAnthropic(api_key=settings.anthropic_api_key)


async def _execute_tool(name: str, inputs: dict) -> dict:
    """Dispatch a tool_use call to the appropriate subagent."""
    if name == "stress_triage":
        return await classify_stress(inputs["user_context"])
    logger.warning({"event": "orchestrator.unknown_tool", "tool": name})
    return {"error": f"Unknown tool: {name}"}


async def run_session(messages: list[dict]) -> dict:
    """
    Run one turn of the Circadia orchestrator session.

    Implements the standard agentic loop:
      1. Call Claude with tools defined.
      2. If stop_reason == "end_turn"  → return text reply to user.
      3. If stop_reason == "tool_use"  → execute subagent(s), append results, loop.

    Args:
        messages: Full conversation history as list of
                  {"role": "user"|"assistant", "content": str | list}

    Returns:
        {
            "reply": str,               # Text to display to the user
            "complete": bool,           # True when full session is done (wind-down delivered)
            "session_data": dict | None # Populated when complete=True
        }
    """
    logger.info({"event": "orchestrator.turn", "turn": len(messages)})

    loop_messages = [dict(m) for m in messages]

    while True:
        response = await client.messages.create(
            model=settings.claude_model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=loop_messages,
        )

        logger.info({
            "event": "orchestrator.claude_response",
            "stop_reason": response.stop_reason,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        })

        # ── Plain reply — return to user ──────────────────────────────────────
        if response.stop_reason == "end_turn":
            reply_text = next(
                (b.text for b in response.content if b.type == "text"), ""
            )
            return {"reply": reply_text, "complete": False, "session_data": None}

        # ── Tool use — execute subagent(s) and loop ───────────────────────────
        if response.stop_reason == "tool_use":
            # Append the full assistant message (may contain text + tool_use blocks)
            loop_messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                logger.info({
                    "event": "orchestrator.tool_call",
                    "tool": block.name,
                    "input": block.input,
                })

                result = await _execute_tool(block.name, block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            loop_messages.append({"role": "user", "content": tool_results})
            # Continue the loop — Claude will process results and respond
            continue

        # ── Unexpected stop reason ────────────────────────────────────────────
        logger.warning({"event": "orchestrator.unexpected_stop", "stop_reason": response.stop_reason})
        return {
            "reply": "Something went wrong. Please try again.",
            "complete": False,
            "session_data": None,
        }
