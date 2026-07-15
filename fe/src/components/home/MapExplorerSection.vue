```vue
<template>
  <section class="bg-[var(--color-background)] py-16">
    <div class="page-container">
      <div class="mb-6">
        <h2 class="text-3xl font-semibold text-[var(--color-text)]">
          지도로 둘러보는 지역
        </h2>

        <p class="mt-2 max-w-2xl text-sm text-[var(--color-text-muted)]">
          지도와 목록을 함께 확인하면서 관심 장소를 빠르게 찾아보세요.
        </p>
      </div>

      <div
        v-if="validPlaces.length > 0"
        class="grid items-stretch gap-6 xl:grid-cols-[2fr_1fr]"
      >
        <!-- 왼쪽: 지도 -->
        <div
          class="
            relative
            z-0
            isolate
            min-h-[420px]
            overflow-hidden
            rounded-[24px]
            border
            border-[var(--color-border)]
            bg-white
            p-4
            md:min-h-[520px]
          "
        >
          <PlaceMap
            class="relative z-0 h-full min-h-[388px] md:min-h-[488px]"
            :places="validPlaces"
            :selected-place-id="effectiveSelectedId"
            map-height="100%"
            @select-place="handleMapSelectPlace"
          />
        </div>

        <!-- 오른쪽: 최대 4개 표시 -->
        <div class="flex h-full flex-col gap-3">
          <div
            v-for="place in visiblePlaces"
            :key="place.id"
            class="
              cursor-pointer
              rounded-[20px]
              border
              border-[var(--color-border)]
              bg-white
              p-5
              transition
              hover:border-[var(--color-primary)]
              hover:shadow-sm
            "
            @mouseenter="hoveredPlaceId = place.id"
            @mouseleave="hoveredPlaceId = null"
            @click="selectedPlaceId = place.id"
          >
            <div class="flex gap-4">
              <div
                class="
                  h-24
                  w-24
                  flex-shrink-0
                  overflow-hidden
                  rounded-[18px]
                  bg-[var(--color-surface-muted)]
                "
              >
                <img
                  v-if="place.imageUrl"
                  :src="place.imageUrl"
                  :alt="place.name"
                  class="h-full w-full object-cover"
                />

                <div
                  v-else
                  class="
                    flex
                    h-full
                    items-center
                    justify-center
                    text-[var(--color-text-muted)]
                  "
                >
                  이미지 없음
                </div>
              </div>

              <div class="min-w-0 flex-1">
                <p
                  class="
                    text-xs
                    font-semibold
                    uppercase
                    tracking-[0.2em]
                    text-[var(--color-secondary)]
                  "
                >
                  {{ place.category }}
                </p>

                <h3
                  class="
                    mt-2
                    line-clamp-2
                    text-lg
                    font-semibold
                    text-[var(--color-text)]
                  "
                >
                  {{ place.name }}
                </h3>

                <p
                  class="
                    mt-2
                    line-clamp-2
                    text-sm
                    text-[var(--color-text-muted)]
                  "
                >
                  {{
                    place.shortDescription ||
                    place.address ||
                    '설명 없음'
                  }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        v-else
        class="
          rounded-[24px]
          border
          border-[var(--color-border)]
          bg-white
          p-12
          text-center
          text-[var(--color-text-muted)]
        "
      >
        표시할 장소가 없습니다.
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, watchEffect } from 'vue'
import PlaceMap from '@/components/place/PlaceMap.vue'

const props = defineProps({
  places: {
    type: Array,
    required: true,
  },
})

const selectedPlaceId = ref(null)
const hoveredPlaceId = ref(null)

const validPlaces = computed(() => {
  return props.places.filter((place) => {
    return (
      typeof place.latitude === 'number' &&
      typeof place.longitude === 'number' &&
      !Number.isNaN(place.latitude) &&
      !Number.isNaN(place.longitude)
    )
  })
})

const visiblePlaces = computed(() => {
  return validPlaces.value.slice(0, 4)
})

const effectiveSelectedId = computed(() => {
  return hoveredPlaceId.value ?? selectedPlaceId.value
})

const handleMapSelectPlace = (placeId) => {
  selectedPlaceId.value = placeId
}

watchEffect(() => {
  if (
    selectedPlaceId.value === null &&
    validPlaces.value.length > 0
  ) {
    selectedPlaceId.value = validPlaces.value[0].id
  }
})
</script>
```
