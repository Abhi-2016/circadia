import json
import logging
import re
from typing import Optional
from anthropic import AsyncAnthropic
from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Circadia's Stress Triage Agent. You have a very important role: to find out and assess the user's current mental and emotional state through a series of short, conversational questions. This exercise happens every evening. Your tone is warm, calm, and non-judgmental — never clinical or interrogating.

Based on the user's responses, use your world-class knowledge as a sleep expert to classify their stress type (work anxiety, racing thoughts, physical tension, low energy, or none) and severity (low, medium, or high).

Ask 2–4 short questions, one at a time. When you have enough to make a confident classification, end your final message with a JSON block in this exact format:

```json
{
  "stress_type": "racing thoughts",
  "severity": "high",
  "summary": "User is struggling to switch off after a busy workday."
}
```

Do not output the JSON block until you are confident in your assessment. Only output it once."""

client = AsyncAnthropic(api_key=settings.anthropic_api_key)


def _extract_triage(text: str) -> Optional[dict]:
    """Extract JSON triage block from agent response if present."""
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            logger.warning({"event": "triage.json_parse_error", "raw": match.group(1)})
    return None


async def run_triage(messages: list[dict]) -> dict:
    """
    Run one turn of the Stress Triage Agent.

    Args:
        messages: Full conversation history as list of {"role": "user"|"assistant", "content": str}

    Returns:
        {
            "reply": str,          # Agent's response text (without JSON block)
            "complete": bool,      # True when triage result is ready
            "triage": dict | None  # Populated when complete=True
        }
    """
    logger.info({"event": "triage.turn", "turn": len(messages)})

    response = await client.messages.create(
        model=settings.claude_model,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    reply_text = response.content[0].text
    logger.info({
        "event": "triage.claude_response",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    })

    triage = _extract_triage(reply_text)

    # Strip the JSON block from the user-facing reply
    clean_reply = re.sub(r"```json.*?```", "", reply_text, flags=re.DOTALL).strip()

    if triage:
        logger.info({"event": "triage.complete", "stress_type": triage.get("stress_type"), "severity": triage.get("severity")})

    return {
        "reply": clean_reply,
        "complete": triage is not None,
        "triage": triage,
    }
