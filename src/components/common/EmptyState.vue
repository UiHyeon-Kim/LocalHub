<template>
  <div class="flex flex-col items-center justify-center py-20 text-center">
    <!-- 아이콘 -->
    <div class="mb-6 text-6xl">📭</div>

    <!-- 제목 -->
    <h3 class="text-2xl font-bold text-[var(--color-text)]">
      {{ title }}
    </h3>

    <!-- 설명 -->
    <p class="mt-2 text-[var(--color-text-muted)]">
      {{ description }}
    </p>

    <!-- 버튼 -->
    <button
      v-if="actionText"
      @click="$emit('action')"
      class="mt-8 rounded-lg bg-[var(--color-primary)] px-6 py-3 font-semibold text-white transition-all hover:bg-[var(--color-primary-hover)]"
    >
      {{ actionText }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  actionText: {
    type: String,
    default: null
  }
})

defineEmits(['action'])
</script>