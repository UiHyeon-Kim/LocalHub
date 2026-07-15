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
        create_response = self.client.post(
            "/api/posts",
            json={
                "title": "테스트 제목",
                "content": "테스트 내용",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "1234",
            },
        )
        self.assertEqual(create_response.status_code, 201)

        list_response = self.client.get("/api/posts?keyword=금오산&page=1&size=10")
        self.assertEqual(list_response.status_code, 200)

        payload = list_response.json()
        self.assertEqual(payload["total"], 1)
        self.assertEqual(payload["page"], 1)
        self.assertEqual(payload["size"], 10)
        self.assertEqual(len(payload["items"]), 1)
        self.assertNotIn("password", payload["items"][0])

    def test_get_post_increments_view_count_and_omits_password(self):
        create_response = self.client.post(
            "/api/posts",
            json={
                "title": "조회수 테스트",
                "content": "조회수 증가 확인",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "1234",
            },
        )
        post_id = create_response.json()["id"]

        detail_response = self.client.get(f"/api/posts/{post_id}")
        self.assertEqual(detail_response.status_code, 200)

        body = detail_response.json()
        self.assertEqual(body["view_count"], 1)
        self.assertNotIn("password", body)

    def test_list_posts_supports_keyword_search_and_pagination(self):
        self.client.post(
            "/api/posts",
            json={
                "title": "금오산 산책 후기",
                "content": "좋았어요",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "1234",
            },
        )
        self.client.post(
            "/api/posts",
            json={
                "title": "구미역 방문",
                "content": "금오산 근처라서 들렀어요",
                "category": "맛집",
                "location_name": "구미역",
                "password": "5678",
            },
        )

        response = self.client.get("/api/posts?keyword=금오산&page=1&size=1")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["total"], 2)
        self.assertEqual(payload["page"], 1)
        self.assertEqual(payload["size"], 1)
        self.assertEqual(len(payload["items"]), 1)

    def test_create_post_rejects_blank_required_fields(self):
        response = self.client.post(
            "/api/posts",
            json={
                "title": "   ",
                "content": "내용",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_update_and_delete_post_password_validation(self):
        create_response = self.client.post(
            "/api/posts",
            json={
                "title": "원본 제목",
                "content": "원본 내용",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "1234",
            },
        )
        post_id = create_response.json()["id"]

        wrong_update = self.client.put(
            f"/api/posts/{post_id}",
            json={
                "title": "수정 제목",
                "content": "수정 내용",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "wrong",
            },
        )
        self.assertEqual(wrong_update.status_code, 403)

        missing_update = self.client.put(
            "/api/posts/999999",
            json={
                "title": "수정 제목",
                "content": "수정 내용",
                "category": "여행후기",
                "location_name": "금오산",
                "password": "1234",
            },
        )
        self.assertEqual(missing_update.status_code, 404)

        wrong_delete = self.client.request(
            "DELETE",
            f"/api/posts/{post_id}",
            json={"password": "wrong"},
        )
        self.assertEqual(wrong_delete.status_code, 403)

        missing_delete = self.client.request(
            "DELETE",
            "/api/posts/999999",
            json={"password": "1234"},
        )
        self.assertEqual(missing_delete.status_code, 404)


if __name__ == "__main__":
    unittest.main()