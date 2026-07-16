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
          <div
            class="flex w-full items-end justify-between gap-6 pb-6 md:pb-8"
          >
            <!-- 왼쪽 제목 -->
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

            <!-- 좋아요 / 조회수 -->
            <div
              class="flex shrink-0 items-center gap-4 rounded-full bg-black/45 px-5 py-3 text-white backdrop-blur-sm"
            >
              <button
                type="button"
                class="inline-flex items-center gap-2 rounded-full transition hover:opacity-80 disabled:cursor-not-allowed disabled:opacity-60"
                :aria-pressed="liked"
                :disabled="likeLoading"
                @click="emit('toggle-like')"
              >
                <span
                  class="text-lg"
                  aria-hidden="true"
                >
                  {{ liked ? '❤️' : '🤍' }}
                </span>

                <span class="text-sm font-semibold">
                  {{ place.likeCount ?? 0 }}
                </span>
              </button>

              <div class="h-5 w-px bg-white/30" />

              <div class="inline-flex items-center gap-2">
                <span
                  class="text-lg"
                  aria-hidden="true"
                >
                  👁️
                </span>

                <span class="text-sm font-semibold">
                  {{ place.viewCount ?? 0 }}
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
  liked: {
    type: Boolean,
    default: false,
  },
  likeLoading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits([
  'toggle-like',
])

const heroImage = computed(() => {
  return (
    props.place.imageUrl ||
    props.place.thumbnailUrl ||
    'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1400&q=80'
  )
})
</script>