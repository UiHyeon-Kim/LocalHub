<template>
  <!-- 플로팅 버튼 -->
  <button
    v-if="!isOpen"
    type="button"
    aria-label="지역 정보 챗봇 열기"
    class="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-primary)] text-white shadow-xl transition-all hover:-translate-y-1 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
    @click="isOpen = true"
  >
    <span class="text-2xl">💬</span>
  </button>

  <!-- 챗봇 위젯 -->
  <Transition name="slide">
    <section
      v-if="isOpen"
      role="dialog"
      aria-label="LocalHub 지역 정보 챗봇"
      class="fixed bottom-6 right-6 z-50 flex w-[calc(100%-32px)] max-w-[480px] flex-col overflow-hidden rounded-3xl bg-white shadow-2xl"
      :style="{
        height: 'min(640px, calc(100vh - 48px))',
      }"
      @wheel.stop
      @touchmove.stop
    >
      <!-- Header -->
      <header
        class="flex flex-shrink-0 items-center justify-between bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-secondary)] px-5 py-4 text-white"
      >
        <div class="flex min-w-0 items-center gap-3">
          <div
            class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-white/20 text-lg"
          >
            LH
          </div>

          <div class="min-w-0 leading-tight">
            <div class="truncate text-base font-semibold">
              LocalHub 챗봇
            </div>

            <div class="truncate text-xs text-white/80">
              장소·커뮤니티 정보를 도와드려요
            </div>
          </div>
        </div>

        <div class="flex flex-shrink-0 items-center gap-2">
          <button
            type="button"
            aria-label="새 대화 시작"
            class="rounded-lg bg-white/10 px-3 py-2 text-sm font-medium transition-all hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/30"
            @click="handleReset"
          >
            🔄
          </button>

          <button
            type="button"
            aria-label="챗봇 닫기"
            class="rounded-lg bg-white/10 px-3 py-2 text-sm font-medium transition-all hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/30"
            @click="isOpen = false"
          >
            ✕
          </button>
        </div>
      </header>

      <!-- 메시지와 입력창 -->
      <div class="flex min-h-0 flex-1 flex-col">
        <!-- 메시지 영역 -->
        <div
          ref="messagesContainer"
          class="min-h-0 flex-1 overflow-y-auto overscroll-contain px-5 py-4"
          @wheel.stop
          @touchmove.stop
        >
          <div class="space-y-4">
            <ChatMessage
              v-for="message in messages"
              :key="message.id"
              :message="message"
            />
          </div>

          <!-- 추천 질문 -->
          <div
            v-if="messages.length === 1"
            class="mt-5 px-2 pb-2"
          >
            <div
              class="mb-3 text-xs font-semibold text-[var(--color-text-muted)]"
            >
              💡 이렇게 물어보세요
            </div>

            <ChatSuggestionList
              :suggestions="suggestions"
              @select="handleSendMessage"
            />
          </div>
        </div>

        <!-- 입력 영역 -->
        <footer
          class="flex-shrink-0 border-t border-[var(--color-border)] bg-[var(--color-surface-muted)] px-5 py-4"
        >
          <label
            for="chat-message-input"
            class="sr-only"
          >
            메시지 입력
          </label>

          <div class="flex items-end gap-3">
            <textarea
              id="chat-message-input"
              v-model="inputMessage"
              rows="1"
              placeholder="궁금한 점을 입력해보세요. 예: 근처 맛집 추천해줘"
              class="max-h-36 min-h-11 flex-1 resize-none overflow-y-auto rounded-xl border border-[var(--color-border)] bg-white px-4 py-3 text-sm text-[var(--color-text)] placeholder-[var(--color-text-muted)] focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
              @keydown.enter.prevent="handleKeydown"
              @keydown.escape="isOpen = false"
              @wheel.stop
            />

            <button
              type="button"
              aria-label="메시지 전송"
              :disabled="isSending || !inputMessage.trim()"
              class="h-11 rounded-lg bg-[var(--color-primary)] px-4 text-sm font-medium text-white transition-all hover:bg-[var(--color-primary-hover)] disabled:cursor-not-allowed disabled:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
              @click="handleSendMessage(inputMessage)"
            >
              전송
            </button>
          </div>

          <div
            v-if="isSending"
            class="mt-2 text-xs text-[var(--color-text-muted)]"
          >
            답변을 기다리는 중입니다.
          </div>

          <div
            v-if="errorMessage"
            class="mt-2 text-xs text-red-600"
          >
            {{ errorMessage }}
          </div>
        </footer>
      </div>
    </section>
  </Transition>
