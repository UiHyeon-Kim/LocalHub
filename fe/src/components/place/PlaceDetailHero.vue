<template>
  <section class="relative overflow-hidden rounded-b-[32px]">
    <div class="relative h-[320px] w-full md:h-[380px]">
      <img
        :src="heroImage"
        :alt="place.name"
        class="h-full w-full object-cover"
      />
      <div class="absolute inset-0 bg-black/45" />

      <div class="absolute inset-0">
        <div class="page-container flex h-full items-end py-10">
          <div class="flex w-full items-end justify-between gap-6 pb-6 md:pb-8">
            <!-- 왼쪽 텍스트 -->
            <div class="min-w-0">
              <span
                v-if="place.category"
                class="inline-flex rounded-full bg-[var(--color-primary)] px-4 py-2 text-sm font-semibold text-white"
              >
                {{ place.category }}
              </span>

              <h1
                class="mt-4 break-keep text-4xl font-bold leading-tight text-white md:text-5xl"
              >
                {{ place.name }}
              </h1>
            </div>

            <!-- 우측 메타 -->
            <div
              class="flex shrink-0 items-center gap-4 rounded-full bg-white/12 px-5 py-3 text-white backdrop-blur-sm"
            >
              <button
                type="button"
                class="inline-flex items-center gap-2 transition hover:opacity-80"
              >
                <span class="text-lg">❤️</span>
                <span class="text-sm font-semibold">
                  {{ likeCount }}
                </span>
              </button>

              <div class="h-5 w-px bg-white/30" />

              <div class="inline-flex items-center gap-2">
                <span class="text-lg">👁️</span>
                <span class="text-sm font-semibold">
                  {{ viewCount }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  place: {
    type: Object,
    required: true,
  },
})

const heroImage = computed(() => {
  return (
    props.place.imageUrl ||
    props.place.thumbnailUrl ||
    'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=80'
  )
})

const likeCount = computed(() => {
  return props.place.likeCount ?? props.place.likes ?? 0
})

const viewCount = computed(() => {
  return props.place.viewCount ?? props.place.views ?? 0
})
</script>