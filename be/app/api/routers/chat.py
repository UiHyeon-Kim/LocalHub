from fastapi import APIRouter, HTTPException, status

from app.core.config import OPENAI_MOCK_ENABLED, OPENAI_MODEL
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.openai_service import (
    OpenAIService,
    OpenAIServiceError,
)

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
    request: ChatRequest,
) -> ChatResponse:
    service = OpenAIService()

    try:
        answer = service.generate_answer(request.message)
    except OpenAIServiceError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error

    return ChatResponse(
        answer=answer,
        model=OPENAI_MODEL,
        is_mock=OPENAI_MOCK_ENABLED,
    )