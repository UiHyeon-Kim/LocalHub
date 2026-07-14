<template>
  <div
    class="relative h-[600px] w-full overflow-hidden bg-gray-900"
    :style="place.imageUrl ? { backgroundImage: `url('${place.imageUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}"
  >
    <!-- 오버레이 -->
    <div class="absolute inset-0 bg-gradient-to-b from-black/40 via-black/20 to-black/70"></div>

    <!-- 콘텐츠 -->
    <div class="relative flex h-full flex-col items-start justify-end px-8 pb-12">
      <div class="max-w-3xl">
        <!-- 카테고리 배지 -->
        <div class="mb-4">
          <span class="inline-block rounded-full bg-[var(--color-primary)] px-4 py-2 text-sm font-semibold text-white">
            {{ place.category }}
          </span>
        </div>

        <!-- 제목 -->
        <h1 class="text-5xl font-bold leading-tight text-white">
          {{ place.name }}
        </h1>

        <!-- 한 줄 설명 -->
        <p class="mt-4 text-xl text-white/90">
          {{ place.shortDescription }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  place: {
    type: Object,
    required: true
  }
})
</script>