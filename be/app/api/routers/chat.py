from typing import Optional

from fastapi import APIRouter, Body, HTTPException, status

from app.core.config import OPENAI_MOCK_ENABLED, OPENAI_MODEL
from app.schemas.chat import ChatResponse
from app.services.openai_service import OpenAIService, OpenAIServiceError

router = APIRouter(
    prefix="/api/chat",
    tags=["AI Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    summary="LocalHub AI 질문",
)
def create_chat_response(
    payload: Optional[dict] = Body(default=None),
) -> ChatResponse:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="request body is required")

    message = payload.get("message")
    if not isinstance(message, str) or not message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    service = OpenAIService()

    try:
        answer = service.generate_answer(message.strip())
    except OpenAIServiceError:
        answer = "현재 제공된 데이터에서는 확인되지 않습니다."

    return ChatResponse(
        answer=answer,
        model=OPENAI_MODEL,
        is_mock=OPENAI_MOCK_ENABLED,
    )