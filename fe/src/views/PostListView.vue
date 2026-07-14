<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="mx-auto max-w-7xl px-6 py-16">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-slate-900">
          커뮤니티
        </h1>

        <p class="mt-4 text-slate-600">
          구미 지역 정보를 자유롭게 공유하는 익명 게시판입니다.
        </p>
      </div>

      <RouterLink
        to="/posts/new"
        class="rounded-lg bg-emerald-900 px-5 py-3 font-medium text-white"
      >
        글쓰기
      </RouterLink>
    </div>
  </section>
</template>