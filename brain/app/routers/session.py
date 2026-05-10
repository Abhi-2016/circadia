from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.agents.orchestrator_agent import run_session
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/session", tags=["session"])


class Message(BaseModel):
    role: str    # "user" or "assistant"
    content: str


class SessionChatRequest(BaseModel):
    messages: list[Message]


class SessionChatResponse(BaseModel):
    reply: str
    complete: bool
    session_data: Optional[dict] = None


@router.post("/chat", response_model=SessionChatResponse)
async def session_chat(request: SessionChatRequest):
    """
    Send the next user message and get Circadia's reply.
    Pass the full conversation history on every call.
    When complete=True, the session is fully done (wind-down delivered).
    """
    if not request.messages:
        raise HTTPException(status_code=400, detail="messages cannot be empty")

    for msg in request.messages:
        if msg.role not in ("user", "assistant"):
            raise HTTPException(status_code=400, detail=f"Invalid role: {msg.role}")

    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    result = await run_session(messages)
    return SessionChatResponse(**result)
