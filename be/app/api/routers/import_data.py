import json
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine, get_db
from app.models.place import Place

router = APIRouter()

def resolve_data_dir():
    candidates = [
        Path(__file__).resolve().parents[3] / "data",
        Path(__file__).resolve().parents[3] / "be" / "data",
        Path(__file__).resolve().parents[4] / "data",
        Path(__file__).resolve().parents[3].parent / "data",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]

DATA_DIR = resolve_data_dir()

@router.post("/api/import-json")
def import_json(db: Session = Depends(get_db)):
    Base.metadata.create_all(bind=engine)

    if not DATA_DIR.exists():
        return {
            "message": "data directory not found",
            "data_dir": str(DATA_DIR),
            "imported_count": 0,
        }

    json_files = sorted(DATA_DIR.glob("*.json"))

    if not json_files:
        return {
            "message": "no matching json files",
            "imported_count": 0,
            "data_dir": str(DATA_DIR),
        }

    imported_count = 0
    skipped_count = 0
    file_results = []

    for json_file in json_files:
        with json_file.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        items = payload.get("items", [])

        for item in items:
            title = (item.get("title") or "").strip()
            content_type = (payload.get("contentType") or "").strip()
            addr1 = (item.get("addr1") or "").strip()

            if not title:
                continue

            existing = (
                db.query(Place)
                .filter(
                    Place.title == title,
                    Place.content_type == content_type,
                    Place.addr1 == addr1,
                )
                .first()
            )

            if existing:
                skipped_count += 1
                continue

            place = Place(
                content_id=item.get("contentid"),
                content_type_id=item.get("contenttypeid"),
                title=title,
                content_type=content_type,
                addr1=addr1,
                addr2=item.get("addr2"),
                zipcode=item.get("zipcode"),
                tel=item.get("tel"),
                mapx=item.get("mapx"),
                mapy=item.get("mapy"),
                latitude=float(item["mapy"]) if item.get("mapy") else None,
                longitude=float(item["mapx"]) if item.get("mapx") else None,
                firstimage=item.get("firstimage"),
                firstimage2=item.get("firstimage2"),
                createdtime=item.get("createdtime"),
                modifiedtime=item.get("modifiedtime"),
            )
            db.add(place)
            imported_count += 1

        file_results.append({
            "file": json_file.name,
            "items": len(items),
        })

    db.commit()

    return {
        "message": "json imported",
        "file_count": len(json_files),
        "imported_count": imported_count,
        "skipped_count": skipped_count,
        "files": file_results,
    }