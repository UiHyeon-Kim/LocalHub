from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=1_000,
        examples=["구미역 근처에서 가볼 만한 곳을 알려줘"],
    )

class ChatResponse(BaseModel):
    answer: str
    model: str
    is_mock: bool