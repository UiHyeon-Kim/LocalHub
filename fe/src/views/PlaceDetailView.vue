<template>
  <div v-if="place" class="min-h-screen bg-[var(--color-background)]">
    <!-- Hero -->
    <PlaceDetailHero :place="place" />

    <!-- 본문 -->
    <div class="page-container page-section py-10 lg:py-14">
      <div class="grid grid-cols-12 gap-8">
        <!-- 왼쪽 콘텐츠 (8/12) -->
        <div class="col-span-12 lg:col-span-8 space-y-8">
          <!-- 정보 그리드 (card) -->
          <section class="overflow-hidden rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm">
            <PlaceInfoGrid :place="place" />
          </section>

          <!-- 상세 설명 -->
          <section class="overflow-hidden rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm">
            <PlaceDescription :place="place" />
          </section>

          <!-- 주변 장소 -->
          <section>
            <h3 class="text-xl font-bold text-[var(--color-text)] mb-4">함께 둘러보기 좋은 장소</h3>
            <NearbyPlacesSection :nearby-places="nearbyPlaces" />
          </section>
        </div>

        <!-- 우측 사이드 (4/12) -->
        <aside class="col-span-12 lg:col-span-4">
          <div class="lg:sticky lg:top-[calc(var(--header-height)+24px)] space-y-4">
            <PlaceLocationCard :place="place" />
          </div>
        </aside>
      </div>
    </div>
  </div>

  <!-- Not Found -->
  <div v-else class="flex h-screen items-center justify-center bg-[var(--color-background)] px-6">
    <div class="w-full max-w-lg rounded-2xl border border-[var(--color-border)] bg-white px-8 py-14 text-center shadow-sm">
      <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-surface-muted)] text-2xl">📍</div>
      <h1 class="mt-6 text-2xl font-semibold text-[var(--color-text)]">장소를 찾을 수 없습니다</h1>
      <p class="mt-3 text-sm text-[var(--color-text-muted)]">요청하신 장소 정보가 없거나 삭제된 장소입니다.</p>
      <div class="mt-8">
        <RouterLink to="/places" class="inline-block rounded-lg bg-[var(--color-primary)] px-6 py-3 text-white font-semibold hover:bg-[var(--color-primary-hover)]">
          장소 목록으로 돌아가기
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import PlaceDetailHero from '@/components/place/PlaceDetailHero.vue'
import PlaceInfoGrid from '@/components/place/PlaceInfoGrid.vue'
import PlaceDescription from '@/components/place/PlaceDescription.vue'
import PlaceLocationCard from '@/components/place/PlaceLocationCard.vue'
import NearbyPlacesSection from '@/components/place/NearbyPlacesSection.vue'

import { getPlaceById, getNearbyPlaces } from '@/data/mockPlaces'

const route = useRoute()
const placeId = computed(() => route.params.id)

const place = computed(() => getPlaceById(placeId.value))
const nearbyPlaces = computed(() => getNearbyPlaces(placeId.value, 3))
</script>