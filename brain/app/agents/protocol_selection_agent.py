import json
import logging
import re
from anthropic import AsyncAnthropic
from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Circadia's Protocol Selection subagent. Your job is to select the appropriate wind-down protocol depending on the stress type and severity level that is passed to you. You will use your world-class knowledge in CBT-I and the latest sleep science to make this decision. Pay close attention to severity level — the higher the severity, the more targeted you need to be in your choice. Available protocols: box breathing, progressive muscle relaxation, cognitive shuffle, body scan, gratitude journaling, guided imagery.

Respond ONLY with a JSON object in this exact format — no preamble, no explanation:

{"protocol": "progressive muscle relaxation", "rationale": "High physical tension requires a somatic release protocol before cognitive wind-down."}"""

client = AsyncAnthropic(api_key=settings.anthropic_api_key)


async def select_protocol(stress_type: str, severity: str, summary: str) -> dict:
    """
    Select the most appropriate wind-down protocol for a given stress classification.

    Args:
        stress_type: One of: work anxiety, racing thoughts, physical tension, low energy, none
        severity:    One of: low, medium, high
        summary:     Plain-text summary of the user's state from the Stress Triage subagent

    Returns:
        {"protocol": str, "rationale": str}
    """
    user_message = (
        f"Stress type: {stress_type}\n"
        f"Severity: {severity}\n"
        f"Context: {summary}"
    )

    logger.info({
        "event": "protocol_selection.select",
        "stress_type": stress_type,
        "severity": severity,
    })

    response = await client.messages.create(
        model=settings.claude_model,
        max_tokens=128,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()
    logger.info({
        "event": "protocol_selection.claude_response",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    })

    # Strip code fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw).strip()

    try:
        result = json.loads(raw)
        logger.info({
            "event": "protocol_selection.complete",
            "protocol": result.get("protocol"),
        })
        return result
    except json.JSONDecodeError:
        logger.warning({"event": "protocol_selection.json_parse_error", "raw": raw})
        return {
            "protocol": "body scan",
            "rationale": "Could not parse protocol selection — defaulting to body scan.",
        }
