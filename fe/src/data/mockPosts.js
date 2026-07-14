/**
 * Mock 데이터 - 프론트엔드 개발용
 * 실제 서버나 데이터베이스가 아닌 프론트엔드 개발 단계에서만 사용됩니다.
 * 실제 FastAPI API 연결 시 이 파일은 삭제되고 axios 호출로 대체됩니다.
 */

let mockPosts = [
  {
    id: 12,
    title: '금오산 정상까지 초보자 코스 있나요?',
    content: '안녕하세요. 등산을 처음 하는데 금오산에 초보자도 올라갈 수 있는 코스가 있을까요? 난이도와 소요 시간을 알려주시면 감사하겠습니다.',
    category: '질문',
    password: '1234',
    createdAt: '2024-01-20T10:30:00Z',
    updatedAt: null,
    viewCount: 45,
    locationName: '금오산 도립공원'
  },
  {
    id: 11,
    title: '동락공원 주차비가 얼마예요?',
    content: '주말에 가족과 동락공원에 가려고 하는데 주차비 정보를 알 수 있을까요? 그리고 장시간 주차할 때는 할인이 있나요?',
    category: '생활',
    password: '5678',
    createdAt: '2024-01-19T14:15:00Z',
    updatedAt: null,
    viewCount: 32,
    locationName: '동락공원'
  },
  {
    id: 10,
    title: '구미 숨은 맛집 3곳 추천합니다',
    content: '구미에 자주 가는데 발견한 맛집들을 소개합니다.\n\n1. 북문로 국수 전문점 - 우육국수가 정말 맛있어요\n2. 공단 근처 칼국수 - 현지인 단골이 많습니다\n3. 신동 식당 - 정갈한 반찬과 깔끔한 국물\n\n모두 가성비가 좋습니다!',
    category: '맛집',
    password: 'pass',
    createdAt: '2024-01-18T11:22:00Z',
    updatedAt: '2024-01-19T09:10:00Z',
    viewCount: 78,
    locationName: null
  },
  {
    id: 9,
    title: '낙동강 산책길 자전거 타기 정보',
    content: '낙동강 둔치길에 자전거를 타러 가고 싶은데 대여 장소가 있나요? 그리고 코스 난이도는 어느 정도일까요? 초보자도 가능할까요?',
    category: '질문',
    password: 'abcd',
    createdAt: '2024-01-17T16:45:00Z',
    updatedAt: null,
    viewCount: 56,
    locationName: '낙동강 둔치길'
  },
  {
    id: 8,
    title: '구미문화예술회관 1월 공연 후기',
    content: '지난 주말에 구미문화예술회관에서 본 뮤지컬이 정말 좋았어요. 배우들의 연기도 훌륭하고 무대 세트도 멋있었습니다. 앞으로 자주 찾을 것 같습니다. 구미 주민들도 더 많이 방문했으면 좋겠어요!',
    category: '자유',
    password: '9999',
    createdAt: '2024-01-16T13:20:00Z',
    updatedAt: null,
    viewCount: 41,
    locationName: '구미문화예술회관'
  },
  {
    id: 7,
    title: '아이와 함께 갈 만한 실내 시설',
    content: '비오는 날씨에도 아이와 함께 즐길 수 있는 실내 시설을 찾고 있습니다. 구미에는 어떤 곳들이 있을까요? 추천 부탁드립니다!',
    category: '질문',
    password: 'qwer',
    createdAt: '2024-01-15T09:30:00Z',
    updatedAt: null,
    viewCount: 67,
    locationName: null
  },
  {
    id: 6,
    title: '올봄 구미 벚꽃 축제 일정 안내',
    content: '올해 구미에서 벚꽃 축제가 3월 28일부터 4월 7일까지 개최됩니다. 주요 행사로는 야외 공연, 푸드트럭, 벚꽃 사진 대회 등이 있을 예정입니다. 자세한 정보는 구미시청 홈페이지에서 확인하실 수 있습니다.',
    category: '행사',
    password: '1111',
    createdAt: '2024-01-14T15:00:00Z',
    updatedAt: null,
    viewCount: 102,
    locationName: null
  },
  {
    id: 5,
    title: '구미 야경 명소 알려주세요',
    content: '구미에서 야경이 좋은 곳이 어디가 있을까요? 데이트하기 좋은 장소를 찾고 있습니다. 추천 부탁드려요!',
    category: '질문',
    password: '2222',
    createdAt: '2024-01-13T12:10:00Z',
    updatedAt: null,
    viewCount: 88,
    locationName: null
  },
  {
    id: 4,
    title: '금오산 철쭉 만발 시기',
    content: '금오산에 철쭉이 정말 멋있더라구요. 올해는 언제쯤 철쭉이 만발할 예정인가요? 작년과 비교해서 시기가 비슷한지 궁금합니다.',
    category: '관광',
    password: '3333',
    createdAt: '2024-01-12T10:40:00Z',
    updatedAt: null,
    viewCount: 71,
    locationName: '금오산 도립공원'
  },
  {
    id: 3,
    title: '구미 새로 생긴 카페 정보',
    content: '요즘 구미에 카페가 많이 생기고 있더라구요. 공단 근처에 새로 생긴 카페 알고 계신 분 있나요? 특히 분위기 좋은 카페를 찾고 있습니다.',
    category: '맛집',
    password: '4444',
    createdAt: '2024-01-11T14:25:00Z',
    updatedAt: null,
    viewCount: 54,
    locationName: null
  },
  {
    id: 2,
    title: '주말 가족 나들이 코스 추천',
    content: '주말에 가족과 하루 일정으로 다닐 수 있는 코스를 추천해주세요. 아이가 초등학교 저학년이라 너무 힘들지 않은 장소들을 원합니다. 감사합니다!',
    category: '관광',
    password: '5555',
    createdAt: '2024-01-10T11:50:00Z',
    updatedAt: null,
    viewCount: 93,
    locationName: null
  },
  {
    id: 1,
    title: 'LocalHub 커뮤니티에 오신 것을 환영합니다',
    content: '안녕하세요! LocalHub 익명 커뮤니티에 오신 것을 환영합니다.\n\n이곳은 구미와 경북 지역에 대한 정보를 자유롭게 공유하고 질문할 수 있는 커뮤니티입니다.\n\n회원가입 없이 익명으로 이용할 수 있으며, 수정과 삭제는 작성 시 등록한 비밀번호로 가능합니다.\n\n지역에 대한 다양한 정보와 경험을 함께 나눠주세요!',
    category: '자유',
    password: 'admin',
    createdAt: '2024-01-09T09:00:00Z',
    updatedAt: null,
    viewCount: 156,
    locationName: null
  }
]

