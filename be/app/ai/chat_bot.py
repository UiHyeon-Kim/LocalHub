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


def tokenize_message(message: str) -> List[str]:
    normalized = re.sub(r"[\s,]+", " ", message.strip())
    return [token for token in normalized.lower().split(" ") if token]


def expand_search_tokens(message: str) -> List[str]:
    synonym_map = {
        "가족": ["가족", "아이", "어린이", "부모님"],
        "아이": ["아이", "어린이", "가족", "유아"],
        "어린이": ["어린이", "아이", "가족"],
        "산책": ["산책", "걷기", "공원", "자연"],
        "비오는": ["비오는", "우천", "실내", "실내장소"],
        "실내": ["실내", "우천", "체험", "전시"],
        "축제": ["축제", "행사", "공연", "페스티벌"],
        "구미": ["구미", "구미시", "경북 구미"],
        "데이트": ["데이트", "로맨틱", "커플", "야경"],
    }

    tokens = tokenize_message(message)
    expanded: List[str] = []

    for token in tokens:
        expanded.append(token)
        for key, synonyms in synonym_map.items():
            if key in token or token in synonyms:
                expanded.extend(synonyms)

    unique_tokens = []
    for token in expanded:
        token = token.strip()
        if token and token not in unique_tokens:
            unique_tokens.append(token)

    return unique_tokens


def compute_match_score(place: Place, message: str, direct_tokens: List[str], expanded_tokens: List[str]) -> int:
    score = 0
    message_lower = message.lower()
    direct_token_set = set(direct_tokens)
    expanded_token_set = set(expanded_tokens)

    field_weights = {
        "title": 20,
        "addr1": 15,
        "content_type": 10,
        "keywords": 25,
    }

    for field_name, weight in field_weights.items():
        value = getattr(place, field_name) or ""
        value_lower = value.lower()

        if message_lower and message_lower in value_lower:
            score += weight * 3

        for token in direct_token_set:
            if token in value_lower:
                score += weight
        for token in expanded_token_set - direct_token_set:
            if token in value_lower:
                score += max(2, weight // 4)

    return score


def search_places(db: Session, message: str, limit: int = 10) -> List[Place]:
    message = message or ""
    if not message.strip():
        return []

    direct_tokens = tokenize_message(message)
    if not direct_tokens:
        return []

    expanded_tokens = expand_search_tokens(message)
    search_tokens = list(dict.fromkeys(direct_tokens + expanded_tokens))
    patterns = [f"%{token}%" for token in search_tokens]

    filters = []
    for pattern in patterns:
        filters.append(
            or_(
                Place.title.ilike(pattern),
                Place.addr1.ilike(pattern),
                Place.content_type.ilike(pattern),
                Place.keywords.ilike(pattern),
            )
        )

    candidates = db.query(Place).filter(or_(*filters)).all()
    scored: List[tuple[int, Place]] = []

    for place in candidates:
        score = compute_match_score(place, message, direct_tokens, expanded_tokens)
        if score >= 20:
            scored.append((score, place))

    if not scored:
        return []

    scored.sort(key=lambda item: item[0], reverse=True)
    return [place for _, place in scored[:limit]]


def build_prompt(message: str, history: List[str], places: List[Place]) -> str:
    recent_context = "\n".join(f"- {item}" for item in history[-3:]) if history else "- 없음"

    place_context_lines = []
    for place in places:
        place_context_lines.append(
            f"- id={place.id}, title={place.title}, addr1={place.addr1 or '-'}, category={place.content_type or '-'}, keywords={place.keywords or '-'}"
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