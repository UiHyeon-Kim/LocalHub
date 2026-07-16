<template>
  <div
    :class="[
      'flex gap-3',
      message.role === 'user' ? 'justify-end' : 'justify-start'
    ]"
  >
    <!-- 챗봇 아이콘 (assistant만) -->
    <div v-if="message.role === 'assistant'" class="mt-1 flex-shrink-0">
      <div class="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--color-primary)] text-white text-sm font-bold">
        💬
      </div>
    </div>

    <!-- 메시지 콘텐츠 -->
    <div
      :class="[
        'max-w-xs rounded-2xl px-4 py-3 whitespace-pre-wrap text-sm leading-relaxed',
        message.role === 'user'
          ? 'bg-[var(--color-primary)] text-white'
          : 'bg-gray-100 text-[var(--color-text)]'
      ]"
    >
      <!-- 전송 중 상태 -->
      <div v-if="message.status === 'sending'" class="text-gray-500">
        답변을 기다리는 중...
      </div>

      <!-- 오류 상태 -->
      <div v-else-if="message.status === 'error'" class="text-red-600">
        {{ message.content }}
      </div>

      <!-- 일반 메시지 -->
      <div v-else>
        {{ message.content }}
      </div>

      <!-- References -->
      <div v-if="message.references && message.references.length > 0" class="mt-3 space-y-2 border-t border-opacity-30 border-current pt-3">
        <div v-for="ref in message.references" :key="`${ref.id}-${ref.type}`" class="text-xs">
          <RouterLink
            :to="ref.path"
            class="inline-flex items-center gap-1 rounded-full bg-white/30 px-2 py-1 transition-colors hover:bg-white/50"
            :class="message.role === 'user' ? 'text-white hover:text-white' : 'text-[var(--color-primary)]'"
          >
            <span v-if="ref.type === 'place'" class="font-semibold">📍 장소</span>
            <span v-else class="font-semibold">📝 게시글</span>
            <span>{{ ref.title }}</span>
          </RouterLink>
        </div>
      </div>

      <!-- 시간 표시 -->
      <div
        v-if="message.createdAt"
        :class="[
          'mt-2 text-xs opacity-70',
          message.role === 'user' ? 'text-white' : 'text-gray-600'
        ]"
      >
        {{ formatTime(message.createdAt) }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: Object,
    required: true
  }
})

const formatTime = (date) => {
  if (!(date instanceof Date)) {
    date = new Date(date)
  }
  return date.toLocaleTimeString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>