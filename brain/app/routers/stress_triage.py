from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.agents.stress_triage_agent import run_triage
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/triage", tags=["triage"])


class Message(BaseModel):
    role: str   # "user" or "assistant"
    content: str


class TriageChatRequest(BaseModel):
    messages: list[Message]


class TriageResult(BaseModel):
    stress_type: str
    severity: str
    summary: str


class TriageChatResponse(BaseModel):
    reply: str
    complete: bool
    triage: Optional[TriageResult] = None


@router.post("/chat", response_model=TriageChatResponse)
async def triage_chat(request: TriageChatRequest):
    """
    Send the next user message and get the agent's reply.
    Pass the full conversation history on every call.
    When complete=True, the triage result is ready.
    """
    if not request.messages:
        raise HTTPException(status_code=400, detail="messages cannot be empty")

    # Validate roles
    for msg in request.messages:
        if msg.role not in ("user", "assistant"):
            raise HTTPException(status_code=400, detail=f"Invalid role: {msg.role}")

    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    result = await run_triage(messages)
    return TriageChatResponse(**result)
