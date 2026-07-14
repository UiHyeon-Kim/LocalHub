import json
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine, get_db
from app.models.place import Place

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[3] / "data"

@router.post("/api/import-json")
def import_json(db: Session = Depends(get_db)):
    Base.metadata.create_all(bind=engine)

    # SCHEMA.md, SOURCE.md는 제외하고 구미_경북권_*.json만 읽음
    json_files = sorted(DATA_DIR.glob("구미_경북권_*.json"))

    if not json_files:
        return {"message": "no matching json files", "imported_count": 0}

    imported_count = 0

    for json_file in json_files:
        with json_file.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        items = payload.get("items", [])

        for item in items:
            place = Place(
                title=item.get("title", ""),
                content_type=payload.get("contentType", ""),
                address=item.get("addr1", ""),
                latitude=float(item["mapy"]) if item.get("mapy") else None,
                longitude=float(item["mapx"]) if item.get("mapx") else None,
            )
            db.add(place)

        imported_count += len(items)

    db.commit()

    return {
        "message": "json imported",
        "file_count": len(json_files),
        "imported_count": imported_count,
    }