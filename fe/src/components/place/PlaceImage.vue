<template>
  <div
    class="relative w-full overflow-hidden bg-gray-200"
    :style="{ aspectRatio: aspectRatio }"
  >
    <!-- 이미지 표시 -->
    <img
      v-if="imageUrl && !imageError"
      :src="imageUrl"
      :alt="`${name} 대표 이미지`"
      class="h-full w-full object-cover"
      @error="imageError = true"
    />

    <!-- Fallback UI -->
    <div
      v-if="!imageUrl || imageError"
      class="flex h-full w-full flex-col items-center justify-center bg-gradient-to-br from-green-100 to-teal-50"
    >
      <div class="mb-2 flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-primary)]">
        <span class="text-2xl font-bold text-white">
          {{ name.charAt(0) }}
        </span>
      </div>
      <p class="text-sm text-[var(--color-text)]">
        {{ category }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

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
    default: '16 / 9'
  }
})

const imageError = ref(false)

watch(() => props.imageUrl, () => {
  imageError.value = false
})
</script>