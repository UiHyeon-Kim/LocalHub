<template>
  <!-- 플로팅 버튼 (접힌 상태) -->
  <button
    v-if="!isOpen"
    @click="isOpen = true"
    aria-label="지역 정보 챗봇 열기"
    class="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-primary)] text-white shadow-xl transition-all hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
  >
    <span class="text-2xl">💬</span>
  </button>

  <!-- 챗봇 위젯 (펼친 상태) -->
  <Transition name="slide">
    <div
      v-if="isOpen"
      class="fixed bottom-6 right-6 z-40 w-full max-w-[480px] rounded-3xl bg-white shadow-2xl"
      :style="{ maxHeight: 'calc(100vh - 48px)' }"
    >
      <!-- Header (Stitch 스타일) -->
      <div class="flex items-center justify-between rounded-t-3xl bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-secondary)] px-5 py-4 text-white">
        <div class="flex items-center gap-3">
          <div class="h-10 w-10 flex-shrink-0 rounded-lg bg-white/20 p-2 text-center text-lg">LH</div>
          <div class="leading-tight">
            <div class="text-base font-semibold">LocalHub 챗봇</div>
            <div class="text-xs text-white/80">장소·커뮤니티 정보를 도와드려요</div>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button
            @click="handleReset"
            aria-label="새 대화 시작"
            class="rounded-lg bg-white/10 px-3 py-2 text-sm font-medium transition-all hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/30"
          >
            🔄
          </button>

          <button
            @click="isOpen = false"
            aria-label="챗봇 닫기"
            class="rounded-lg bg-white/10 px-3 py-2 text-sm font-medium transition-all hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/30"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- Body: messages + suggestions -->
      <div class="flex max-h-[640px] flex-col" :style="{ maxHeight: 'calc(100vh - 160px)' }">
        <div
          ref="messagesContainer"
          class="flex-1 overflow-y-auto px-5 py-4"
        >
          <div class="space-y-4">
            <ChatMessage
              v-for="msg in messages"
              :key="msg.id"
              :message="msg"
            />
          </div>

          <!-- 추천 질문 (초기 메시지 섹션) -->
          <div v-if="messages.length === 1" class="mt-4 px-2">
            <div class="mb-2 text-xs font-semibold text-[var(--color-text-muted)]">💡 이렇게 물어보세요</div>
            <ChatSuggestionList :suggestions="suggestions" @select="handleSendMessage" />
          </div>
        </div>

        <!-- Input area (Stitch: card-like) -->
        <div class="border-t border-[var(--color-border)] bg-[var(--color-surface-muted)] px-5 py-4 rounded-b-3xl">
          <label class="sr-only">메시지 입력</label>
          <div class="flex items-end gap-3">
            <textarea
              v-model="inputMessage"
              @keydown.enter.prevent="handleKeydown"
              @keydown.escape="isOpen = false"
              placeholder="궁금한 점을 입력해보세요. 예: 근처 맛집 추천해줘"
              rows="1"
              class="flex-1 max-h-36 resize-none rounded-xl border border-[var(--color-border)] bg-white px-4 py-3 text-sm text-[var(--color-text)] placeholder-[var(--color-text-muted)] focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
              :style="{ minHeight: '44px', overflow: 'auto' }"
            ></textarea>

            <div class="flex flex-col items-center gap-2">
              <button
                @click="handleSendMessage(inputMessage)"
                :disabled="isSending || !inputMessage.trim()"
                aria-label="메시지 전송"
                class="rounded-lg bg-[var(--color-primary)] px-4 py-2 text-sm font-medium text-white transition-all hover:bg-[var(--color-primary-hover)] disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
              >
                전송
              </button>

              <div v-if="isSending" class="text-xs text-[var(--color-text-muted)]">전송 중…</div>
            </div>
          </div>

          <div v-if="errorMessage" class="mt-3 text-xs text-red-600">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { sendChatMessage } from '@/api/chatApi'
import { chatSuggestions } from '@/data/mockChat'
import ChatMessage from '@/components/chat/ChatMessage.vue'
import ChatSuggestionList from '@/components/chat/ChatSuggestionList.vue'

const isOpen = ref(false)
const inputMessage = ref('')
const messages = ref([])
const isSending = ref(false)
const errorMessage = ref('')
const messagesContainer = ref(null)

const suggestions = computed(() => chatSuggestions)

const generateMessageId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

const initializeChat = () => {
  messages.value = [
    {
      id: generateMessageId(),
      role: 'assistant',
      content: '안녕하세요. LocalHub 지역 정보 챗봇입니다.\n궁금한 장소나 지역 정보를 물어보세요.',
      references: null,
      createdAt: new Date(),
      status: 'success'
    }
  ]
}

const handleReset = () => {
  messages.value = []
  inputMessage.value = ''
  errorMessage.value = ''
  initializeChat()
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const handleKeydown = (event) => {
  if (event.shiftKey) return
  handleSendMessage(inputMessage.value)
}

const handleSendMessage = async (message) => {
  const trimmedMessage = message.trim()
  if (!trimmedMessage || isSending.value) return

  errorMessage.value = ''
  isSending.value = true

  const userMessageId = generateMessageId()
  messages.value.push({
    id: userMessageId,
    role: 'user',
    content: trimmedMessage,
    references: null,
    createdAt: new Date(),
    status: 'success'
  })

  inputMessage.value = ''
  await scrollToBottom()

  const assistantMessageId = generateMessageId()
  messages.value.push({
    id: assistantMessageId,
    role: 'assistant',
    content: '',
    references: null,
    createdAt: new Date(),
    status: 'sending'
  })
  await scrollToBottom()

  try {
    const response = await sendChatMessage(trimmedMessage)

    const assistantMessage = messages.value.find(m => m.id === assistantMessageId)
    if (assistantMessage) {
      assistantMessage.content = response.answer
      assistantMessage.references = response.references || null
      assistantMessage.status = 'success'
    }
  } catch (error) {
    const assistantMessage = messages.value.find(m => m.id === assistantMessageId)
    if (assistantMessage) {
      assistantMessage.content = error.message || '답변을 가져올 수 없습니다. 다시 시도해주세요.'
      assistantMessage.status = 'error'
    }
    errorMessage.value = error.message || '오류가 발생했습니다.'
  } finally {
    isSending.value = false
    await scrollToBottom()
  }
}

onMounted(() => {
  initializeChat()
})
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.28s cubic-bezier(.22,.9,.19,1);
}
.slide-enter-from {
  transform: translateX(420px);
  opacity: 0;
}
.slide-leave-to {
  transform: translateX(420px);
  opacity: 0;
}
</style>