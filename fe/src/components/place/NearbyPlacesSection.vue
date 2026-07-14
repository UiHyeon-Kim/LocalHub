<template>
  <section v-if="nearbyPlaces.length > 0" class="mt-20">
    <h2 class="text-3xl font-bold text-[var(--color-text)] mb-10">
      이 장소와 가까운 곳
    </h2>

    <div class="grid grid-cols-3 gap-6">
      <RouterLink
        v-for="place in nearbyPlaces"
        :key="place.id"
        :to="`/places/${place.id}`"
        class="group overflow-hidden rounded-3xl bg-white shadow-md transition-all duration-300 hover:-translate-y-2 hover:shadow-xl"
      >
        <!-- 이미지 -->
        <div class="relative h-56 overflow-hidden bg-gray-200">
          <img
            v-if="place.imageUrl"
            :src="place.imageUrl"
            :alt="place.name"
            class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-110"
          />
          <div v-else class="h-full w-full flex items-center justify-center bg-gradient-to-br from-green-100 to-teal-50">
            <span class="text-4xl">📍</span>
          </div>

          <!-- 카테고리 배지 -->
          <div class="absolute left-4 top-4">
            <span class="inline-block rounded-full bg-[var(--color-primary)] px-3 py-1 text-sm font-semibold text-white">
              {{ place.category }}
            </span>
          </div>
        </div>

        <!-- 콘텐츠 -->
        <div class="p-6">
          <h3 class="font-bold text-[var(--color-text)] line-clamp-2 text-lg">
            {{ place.name }}
          </h3>

          <p class="mt-2 line-clamp-2 text-sm text-[var(--color-text-muted)]">
            {{ place.shortDescription }}
          </p>

          <!-- 거리 정보 -->
          <div class="mt-4 flex items-center justify-between">
            <span class="text-sm font-medium text-[var(--color-secondary)]">
              📍 {{ place.distanceKm }}km
            </span>
            <span class="text-[var(--color-primary)] font-medium">→</span>
          </div>
        </div>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
defineProps({
  nearbyPlaces: {
    type: Array,
    required: true
  }
})
</script>