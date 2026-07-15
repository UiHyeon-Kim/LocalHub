import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from fastapi import APIRouter, HTTPException, Query

from app.core.config import TOUR_API_SERVICE_KEY


TOUR_API_BASE_URL = "https://apis.data.go.kr/B551011/KorService2"
REQUEST_TIMEOUT_SECONDS = 10

router = APIRouter(prefix="/api/tourism", tags=["tourism"])


def request_tour_api(endpoint: str, **params: int) -> dict[str, Any]:
    if not TOUR_API_SERVICE_KEY:
        raise HTTPException(
            status_code=500,
            detail="TOUR_API_SERVICE_KEY is not configured",
        )

    query_params = {
        "serviceKey": TOUR_API_SERVICE_KEY,
        "MobileApp": "AppTest",
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


@router.get("/common")
def get_common_info(
    content_id: int = Query(..., gt=0),
) -> dict[str, Any]:
    return request_tour_api("detailCommon2", contentId=content_id)


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