import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.base import Base
from app.models.post import Post


class PostModelTest(unittest.TestCase):
    def test_post_model_has_expected_columns(self):
        column_names = {column.name for column in Post.__table__.columns}

        self.assertIn("id", column_names)
        self.assertIn("title", column_names)
        self.assertIn("content", column_names)
        self.assertIn("category", column_names)
        self.assertIn("location_name", column_names)
        self.assertIn("password", column_names)
        self.assertIn("view_count", column_names)
        self.assertIn("created_at", column_names)
        self.assertIn("updated_at", column_names)

    def test_post_model_is_registered_in_metadata(self):
        self.assertIn("posts", Base.metadata.tables)


if __name__ == "__main__":
    unittest.main()