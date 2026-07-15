from typing import List, Optional
import math

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.place import Place

router = APIRouter(prefix="/api/locations", tags=["locations"])


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


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return math.hypot(lat1 - lat2, lon1 - lon2)


@router.get("")
def list_locations(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    district: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    limit = max(1, min(limit, 100))
    offset = max(offset, 0)

    query = db.query(Place)

    if keyword and keyword.strip():
        keyword_value = f"%{keyword.strip()}%"
        query = query.filter(
            or_(
                Place.title.ilike(keyword_value),
                Place.addr1.ilike(keyword_value),
            )
        )

    if category and category.strip():
        query = query.filter(Place.content_type == category.strip())

    if district and district.strip():
        district_value = f"%{district.strip()}%"
        query = query.filter(Place.addr1.ilike(district_value))

    total = query.count()
    places = query.order_by(Place.id).offset(offset).limit(limit).all()

    return {"items": [map_place(place) for place in places], "total": total}


@router.get("/{location_id}")
def get_location(location_id: int, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == location_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="location not found")

    return map_place(place)


@router.get("/{location_id}/nearby")
def get_location_nearby(
    location_id: int,
    limit: int = 3,
    db: Session = Depends(get_db),
):
    place = db.query(Place).filter(Place.id == location_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="location not found")

    if place.latitude is None or place.longitude is None:
        return []

    nearby_places = (
        db.query(Place)
        .filter(
            Place.id != location_id,
            Place.latitude.isnot(None),
            Place.longitude.isnot(None),
        )
        .all()
    )

    nearby_places.sort(
        key=lambda other: calculate_distance(
            place.latitude,
            place.longitude,
            other.latitude,
            other.longitude,
        )
    )

    return [map_place(other) for other in nearby_places[: max(1, limit)]]