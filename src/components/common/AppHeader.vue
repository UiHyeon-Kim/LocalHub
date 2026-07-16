<template>
  <header class="sticky top-0 z-50 h-[var(--header-height)] border-b border-[var(--color-border)] bg-white/80 backdrop-blur-md">
    <div class="page-container flex h-full items-center justify-between">
      <!-- 로고 -->
      <RouterLink to="/" class="text-xl font-bold text-[var(--color-primary)]">
        LocalHub
      </RouterLink>

      <!-- 메뉴 -->
      <nav class="flex gap-8">
        <RouterLink
          to="/"
          :class="[
            'relative pb-2 text-[var(--color-text)] transition-colors hover:text-[var(--color-primary)]',
            isActive('/') && 'text-[var(--color-primary)] font-semibold'
          ]"
        >
          홈
          <span
            v-if="isActive('/')"
            class="absolute bottom-0 left-0 right-0 h-1 bg-[var(--color-primary)]"
          ></span>
        </RouterLink>

        <RouterLink
          to="/places"
          :class="[
            'relative pb-2 text-[var(--color-text)] transition-colors hover:text-[var(--color-primary)]',
            isActive('/places') && 'text-[var(--color-primary)] font-semibold'
          ]"
        >
          장소 둘러보기
          <span
            v-if="isActive('/places')"
            class="absolute bottom-0 left-0 right-0 h-1 bg-[var(--color-primary)]"
          ></span>
        </RouterLink>

        <RouterLink
          to="/posts"
          :class="[
            'relative pb-2 text-[var(--color-text)] transition-colors hover:text-[var(--color-primary)]',
            isActive('/posts') && 'text-[var(--color-primary)] font-semibold'
          ]"
        >
          커뮤니티
          <span
            v-if="isActive('/posts')"
            class="absolute bottom-0 left-0 right-0 h-1 bg-[var(--color-primary)]"
          ></span>
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path === path || route.path.startsWith(path + '/')
}
</script>