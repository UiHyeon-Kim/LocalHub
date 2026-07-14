<template>
  <div
    class="relative h-[680px] w-full overflow-hidden bg-gray-900"
    :style="{ backgroundImage: `url('${heroBackgroundImage}')`, backgroundSize: 'cover', backgroundPosition: 'center' }"
  >
    <!-- 오버레이 -->
    <div class="absolute inset-0 bg-gradient-to-b from-black/40 via-black/30 to-black/60"></div>

    <!-- 콘텐츠 -->
    <div class="relative flex h-full flex-col items-center justify-center px-6">
      <div class="max-w-2xl text-center">
        <!-- 제목 -->
        <h1 class="text-5xl font-bold leading-tight text-white md:text-6xl">
          오늘, 우리 지역에서<br />어디 가볼까요?
        </h1>

        <!-- 보조 문구 -->
        <p class="mt-6 text-lg text-white/80">
          익숙한 장소부터 아직 발견하지 못한 공간까지,<br />지역의 새로운 매력을 만나보세요.
        </p>

        <!-- 검색창 -->
        <div class="mt-10 flex gap-2">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="장소, 카테고리, 분위기 검색..."
            class="flex-1 rounded-full border-0 bg-white/95 px-6 py-4 text-gray-900 placeholder-gray-500 shadow-2xl focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]"
            @keyup.enter="handleSearch"
          />
          <button
            @click="handleSearch"
            class="rounded-full bg-[var(--color-primary)] px-8 py-4 font-semibold text-white transition-all hover:bg-[var(--color-primary-hover)] hover:shadow-xl"
          >
            검색
          </button>
        </div>

        <!-- 추천 검색어 -->
        <div class="mt-8 flex flex-wrap justify-center gap-3">
          <span class="text-sm text-white/70">추천:</span>
          <button
            v-for="keyword in recommendedKeywords"
            :key="keyword"
            @click="searchQuery = keyword"
            class="rounded-full bg-white/20 px-4 py-2 text-sm text-white transition-colors hover:bg-white/30"
          >
            {{ keyword }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { heroBackgroundImage } from '@/data/homeMockData'

const searchQuery = ref('')
const recommendedKeywords = ['금오산', '산책하기 좋은 곳', '가족 나들이', '실내 문화시설']

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    console.log('검색:', searchQuery.value)
    // 추후 라우팅이나 필터링 구현
  }
}
</script>