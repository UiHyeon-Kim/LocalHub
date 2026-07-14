<template>
  <div class="min-h-screen bg-[var(--color-background)]">
    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-secondary)] py-16 text-white">
      <div class="page-container">
        <h1 class="text-4xl font-bold">지역의 이야기를 함께 나눠보세요</h1>
        <p class="mt-3 text-lg text-white/90">
          궁금한 점을 묻고, 알고 있는 지역 정보를 자유롭게 공유할 수 있습니다.
        </p>
        <RouterLink
          to="/posts/new"
          class="mt-6 inline-block rounded-lg bg-white px-6 py-3 font-semibold text-[var(--color-primary)] transition-all hover:shadow-lg"
        >
          글쓰기
        </RouterLink>
      </div>
    </div>

    <!-- 안내 -->
    <div class="page-container page-section">
      <div class="rounded-lg border border-blue-200 bg-blue-50 p-4 text-sm text-blue-800">
        <p class="font-semibold">💡 익명 게시판 안내</p>
        <p class="mt-2">
          모든 게시글은 익명으로 작성되며, 수정과 삭제는 작성 당시 등록한 비밀번호가 필요합니다.
        </p>
      </div>
    </div>

    <!-- 검색 및 필터 -->
    <div class="page-container">
      <div class="mb-6">
        <PostSearchBar
          :model-value="searchKeyword"
          :selected-category="selectedCategory"
          @update:model-value="searchKeyword = $event"
          @update:selected-category="selectedCategory = $event; currentPage = 1"
          @search="currentPage = 1"
          @reset="handleReset"
        />
      </div>

      <!-- 게시글 개수 -->
      <div class="mb-4 text-sm text-[var(--color-text-muted)] font-medium">
        총 {{ filteredPosts.length }}개의 게시글
      </div>
    </div>

    <!-- 게시글 목록 또는 빈 상태 -->
    <div class="page-container pb-12">
      <div v-if="paginatedPosts.length > 0" class="rounded-lg border border-[var(--color-border)] bg-white">
        <PostListItem
          v-for="post in paginatedPosts"
          :key="post.id"
          :post="post"
        />
      </div>

      <EmptyState
        v-else
        title="게시글이 없습니다"
        :description="`'${searchKeyword || selectedCategory}'에 해당하는 게시글이 없습니다.`"
        action-text="새 글 작성하기"
        @action="$router.push('/posts/new')"
      />
    </div>

    <!-- 페이지네이션 -->
    <div v-if="filteredPosts.length > 0" class="page-container page-section">
      <div class="flex items-center justify-center gap-2">
        <!-- 이전 버튼 -->
        <button
          :disabled="currentPage === 1"
          @click="currentPage--"
          class="rounded-lg border border-[var(--color-border)] px-4 py-2 text-[var(--color-text)] transition-all disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed hover:border-[var(--color-primary)] hover:text-[var(--color-primary)]"
        >
          ← 이전
        </button>

        <!-- 페이지 번호 -->
        <div class="flex gap-1">
          <button
            v-for="page in totalPages"
            :key="page"
            :class="[
              'rounded-lg px-3 py-2 font-medium transition-all',
              currentPage === page
                ? 'bg-[var(--color-primary)] text-white'
                : 'border border-[var(--color-border)] text-[var(--color-text)] hover:border-[var(--color-primary)] hover:text-[var(--color-primary)]'
            ]"
            @click="currentPage = page"
          >
            {{ page }}
          </button>
        </div>

        <!-- 다음 버튼 -->
        <button
          :disabled="currentPage === totalPages"
          @click="currentPage++"
          class="rounded-lg border border-[var(--color-border)] px-4 py-2 text-[var(--color-text)] transition-all disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed hover:border-[var(--color-primary)] hover:text-[var(--color-primary)]"
        >
          다음 →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { searchPosts } from '@/data/mockPosts'
import PostListItem from '@/components/post/PostListItem.vue'
import PostSearchBar from '@/components/post/PostSearchBar.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const searchKeyword = ref('')
const selectedCategory = ref('전체')
const currentPage = ref(1)
const pageSize = 5

const filteredPosts = computed(() => {
  return searchPosts(searchKeyword.value, selectedCategory.value)
})

const totalPages = computed(() => {
  return Math.ceil(filteredPosts.value.length / pageSize)
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredPosts.value.slice(start, end)
})

const handleReset = () => {
  searchKeyword.value = ''
  selectedCategory.value = '전체'
  currentPage.value = 1
}
</script>