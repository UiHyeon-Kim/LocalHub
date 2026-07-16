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
      <PlaceDetailHero
        :place="place"
        :liked="liked"
        :like-loading="likeLoading"
        @toggle-like="toggleLike"
      />

      <main class="py-10 lg:py-14">
        <div class="page-container">
          <div class="grid grid-cols-12 gap-8">
            <!-- 왼쪽 콘텐츠 -->
            <div class="col-span-12 space-y-8 lg:col-span-8">
              <PlaceInfoGrid :place="place" />

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

            <!-- 오른쪽 위치 정보 -->
            <aside class="col-span-12 lg:col-span-4">
              <div
                class="space-y-4 lg:sticky lg:top-[calc(var(--header-height)+24px)]"
              >
                <PlaceLocationCard :place="place" />
              </div>
            </aside>
          </div>
        </div>
      </main>
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

        <p class="mt-3 text-sm text-[var(--color-text-muted)]">
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
            class="inline-block rounded-lg bg-[var(--color-primary)] px-6 py-3 font-semibold !text-white transition hover:bg-[var(--color-primary-hover)] hover:!text-white"
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

import {
  getNearbyPlaces,
  getPlace,
  likePlace,
  unlikePlace,
} from '@/api/placeApi'

import NearbyPlacesSection from '@/components/place/NearbyPlacesSection.vue'
import PlaceDescription from '@/components/place/PlaceDescription.vue'
import PlaceDetailHero from '@/components/place/PlaceDetailHero.vue'
import PlaceInfoGrid from '@/components/place/PlaceInfoGrid.vue'
import PlaceLocationCard from '@/components/place/PlaceLocationCard.vue'

const route = useRoute()

const place = ref(null)
const nearbyPlaces = ref([])

const loading = ref(false)
const likeLoading = ref(false)

const liked = ref(false)
const error = ref('')

const DEFAULT_NEARBY_REFERENCE = {
  lat: 36.1173,
  lon: 128.3440,
}

/**
 * 장소별 좋아요 상태를 브라우저에 저장할 때 사용하는 키
 */
const getLikeStorageKey = (placeId) => {
  return `localhub:place-like:${placeId}`
}

/**
 * 현재 브라우저에서 해당 장소를 좋아요 했는지 확인
 */
const readLikedState = (placeId) => {
  return (
    localStorage.getItem(
      getLikeStorageKey(placeId),
    ) === 'true'
  )
}

/**
 * 현재 브라우저의 좋아요 상태 저장
 */
const saveLikedState = (
  placeId,
  isLiked,
) => {
  const storageKey = getLikeStorageKey(placeId)

  if (isLiked) {
    localStorage.setItem(
      storageKey,
      'true',
    )
    return
  }

  localStorage.removeItem(storageKey)
}

/**
 * 좋아요 추가 또는 취소
 */
const toggleLike = async () => {
  if (
    !place.value ||
    likeLoading.value
  ) {
    return
  }

  const placeId = place.value.id
  const previousLiked = liked.value
  const previousLikeCount =
    place.value.likeCount ?? 0

  likeLoading.value = true

  /*
   * API 응답 전에 화면을 먼저 변경하는 낙관적 업데이트
   */
  liked.value = !previousLiked

  place.value.likeCount = Math.max(
    0,
    previousLikeCount +
      (liked.value ? 1 : -1),
  )

  try {
    const result = liked.value
      ? await likePlace(placeId)
      : await unlikePlace(placeId)

    liked.value = result.liked
    place.value.likeCount = result.likeCount

    saveLikedState(
      placeId,
      result.liked,
    )
  } catch (likeError) {
    console.error(
      '좋아요 처리 실패:',
      likeError,
    )

    /*
     * API 실패 시 기존 상태로 복구
     */
    liked.value = previousLiked
    place.value.likeCount =
      previousLikeCount
  } finally {
    likeLoading.value = false
  }
}

/**
 * 주변 장소 조회 기준 위치
 */
const getNearbyReference = async () => {
  if (!('geolocation' in navigator)) {
    return DEFAULT_NEARBY_REFERENCE
  }

  try {
    const position = await new Promise(
      (resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          resolve,
          reject,
          {
            enableHighAccuracy: false,
            timeout: 4000,
          },
        )
      },
    )

    return {
      lat: position.coords.latitude,
      lon: position.coords.longitude,
    }
  } catch {
    return DEFAULT_NEARBY_REFERENCE
  }
}

/**
 * 장소 상세 정보 조회
 */
const loadPlace = async () => {
  const placeId = route.params.id

  loading.value = true
  error.value = ''

  place.value = null
  nearbyPlaces.value = []
  liked.value = false

  try {
    place.value = await getPlace(placeId)

    liked.value = readLikedState(
      place.value.id,
    )

    try {
      const reference =
        await getNearbyReference()

      nearbyPlaces.value =
        await getNearbyPlaces(
          placeId,
          3,
          reference,
        )
    } catch (nearbyError) {
      console.error(
        '주변 장소 조회 실패:',
        nearbyError,
      )

      nearbyPlaces.value = []
    }
  } catch (loadError) {
    error.value =
      loadError instanceof Error
        ? loadError.message
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
  {
    immediate: true,
  },
)
</script>