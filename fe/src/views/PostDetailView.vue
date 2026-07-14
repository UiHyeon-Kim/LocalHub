<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const postId = computed(() => route.params.id)
</script>

<template>
  <section class="mx-auto max-w-7xl px-6 py-16">
    <h1 class="text-3xl font-bold text-slate-900">
      게시글 상세
    </h1>

    <p class="mt-4 text-slate-600">
      게시글 ID: {{ postId }}
    </p>

    <RouterLink
      to="/posts"
      class="mt-8 inline-flex text-emerald-800 hover:underline"
    >
      목록으로 돌아가기
    </RouterLink>
  </section>
</template>