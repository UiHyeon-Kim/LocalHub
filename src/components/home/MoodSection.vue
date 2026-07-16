<template>
  <section class="py-16">
    <div class="page-container">
      <!-- 제목 -->
      <h2 class="mb-12 text-3xl font-bold text-[var(--color-text)]">
        오늘은 어떤 시간을 보내고 싶나요?
      </h2>

      <!-- 그리드 -->
      <div class="grid grid-cols-2 gap-6">
        <button
          v-for="mood in moods"
          :key="mood.id"
          @click="handleMoodClick(mood)"
          :class="[
            'group relative h-96 overflow-hidden rounded-3xl transition-all duration-300',
            selectedMood === mood.id && 'ring-4 ring-[var(--color-primary)]'
          ]"
        >
          <!-- 배경 이미지 -->
          <img
            :src="mood.imageUrl"
            :alt="mood.title"
            class="absolute inset-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
          />

          <!-- 그라데이션 오버레이 -->
          <div class="absolute inset-0 bg-gradient-to-b from-black/20 via-black/30 to-black/60"></div>

          <!-- 텍스트 콘텐츠 -->
          <div class="absolute inset-0 flex flex-col justify-end p-8 text-white">
            <h3 class="text-2xl font-bold">
              {{ mood.title }}
            </h3>
            <p class="mt-2 text-sm text-white/90">
              {{ mood.description }}
            </p>
            <div class="mt-4 inline-flex items-center text-sm font-medium transition-transform group-hover:translate-x-2">
              탐색하기 →
            </div>
          </div>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { moods } from '@/data/homeMockData'

const router = useRouter()
const selectedMood = ref(null)

const handleMoodClick = (mood) => {
  selectedMood.value = mood.id

  const searchMap = {
    'mood-1': { keyword: '공원' },
    'mood-2': { category: '문화시설' },
    'mood-3': { category: '관광지' },
    'mood-4': { category: '레포츠' },
  }

  const config = searchMap[mood.id] || {}
  const query = {}

  if (config.keyword) {
    query.keyword = config.keyword
  }

  if (config.category) {
    query.category = config.category
  }

  router.push({
    path: '/places',
    query,
  })
}
</script>