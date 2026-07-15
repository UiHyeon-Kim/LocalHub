import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.place import Place

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


class ChatApiTest(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)

    def test_chat_returns_connection_error_when_api_key_missing(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
            response = self.client.post(
                "/api/chat",
                json={"message": "구미 관광지 추천해줘", "history": []},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["answer"], "OpenAI 연결 안됨")
        self.assertEqual(response.json()["references"], [])

    def test_chat_returns_no_data_message_when_db_has_no_match(self):
        response = self.client.post(
            "/api/chat",
            json={"message": "존재하지 않는 장소 추천해줘", "history": []},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["answer"],
            "현재 제공된 데이터에서는 확인되지 않습니다.",
        )
        self.assertEqual(response.json()["references"], [])

    def test_chat_returns_references_for_db_matches(self):
        db = TestingSessionLocal()
        place = Place(title="금오산", content_type="관광지", addr1="구미시 금오동")
        db.add(place)
        db.commit()
        db.refresh(place)
        db.close()

        with patch("app.ai.chat_bot.OpenAI") as mock_openai:
            mock_client = mock_openai.return_value
            mock_client.chat.completions.create.return_value = SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(content="금오산을 추천합니다.")
                    )
                ]
            )

            response = self.client.post(
                "/api/chat",
                json={"message": "금오산 추천해줘", "history": []},
            )

        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertTrue(payload["answer"])
        self.assertTrue(payload["references"])
        self.assertEqual(payload["references"][0]["id"], place.id)
        self.assertEqual(payload["references"][0]["type"], "place")
        self.assertEqual(payload["references"][0]["title"], "금오산")
        self.assertEqual(payload["references"][0]["path"], f"/places/{place.id}")