import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from app.main import app


class TourismApiTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.api.routers.tourism.TOUR_API_SERVICE_KEY", "test-service-key")
    @patch("app.api.routers.tourism.urlopen")
    def test_get_common_info_requests_detail_common_api(self, mock_urlopen):
        response = mock_urlopen.return_value.__enter__.return_value
        response.read.return_value = b'{"response": {"body": {"items": {}}}}'

        result = self.client.get("/api/tourism/common?content_id=3310483")

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {"response": {"body": {"items": {}}}})

        request_url = mock_urlopen.call_args.args[0]
        parsed = urlparse(request_url)
        query = parse_qs(parsed.query)
        self.assertEqual(parsed.path, "/B551011/KorService2/detailCommon2")
        self.assertEqual(query["contentId"], ["3310483"])
        self.assertEqual(query["serviceKey"], ["test-service-key"])
        self.assertEqual(query["MobileApp"], ["AppTest"])
        self.assertEqual(query["MobileOS"], ["ETC"])

    @patch("app.api.routers.tourism.TOUR_API_SERVICE_KEY", "test-service-key")
    @patch("app.api.routers.tourism.urlopen")
    def test_get_intro_info_requests_detail_intro_api(self, mock_urlopen):
        response = mock_urlopen.return_value.__enter__.return_value
        response.read.return_value = b'{"response": {"body": {"items": {}}}}'

        result = self.client.get(
            "/api/tourism/intro?content_id=3310483&content_type_id=15"
        )

        self.assertEqual(result.status_code, 200)

        request_url = mock_urlopen.call_args.args[0]
        parsed = urlparse(request_url)
        query = parse_qs(parsed.query)
        self.assertEqual(parsed.path, "/B551011/KorService2/detailIntro2")
        self.assertEqual(query["contentId"], ["3310483"])
        self.assertEqual(query["contentTypeId"], ["15"])

    def test_get_intro_info_requires_content_type_id(self):
        result = self.client.get("/api/tourism/intro?content_id=3310483")

        self.assertEqual(result.status_code, 422)


if __name__ == "__main__":
    unittest.main()