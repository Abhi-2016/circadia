import json
import logging
import re
from anthropic import AsyncAnthropic
from app.config import settings

logger = logging.getLogger(__name__)

# Pure classification prompt — no conversation, no questions.
# The orchestrator handles conversation; this subagent only classifies.
SYSTEM_PROMPT = """You are Circadia's Stress Triage subagent. You receive a summary of what a user has shared about their current mood and mental state. Your job is to classify their stress type and severity.

Stress types: work anxiety, racing thoughts, physical tension, low energy, none
Severity levels: low, medium, high

Respond ONLY with a JSON object in this exact format — no preamble, no explanation:

{
  "stress_type": "racing thoughts",
  "severity": "high",
  "summary": "User is struggling to switch off after a busy workday."
}"""

client = AsyncAnthropic(api_key=settings.anthropic_api_key)


async def classify_stress(user_context: str) -> dict:
    """
    Classify stress type and severity from a user context summary.

    Args:
        user_context: A plain-text summary of what the user has shared about
                      their current mood and state (provided by the orchestrator).

    Returns:
        {"stress_type": str, "severity": str, "summary": str}
    """
    logger.info({"event": "stress_triage.classify", "context_length": len(user_context)})

    response = await client.messages.create(
        model=settings.claude_model,
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_context}],
    )

    raw = response.content[0].text.strip()
    logger.info({
        "event": "stress_triage.claude_response",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    })

    # Strip code fences if Claude wraps the JSON despite instructions
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw).strip()

    try:
        result = json.loads(raw)
        logger.info({
            "event": "stress_triage.complete",
            "stress_type": result.get("stress_type"),
            "severity": result.get("severity"),
        })
        return result
    except json.JSONDecodeError:
        logger.warning({"event": "stress_triage.json_parse_error", "raw": raw})
        return {
            "stress_type": "unknown",
            "severity": "unknown",
            "summary": "Could not parse stress classification.",
        }
