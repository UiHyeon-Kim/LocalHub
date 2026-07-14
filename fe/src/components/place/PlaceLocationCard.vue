<template>
  <div class="sticky space-y-6" :style="{ top: `calc(var(--header-height) + 24px)` }">
    <!-- 위치 정보 카드 -->
    <div class="rounded-3xl border border-[var(--color-border)] bg-white p-8 shadow-md">
      <h2 class="text-2xl font-bold text-[var(--color-text)]">
        위치 안내
      </h2>

      <!-- 지도 또는 대체 UI -->
      <div v-if="place.latitude && place.longitude" class="mt-6">
        <PlaceMap
          :places="[place]"
          :selected-place-id="place.id"
          :center="[place.latitude, place.longitude]"
          :zoom="15"
          map-height="300px"
        />
      </div>

      <div v-else class="mt-6 rounded-2xl bg-gray-100 h-80 flex items-center justify-center">
        <div class="text-center">
          <div class="text-4xl mb-2">📍</div>
          <p class="text-[var(--color-text-muted)]">
            위치 정보가 제공되지 않는 장소입니다.
          </p>
        </div>
      </div>

      <!-- 주소 -->
      <div v-if="place.address" class="mt-6">
        <p class="text-sm text-[var(--color-text-muted)] font-semibold">주소</p>
        <p class="mt-2 text-base text-[var(--color-text)] font-medium">
          {{ place.address }}
        </p>
      </div>

      <!-- 지도에서 크게 보기 버튼 -->
      <a
        v-if="place.latitude && place.longitude"
        :href="`https://www.openstreetmap.org/?mlat=${place.latitude}&mlon=${place.longitude}&zoom=15`"
        target="_blank"
        rel="noopener noreferrer"
        class="mt-6 block w-full rounded-xl bg-[var(--color-primary)] px-4 py-3 text-center text-[var(--color-primary)] font-semibold text-white transition-all hover:bg-[var(--color-primary-hover)]"
      >
        지도에서 크게 보기
      </a>
      <button
        v-else
        disabled
        class="mt-6 w-full rounded-xl bg-gray-200 px-4 py-3 text-gray-500 font-semibold cursor-not-allowed"
      >
        위치 정보 없음
      </button>
    </div>

    <!-- 목록으로 돌아가기 -->
    <RouterLink
      to="/"
      class="block w-full rounded-xl border-2 border-[var(--color-primary)] bg-white px-4 py-3 text-center text-[var(--color-primary)] font-semibold transition-all hover:bg-[var(--color-primary)] hover:text-white"
    >
      목록으로 돌아가기
    </RouterLink>
  </div>
</template>

<script setup>
import PlaceMap from '@/components/place/PlaceMap.vue'

defineProps({
  place: {
    type: Object,
    required: true
  }
})
</script>