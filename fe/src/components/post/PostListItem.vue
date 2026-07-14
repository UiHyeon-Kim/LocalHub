<template>
  <RouterLink :to="`/posts/${post.id}`" class="block border-b border-[var(--color-border)] last:border-b-0">
    <div class="flex items-center gap-4 py-4 px-0 transition-colors hover:bg-gray-50">
      <!-- 카테고리 -->
      <div class="flex-shrink-0 w-16">
        <span class="inline-block rounded-md bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700">
          {{ post.category }}
        </span>
      </div>

      <!-- 제목 -->
      <div class="flex-1 min-w-0">
        <h3 class="font-semibold text-[var(--color-text)] line-clamp-1 text-base">
          {{ post.title }}
        </h3>
        <div v-if="post.locationName" class="mt-1 text-sm text-[var(--color-text-muted)]">
          📍 {{ post.locationName }}
        </div>
      </div>

      <!-- 메타 정보 -->
      <div class="flex-shrink-0 text-right text-sm text-[var(--color-text-muted)] space-y-1">
        <div>{{ formatDate(post.createdAt) }}</div>
        <div>조회 {{ post.viewCount }}</div>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
defineProps({
  post: {
    type: Object,
    required: true
  }
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return date.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
  }

  if (date.toDateString() === yesterday.toDateString()) {
    return '어제'
  }

  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })
}
</script>