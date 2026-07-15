from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.place import Place

router = APIRouter(prefix="/api/places", tags=["places"])


def map_place(place: Place) -> dict:
    return {
        "id": place.id,
        "name": place.title,
        "category": place.content_type,
        "address": place.addr1,
        "phone": place.tel,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "image_url": place.firstimage,
    }


@router.get("/search")
def search_places(
    keywords: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Query parameters:
      - keywords: space-separated keywords from frontend, e.g. "조용 자연 산책"
    Behavior:
      - OR 검색: 전달된 키워드 중 하나라도 places.keywords 필드에 부분 문자열로 포함되면 결과에 포함.
      - SQLite 기반으로 `ilike` 사용 (case-insensitive 부분문자열 매칭).
      - 기존 Place 리스트 반환 형식 유지: {"items": [...], "total": N}
    """
    limit = max(1, min(limit, 100))
    offset = max(offset, 0)

    query = db.query(Place)

    if keywords and keywords.strip():
        # 프론트에서 전달한 문자열을 공백 기준으로 분리
        kw_list = [k.strip() for k in keywords.strip().split() if k.strip()]
        if kw_list:
            filters = [Place.keywords.ilike(f"%{kw}%") for kw in kw_list]
            query = query.filter(or_(*filters))

    total = query.count()
    places = query.order_by(Place.id).offset(offset).limit(limit).all()

    return {"items": [map_place(p) for p in places], "total": total}