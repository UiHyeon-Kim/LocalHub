import os
import re
from pathlib import Path
from typing import Any, List

from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.place import Place
from app.prompts.localhub_chat import LOCALHUB_CHAT_INSTRUCTIONS

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def normalize_history(history: List[Any]) -> List[str]:
    if not isinstance(history, list):
        return []

    items: List[str] = []
    for entry in history[-3:]:
        if isinstance(entry, str) and entry.strip():
            items.append(entry.strip())
        elif isinstance(entry, dict):
            content = entry.get("content") or entry.get("message")
            if isinstance(content, str) and content.strip():
                items.append(content.strip())

    return items


def search_places(db: Session, message: str, limit: int = 5) -> List[Place]:
    tokens = [token for token in re.split(r"[\s,]+", message.strip()) if token]
    if not tokens:
        return []

    filters = []
    for token in tokens:
        pattern = f"%{token}%"
        filters.append(
            or_(
                Place.title.ilike(pattern),
                Place.addr1.ilike(pattern),
                Place.content_type.ilike(pattern),
            )
        )

    query = db.query(Place).filter(or_(*filters))
    return query.order_by(Place.id).limit(limit).all()


def build_prompt(message: str, history: List[str], places: List[Place]) -> str:
    recent_context = "\n".join(f"- {item}" for item in history[-3:]) if history else "- 없음"

    place_context_lines = []
    for place in places:
        place_context_lines.append(
            f"- id={place.id}, title={place.title}, addr1={place.addr1 or '-'}, content_type={place.content_type or '-'}"
        )

    return f"""
{LOCALHUB_CHAT_INSTRUCTIONS}

사용자 질문: {message}

최근 대화 맥락:
{recent_context}

검색된 장소 데이터:
{chr(10).join(place_context_lines) if place_context_lines else '- 검색된 장소 없음'}

지시:
- 오직 위 검색된 장소 데이터만 사용해 답변하세요.
- DB에 없는 정보는 추가하지 마세요.
- 존재하지 않는 주소, 설명, 카테고리, 운영시간, 가격, 행사 정보를 만들지 마세요.
- 답변은 한국어로 짧고 자연스럽게 작성하세요.
""".strip()


def generate_chat_answer(db: Session, message: str, history: List[Any]):
    if not message or not message.strip():
        return None

    places = search_places(db, message)
    if not places:
        return {
            "answer": "현재 제공된 데이터에서는 확인되지 않습니다.",
            "references": [],
        }

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": "OpenAI 연결 안됨",
            "references": [],
        }

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 LocalHub의 지역 안내 도우미입니다.",
                },
                {
                    "role": "user",
                    "content": build_prompt(message, normalize_history(history), places),
                },
            ],
        )
        answer = response.choices[0].message.content
        if not answer or not answer.strip():
            raise RuntimeError("empty")
    except Exception as exc:
        import traceback
        print("OpenAI error:", repr(exc))
        traceback.print_exc()
        return {
            "answer": "OpenAI 연결 안됨",
            "references": [],
        }

    references = [
        {
            "id": place.id,
            "type": "place",
            "title": place.title,
            "path": f"/places/{place.id}",
        }
        for place in places
    ]

    return {
        "answer": answer.strip(),
        "references": references,
    }