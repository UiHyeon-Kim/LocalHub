/**
 * FastAPI 응답을 Vue 화면 모델로 변환
 */

const toCamelCase = (str) => {
  return str.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase())
}

const transformKeys = (obj) => {
  if (!obj || typeof obj !== 'object') return obj

  if (Array.isArray(obj)) {
    return obj.map(transformKeys)
  }

  const transformed = {}
  for (const [key, value] of Object.entries(obj)) {
    const camelKey = toCamelCase(key)
    if (Array.isArray(value)) {
      transformed[camelKey] = value
    } else if (typeof value === 'object' && value !== null) {
      transformed[camelKey] = transformKeys(value)
    } else {
      transformed[camelKey] = value
    }
  }
  return transformed
}

const parseCoordinate = (value) => {
  if (value === null || value === undefined) return null
  const num = Number(value)
  return isNaN(num) ? null : num
}

export const mapPlace = (rawPlace) => {
  if (!rawPlace || typeof rawPlace !== 'object') {
    return null
  }

  const place = transformKeys(rawPlace)

  return {
    id: place.id,
    contentId: place.contentId || null,
    contentTypeId: place.contentTypeId || null,
    name: place.name || place.title || '',
    category: place.category || place.contentType || '',
    shortDescription:
      place.shortDescription ||
      place.address ||
      place.addr1 ||
      '',
    likeCount: place.likeCount ?? place.like_count ?? 0,
    viewCount: place.viewCount ?? place.view_count ?? 0,
    description: place.description || '',
    address: place.address || place.addr1 || '',
    phone: place.phone || place.tel || null,
    operatingHours: place.operatingHours || null,
    fee: place.fee || null,
    latitude: parseCoordinate(
      place.latitude ?? place.mapy,
    ),
    longitude: parseCoordinate(
      place.longitude ?? place.mapx,
    ),
    imageUrl:
      place.imageUrl ||
      place.firstimage ||
      place.firstimage2 ||
      null,
    district: place.district || '',
    distanceKm:
      place.distanceKm ?? null,
    tags: Array.isArray(place.tags)
      ? place.tags
      : [],
    recommendedFor: Array.isArray(place.recommendedFor)
      ? place.recommendedFor
      : [],
    highlights: Array.isArray(place.highlights)
      ? place.highlights
      : [],
  }
}

export const mapPlaces = (rawPlaces) => {
  if (!Array.isArray(rawPlaces)) {
    return []
  }
  return rawPlaces.map(mapPlace).filter((p) => p !== null)
}