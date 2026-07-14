/**
 * Mock 데이터 - 개발용으로만 사용
 * 실제 공공데이터 API 연결 전까지 화면 개발에 사용되는 임시 데이터입니다.
 * 실제 운영 정보는 공공데이터 포털을 통해 제공받아야 합니다.
 */

const mockPlaces = [
  {
    id: '1',
    name: '금오산 도립공원',
    category: '관광지',
    shortDescription: '구미를 대표하는 자연경관과 역사문화를 담은 도립공원',
    description: '금오산 도립공원은 해발 976.5m의 금오산을 중심으로 형성된 공원으로, 수려한 자연경관과 역사유적이 어우러져 있습니다. 정상에서는 구미 전경과 주변 경관을 한눈에 볼 수 있으며, 여러 등산로와 산책길이 조성되어 있습니다. 봄의 철쭉, 여름의 녹음, 가을의 단풍, 겨울의 설경까지 사계절 내내 다양한 자연의 아름다움을 경험할 수 있습니다. 또한 고려시대부터 이어져 온 문화유산들이 곳곳에 자리하고 있어 역사와 자연을 함께 느낄 수 있는 특별한 장소입니다.',
    address: '경상북도 구미시 신동읍 금오산로 523',
    phone: '054-480-6633',
    operatingHours: '24시간 개방',
    fee: '무료',
    latitude: 36.1089,
    longitude: 128.4136,
    imageUrl: 'https://images.unsplash.com/photo-1469022563149-aa64e87c3ce2?w=1200&h=600&fit=crop',
    district: '신동읍',
    tags: ['등산', '자연경관', '사계절', '전망', '문화유산'],
    recommendedFor: ['가족 나들이', '등산 활동', '사진 촬영', '데이트'],
    highlights: ['해발 976.5m 구미 최고봉', '360도 전망', '역사유적 풍부', '잘 정비된 등산로']
  },
  {
    id: '2',
    name: '동락공원',
    category: '레포츠',
    shortDescription: '도심 속 휴식을 제공하는 산림공원',
    description: '동락공원은 구미의 중심 지역에 위치한 산림공원으로, 산책로, 운동시설, 휴게 공간 등 다양한 편의시설을 갖추고 있습니다. 시민들의 건강한 여가활동을 위한 최적의 장소이며, 대나무 숲길을 비롯한 다양한 테마의 산책로가 있어 매력적입니다. 공원 곳곳에 벤치와 쉼터가 설치되어 있어 가족 단위의 방문객들이 편하게 즐길 수 있습니다. 저녁 시간에 산책로가 밝게 조명되어 야간 산책도 가능합니다.',
    address: '경상북도 구미시 동락로 46',
    phone: '054-480-4000',
    operatingHours: '06:00 - 22:00',
    fee: '무료',
    latitude: 36.1082,
    longitude: 128.4089,
    imageUrl: 'https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=1200&h=600&fit=crop',
    district: '구미시',
    tags: ['산책', '휴식', '운동', '대나무숲', '조명'],
    recommendedFor: ['조깅', '산책', '피크닉', '아침 운동'],
    highlights: ['도심 속 산림', '잘 정비된 산책로', '운동시설 완비', '야간 조명']
  },
  {
    id: '3',
    name: '구미문화예술회관',
    category: '문화시설',
    shortDescription: '다양한 공연과 전시를 즐길 수 있는 문화 거점',
    description: '구미문화예술회관은 지역의 문화예술 활동 중심으로, 대극장과 소극장, 전시갤러리를 보유하고 있습니다. 연중 다양한 공연, 전시, 강좌 등의 문화 프로그램을 개최합니다. 음악회, 연극, 무용, 전시 등 다양한 형태의 문화예술을 경험할 수 있으며, 지역 예술인들의 창작 활동을 지원하는 중요한 문화 플랫폼입니다. 현대식 시설과 우수한 음향 시스템을 갖추고 있어 높은 수준의 공연을 감상할 수 있습니다.',
    address: '경상북도 구미시 도인동 공단로 70',
    phone: '054-450-1700',
    operatingHours: null,
    fee: '프로그램별 상이',
    latitude: 36.1156,
    longitude: 128.4223,
    imageUrl: 'https://images.unsplash.com/photo-1493246507139-91e8fad9978e?w=1200&h=600&fit=crop',
    district: '도인동',
    tags: ['공연', '전시', '문화', '예술', '강좌'],
    recommendedFor: ['공연 관람', '전시 감상', '문화생활', '문화 교육'],
    highlights: ['현대식 시설', '다양한 공연', '지역 문화 허브', '높은 음향 수준']
  },
  {
    id: '4',
    name: '한국 야금 박물관',
    category: '문화시설',
    shortDescription: '구미 산업의 역사를 담은 특성화 박물관',
    description: '한국 야금 박물관은 구미의 주요 산업인 야금산업의 발전 과정과 기술을 소개하는 박물관입니다. 산업 유산과 기술 발전의 역사를 생생하게 체험할 수 있습니다. 다양한 전시물과 대화형 체험 공간을 통해 우리 산업의 발전상을 이해할 수 있으며, 학생들의 교육 현장으로도 많이 활용되고 있습니다. 정기적으로 특별 전시와 교육 프로그램을 운영하고 있습니다.',
    address: '경상북도 구미시 장재로 20',
    phone: null,
    operatingHours: '09:00 - 18:00',
    fee: '성인 5,000원',
    latitude: 36.1201,
    longitude: 128.4289,
    imageUrl: null,
    district: '구미시',
    tags: ['박물관', '산업유산', '체험', '교육', '기술'],
    recommendedFor: ['박물관 관람', '산업 역사 학습', '가족 단위 방문', '학교 견학'],
    highlights: ['특성화 박물관', '산업 역사', '교육 프로그램', '체험 공간']
  },
  {
    id: '5',
    name: '낙동강 둔치길',
    category: '여행 코스',
    shortDescription: '낙동강을 따라 산책할 수 있는 자연 친화적인 코스',
    description: '낙동강을 따라 조성된 산책로로, 계절마다 다른 자연의 아름다움을 만날 수 있습니다. 자전거 도로도 함께 조성되어 있어 다양한 방식의 야외활동이 가능합니다. 긴 산책로로 인해 충분한 운동량을 보장하며, 낙동강의 자연 생태를 관찰할 수 있는 좋은 기회를 제공합니다. 특히 일몰 시간의 낙동강 경관은 매우 아름다우며, 사진 촬영의 명소로 알려져 있습니다.',
    address: '경상북도 구미시 낙동강변 일원',
    phone: '054-480-4000',
    operatingHours: '24시간',
    fee: '무료',
    latitude: 36.1045,
    longitude: 128.4045,
    imageUrl: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=600&fit=crop',
    district: '구미시',
    tags: ['산책', '자전거', '자연', '야외활동', '일몰'],
    recommendedFor: ['산책', '자전거 타기', '경치 감상', '사진 촬영'],
    highlights: ['강변 경치', '길이 긴 코스', '사계절 이용 가능', '일몰 명소']
  },
  {
    id: '6',
    name: '구미공단 쇼핑거리',
    category: '쇼핑',
    shortDescription: '다양한 제품을 만날 수 있는 공단 지역의 쇼핑 명소',
    description: '구미의 산업 중심지인 공단 지역에 형성된 쇼핑 거리로, 의류, 생활용품, 공산품 등 다양한 제품을 저렴한 가격에 만날 수 있습니다. 많은 상점들이 밀집해 있어 한 장소에서 다양한 쇼핑을 즐길 수 있습니다. 대형 마트와 전문점들이 함께 있어 필요한 모든 것을 찾을 수 있으며, 주말에는 많은 쇼핑객으로 활성을 띱니다.',
    address: '경상북도 구미시 공단로 일원',
    phone: '054-451-0120',
    operatingHours: '10:00 - 20:00',
    fee: null,
    latitude: 36.1128,
    longitude: 128.4178,
    imageUrl: 'https://images.unsplash.com/photo-1555529669-e69e7ea0bb9b?w=1200&h=600&fit=crop',
    district: '공단',
    tags: ['쇼핑', '저가', '상점', '마트', '유통'],
    recommendedFor: ['쇼핑', '생활용품 구매', '실속 있는 쇼핑', '가족 나들이'],
    highlights: ['저렴한 가격', '다양한 상품', '접근성 좋음', '대형 시설']
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

export { mockPlaces }