</template>

<script setup>
import {
  computed,
  nextTick,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from 'vue'

import { sendChatMessage } from '@/api/chatApi'
import ChatMessage from '@/components/chat/ChatMessage.vue'
import ChatSuggestionList from '@/components/chat/ChatSuggestionList.vue'
import { chatSuggestions } from '@/data/mockChat'

const isOpen = ref(false)
const inputMessage = ref('')
const messages = ref([])
const isSending = ref(false)
const errorMessage = ref('')
const messagesContainer = ref(null)

const suggestions = computed(() => chatSuggestions)

let savedScrollY = 0

const generateMessageId = () => {
  if (
    typeof crypto !== 'undefined' &&
    typeof crypto.randomUUID === 'function'
  ) {
    return crypto.randomUUID()
  }

  return `msg-${Date.now()}-${Math.random()
    .toString(36)
    .slice(2, 11)}`
}

const initializeChat = () => {
  messages.value = [
    {
      id: generateMessageId(),
      role: 'assistant',
      content:
        '안녕하세요. LocalHub 지역 정보 챗봇입니다.\n궁금한 장소나 지역 정보를 물어보세요.',
      references: null,
      createdAt: new Date(),
      status: 'success',
    },
  ]
}

const lockPageScroll = () => {
  savedScrollY = window.scrollY

  document.body.style.position = 'fixed'
  document.body.style.top = `-${savedScrollY}px`
  document.body.style.left = '0'
  document.body.style.right = '0'
  document.body.style.width = '100%'
  document.body.style.overflow = 'hidden'
}

const unlockPageScroll = () => {
  const scrollY = savedScrollY

  document.body.style.position = ''
  document.body.style.top = ''
  document.body.style.left = ''
  document.body.style.right = ''
  document.body.style.width = ''
  document.body.style.overflow = ''

  window.scrollTo(0, scrollY)
}

const handleReset = () => {
  inputMessage.value = ''
  errorMessage.value = ''
  initializeChat()
  scrollToBottom()
}

const scrollToBottom = async () => {
  await nextTick()

  if (!messagesContainer.value) {
    return
  }

  messagesContainer.value.scrollTop =
    messagesContainer.value.scrollHeight
}

const handleKeydown = (event) => {
  if (event.shiftKey) {
    inputMessage.value += '\n'
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

  messages.value.push({
    id: generateMessageId(),
    role: 'user',
    content: trimmedMessage,
    references: null,
    createdAt: new Date(),
    status: 'success',
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
    status: 'sending',
  })

  await scrollToBottom()

  try {
    const response = await sendChatMessage(trimmedMessage)

    const assistantMessage = messages.value.find(
      (messageItem) => messageItem.id === assistantMessageId,
    )

    if (assistantMessage) {
      assistantMessage.content = response.answer
      assistantMessage.references =
        response.references ?? null
      assistantMessage.status = 'success'
    }
  } catch (error) {
    const assistantMessage = messages.value.find(
      (messageItem) => messageItem.id === assistantMessageId,
    )

    const message =
      error instanceof Error
        ? error.message
        : '답변을 가져올 수 없습니다. 다시 시도해주세요.'

    if (assistantMessage) {
      assistantMessage.content = message
      assistantMessage.status = 'error'
    }

    errorMessage.value = message
  } finally {
    isSending.value = false
    await scrollToBottom()
  }
}

watch(isOpen, async (open) => {
  if (open) {
    lockPageScroll()
    await scrollToBottom()
    return
  }

  unlockPageScroll()
})

onMounted(() => {
  initializeChat()
})

onBeforeUnmount(() => {
  unlockPageScroll()
})
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition:
    transform 0.28s cubic-bezier(0.22, 0.9, 0.19, 1),
    opacity 0.28s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(420px);
  opacity: 0;
}
</style>