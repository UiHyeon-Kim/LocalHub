<template>
  <section class="bg-gray-50 py-16">
    <div class="page-container">
      <div class="grid grid-cols-2 gap-12">
        <!-- 왼쪽: 소개 -->
        <div class="flex flex-col justify-center">
          <h2 class="text-3xl font-bold text-[var(--color-text)]">
            사람과 장소가 만나는 곳
          </h2>
          <p class="mt-6 text-lg text-[var(--color-text-muted)] leading-relaxed">
            LocalHub는 단순한 장소 소개 사이트가 아닙니다.<br />
            지역의 사람들이 직접 경험을 나누고, 새로운 발견을 함께하는 커뮤니티입니다.
          </p>
          <RouterLink
            to="/posts"
            class="mt-8 inline-flex w-fit items-center gap-2 rounded-full bg-[var(--color-primary)] px-6 py-3 font-semibold text-white transition-all hover:bg-[var(--color-primary-hover)] hover:shadow-lg"
          >
            커뮤니티 전체보기
            <span>→</span>
          </RouterLink>
        </div>

        <!-- 오른쪽: 게시글 목록 -->
        <div class="space-y-4">
          <RouterLink
            v-for="post in communityPosts"
            :key="post.id"
            :to="`/posts/${post.id}`"
            class="block rounded-xl border border-[var(--color-border)] bg-white p-5 transition-all hover:border-[var(--color-primary)] hover:shadow-md"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="flex-1">
                <h4 class="font-semibold text-[var(--color-text)] line-clamp-2 hover:text-[var(--color-primary)]">
                  {{ post.title }}
                </h4>
                <div class="mt-3 flex items-center gap-3 text-xs text-[var(--color-text-muted)]">
                  <span class="rounded-full bg-gray-100 px-2 py-1">
                    {{ post.category }}
                  </span>
                  <span>{{ post.timeAgo }}</span>
                </div>
              </div>
              <div class="text-[var(--color-primary)] text-lg">→</div>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { communityPosts } from '@/data/homeMockData'
</script>