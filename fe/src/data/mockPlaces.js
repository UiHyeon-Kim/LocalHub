/**
 * Mock 데이터 - 개발용으로만 사용
 * 실제 공공데이터 API 연결 전까지 화면 개발에 사용되는 임시 데이터입니다.
 * 실제 운영 정보는 공공데이터 포털을 통해 제공받아야 합니다.
 */

export const mockPlaces = [
  {
    id: '1',
    name: '금오산 도립공원',
    category: '관광지',
    shortDescription: '구미를 대표하는 자연경관과 역사문화를 담은 도립공원',
    description: '금오산 도립공원은 해발 976.5m의 금오산을 중심으로 형성된 공원으로, 수려한 자연경관과 역사유적이 어우러져 있습니다. 정상에서는 구미 전경과 주변 경관을 한눈에 볼 수 있으며, 여러 등산로와 산책길이 조성되어 있습니다.',
    address: '경상북도 구미시 신동읍 금오산로 523',
    phone: '054-480-6633',
    operatingHours: '24시간',
    fee: '무료',
    latitude: 36.1089,
    longitude: 128.4136,
    imageUrl: null,
    district: '신동읍',
    tags: ['등산', '자연경관', '사계절'],
    recommendedFor: ['가족 나들이', '등산 활동', '사진 촬영'],
    highlights: ['구미 최고봉', '360도 전망', '역사유적']
  },
  {
    id: '2',
    name: '동락공원',
    category: '레포츠',
    shortDescription: '도심 속 휴식을 제공하는 산림공원',
    description: '동락공원은 구미의 중심 지역에 위치한 산림공원으로, 산책로, 운동시설, 휴게 공간 등 다양한 편의시설을 갖추고 있습니다. 시민들의 건강한 여가활동을 위한 최적의 장소입니다.',
    address: '경상북도 구미시 동락로 46',
    phone: null,
    operatingHours: '06:00 - 22:00',
    fee: '무료',
    latitude: 36.1082,
    longitude: 128.4089,
    imageUrl: 'https://via.placeholder.com/400x300?text=동락공원',
    district: '구미시',
    tags: ['산책', '휴식', '운동'],
    recommendedFor: ['조깅', '산책', '피크닉'],
    highlights: ['도심 속 산림', '잘 정비된 산책로', '운동시설']
  },
  {
    id: '3',
    name: '구미문화예술회관',
    category: '문화시설',
    shortDescription: '다양한 공연과 전시를 즐길 수 있는 문화 거점',
    description: '구미문화예술회관은 지역의 문화예술 활동 중심으로, 대극장과 소극장, 전시갤러리를 보유하고 있습니다. 연중 다양한 공연, 전시, 강좌 등의 문화 프로그램을 개최합니다.',
    address: '경상북도 구미시 도인동 공단로 70',
    phone: '054-450-1700',
    operatingHours: null,
    fee: '프로그램별 상이',
    latitude: 36.1156,
    longitude: 128.4223,
    imageUrl: 'https://via.placeholder.com/400x300?text=구미문화예술회관',
    district: '도인동',
    tags: ['공연', '전시', '문화'],
    recommendedFor: ['공연 관람', '전시 감상', '문화생활'],
    highlights: ['현대식 시설', '다양한 공연', '지역 문화 허브']
  },
  {
    id: '4',
    name: '구미 공단 쇼핑 거리',
    category: '쇼핑',
    shortDescription: '다양한 제품을 만날 수 있는 공단 지역의 쇼핑 명소',
    description: '구미의 산업 중심지인 공단 지역에 형성된 쇼핑 거리로, 의류, 생활용품, 공산품 등 다양한 제품을 저렴한 가격에 만날 수 있습니다.',
    address: '경상북도 구미시 공단로 일원',
    phone: '054-451-0120',
    operatingHours: '10:00 - 20:00',
    fee: null,
    latitude: 36.1128,
    longitude: 128.4178,
    imageUrl: 'https://via.placeholder.com/400x300?text=공단쇼핑',
    district: '공단',
    tags: ['쇼핑', '저가', '상점'],
    recommendedFor: ['쇼핑', '생활용품 구매', '실속 있는 쇼핑'],
    highlights: ['저렴한 가격', '다양한 상품', '접근성']
  },
  {
    id: '5',
    name: '한국 야금 박물관',
    category: '문화시설',
    shortDescription: '구미 산업의 역사를 담은 특성화 박물관',
    description: '한국 야금 박물관은 구미의 주요 산업인 야금산업의 발전 과정과 기술을 소개하는 박물관입니다. 산업 유산과 기술 발전의 역사를 생생하게 체험할 수 있습니다.',
    address: '경상북도 구미시 장재로 20',
    phone: '054-461-7000',
    operatingHours: '09:00 - 18:00',
    fee: '성인 5,000원',
    latitude: 36.1201,
    longitude: 128.4289,
    imageUrl: 'https://via.placeholder.com/400x300?text=야금박물관',
    district: '구미시',
    tags: ['박물관', '산업유산', '체험'],
    recommendedFor: ['박물관 관람', '산업 역사 학습', '가족 단위 방문'],
    highlights: ['특성화 박물관', '산업 역사', '교육 프로그램']
  },
  {
    id: '6',
    name: '낙동강 둔치길',
    category: '여행 코스',
    shortDescription: '낙동강을 따라 산책할 수 있는 자연 친화적인 코스',
    description: '낙동강을 따라 조성된 산책로로, 계절마다 다른 자연의 아름다움을 만날 수 있습니다. 자전거 도로도 함께 조성되어 있어 다양한 방식의 야외활동이 가능합니다.',
    address: '경상북도 구미시 낙동강변 일원',
    phone: '054-480-4000',
    operatingHours: '24시간',
    fee: '무료',
    latitude: 36.1045,
    longitude: 128.4045,
    imageUrl: 'https://via.placeholder.com/400x300?text=낙동강둔치길',
    district: '구미시',
    tags: ['산책', '자전거', '자연', '야외활동'],
    recommendedFor: ['산책', '자전거 타기', '경치 감상'],
    highlights: ['강변 경치', '길이 긴 코스', '사계절 이용 가능']
  }
]

/**
 * Haversine 공식으로 두 지점 간의 거리(km) 계산
 */
const getDistanceKm = (lat1, lon1, lat2, lon2) => {
  const R = 6371 // 지구 반지름 (km)
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return parseFloat((R * c).toFixed(2))
}

/**
 * ID로 장소 조회
 */
export const getPlaceById = (id) => {
  return mockPlaces.find(place => place.id === id) || null
}

/**
 * 추천 장소 조회 (상위 limit개)
 */
export const getFeaturedPlaces = (limit = 3) => {
  return mockPlaces.slice(0, limit)
}

/**
 * 카테고리별 장소 조회
 */
export const getPlacesByCategory = (category) => {
  if (category === '전체') {
    return mockPlaces
  }
  return mockPlaces.filter(place => place.category === category)
}

/**
 * 특정 장소 주변의 가까운 장소 조회
 */
export const getNearbyPlaces = (placeId, limit = 3) => {
  const currentPlace = getPlaceById(placeId)
  if (!currentPlace) return []

  const nearby = mockPlaces
    .filter(place => place.id !== placeId)
    .map(place => ({
      ...place,
      distanceKm: getDistanceKm(
        currentPlace.latitude,
        currentPlace.longitude,
        place.latitude,
        place.longitude
      )
    }))
    .sort((a, b) => a.distanceKm - b.distanceKm)
    .slice(0, limit)

  return nearby
}