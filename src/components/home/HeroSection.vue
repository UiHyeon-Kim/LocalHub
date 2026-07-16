<template>
  <section class="relative overflow-hidden rounded-[24px] bg-gray-900 text-white">
    <img
      :src="heroBackgroundImage"
      alt="LocalHub 지역 이미지"
      class="absolute inset-0 h-full w-full object-cover"
    />
    <div class="absolute inset-0 bg-gradient-to-b from-black/30 via-black/10 to-black/80"></div>

    <div class="relative mx-auto flex min-h-[560px] max-w-7xl flex-col justify-center px-6 py-16 sm:px-10">
      <div class="max-w-2xl">
        <p class="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-[var(--color-secondary)]">
          지역 탐색 시작
        </p>
        <h1 class="text-5xl font-semibold leading-tight tracking-[-0.03em] sm:text-6xl">
          구미·경북의 특별한 여정을<br />
          LocalHub에서 발견하세요.
        </h1>
        <p class="mt-6 max-w-xl text-base leading-8 text-white/80">
          관광지, 문화시설, 음식점, 축제까지. 필요한 지역 정보를 쉽고 빠르게 찾을 수 있습니다.
        </p>

        <div class="mt-10 flex flex-col gap-4 sm:flex-row sm:items-center">
          <label class="sr-only" for="home-search">장소 검색</label>
          <div class="relative flex-1">
            <span class="pointer-events-none absolute inset-y-0 left-4 flex items-center text-white/70">
              🔍
            </span>
            <input
              id="home-search"
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              type="text"
              placeholder="장소 또는 주소 검색"
              class="h-14 w-full rounded-[14px] border border-white/20 bg-white/10 px-14 text-base text-white placeholder:text-white/60 outline-none transition focus:border-white/40 focus:ring-2 focus:ring-white/20"
            />
          </div>

          <button
            @click="handleSearch"
            type="button"
            class="inline-flex h-14 items-center justify-center rounded-[14px] bg-[var(--color-secondary)] px-8 text-sm font-semibold text-white transition hover:bg-[var(--color-primary)]"
          >
            검색
          </button>
        </div>

        <div class="mt-8 flex flex-wrap gap-3">
          <p class="text-sm text-white/70">추천 검색:</p>
          <button
            v-for="keyword in recommendedKeywords"
            :key="keyword"
            @click="handleKeyword(keyword)"
            type="button"
            class="rounded-full border border-white/20 bg-white/10 px-4 py-2 text-sm text-white transition hover:bg-white/20"
          >
            {{ keyword }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { heroBackgroundImage } from '@/data/homeMockData'

const router = useRouter()
const searchQuery = ref('')

const recommendedKeywords = ['금오산', '낙동강', '공원', '미술관']

const goToPlaces = (keyword) => {
  if (!keyword || !keyword.trim()) return
  router.push({
    path: '/places',
    query: { keyword: keyword.trim() }
  })
}

const handleSearch = () => {
  goToPlaces(searchQuery.value)
}

const handleKeyword = (keyword) => {
  searchQuery.value = keyword
  goToPlaces(keyword)
}
</script>