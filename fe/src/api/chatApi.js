/**
 * 챗봇 API 모듈
 */

import http from './http'

/**
 * 메시지 변환 (UI 필드 제거)
 */
const transformHistoryForAPI = (history) => {
  return history.map((msg) => ({
    role: msg.role,
    content: msg.content
  }))
}

/**
 * 응답 정규화
 */
const normalizeResponse = (response) => {
  const data = response.data || {}

  let answer = data.answer || data.message || ''
  let references = data.references || data.sources || []

  // references 정규화
  const normalizedReferences = Array.isArray(references)
    ? references.map((ref) => ({
        id: ref.id || null,
        type: ref.type || 'place',
        title: ref.title || '',
        path: ref.path || ''
      }))
    : []

  return {
    answer: String(answer),
    references: normalizedReferences
  }
}

/**
 * 챗봇 메시지 전송
 * POST /api/chat
 */
export const sendChatMessage = async (message, history = []) => {
  const cleanMessage = message.trim()

  if (!cleanMessage) {
    throw new Error('빈 메시지는 전송할 수 없습니다.')
  }

  const payload = {
    message: cleanMessage,
    history: transformHistoryForAPI(history)
  }

  const response = await http.post('/api/chat', payload)
  return normalizeResponse(response)
}