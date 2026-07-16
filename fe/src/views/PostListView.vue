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


    <main class="py-10 md:py-12">
      <div class="page-container">
        <div class="space-y-8">

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
                  {{ totalCount }}
                </span>
                개의 게시글
              </p>


              <p v-if="posts.length > 0">
                현재 페이지 {{ currentPage }} / {{ totalPages }}
              </p>

            </div>

          </section>



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



          <nav
            v-if="posts.length > 0 && totalPages > 1"
            aria-label="게시글 페이지 이동"
            class="flex flex-wrap items-center justify-center gap-2 pt-2"
          >

            <button
              type="button"
              :disabled="currentPage === 1"
              class="h-11 rounded-[12px] border border-[var(--color-border)] bg-white px-4 text-sm font-semibold text-[var(--color-text)]"
              @click="changePage(currentPage - 1)"
            >
              ← 이전
            </button>


            <div class="flex gap-1.5">

              <button
                v-for="pageNumber in visiblePages"
                :key="pageNumber"
                type="button"
                class="flex h-11 min-w-11 items-center justify-center rounded-[12px] px-3 text-sm font-semibold"
                @click="changePage(pageNumber)"
              >
                {{ pageNumber }}
              </button>

            </div>


            <button
              type="button"
              :disabled="currentPage === totalPages"
              class="h-11 rounded-[12px] border border-[var(--color-border)] bg-white px-4 text-sm font-semibold"
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

import {
  computed,
  ref,
  onMounted,
  onActivated
} from 'vue'


import EmptyState from '@/components/common/EmptyState.vue'
import PostListItem from '@/components/post/PostListItem.vue'
import PostSearchBar from '@/components/post/PostSearchBar.vue'


import {
  getPosts
} from '@/api/postApi'



const posts = ref([])

const totalCount = ref(0)


const searchKeyword = ref('')

const selectedCategory = ref('전체')

const currentPage = ref(1)


const pageSize = 5



const fetchPosts = async () => {

  try {

    const response = await getPosts({

      keyword: searchKeyword.value,

      category:
        selectedCategory.value === '전체'
          ? ''
          : selectedCategory.value,

      page: currentPage.value,

      size: pageSize

    })


    posts.value =
      response.items || response


    totalCount.value =
      response.total || posts.value.length



  } catch(error) {

    console.error(
      '게시글 조회 실패',
      error
    )


    posts.value = []

    totalCount.value = 0

  }

}



onMounted(() => {

  fetchPosts()

})

onActivated(() => {
  fetchPosts()
})



const totalPages = computed(() => {

  return Math.max(
    1,
    Math.ceil(
      totalCount.value / pageSize
    )
  )

})



const paginatedPosts = computed(() => {

  return posts.value

})



const visiblePages = computed(() => {

  const pages = []


  const start = Math.max(
    1,
    currentPage.value - 2
  )


  const end = Math.min(
    totalPages.value,
    currentPage.value + 2
  )


  for(
    let page=start;
    page<=end;
    page++
  ){

    pages.push(page)

  }


  return pages

})



const emptyDescription = computed(() => {

  if(searchKeyword.value){

    return `"${searchKeyword.value}" 검색 결과가 없습니다.`

  }


  return '아직 작성된 게시글이 없습니다.'

})



const handleSearch = () => {

  currentPage.value = 1

  fetchPosts()

}



const handleCategoryChange = (category) => {

  selectedCategory.value = category

  currentPage.value = 1

  fetchPosts()

}



const handleReset = () => {

  searchKeyword.value = ''

  selectedCategory.value = '전체'

  currentPage.value = 1

  fetchPosts()

}



const changePage = (page) => {


  if(
    page < 1 ||
    page > totalPages.value
  ){

    return

  }


  currentPage.value = page

  fetchPosts()

}


</script>