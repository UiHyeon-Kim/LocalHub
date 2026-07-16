/**
 * 장소 API 모듈
 */

import http from './http'
import {
  mapPlace,
  mapPlaces,
} from './mappers/placeMapper'

/**
 * 장소 목록 조회
 * GET /api/locations
 */
export const getPlaces = async (params = {}) => {
  const queryParams = {}

  if (params.keyword && params.keyword.trim()) {
    queryParams.keyword = params.keyword.trim()
  }

  if (
    params.category &&
    params.category !== '전체'
  ) {
    queryParams.category = params.category
  }

  if (params.district) {
    queryParams.district = params.district
  }

  if (
    params.limit !== undefined &&
    params.limit !== null
  ) {
    queryParams.limit = params.limit
  }

  if (
    params.offset !== undefined &&
    params.offset !== null
  ) {
    queryParams.offset = params.offset
  }

  const response = await http.get(
    '/api/locations',
    {
      params: queryParams,
    },
  )

  let items = []
  let total = 0

  if (Array.isArray(response.data)) {
    items = mapPlaces(response.data)
    total = items.length
  } else if (
    response.data &&
    typeof response.data === 'object'
  ) {
    if (Array.isArray(response.data.items)) {
      items = mapPlaces(response.data.items)
    }

    total = response.data.total || 0
  }

  return {
    items,
    total,
  }
}

/**
 * 단일 장소 조회
 * GET /api/locations/{id}
 *
 * 호출 시 백엔드에서 조회수가 1 증가한다.
 */
export const getPlace = async (placeId) => {
  if (!placeId) {
    throw new Error('장소 ID가 필요합니다.')
  }

  const response = await http.get(
    `/api/locations/${placeId}`,
  )

  const place = mapPlace(response.data)

  if (!place) {
    throw new Error(
      '장소 정보를 찾을 수 없습니다.',
    )
  }

  return place
}

/**
 * 장소 좋아요 추가
 * POST /api/locations/{id}/like
 */
export const likePlace = async (placeId) => {
  if (!placeId) {
    throw new Error('장소 ID가 필요합니다.')
  }

  const response = await http.post(
    `/api/locations/${placeId}/like`,
  )

  return {
    liked: response.data.liked === true,
    likeCount:
      response.data.like_count ?? 0,
  }
}

/**
 * 장소 좋아요 취소
 * DELETE /api/locations/{id}/like
 */
export const unlikePlace = async (placeId) => {
  if (!placeId) {
    throw new Error('장소 ID가 필요합니다.')
  }

  const response = await http.delete(
    `/api/locations/${placeId}/like`,
  )

  return {
    liked: response.data.liked === true,
    likeCount:
      response.data.like_count ?? 0,
  }
}

/**
 * 주변 장소 조회
 * GET /api/locations/{id}/nearby
 */
export const getNearbyPlaces = async (
  placeId,
  limit = 3,
  reference = null,
) => {
  if (!placeId) {
    throw new Error('장소 ID가 필요합니다.')
  }

  const params = {
    limit,
  }

  if (
    reference &&
    typeof reference.lat === 'number' &&
    typeof reference.lon === 'number'
  ) {
    params.lat = reference.lat
    params.lon = reference.lon
  }

  const response = await http.get(
    `/api/locations/${placeId}/nearby`,
    {
      params,
    },
  )

  let places = []

  if (Array.isArray(response.data)) {
    places = mapPlaces(response.data)
  } else if (
    response.data &&
    Array.isArray(response.data.items)
  ) {
    places = mapPlaces(response.data.items)
  }

  return places
}

/**
 * 관광 상세 정보 조회
 * GET /api/tourism/common
 */
export const getTourismCommon = async (
  contentId,
  contentTypeId = null,
) => {
  if (!contentId) {
    throw new Error(
      '관광 콘텐츠 ID가 필요합니다.',
    )
  }

  const params = {
    content_id: contentId,
  }

  if (contentTypeId) {
    params.content_type_id = contentTypeId
  }

  const response = await http.get(
    '/api/tourism/common',
    {
      params,
    },
  )

  return response.data
}