<template>
  <section class="bg-[var(--color-background)] py-16">
    <div class="page-container">
      <div class="mb-8 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 class="text-3xl font-semibold text-[var(--color-text)]">
            지금 주목할 지역의 장소
          </h2>
          <p class="mt-2 max-w-xl text-sm text-[var(--color-text-muted)]">
            추천 장소를 살펴보고 상세 정보를 확인해보세요.
          </p>
        </div>

        <RouterLink
          to="/places"
          class="inline-flex items-center gap-2 text-sm font-semibold text-[var(--color-primary)] transition hover:text-[var(--color-secondary)]"
        >
          전체 장소 보기
          <span>→</span>
        </RouterLink>
      </div>

      <div class="grid grid-cols-12 gap-6">
        <RouterLink
          :to="`/places/${featuredPlaces[0].id}`"
          class="group col-span-12 overflow-hidden rounded-[24px] border border-[var(--color-border)] bg-white transition duration-300 hover:-translate-y-1 hover:shadow-sm md:col-span-8"
        >
          <div class="relative overflow-hidden">
            <img
              :src="featuredPlaces[0].imageUrl"
              :alt="featuredPlaces[0].name"
              class="h-[420px] w-full object-cover transition duration-300 group-hover:scale-105"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>

            <div class="absolute left-6 bottom-6 right-6">
              <span class="inline-flex rounded-full bg-[var(--color-primary)] px-3 py-1 text-sm font-semibold text-white">
                {{ featuredPlaces[0].category }}
              </span>
              <h3 class="mt-4 text-3xl font-semibold text-white">
                {{ featuredPlaces[0].name }}
              </h3>
              <p class="mt-3 max-w-xl text-sm text-white/80 line-clamp-2">
                {{ featuredPlaces[0].description }}
              </p>
            </div>
          </div>
        </RouterLink>

        <div class="col-span-12 flex flex-col gap-6 md:col-span-4">
          <RouterLink
            v-for="place in featuredPlaces.slice(1, 3)"
            :key="place.id"
            :to="`/places/${place.id}`"
            class="group overflow-hidden rounded-[20px] border border-[var(--color-border)] bg-white transition duration-300 hover:-translate-y-1 hover:shadow-sm"
          >
            <div class="relative overflow-hidden h-40">
              <img
                :src="place.imageUrl"
                :alt="place.name"
                class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
              />
            </div>
            <div class="p-5">
              <span class="inline-flex rounded-full bg-[var(--color-surface)] px-3 py-1 text-xs font-semibold text-[var(--color-primary)]">
                {{ place.category }}
              </span>
              <h4 class="mt-3 line-clamp-2 text-xl font-semibold text-[var(--color-text)]">
                {{ place.name }}
              </h4>
              <p class="mt-2 text-sm text-[var(--color-text-muted)] line-clamp-2">
                {{ place.shortDescription }}
              </p>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { featuredPlaces } from '@/data/homeMockData'
</script>