<template>
  <div class="min-h-screen bg-[var(--color-background)]">
    <!-- Loading -->
    <div
      v-if="loading"
      class="page-container flex min-h-[calc(100vh-var(--header-height))] items-center justify-center px-6"
    >
      <div class="text-center">
        <div
          class="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-[var(--color-border)] border-t-[var(--color-primary)]"
        />
        <p class="mt-4 text-sm text-[var(--color-text-muted)]">
          장소 정보를 불러오는 중입니다.
        </p>
      </div>
    </div>

    <!-- Place Detail -->
    <template v-else-if="place">
      <!-- Hero -->
      <PlaceDetailHero :place="place" />

      <!-- 본문 -->
      <div class="page-container page-section py-10 lg:py-14">
        <div class="grid grid-cols-12 gap-8">
          <!-- 왼쪽 콘텐츠 (8/12) -->
          <div class="col-span-12 space-y-8 lg:col-span-8">
            <!-- 정보 그리드 -->
            <section
              class="overflow-hidden rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm"
            >
              <PlaceInfoGrid :place="place" />
            </section>

            <!-- 상세 설명 -->
            <section
              class="overflow-hidden rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm"
            >
              <PlaceDescription :place="place" />
            </section>

            <!-- 주변 장소 -->
            <section v-if="nearbyPlaces.length > 0">
              <h3
                class="mb-4 text-xl font-bold text-[var(--color-text)]"
              >
                함께 둘러보기 좋은 장소
              </h3>

              <NearbyPlacesSection
                :nearby-places="nearbyPlaces"
              />
            </section>
          </div>

          <!-- 우측 사이드 (4/12) -->
          <aside class="col-span-12 lg:col-span-4">
            <div
              class="space-y-4 lg:sticky lg:top-[calc(var(--header-height)+24px)]"
            >
              <PlaceLocationCard :place="place" />
            </div>
          </aside>
        </div>
      </div>
    </template>

    <!-- Error / Not Found -->
    <div
      v-else
      class="flex min-h-[calc(100vh-var(--header-height))] items-center justify-center px-6"
    >
      <div
        class="w-full max-w-lg rounded-2xl border border-[var(--color-border)] bg-white px-8 py-14 text-center shadow-sm"
      >
        <div
          class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-[var(--color-surface-muted)] text-2xl"
        >
          📍
        </div>

        <h1
          class="mt-6 text-2xl font-semibold text-[var(--color-text)]"
        >
          {{
            error
              ? '장소 정보를 불러오지 못했습니다'
              : '장소를 찾을 수 없습니다'
          }}
        </h1>

        <p
          class="mt-3 text-sm text-[var(--color-text-muted)]"
        >
          {{
            error ||
            '요청하신 장소 정보가 없거나 삭제된 장소입니다.'
          }}
        </p>

        <div class="mt-8 flex justify-center gap-3">
          <button
            v-if="error"
            type="button"
            class="rounded-lg border border-[var(--color-primary)] px-6 py-3 font-semibold text-[var(--color-primary)] transition hover:bg-[var(--color-surface-muted)]"
            @click="loadPlace"
          >
            다시 시도
          </button>

          <RouterLink
            to="/places"
            class="inline-block rounded-lg bg-[var(--color-primary)] px-6 py-3 font-semibold text-white transition hover:bg-[var(--color-primary-hover)]"
          >
            장소 목록으로 돌아가기
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { getPlace, getNearbyPlaces } from '@/api/placeApi'
import PlaceDetailHero from '@/components/place/PlaceDetailHero.vue'
import PlaceInfoGrid from '@/components/place/PlaceInfoGrid.vue'
import PlaceDescription from '@/components/place/PlaceDescription.vue'
import PlaceLocationCard from '@/components/place/PlaceLocationCard.vue'
import NearbyPlacesSection from '@/components/place/NearbyPlacesSection.vue'

const route = useRoute()

const place = ref(null)
const nearbyPlaces = ref([])
const loading = ref(false)
const error = ref('')

const DEFAULT_NEARBY_REFERENCE = { lat: 36.1173, lon: 128.3440 }

const getNearbyReference = async () => {
  if ('geolocation' in navigator) {
    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: false,
          timeout: 4000,
        })
      })

      return {
        lat: position.coords.latitude,
        lon: position.coords.longitude,
      }
    } catch {
      return DEFAULT_NEARBY_REFERENCE
    }
  }

  return DEFAULT_NEARBY_REFERENCE
}

const loadPlace = async () => {
  const placeId = route.params.id

  loading.value = true
  error.value = ''
  place.value = null
  nearbyPlaces.value = []

  try {
    place.value = await getPlace(placeId)

    try {
      const reference = await getNearbyReference()
      nearbyPlaces.value = await getNearbyPlaces(placeId, 3, reference)
    } catch {
      nearbyPlaces.value = []
    }
  } catch (e) {
    error.value =
      e instanceof Error
        ? e.message
        : '장소 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

watch(
  () => route.params.id,
  () => {
    loadPlace()
  },
  { immediate: true },
)
</script>