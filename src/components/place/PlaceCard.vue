<template>
  <RouterLink :to="`/places/${place.id}`" class="block">
    <div
      :class="[
        'overflow-hidden rounded-[18px] border border-[var(--color-border)] bg-white transition-all duration-300 hover:-translate-y-1 hover:shadow-md',
        selected ? 'border-[var(--color-primary)] bg-green-50' : ''
      ]"
    >
      <div class="relative overflow-hidden transition-transform duration-300 group-hover:scale-105">
        <PlaceImage
          :image-url="place.imageUrl"
          :name="place.name || '장소'"
          :category="place.category"
          aspectRatio="4 / 3"
        />
        <div class="absolute left-4 top-4">
          <CategoryBadge :category="place.category || '기타'" />
        </div>
      </div>

      <div class="p-4">
        <h3 class="font-semibold text-[var(--color-text)] line-clamp-2">
          {{ place.name || '이름 미정' }}
        </h3>

        <p v-if="place.shortDescription" class="mt-2 line-clamp-2 text-sm text-[var(--color-text-muted)]">
          {{ place.shortDescription }}
        </p>

        <p class="mt-3 text-sm text-[var(--color-text-muted)] line-clamp-2">
          {{ place.address || place.district || '주소 정보 없음' }}
        </p>

        <div class="mt-4 inline-flex items-center gap-1 text-sm font-medium text-[var(--color-primary)]">
          상세보기
          <span>→</span>
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