import json
import re
from html import unescape
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from fastapi import APIRouter, HTTPException, Query

from app.core.config import TOUR_API_SERVICE_KEY


TOUR_API_BASE_URL = "https://apis.data.go.kr/B551011/KorService2"
REQUEST_TIMEOUT_SECONDS = 10

router = APIRouter(prefix="/api/tourism", tags=["tourism"])


def request_tour_api(endpoint: str, **params: Any) -> dict[str, Any]:
    if not TOUR_API_SERVICE_KEY:
        raise HTTPException(
            status_code=500,
            detail="TOUR_API_SERVICE_KEY is not configured",
        )

    query_params = {
        "serviceKey": TOUR_API_SERVICE_KEY,
        "MobileApp": "LocalHub",
        "MobileOS": "ETC",
        "pageNo": 1,
        "numOfRows": 10,
        "_type": "json",
        **params,
    }

    url = f"{TOUR_API_BASE_URL}/{endpoint}?{urlencode(query_params)}"

    try:
        with urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Tour API request failed with status {error.code}",
        ) from error
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise HTTPException(
            status_code=502,
            detail="Tour API request failed",
        ) from error


def extract_first_item(payload: dict[str, Any]) -> dict[str, Any]:
    items = (
        payload.get("response", {})
        .get("body", {})
        .get("items", {})
        .get("item", [])
    )

    if isinstance(items, list):
        return items[0] if items else {}

    if isinstance(items, dict):
        return items

    return {}


def first_non_empty(data: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = data.get(key)

        if value is not None and str(value).strip():
            return str(value).strip()

    return None


def clean_html(value: str | None) -> str | None:
    if not value:
        return None

    cleaned = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = unescape(cleaned).replace("\xa0", " ").strip()

    return cleaned or None


@router.get("/common")
def get_common_info(
    content_id: int = Query(..., gt=0),
    content_type_id: int | None = Query(default=None, gt=0),
) -> dict[str, Any]:
    common_payload = request_tour_api(
        "detailCommon2",
        contentId=content_id,
    )
    common = extract_first_item(common_payload)

    resolved_content_type_id = content_type_id

    if resolved_content_type_id is None:
        raw_content_type_id = common.get("contenttypeid")

        if raw_content_type_id:
            resolved_content_type_id = int(raw_content_type_id)

    intro: dict[str, Any] = {}

    if resolved_content_type_id is not None:
        intro_payload = request_tour_api(
            "detailIntro2",
            contentId=content_id,
            contentTypeId=resolved_content_type_id,
        )
        intro = extract_first_item(intro_payload)

    address_parts = [
        first_non_empty(common, "addr1"),
        first_non_empty(common, "addr2"),
    ]
    address = " ".join(part for part in address_parts if part) or None

    return {
        "content_id": content_id,
        "content_type_id": resolved_content_type_id,
        "address": clean_html(address),
        "phone": clean_html(
            first_non_empty(
                common,
                "tel",
            )
            or first_non_empty(
                intro,
                "infocenter",
                "infocenterculture",
                "infocenterfood",
                "infocenterlodging",
                "sponsor1tel",
            )
        ),
        "operating_hours": clean_html(
            first_non_empty(
                intro,
                "usetime",
                "usetimeculture",
                "opentime",
                "opentimefood",
                "playtime",
                "checkintime",
            )
        ),
        "fee": clean_html(
            first_non_empty(
                intro,
                "usefee",
                "usefeefestival",
                "usetimefestival",
            )
        ),
    }


@router.get("/intro")
def get_intro_info(
    content_id: int = Query(..., gt=0),
    content_type_id: int = Query(..., gt=0),
) -> dict[str, Any]:
    return request_tour_api(
        "detailIntro2",
        contentId=content_id,
        contentTypeId=content_type_id,
    )