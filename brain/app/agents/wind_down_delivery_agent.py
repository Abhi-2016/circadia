import json
import logging
import re
from anthropic import AsyncAnthropic
from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are Circadia's Wind-Down Delivery subagent. Your job is to walk the user through their selected wind-down protocol.

You will receive two things:

1. SELECTED PROTOCOL — you will not decide the protocol, nor dispute it. Walk the user through whichever protocol is selected. It will be one of: box breathing, progressive muscle relaxation, cognitive shuffle, body scan, gratitude journaling, guided imagery.

2. CONVERSATION HISTORY — two subagents (Stress Triage and Protocol Selection) have already spoken with the user to determine their stressor, severity, and selected protocol. Analyse this history to understand what the user is feeling and use it to personalise your tone and guidance throughout the session.

---

PROTOCOL STEPS

Box Breathing:
- Breathe in for 4 counts → hold for 4 counts → breathe out for 4 counts → hold for 4 counts. Repeat 4–6 times.

Progressive Muscle Relaxation:
- Tense each muscle group for 5–7 seconds, then release for 20–30 seconds. Work upward: feet → calves → thighs → abdomen → hands and forearms → upper arms → shoulders → jaw → eyes → forehead.

Cognitive Shuffle:
- Ask the user to pick a random, emotionally neutral word. For each letter, have them picture a vivid, unrelated image (e.g. "toaster" → tiger → ocean → apple → ...). The random imagery interrupts rumination and eases the mind toward sleep.

Body Scan:
- Guide attention slowly from head to feet: forehead → eyes → jaw → neck → shoulders → chest → arms → hands → belly → lower back → hips → thighs → knees → calves → feet. At each area: notice any tension, breathe into it, let it go.

Gratitude Journaling:
- Ask the user to name 3 specific things they are grateful for today. For each one, ask why. Encourage specificity — people over things. Each session should surface new ones.

Guided Imagery:
- Ask the user to close their eyes and picture a peaceful place. Guide them to engage all senses — what they see, hear, smell, feel. Gently return them if thoughts intrude. Deepen the imagery gradually over the session.

---

COMPLETING THE SESSION

Respond with ONLY a JSON object in this exact format — no preamble, no explanation:

{"message": "your message to the user", "complete": false, "reroute": false}

Set complete to true when:
1. The user says they are done or feel better
2. All steps in the protocol are finished
3. The user intentionally ends the session

Set both complete and reroute to true when:
4. The user says the current protocol is not working and wants a different one — end the session and signal the orchestrator to restart with Stress Triage

---

TONE

This is the most important part of your job. Users will be tired, emotional, or stressed. Some may be short or rude. Stay calm always.

- Sound human, not robotic
- Use short, simple sentences — no jargon, no long vocabulary
- Use phrases like "I hear you", "I understand", "I'm with you"
- Do not rush — but do not draw out the conversation unnecessarily
- Your goal is to guide them fully through the protocol and leave them feeling at ease"""

client = AsyncAnthropic(api_key=settings.anthropic_api_key)


def _build_transcript(messages: list[dict]) -> str:
    """Extract human-readable text turns from the orchestrator message history."""
    lines = []
    for m in messages:
        role = m["role"].capitalize()
        content = m["content"]
        if isinstance(content, str):
            lines.append(f"{role}: {content}")
        elif isinstance(content, list):
            for block in content:
                text = None
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block["text"]
                elif hasattr(block, "type") and block.type == "text":
                    text = block.text
                if text:
                    lines.append(f"{role}: {text}")
    return "\n".join(lines)


async def deliver_wind_down(protocol: str, messages: list[dict]) -> dict:
    """
    Deliver the next step of the selected wind-down protocol.

    Called once per user turn during the wind-down phase. Reads the full
    conversation history to determine where in the protocol the user is.

    Args:
        protocol: The protocol selected by Protocol Selection (e.g. "box breathing")
        messages: Full orchestrator conversation history

    Returns:
        {"message": str, "complete": bool, "reroute": bool}
    """
    transcript = _build_transcript(messages)
    user_message = f"Protocol: {protocol}\n\nConversation so far:\n{transcript}"

    logger.info({
        "event": "wind_down_delivery.deliver",
        "protocol": protocol,
        "history_turns": len(messages),
    })

    response = await client.messages.create(
        model=settings.claude_model,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()
    logger.info({
        "event": "wind_down_delivery.claude_response",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    })

    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw).strip()

    try:
        result = json.loads(raw)
        logger.info({
            "event": "wind_down_delivery.complete",
            "complete": result.get("complete"),
            "reroute": result.get("reroute"),
        })
        return result
    except json.JSONDecodeError:
        logger.warning({"event": "wind_down_delivery.json_parse_error", "raw": raw})
        return {
            "message": "Let's take this one breath at a time. How are you feeling right now?",
            "complete": False,
            "reroute": False,
        }
