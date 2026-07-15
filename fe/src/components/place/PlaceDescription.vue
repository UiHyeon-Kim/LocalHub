<template>
  <div class="space-y-8">
    <div>
      <h2 class="text-2xl font-bold text-[var(--color-text)]">장소 소개</h2>
      <p class="mt-6 whitespace-pre-wrap text-lg leading-relaxed text-[var(--color-text-muted)]">
        {{ descriptionText }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  place: {
    type: Object,
    required: true,
  },
})

const descriptionText = computed(() => {
  if (props.place?.description) {
    return props.place.description
  }

  const name = props.place?.name || props.place?.title || '이 장소'
  const category = props.place?.category || '명소'
  const address = props.place?.address || '구미·경북 지역'

  return `${name}는 ${category}로, ${address}에 위치한 곳입니다. 지역의 분위기와 함께 둘러보기 좋은 추천 장소입니다.`
})
</script>