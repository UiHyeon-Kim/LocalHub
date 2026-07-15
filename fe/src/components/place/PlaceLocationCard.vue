<template>
  <div class="sticky top-[calc(var(--header-height)+24px)] space-y-6">
    <div class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm">
      <h3 class="text-lg font-semibold text-[var(--color-text)]">위치</h3>

      <p class="mt-2 text-sm text-[var(--color-text-muted)] line-clamp-3">
        {{ place.address || '주소 정보 없음' }}
      </p>

      <div class="mt-4">
        <PlaceMap
          :places="[place]"
          :selected-place-id="place.id"
          :center="[place.latitude, place.longitude]"
          :zoom="15"
          map-height="280px"
        />
      </div>

      <div class="mt-4 flex gap-2">
        <a
          v-if="place.latitude && place.longitude"
          :href="`https://www.openstreetmap.org/?mlat=${place.latitude}&mlon=${place.longitude}&zoom=15`"
          target="_blank"
          rel="noopener noreferrer"
          class="flex-1 rounded-lg bg-[var(--color-primary)] px-4 py-3 text-center text-white font-semibold hover:bg-[var(--color-primary-hover)]"
        >
          길찾기
        </a>

        <button class="rounded-lg border px-4 py-3 text-sm text-[var(--color-text)] bg-white">공유 위치</button>
      </div>
    </div>

    <RouterLink to="/" class="block rounded-lg border border-[var(--color-border)] bg-white px-4 py-3 text-center text-[var(--color-text)] font-semibold shadow-sm">
      목록으로 돌아가기
    </RouterLink>
  </div>
</template>

<script setup>
import PlaceMap from '@/components/place/PlaceMap.vue'
defineProps({
  place: { type: Object, required: true }
})
</script>