/**
 * 전체 게시글 조회
 */
export const getPosts = () => {
  return JSON.parse(JSON.stringify(mockPosts)).sort((a, b) => b.id - a.id)
}

/**
 * ID로 게시글 조회
 */
export const getPostById = (id) => {
  const post = mockPosts.find(p => p.id === Number(id))
  if (!post) return null
  const result = JSON.parse(JSON.stringify(post))
  mockPosts.find(p => p.id === Number(id)).viewCount += 1
  return result
}

/**
 * 검색 및 필터
 */
export const searchPosts = (keyword = '', category = '전체') => {
  let results = mockPosts

  if (category !== '전체') {
    results = results.filter(p => p.category === category)
  }

  if (keyword.trim()) {
    const searchTerm = keyword.toLowerCase().trim()
    results = results.filter(p =>
      p.title.toLowerCase().includes(searchTerm) ||
      p.content.toLowerCase().includes(searchTerm)
    )
  }

  return JSON.parse(JSON.stringify(results)).sort((a, b) => b.id - a.id)
}

/**
 * 게시글 작성
 */
export const createMockPost = (payload) => {
  const { title, content, category, password, locationName } = payload

  const newId = Math.max(...mockPosts.map(p => p.id), 0) + 1
  const now = new Date().toISOString()

  const newPost = {
    id: newId,
    title: title.trim(),
    content: content.trim(),
    category,
    password,
    createdAt: now,
    updatedAt: null,
    viewCount: 0,
    locationName: locationName || null
  }

  mockPosts.push(newPost)
  return JSON.parse(JSON.stringify(newPost))
}

/**
 * 게시글 수정
 */
export const updateMockPost = (id, payload) => {
  const { title, content, category, locationName } = payload

  const post = mockPosts.find(p => p.id === Number(id))
  if (!post) {
    throw new Error('게시글을 찾을 수 없습니다.')
  }

  post.title = title.trim()
  post.content = content.trim()
  post.category = category
  post.locationName = locationName || null
  post.updatedAt = new Date().toISOString()

  return JSON.parse(JSON.stringify(post))
}

/**
 * 게시글 삭제
 */
export const deleteMockPost = (id, password) => {
  const post = mockPosts.find(p => p.id === Number(id))

  if (!post) {
    throw new Error('게시글을 찾을 수 없습니다.')
  }

  if (post.password !== password) {
    throw new Error('비밀번호가 일치하지 않습니다.')
  }

  mockPosts = mockPosts.filter(p => p.id !== Number(id))
  return true
}

/**
 * 비밀번호 검증
 */
export const verifyPostPassword = (id, password) => {
  const post = mockPosts.find(p => p.id === Number(id))

  if (!post) {
    throw new Error('게시글을 찾을 수 없습니다.')
  }

  if (post.password !== password) {
    throw new Error('비밀번호가 일치하지 않습니다.')
  }

  return true
}