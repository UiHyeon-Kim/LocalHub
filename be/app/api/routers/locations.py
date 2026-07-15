from typing import Optional
import math

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.place import Place
from app.models.post import Post

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


@router.get("/ranking")
def get_location_ranking(limit: int = 5, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 100))
    places = db.query(Place).all()

    if not places:
        return {"items": []}

    explicit_counts = {
        place_id: count
        for place_id, count in db.query(Post.place_id, func.count(Post.id))
        .filter(Post.place_id.isnot(None))
        .group_by(Post.place_id)
        .all()
    }

    title_to_id = {place.title: place.id for place in places}
    fallback_counts = {}
    for location_name, count in db.query(Post.location_name, func.count(Post.id)).filter(
        Post.place_id.is_(None),
        Post.location_name.isnot(None),
        Post.location_name != "",
    ).group_by(Post.location_name).all():
        place_id = title_to_id.get(location_name)
        if place_id:
            fallback_counts[place_id] = fallback_counts.get(place_id, 0) + count

    ranking = []
    for place in places:
        post_count = explicit_counts.get(place.id, 0) + fallback_counts.get(place.id, 0)
        score = place.view_count + post_count
        ranking.append((score, post_count, place))

    ranking.sort(key=lambda item: (-item[0], -item[2].view_count, item[2].id))

    items = [
        {
            **map_place(place),
            "view_count": place.view_count,
            "post_count": post_count,
            "score": score,
        }
        for score, post_count, place in ranking[:limit]
    ]

    return {"items": items}


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

    place.view_count += 1
    db.commit()
    db.refresh(place)

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