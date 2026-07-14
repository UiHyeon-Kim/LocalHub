<template>
  <RouterLink :to="`/places/${place.id}`" class="block">
    <div
      :class="[
        'overflow-hidden rounded-lg border border-[var(--color-border)] bg-white transition-all duration-300 hover:shadow-lg hover:-translate-y-1',
        selected && 'border-[var(--color-primary)] border-2 bg-green-50'
      ]"
    >
      <!-- 이미지 -->
      <div
        :class="[
          'relative overflow-hidden transition-transform duration-300 hover:scale-105',
          featured ? 'h-56' : 'h-40'
        ]"
      >
        <PlaceImage
          :image-url="place.imageUrl"
          :name="place.name"
          :category="place.category"
        />

        <!-- 카테고리 배지 -->
        <div class="absolute left-3 top-3">
          <CategoryBadge :category="place.category" />
        </div>
      </div>

      <!-- 콘텐츠 -->
      <div class="p-4">
        <!-- 장소명 -->
        <h3
          :class="[
            'font-semibold text-[var(--color-text)] line-clamp-2',
            featured ? 'text-lg' : 'text-base'
          ]"
        >
          {{ place.name }}
        </h3>

        <!-- 짧은 설명 -->
        <p
          v-if="place.shortDescription"
          class="mt-2 line-clamp-2 text-sm text-[var(--color-text-muted)]"
        >
          {{ place.shortDescription }}
        </p>

        <!-- 주소 또는 지역명 -->
        <p class="mt-3 text-sm text-[var(--color-text-muted)]">
          {{ place.address || place.district }}
        </p>

        <!-- 거리 정보 -->
        <p
          v-if="place.distanceKm"
          class="mt-1 text-sm font-medium text-[var(--color-secondary)]"
        >
          현재 위치에서 {{ place.distanceKm }}km
        </p>

        <!-- 상세보기 링크 표시 -->
        <div class="mt-4 inline-flex items-center text-sm font-medium text-[var(--color-primary)]">
          상세보기
          <span class="ml-1">→</span>
        </div>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import CategoryBadge from '@/components/place/CategoryBadge.vue'
import PlaceImage from '@/components/place/PlaceImage.vue'

defineProps({
  place: {
    type: Object,
    required: true
  },
  featured: {
    type: Boolean,
    default: false
  },
  selected: {
    type: Boolean,
    default: false
  }
})
</script>