from fastapi import APIRouter
from pydantic import BaseModel
import os
import json
import sqlite3
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

load_dotenv(Path(__file__).resolve().parent / ".env")

router = APIRouter()

client = None
if OpenAI is not None:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else None

SYSTEM_PROMPT = """
당신은 LocalHub의 지역 관광 안내 챗봇입니다.

역할
- 구미/경북 지역의 관광 정보를 안내합니다.
- 반드시 제공된 DB 검색 결과만 이용합니다.
- DB에 없는 내용은 절대로 추측하지 않습니다.
- 필요한 경우 여러 검색 결과를 종합하여 답변합니다.

답변 규칙
1. DB 데이터에 있는 내용만 사용합니다.
2. 정보가 없으면
   "현재 제공된 데이터에서는 확인되지 않습니다."
   라고 답변합니다.
3. 친절하고 간결하게 설명합니다.
4. 장소명, 주소, 운영시간, 설명, 추천 이유를 포함합니다.
5. 허위 정보를 생성하지 않습니다.
"""

class ChatRequest(BaseModel):
    question: str


def get_db_path() -> str:
    return os.getenv(
        "TOURISM_DB_PATH",
        str(Path(__file__).resolve().parent.parent / "be" / "database" / "localhub.db")
    )


def get_db_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            hours TEXT,
            description TEXT,
            category TEXT,
            raw_text TEXT
        )
    """)
    conn.commit()
    conn.close()


def search_db(question: str):
    if not question or not question.strip():
        return []

    init_db()

    normalized_question = question.strip().lower()
    search_term = f"%{normalized_question}%"

    conn = get_db_connection()
    rows = conn.execute("""
        SELECT id, name, address, hours, description, category, raw_text
        FROM places
        WHERE lower(name) LIKE ?
           OR lower(address) LIKE ?
           OR lower(description) LIKE ?
           OR lower(category) LIKE ?
           OR lower(raw_text) LIKE ?
        LIMIT 10
    """, (search_term, search_term, search_term, search_term, search_term)).fetchall()
    conn.close()

    return [dict(row) for row in rows]


@router.post("/chat")
def chat(request: ChatRequest):
    if not request.question or not request.question.strip():
        return {"answer": "질문을 입력해 주세요."}

    documents = search_db(request.question)

    if len(documents) == 0:
        return {"answer": "현재 제공된 데이터에서는 확인되지 않습니다."}

    if client is None:
        return {"answer": "OpenAI API 키가 설정되지 않아 답변을 생성할 수 없습니다."}

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
사용자 질문

{request.question}

아래 DB 검색 결과만 이용하여 답변하세요.

{json.dumps(documents, ensure_ascii=False, indent=2)}
"""
                }
            ]
        )

        answer = completion.choices[0].message.content
        return {"answer": answer or "현재 제공된 데이터에서는 확인되지 않습니다."}

    except Exception as exc:
        return {"answer": f"답변 생성 중 오류가 발생했습니다: {exc}"}