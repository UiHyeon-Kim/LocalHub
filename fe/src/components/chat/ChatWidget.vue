<template>
  <!-- 플로팅 버튼 (접힌 상태) -->
  <button
    v-if="!isOpen"
    @click="isOpen = true"
    aria-label="지역 정보 챗봇 열기"
    class="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-primary)] text-white shadow-lg transition-all hover:-translate-y-1 hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
  >
    <span class="text-2xl">💬</span>
  </button>

  <!-- 챗봇 위젯 (펼친 상태) -->
  <Transition name="slide">
    <div
      v-if="isOpen"
      class="fixed bottom-6 right-6 z-40 flex w-full max-w-[420px] flex-col rounded-3xl bg-white shadow-2xl md:h-auto md:max-h-[640px]"
      :style="{ maxHeight: 'calc(100vh - 48px)' }"
    >
      <!-- 헤더 -->
      <div class="border-b border-[var(--color-border)] bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-secondary)] px-6 py-4 text-white rounded-t-3xl">
        <div class="flex items-start justify-between">
          <div>
            <h2 class="text-lg font-bold">LocalHub 지역 정보 챗봇</h2>
            <p class="text-sm text-white/80">지역 장소와 커뮤니티 정보를 물어보세요.</p>
          </div>
          <div class="flex gap-2">
            <button
              @click="handleReset"
              aria-label="새 대화 시작"
              class="rounded-lg bg-white/20 px-3 py-2 text-sm font-medium transition-all hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-white/50"
            >
              🔄
            </button>
            <button
              @click="isOpen = false"
              aria-label="챗봇 닫기"
              class="rounded-lg bg-white/20 px-3 py-2 font-medium transition-all hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-white/50"
            >
              ✕
            </button>
          </div>
        </div>
      </div>

      <!-- 메시지 영역 -->
      <div
        ref="messagesContainer"
        class="flex-1 overflow-y-auto space-y-4 px-6 py-4"
      >
        <ChatMessage
          v-for="msg in messages"
          :key="msg.id"
          :message="msg"
        />

        <!-- 추천 질문 (메시지가 1개일 때만 표시) -->
        <div v-if="messages.length === 1" class="space-y-3">
          <div class="text-xs text-[var(--color-text-muted)] font-semibold">
            💡 다음과 같이 물어볼 수 있어요:
          </div>
          <ChatSuggestionList
            :suggestions="suggestions"
            @select="handleSendMessage"
          />
        </div>
      </div>

      <!-- 입력 영역 -->
      <div class="border-t border-[var(--color-border)] bg-gray-50 px-6 py-4 rounded-b-3xl">
        <label class="sr-only">메시지 입력</label>
        <div class="flex gap-2">
          <textarea
            v-model="inputMessage"
            @keydown.enter.prevent="handleKeydown"
            @keydown.escape="isOpen = false"
            placeholder="질문을 입력하세요..."
            rows="1"
            class="flex-1 rounded-lg border border-[var(--color-border)] px-3 py-2 text-sm text-[var(--color-text)] placeholder-[var(--color-text-muted)] resize-none transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
            :style="{ minHeight: '40px', maxHeight: '80px', overflow: 'auto' }"
          ></textarea>
          <button
            @click="handleSendMessage(inputMessage)"
            :disabled="isSending || !inputMessage.trim()"
            aria-label="메시지 전송"
            class="flex-shrink-0 rounded-lg bg-[var(--color-primary)] px-4 py-2 font-medium text-white transition-all hover:bg-[var(--color-primary-hover)] disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
          >
            ↓
          </button>
        </div>
        <div v-if="errorMessage" class="mt-2 text-xs text-red-600">
          {{ errorMessage }}
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
  if (event.shiftKey) {
    return
  }
  handleSendMessage(inputMessage.value)
}

const handleSendMessage = async (message) => {
  const trimmedMessage = message.trim()

  if (!trimmedMessage || isSending.value) {
    return
  }

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
  transition: all 0.3s ease;
}

.slide-enter-from {
  transform: translateX(400px);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(400px);
  opacity: 0;
}
</style>