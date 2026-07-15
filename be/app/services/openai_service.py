from openai import APIConnectionError, APIStatusError, OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_MAX_OUTPUT_TOKENS,
    OPENAI_MOCK_ENABLED,
    OPENAI_MODEL,
    OPENAI_TIMEOUT_SECONDS,
)
from app.prompts.localhub_chat import LOCALHUB_CHAT_INSTRUCTIONS


class OpenAIServiceError(Exception):
    """OpenAI API 호출 실패를 애플리케이션 오류로 변환한다."""


class OpenAIService:
    def __init__(self) -> None:
        self._client = (
            None
            if OPENAI_MOCK_ENABLED
            else OpenAI(
                api_key=OPENAI_API_KEY,
                timeout=OPENAI_TIMEOUT_SECONDS,
            )
        )

    def generate_answer(self, message: str) -> str:
        if OPENAI_MOCK_ENABLED:
            return self._generate_mock_answer(message)

        if not OPENAI_API_KEY:
            raise OpenAIServiceError(
                "OPENAI_API_KEY가 설정되지 않았습니다."
            )

        if self._client is None:
            raise OpenAIServiceError(
                "OpenAI 클라이언트가 초기화되지 않았습니다."
            )

        try:
            response = self._client.responses.create(
                model=OPENAI_MODEL,
                instructions=LOCALHUB_CHAT_INSTRUCTIONS,
                input=message,
                max_output_tokens=OPENAI_MAX_OUTPUT_TOKENS,
            )
        except APIConnectionError as error:
            raise OpenAIServiceError(
                "OpenAI 서버에 연결할 수 없습니다."
            ) from error
        except APIStatusError as error:
            raise OpenAIServiceError(
                f"OpenAI API 요청이 실패했습니다. status={error.status_code}"
            ) from error

        answer = response.output_text.strip()

        if not answer:
            raise OpenAIServiceError(
                "OpenAI API에서 빈 응답을 반환했습니다."
            )

        return answer

    @staticmethod
    def _generate_mock_answer(message: str) -> str:
        return (
            "[Mock 응답] 질문을 정상적으로 전달받았습니다.\n"
            f"입력 내용: {message}\n"
            "OpenAI API 키가 설정되면 실제 AI 응답으로 전환됩니다."
        )