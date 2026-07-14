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
    name: place.name || '',
    category: place.category || '',
    shortDescription: place.shortDescription || '',
    description: place.description || '',
    address: place.address || '',
    phone: place.phone || null,
    operatingHours: place.operatingHours || null,
    fee: place.fee || null,
    latitude: parseCoordinate(place.latitude),
    longitude: parseCoordinate(place.longitude),
    imageUrl: place.imageUrl || null,
    district: place.district || '',
    tags: Array.isArray(place.tags) ? place.tags : [],
    recommendedFor: Array.isArray(place.recommendedFor) ? place.recommendedFor : [],
    highlights: Array.isArray(place.highlights) ? place.highlights : []
  }
}

export const mapPlaces = (rawPlaces) => {
  if (!Array.isArray(rawPlaces)) {
    return []
  }
  return rawPlaces.map(mapPlace).filter((p) => p !== null)
}