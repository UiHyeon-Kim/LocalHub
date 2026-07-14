/**
 * 장소 API 모듈
 */

import http from './http'
import { mapPlace, mapPlaces } from './mappers/placeMapper'

/**
 * 장소 목록 조회
 * GET /api/locations
 */
export const getPlaces = async (params = {}) => {
  const queryParams = {}

  if (params.keyword && params.keyword.trim()) {
    queryParams.keyword = params.keyword.trim()
  }
  if (params.category && params.category !== '전체') {
    queryParams.category = params.category
  }
  if (params.district) {
    queryParams.district = params.district
  }
  if (params.limit !== undefined && params.limit !== null) {
    queryParams.limit = params.limit
  }
  if (params.offset !== undefined && params.offset !== null) {
    queryParams.offset = params.offset
  }

  const response = await http.get('/api/locations', { params: queryParams })

  let items = []
  let total = 0

  if (Array.isArray(response.data)) {
    items = mapPlaces(response.data)
    total = items.length
  } else if (response.data && typeof response.data === 'object') {
    if (Array.isArray(response.data.items)) {
      items = mapPlaces(response.data.items)
    }
    total = response.data.total || 0
  }

  return {
    items,
    total
  }
}

/**
 * 단일 장소 조회
 * GET /api/locations/{id}
 */
export const getPlace = async (placeId) => {
  if (!placeId) {
    throw new Error('장소 ID가 필요합니다.')
  }

  const response = await http.get(`/api/locations/${placeId}`)
  const place = mapPlace(response.data)

  if (!place) {
    throw new Error('장소 정보를 찾을 수 없습니다.')
  }

  return place
}

/**
 * 주변 장소 조회
 * GET /api/locations/{id}/nearby?limit={limit}
 *
 * 주의: 이 API가 백엔드에 구현되지 않았을 수 있습니다.
 */
export const getNearbyPlaces = async (placeId, limit = 3) => {
  if (!placeId) {
    throw new Error('장소 ID가 필요합니다.')
  }

  const response = await http.get(`/api/locations/${placeId}/nearby`, {
    params: { limit }
  })

  let places = []

  if (Array.isArray(response.data)) {
    places = mapPlaces(response.data)
  } else if (response.data && Array.isArray(response.data.items)) {
    places = mapPlaces(response.data.items)
  }

  return places
}