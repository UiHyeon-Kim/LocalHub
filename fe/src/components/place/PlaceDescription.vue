<template>
  <div class="space-y-8">
    <!-- 장소 소개 -->
    <div>
      <h2 class="text-2xl font-bold text-[var(--color-text)]">장소 소개</h2>
      <p class="mt-6 whitespace-pre-wrap text-lg leading-relaxed text-[var(--color-text-muted)]">
        {{ place.description }}
      </p>
    </div>

    <!-- 주요 특징 -->
    <div v-if="place.highlights && place.highlights.length > 0">
      <h3 class="text-xl font-bold text-[var(--color-text)]">주요 특징</h3>
      <ul class="mt-4 space-y-3">
        <li v-for="(highlight, index) in place.highlights" :key="index" class="flex items-start gap-3">
          <span class="mt-1 h-2 w-2 flex-shrink-0 rounded-full bg-[var(--color-primary)]"></span>
          <span class="text-base text-[var(--color-text)]">{{ highlight }}</span>
        </li>
      </ul>
    </div>

    <!-- 추천 상황 -->
    <div v-if="place.recommendedFor && place.recommendedFor.length > 0">
      <h3 class="text-xl font-bold text-[var(--color-text)]">추천할 상황</h3>
      <div class="mt-4 flex flex-wrap gap-2">
        <span
          v-for="(item, index) in place.recommendedFor"
          :key="index"
          class="rounded-full bg-blue-50 px-4 py-2 text-sm text-blue-700 font-medium"
        >
          {{ item }}
        </span>
      </div>
    </div>

    <!-- 태그 -->
    <div v-if="place.tags && place.tags.length > 0">
      <h3 class="text-xl font-bold text-[var(--color-text)]">태그</h3>
      <div class="mt-4 flex flex-wrap gap-2">
        <span
          v-for="(tag, index) in place.tags"
          :key="index"
          class="rounded-full bg-gray-100 px-3 py-1 text-sm text-[var(--color-text)] font-medium"
        >
          #{{ tag }}
        </span>
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