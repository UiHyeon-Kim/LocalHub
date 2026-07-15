import app.services.openai_service as openai_service_module
from app.services.openai_service import OpenAIService


def test_service_can_be_created_without_settings(monkeypatch):
    monkeypatch.setattr(openai_service_module, "OPENAI_MOCK_ENABLED", True, raising=False)
    monkeypatch.setattr(openai_service_module, "OPENAI_API_KEY", "", raising=False)
    monkeypatch.setattr(openai_service_module, "OPENAI_MODEL", "gpt-test", raising=False)
    monkeypatch.setattr(openai_service_module, "OPENAI_MAX_OUTPUT_TOKENS", 123, raising=False)
    monkeypatch.setattr(openai_service_module, "OPENAI_TIMEOUT_SECONDS", 9.5, raising=False)

    service = OpenAIService()
    answer = service.generate_answer("안녕")

    assert "안녕" in answer
    assert answer.startswith("[Mock 응답]")
