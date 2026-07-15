<template>
  <div class="min-h-screen bg-[var(--color-background)]">
    <!-- Hero -->
    <section
      class="bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-secondary)] py-14 text-white md:py-16"
    >
      <div class="page-container">
        <div class="max-w-3xl">
          <h1 class="text-3xl font-bold leading-tight md:text-4xl">
            지역의 이야기를 함께 나눠보세요
          </h1>

          <p class="mt-4 text-base leading-7 text-white/90 md:text-lg">
            궁금한 점을 묻고, 알고 있는 지역 정보를 자유롭게 공유할 수 있습니다.
          </p>

          <RouterLink
            to="/posts/new"
            class="mt-7 inline-flex h-12 items-center justify-center rounded-[14px] bg-white px-6 text-sm font-semibold !text-[var(--color-primary)] shadow-sm transition hover:-translate-y-0.5 hover:shadow-lg"
          >
            글쓰기
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main class="py-10 md:py-12">
      <div class="page-container">
        <div class="space-y-8">
          <!-- 익명 게시판 안내 -->
          <section
            class="rounded-[18px] border border-blue-200 bg-blue-50 px-5 py-4 text-sm text-blue-800"
          >
            <p class="font-semibold">
              💡 익명 게시판 안내
            </p>

            <p class="mt-2 leading-6">
              모든 게시글은 익명으로 작성되며, 수정과 삭제는 작성 당시 등록한
              비밀번호가 필요합니다.
            </p>
          </section>

          <!-- 검색 및 필터 -->
          <section class="space-y-4">
            <PostSearchBar
              :model-value="searchKeyword"
              :selected-category="selectedCategory"
              @update:model-value="searchKeyword = $event"
              @update:selected-category="handleCategoryChange"
              @search="handleSearch"
              @reset="handleReset"
            />

            <div
              class="flex flex-col gap-2 text-sm text-[var(--color-text-muted)] sm:flex-row sm:items-center sm:justify-between"
            >
              <p class="font-medium">
                총
                <span class="font-semibold text-[var(--color-text)]">
                  {{ filteredPosts.length }}
                </span>
                개의 게시글
              </p>

              <p v-if="filteredPosts.length > 0">
                현재 페이지 {{ currentPage }} / {{ totalPages }}
              </p>
            </div>
          </section>

          <!-- 게시글 목록 -->
          <section>
            <div
              v-if="paginatedPosts.length > 0"
              class="overflow-hidden rounded-[18px] border border-[var(--color-border)] bg-white shadow-sm"
            >
              <PostListItem
                v-for="post in paginatedPosts"
                :key="post.id"
                :post="post"
              />
            </div>

            <EmptyState
              v-else
              title="게시글이 없습니다"
              :description="emptyDescription"
              action-text="새 글 작성하기"
              @action="$router.push('/posts/new')"
            />
          </section>

          <!-- 페이지네이션 -->
          <nav
            v-if="filteredPosts.length > 0 && totalPages > 1"
            aria-label="게시글 페이지 이동"
            class="flex flex-wrap items-center justify-center gap-2 pt-2"
          >
            <button
              type="button"
              :disabled="currentPage === 1"
              class="h-11 rounded-[12px] border border-[var(--color-border)] bg-white px-4 text-sm font-semibold text-[var(--color-text)] transition hover:border-[var(--color-primary)] hover:text-[var(--color-primary)] disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400 disabled:hover:border-[var(--color-border)]"
              @click="changePage(currentPage - 1)"
            >
              ← 이전
            </button>

            <div class="flex gap-1.5">
              <button
                v-for="pageNumber in visiblePages"
                :key="pageNumber"
                type="button"
                :class="[
                  'flex h-11 min-w-11 items-center justify-center rounded-[12px] px-3 text-sm font-semibold transition',
                  currentPage === pageNumber
                    ? 'bg-[var(--color-primary)] text-white shadow-sm'
                    : 'border border-[var(--color-border)] bg-white text-[var(--color-text)] hover:border-[var(--color-primary)] hover:text-[var(--color-primary)]',
                ]"
                @click="changePage(pageNumber)"
              >
                {{ pageNumber }}
              </button>
            </div>

            <button
              type="button"
              :disabled="currentPage === totalPages"
              class="h-11 rounded-[12px] border border-[var(--color-border)] bg-white px-4 text-sm font-semibold text-[var(--color-text)] transition hover:border-[var(--color-primary)] hover:text-[var(--color-primary)] disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400 disabled:hover:border-[var(--color-border)]"
              @click="changePage(currentPage + 1)"
            >
              다음 →
            </button>
          </nav>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

import EmptyState from '@/components/common/EmptyState.vue'
import PostListItem from '@/components/post/PostListItem.vue'
import PostSearchBar from '@/components/post/PostSearchBar.vue'
import { searchPosts } from '@/data/mockPosts'

const searchKeyword = ref('')
const selectedCategory = ref('전체')
const currentPage = ref(1)

const pageSize = 5

const filteredPosts = computed(() => {
  return searchPosts(
    searchKeyword.value,
    selectedCategory.value,
  )
})

const totalPages = computed(() => {
  return Math.max(
    1,
    Math.ceil(filteredPosts.value.length / pageSize),
  )
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize

  return filteredPosts.value.slice(start, end)
})

const visiblePages = computed(() => {
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(
    totalPages.value,
    currentPage.value + 2,
  )

  const pages = []

  for (let page = start; page <= end; page += 1) {
    pages.push(page)
  }

  return pages
})

const emptyDescription = computed(() => {
  const keyword = searchKeyword.value.trim()
  const category = selectedCategory.value

  if (keyword && category !== '전체') {
    return `"${keyword}" 검색어와 "${category}" 카테고리에 해당하는 게시글이 없습니다.`
  }

  if (keyword) {
    return `"${keyword}" 검색어에 해당하는 게시글이 없습니다.`
  }

  if (category !== '전체') {
    return `"${category}" 카테고리에 해당하는 게시글이 없습니다.`
  }

  return '아직 작성된 게시글이 없습니다.'
})

const handleSearch = () => {
  currentPage.value = 1
}

const handleCategoryChange = (category) => {
  selectedCategory.value = category
  currentPage.value = 1
}

const handleReset = () => {
  searchKeyword.value = ''
  selectedCategory.value = '전체'
  currentPage.value = 1
}

const changePage = (page) => {
  if (
    page < 1 ||
    page > totalPages.value ||
    page === currentPage.value
  ) {
    return
  }

  currentPage.value = page
}

watch(filteredPosts, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = totalPages.value
  }
})
</script>