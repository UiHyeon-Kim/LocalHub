<template>
  <div class="relative w-full overflow-hidden bg-[var(--color-surface-muted)]" :style="{ aspectRatio: aspectRatio }">
    <img
      v-if="imageUrl && !imageError"
      :src="imageUrl"
      :alt="`${name} 대표 이미지`"
      class="h-full w-full object-cover"
      @error="imageError = true"
    />

    <div
      v-if="!imageUrl || imageError"
      class="flex h-full w-full flex-col items-center justify-center gap-3 bg-[var(--color-surface-muted)] text-[var(--color-text-muted)]"
    >
      <div class="flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-primary)] text-2xl font-semibold text-white">
        {{ displayInitial }}
      </div>
      <p class="text-sm text-[var(--color-text-muted)]">
        {{ category || '장소' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  imageUrl: {
    type: [String, null],
    default: null
  },
  name: {
    type: String,
    required: true
  },
  category: {
    type: String,
    default: '장소'
  },
  aspectRatio: {
    type: String,
    default: '4 / 3'
  }
})

const imageError = ref(false)

watch(() => props.imageUrl, () => {
  imageError.value = false
})

const displayInitial = computed(() => {
  return props.name ? props.name.charAt(0).toUpperCase() : 'L'
})
</script>