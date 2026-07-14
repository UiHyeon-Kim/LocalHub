<template>
  <div v-if="place" class="min-h-screen bg-[var(--color-background)]">
    <!-- Hero -->
    <PlaceDetailHero :place="place" />

    <!-- 본문 -->
    <div class="page-container page-section">
      <div class="grid grid-cols-12 gap-8">
        <!-- 왼쪽 콘텐츠 (8/12) -->
        <div class="col-span-8 space-y-8">
          <!-- 정보 그리드 -->
          <PlaceInfoGrid :place="place" />

          <!-- 상세 설명 -->
          <PlaceDescription :place="place" />

          <!-- 주변 장소 -->
          <NearbyPlacesSection :nearby-places="nearbyPlaces" />
        </div>

        <!-- 우측 사이드 (4/12) -->
        <div class="col-span-4">
          <PlaceLocationCard :place="place" />
        </div>
      </div>
    </div>
  </div>

  <!-- Not Found -->
  <div v-else class="flex h-screen items-center justify-center bg-[var(--color-background)]">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-[var(--color-text)]">
        장소를 찾을 수 없습니다
      </h1>
      <p class="mt-4 text-[var(--color-text-muted)]">
        요청하신 장소 정보가 없습니다.
      </p>
      <RouterLink
        to="/"
        class="mt-8 inline-block rounded-lg bg-[var(--color-primary)] px-6 py-3 text-white font-semibold transition-all hover:bg-[var(--color-primary-hover)]"
      >
        홈으로 돌아가기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getPlaceById, getNearbyPlaces } from '@/data/mockPlaces'
import PlaceDetailHero from '@/components/place/PlaceDetailHero.vue'
import PlaceInfoGrid from '@/components/place/PlaceInfoGrid.vue'
import PlaceDescription from '@/components/place/PlaceDescription.vue'
import PlaceLocationCard from '@/components/place/PlaceLocationCard.vue'
import NearbyPlacesSection from '@/components/place/NearbyPlacesSection.vue'

const route = useRoute()

const placeId = computed(() => route.params.id)
const place = computed(() => getPlaceById(placeId.value))
const nearbyPlaces = computed(() => getNearbyPlaces(placeId.value, 3))
</script>