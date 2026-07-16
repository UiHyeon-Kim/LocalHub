<template>
  <RouterLink
    :to="`/posts/${post.id}`"
    class="block border-b border-[var(--color-border)] px-5 py-4 transition last:border-b-0 hover:bg-[var(--color-surface-muted)] md:px-6"
  >
    <article class="flex items-start justify-between gap-5 md:gap-8">

      <!-- 왼쪽 -->
      <div class="flex min-w-0 flex-1 items-start gap-4">

        <span
          class="flex-shrink-0 rounded-[8px] bg-blue-50 px-2.5 py-1.5 text-xs font-semibold text-blue-600"
        >
          {{ post.category }}
        </span>


        <div class="min-w-0 flex-1">

          <h2
            class="truncate text-sm font-semibold text-[var(--color-text)] md:text-base"
          >
            {{ post.title }}
          </h2>


          <!-- 연관 장소 -->
          <p
            v-if="post.locationName || post.location_name || post.location"
            class="mt-2 truncate text-xs text-[var(--color-text-muted)]"
          >
            <span class="mr-1 text-pink-500">●</span>

            {{
              post.locationName ||
              post.location_name ||
              post.location
            }}

          </p>

        </div>

      </div>



      <!-- 오른쪽 -->
      <div
        class="flex flex-shrink-0 flex-col items-end gap-1 pl-3 text-right text-xs text-[var(--color-text-muted)]"
      >

        <time :datetime="post.createdAt">
          {{ displayDate }}
        </time>


        <span>
          조회 {{ viewCount }}
        </span>

      </div>

    </article>
  </RouterLink>
</template>



<script setup>

import { computed } from 'vue'


const props = defineProps({

  post: {
    type: Object,
    required: true,
  },

})



const displayDate = computed(() => {

  const rawDate =
    props.post.createdAt ??
    props.post.created_at ??
    props.post.date ??
    ''


  if (!rawDate) {
    return ''
  }


  const date = new Date(rawDate)


  if (Number.isNaN(date.getTime())) {

    return rawDate

  }


  return new Intl.DateTimeFormat(
    'ko-KR',
    {
      month: 'long',
      day: 'numeric',
    }
  ).format(date)

})



const viewCount = computed(() => {

   return props.post.viewCount ?? 0

})

</script>