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
from app.models.place import Place
from app.models.post import Post

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


class LocationApiTest(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)

        db = TestingSessionLocal()
        db.add_all(
            [
                Place(
                    title="금오산",
                    content_type="관광지",
                    addr1="구미시 금오동",
                    tel="054-000-0000",
                    latitude=36.1,
                    longitude=128.4,
                    firstimage="http://example.com/1.jpg",
                ),
                Place(
                    title="김천역",
                    content_type="관광지",
                    addr1="김천시 어딘가",
                    tel="054-111-1111",
                    latitude=36.13,
                    longitude=128.12,
                    firstimage="http://example.com/2.jpg",
                ),
                Place(
                    title="좌표 없음 장소",
                    content_type="문화시설",
                    addr1="구미시 테스트동",
                    tel="054-222-2222",
                    latitude=None,
                    longitude=None,
                    firstimage=None,
                ),
            ]
        )
        db.commit()
        db.close()

    def test_list_locations_returns_items_and_total(self):
        response = self.client.get(
            "/api/locations?keyword=금오&category=관광지&district=구미&limit=10&offset=0"
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["total"], 1)
        self.assertEqual(len(payload["items"]), 1)
        self.assertEqual(payload["items"][0]["name"], "금오산")
        self.assertEqual(payload["items"][0]["category"], "관광지")
        self.assertEqual(payload["items"][0]["address"], "구미시 금오동")
        self.assertEqual(payload["items"][0]["image_url"], "http://example.com/1.jpg")

    def test_get_location_detail_returns_mapped_fields(self):
        response = self.client.get("/api/locations/1")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["id"], 1)
        self.assertEqual(payload["name"], "금오산")
        self.assertEqual(payload["category"], "관광지")
        self.assertEqual(payload["address"], "구미시 금오동")
        self.assertEqual(payload["phone"], "054-000-0000")
        self.assertEqual(payload["latitude"], 36.1)
        self.assertEqual(payload["longitude"], 128.4)
        self.assertEqual(payload["image_url"], "http://example.com/1.jpg")

    def test_get_location_detail_missing_id_returns_404(self):
        response = self.client.get("/api/locations/999")
        self.assertEqual(response.status_code, 404)

    def test_get_location_detail_increments_view_count(self):
        self.client.get("/api/locations/1")

        db = TestingSessionLocal()
        place = db.query(Place).filter(Place.id == 1).first()
        self.assertEqual(place.view_count, 1)
        db.close()

    def test_get_nearby_returns_closest_locations_and_excludes_self(self):
        response = self.client.get("/api/locations/1/nearby?limit=3")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["id"], 2)
        self.assertEqual(payload[0]["name"], "김천역")

    def test_get_nearby_without_coordinates_returns_empty_list(self):
        response = self.client.get("/api/locations/3/nearby?limit=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_location_ranking_orders_places_by_score(self):
        db = TestingSessionLocal()
        db.add_all(
            [
                Post(
                    title="금오산 후기",
                    content="좋았어요",
                    category="여행후기",
                    location_name="금오산",
                    place_id=1,
                    password="1234",
                ),
                Post(
                    title="금오산 두번째 후기",
                    content="추천해요",
                    category="여행후기",
                    location_name="금오산",
                    password="1234",
                ),
                Post(
                    title="김천역 후기",
                    content="편리했습니다",
                    category="여행후기",
                    location_name="김천역",
                    password="1234",
                ),
            ]
        )
        db.commit()
        db.close()

        self.client.get("/api/locations/1")
        self.client.get("/api/locations/1")
        self.client.get("/api/locations/2")

        response = self.client.get("/api/locations/ranking?limit=5")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(len(payload["items"]), 3)
        self.assertEqual(payload["items"][0]["id"], 1)
        self.assertEqual(payload["items"][0]["score"], 4)
        self.assertEqual(payload["items"][0]["post_count"], 2)
        self.assertEqual(payload["items"][1]["id"], 2)
        self.assertEqual(payload["items"][1]["score"], 2)


if __name__ == "__main__":
    unittest.main()