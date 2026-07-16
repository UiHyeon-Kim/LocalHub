<template>
  <section
    class="relative h-80 w-full overflow-hidden bg-gray-900"
    :style="{ backgroundImage: `url('${regionBannerImage}')`, backgroundSize: 'cover', backgroundPosition: 'center' }"
  >
    <!-- 오버레이 -->
    <div class="absolute inset-0 bg-gradient-to-r from-black/70 to-black/40"></div>

    <!-- 콘텐츠 -->
    <div class="relative flex h-full items-center">
      <div class="page-container max-w-2xl">
        <h2 class="text-4xl font-bold text-white">
          사람과 장소, 이야기가 연결되는 지역
        </h2>
        <p class="mt-6 text-lg text-white/80">
          LocalHub에서 지역의 새로운 정보를 발견하고<br />직접 이야기를 나눠보세요.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { regionBannerImage } from '@/data/homeMockData'
</script>