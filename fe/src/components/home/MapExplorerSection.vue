<template>
  <section class="bg-gray-50 py-16">
    <div class="page-container">
      <!-- 제목 -->
      <h2 class="text-3xl font-bold text-[var(--color-text)]">
        지도로 둘러보는 지역
      </h2>
      <p class="mt-3 text-[var(--color-text-muted)]">
        장소 목록과 지도를 함께 살펴보며 원하는 지역 정보를 발견해보세요.
      </p>

      <!-- 콘텐츠 -->
      <div v-if="validPlaces.length > 0" class="mt-8 rounded-3xl border border-[var(--color-border)] bg-white p-6 shadow-md overflow-hidden">
        <div class="grid grid-cols-12 gap-6 h-[600px]">
          <!-- 지도 (8/12) -->
          <div class="col-span-8">
            <PlaceMap
              :places="validPlaces"
              :selected-place-id="effectiveSelectedId"
              @select-place="handleMapSelectPlace"
            />
          </div>

          <!-- 장소 목록 (4/12) -->
          <div class="col-span-4 overflow-y-auto space-y-2">
            <div
              v-for="(place, index) in validPlaces"
              :key="place.id"
              ref="placeItemRefs"
              @mouseenter="hoveredPlaceId = place.id"
              @mouseleave="hoveredPlaceId = null"
              @click="selectedPlaceId = place.id"
              :class="[
                'rounded-xl border-2 p-3 cursor-pointer transition-all',
                selectedPlaceId === place.id
                  ? 'border-[var(--color-primary)] bg-green-50'
                  : hoveredPlaceId === place.id
                    ? 'border-[var(--color-secondary)] bg-teal-50'
                    : 'border-[var(--color-border)] hover:border-[var(--color-secondary)]'
              ]"
            >
              <!-- 이미지 -->
              <div v-if="place.imageUrl" class="mb-2 rounded-lg overflow-hidden h-24 bg-gray-200">
                <img
                  :src="place.imageUrl"
                  :alt="place.name"
                  class="w-full h-full object-cover"
                />
              </div>
              <div v-else class="mb-2 rounded-lg overflow-hidden h-24 bg-gradient-to-br from-green-100 to-teal-50 flex items-center justify-center">
                <span class="text-2xl">📍</span>
              </div>

              <!-- 정보 -->
              <div>
                <p class="text-xs font-semibold text-[var(--color-secondary)] mb-1">
                  {{ place.category }}
                </p>
                <h3 class="font-bold text-[var(--color-text)] line-clamp-2">
                  {{ place.name }}
                </h3>
                <p class="text-xs text-[var(--color-text-muted)] mt-1 line-clamp-2">
                  {{ place.shortDescription }}
                </p>
              </div>

              <!-- 상세보기 링크 -->
              <RouterLink
                :to="`/places/${place.id}`"
                class="mt-2 inline-flex items-center gap-1 text-xs font-medium text-[var(--color-primary)] hover:gap-2 transition-all"
              >
                상세보기 →
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- 빈 상태 -->
      <div v-else class="mt-8 rounded-3xl border border-[var(--color-border)] bg-white p-12 text-center">
        <div class="text-4xl mb-4">📍</div>
        <p class="text-[var(--color-text-muted)]">
          표시할 장소가 없습니다.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import PlaceMap from '@/components/place/PlaceMap.vue'

const props = defineProps({
  places: {
    type: Array,
    required: true
  }
})

const selectedPlaceId = ref(null)
const hoveredPlaceId = ref(null)
const placeItemRefs = ref([])

const validPlaces = computed(() => {
  return props.places.filter((place) => {
    return (
      typeof place.latitude === 'number' &&
      typeof place.longitude === 'number' &&
      !isNaN(place.latitude) &&
      !isNaN(place.longitude)
    )
  })
})

const effectiveSelectedId = computed(() => {
  return hoveredPlaceId.value || selectedPlaceId.value
})

const handleMapSelectPlace = (placeId) => {
  selectedPlaceId.value = placeId
}

// 초기 선택
if (validPlaces.value.length > 0 && !selectedPlaceId.value) {
  selectedPlaceId.value = validPlaces.value[0].id
}
</script>