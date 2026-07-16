<template>
  <section v-if="nearbyPlaces && nearbyPlaces.length" class="mt-10">
    <h2 class="text-2xl font-bold text-[var(--color-text)] mb-6">
      주변에 함께 볼 만한 장소
    </h2>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <RouterLink
        v-for="p in nearbyPlaces"
        :key="p.id"
        :to="`/places/${p.id}`"
        class="group flex flex-col overflow-hidden rounded-2xl border border-[var(--color-border)] bg-white shadow-sm transition hover:shadow-md"
      >
        <div class="relative h-44 w-full overflow-hidden">
          <img v-if="p.imageUrl" :src="p.imageUrl" :alt="p.name" class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"/>
          <div v-else class="h-full w-full flex items-center justify-center bg-[var(--color-surface-muted)]">📍</div>
        </div>

        <div class="p-4">
          <h3 class="text-lg font-semibold text-[var(--color-text)] line-clamp-2">{{ p.name }}</h3>
          <p class="mt-2 text-sm text-[var(--color-text-muted)] line-clamp-2">{{ p.shortDescription }}</p>

          <div class="mt-4 flex items-center justify-between text-sm text-[var(--color-text-muted)]">
            <span>📍 {{ p.distanceKm ?? '-' }}km</span>
            <span class="text-[var(--color-primary)] font-semibold">자세히 →</span>
          </div>
        </div>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
defineProps({
  nearbyPlaces: { type: Array, required: true }
})
</script>