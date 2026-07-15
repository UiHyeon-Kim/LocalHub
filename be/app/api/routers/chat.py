from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.ai.chat_bot import generate_chat_answer
from app.db.session import get_db

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    history: List[Any] = Field(default_factory=list)


@router.post("")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    result = generate_chat_answer(db, request.message, request.history)
    if result is None:
        raise HTTPException(status_code=400, detail="message is required")

    return result