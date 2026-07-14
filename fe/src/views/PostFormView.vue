<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const isEditMode = computed(() => Boolean(route.params.id))
const pageTitle = computed(() =>
  isEditMode.value ? '게시글 수정' : '게시글 작성',
)
</script>

<template>
  <section class="mx-auto max-w-7xl px-6 py-16">
    <h1 class="text-3xl font-bold text-slate-900">
      {{ pageTitle }}
    </h1>

    <p class="mt-4 text-slate-600">
      {{ isEditMode ? '게시글 수정 화면입니다.' : '새 게시글 작성 화면입니다.' }}
    </p>

    <RouterLink
      to="/posts"
      class="mt-8 inline-flex text-emerald-800 hover:underline"
    >
      커뮤니티로 돌아가기
    </RouterLink>
  </section>
</template>