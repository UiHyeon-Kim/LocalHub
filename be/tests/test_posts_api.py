import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

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


class PostApiTest(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)

    def test_create_and_list_posts(self):
        response = self.client.post(
            "/api/posts",
            json={
                "title": "테스트 제목",
                "content": "테스트 내용",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 201)

        list_response = self.client.get("/api/posts")
        self.assertEqual(list_response.status_code, 200)
        posts = list_response.json()
        self.assertEqual(len(posts), 1)

    def test_update_and_delete_post(self):
        create_response = self.client.post(
            "/api/posts",
            json={
                "title": "원본 제목",
                "content": "원본 내용",
                "password": "1234",
            },
        )
        post_id = create_response.json()["id"]

        update_response = self.client.put(
            f"/api/posts/{post_id}",
            json={
                "title": "수정 제목",
                "content": "수정 내용",
                "password": "1234",
            },
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["title"], "수정 제목")

        delete_response = self.client.request(
            "DELETE",
            f"/api/posts/{post_id}",
            json={"password": "1234"},
        )
        self.assertEqual(delete_response.status_code, 204)


if __name__ == "__main__":
    unittest.main()