<template>
  <section class="bg-gray-50 py-16">
    <div class="page-container">
      <!-- 제목 -->
      <h2 class="mb-12 text-3xl font-bold text-[var(--color-text)]">
        지금 주목할 지역의 장소
      </h2>

      <!-- Bento Grid -->
      <div class="grid grid-cols-12 gap-6">
        <!-- 큰 카드 (왼쪽) -->
        <RouterLink
          :to="`/places/${featuredPlaces[0].id}`"
          class="group col-span-8 overflow-hidden rounded-3xl bg-white shadow-md transition-all duration-300 hover:-translate-y-2 hover:shadow-xl"
        >
          <div class="relative overflow-hidden">
            <!-- 이미지 -->
            <img
              :src="featuredPlaces[0].imageUrl"
              :alt="featuredPlaces[0].name"
              class="h-96 w-full object-cover transition-transform duration-300 group-hover:scale-105"
            />
            <!-- 그라데이션 오버레이 -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent"></div>

            <!-- 카테고리 배지 -->
            <div class="absolute left-4 top-4">
              <span class="inline-block rounded-full bg-[var(--color-primary)] px-3 py-1 text-sm font-semibold text-white">
                {{ featuredPlaces[0].category }}
              </span>
            </div>
          </div>

          <!-- 콘텐츠 -->
          <div class="p-6">
            <h3 class="text-2xl font-bold text-[var(--color-text)]">
              {{ featuredPlaces[0].name }}
            </h3>
            <p class="mt-3 line-clamp-2 text-gray-600">
              {{ featuredPlaces[0].description }}
            </p>
            <p class="mt-4 text-sm text-[var(--color-text-muted)]">
              {{ featuredPlaces[0].address }}
            </p>
            <div class="mt-5 inline-flex items-center text-[var(--color-primary)] font-medium">
              상세보기 <span class="ml-2">→</span>
            </div>
          </div>
        </RouterLink>

        <!-- 작은 카드들 (오른쪽) -->
        <div class="col-span-4 flex flex-col gap-6">
          <RouterLink
            v-for="place in featuredPlaces.slice(1, 3)"
            :key="place.id"
            :to="`/places/${place.id}`"
            class="group flex overflow-hidden rounded-2xl bg-white shadow-md transition-all duration-300 hover:-translate-y-2 hover:shadow-lg"
          >
            <!-- 이미지 -->
            <div class="relative h-28 w-28 overflow-hidden flex-shrink-0">
              <img
                :src="place.imageUrl"
                :alt="place.name"
                class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
            </div>

            <!-- 콘텐츠 -->
            <div class="flex flex-1 flex-col justify-between p-4">
              <div>
                <p class="text-xs font-semibold text-[var(--color-secondary)]">
                  {{ place.category }}
                </p>
                <h4 class="mt-1 line-clamp-1 font-bold text-[var(--color-text)]">
                  {{ place.name }}
                </h4>
              </div>
              <p class="text-xs text-[var(--color-primary)] font-medium">
                상세보기 →
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