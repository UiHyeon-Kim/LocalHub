<template>
  <div class="min-h-screen bg-[var(--color-background)]">
    <section class="page-container py-10">
      <div class="space-y-6">
        <div class="space-y-3">
          <p class="text-sm font-semibold uppercase tracking-[0.26em] text-[var(--color-secondary)]">
            장소 둘러보기
          </p>
          <h1 class="text-4xl font-semibold text-[var(--color-text)]">
            구미·경북의 장소를 둘러보세요
          </h1>
          <p class="max-w-2xl text-base leading-8 text-[var(--color-text-muted)]">
            관광지, 문화시설, 음식점, 축제 등 다양한 지역 정보를 한눈에 살펴보세요.
          </p>
          <p class="text-sm text-[var(--color-text-muted)]">
            전체 {{ total }}개의 장소 중 {{ places.length }}개를 보고 있습니다.
          </p>
        </div>

        <PlaceFilterBar
          v-model:modelValue="keyword"
          v-model:selectedCategory="category"
          :categories="categories"
          @search="handleSearch"
          @reset="handleReset"
        />

        <div
          class="rounded-[18px] border border-[var(--color-border)] bg-white px-5 py-4 text-sm text-[var(--color-text-muted)] shadow-sm"
        >
          <div class="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
            <div>
              <span class="font-medium text-[var(--color-text)]">장소 {{ total }}개</span>
              <span v-if="filterText"> · {{ filterText }}</span>
            </div>
            <div class="text-[var(--color-text-muted)]">
              현재 페이지 {{ page }} / {{ pageCount }}
            </div>
          </div>
        </div>

        <div v-if="loading" class="grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
          <div
            v-for="index in 8"
            :key="index"
            class="animate-pulse rounded-2xl border border-[var(--color-border)] bg-white p-4"
          >
            <div class="mb-4 h-44 rounded-[18px] bg-[var(--color-border)]"></div>
            <div class="h-5 w-3/4 rounded bg-[var(--color-border)] mb-3"></div>
            <div class="h-4 w-5/6 rounded bg-[var(--color-border)] mb-3"></div>
            <div class="h-4 w-full rounded bg-[var(--color-border)]"></div>
          </div>
        </div>

        <div v-else-if="error">
          <EmptyState
            title="장소 정보를 불러오지 못했습니다."
            description="네트워크를 확인하고 다시 시도해 주세요."
            action-text="다시 시도"
            @action="fetchPlaces"
          />
        </div>

        <div v-else-if="places.length === 0">
          <EmptyState
            title="조건에 맞는 장소를 찾지 못했습니다."
            description="검색어나 카테고리를 변경해 다시 검색해보세요."
            action-text="필터 초기화"
            @action="handleReset"
          />
        </div>

        <div v-else class="grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
          <PlaceCard
            v-for="place in places"
            :key="place.id"
            :place="place"
          />
        </div>

        <div
          v-if="pageCount > 1"
          class="mt-8 flex flex-wrap items-center justify-center gap-2"
        >
          <button
            @click="changePage(page - 1)"
            :disabled="page === 1"
            class="h-12 rounded-[14px] border border-[var(--color-border)] bg-white px-4 text-sm font-semibold text-[var(--color-text)] transition hover:border-[var(--color-primary)] disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400"
          >
            이전
          </button>

          <button
            v-for="pageNumber in visiblePages"
            :key="pageNumber"
            @click="changePage(pageNumber)"
            :class="[
              'h-12 min-w-[44px] rounded-[14px] px-4 text-sm font-semibold transition',
              pageNumber === page
                ? 'bg-[var(--color-primary)] text-white'
                : 'border border-[var(--color-border)] bg-white text-[var(--color-text)] hover:border-[var(--color-primary)]'
            ]"
          >
            {{ pageNumber }}
          </button>

          <button
            @click="changePage(page + 1)"
            :disabled="page === pageCount"
            class="h-12 rounded-[14px] border border-[var(--color-border)] bg-white px-4 text-sm font-semibold text-[var(--color-text)] transition hover:border-[var(--color-primary)] disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-400"
          >
            다음
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PlaceFilterBar from '@/components/place/PlaceFilterBar.vue'
import PlaceCard from '@/components/place/PlaceCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import { getPlaces } from '@/api/placeApi'

const route = useRoute()
const router = useRouter()

const keyword = ref(route.query.keyword ?? '')
const category = ref(route.query.category ?? '전체')
const page = ref(Number(route.query.page ?? 1) || 1)

const places = ref([])
const total = ref(0)
const loading = ref(false)
const error = ref('')

const pageSize = 12
const categories = [
  { id: '전체', name: '전체' },
  { id: '관광지', name: '관광지' },
  { id: '문화시설', name: '문화시설' },
  { id: '축제·행사', name: '축제·행사' },
  { id: '여행 코스', name: '여행 코스' },
  { id: '레포츠', name: '레포츠' },
  { id: '숙박', name: '숙박' },
  { id: '쇼핑', name: '쇼핑' },
  { id: '음식점', name: '음식점' }
]

const filterText = computed(() => {
  const parts = []
  if (keyword.value.trim()) parts.push(`"${keyword.value.trim()}"`)
  if (category.value !== '전체') parts.push(category.value)
  return parts.length ? parts.join(' · ') : '전체 장소'
})

const pageCount = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

const visiblePages = computed(() => {
  const numbers = []
  const start = Math.max(1, page.value - 2)
  const end = Math.min(pageCount.value, page.value + 2)
  for (let i = start; i <= end; i += 1) {
    numbers.push(i)
  }
  return numbers
})

const updateQuery = () => {
  const query = {}
  if (keyword.value.trim()) query.keyword = keyword.value.trim()
  if (category.value !== '전체') query.category = category.value
  if (page.value > 1) query.page = page.value
  router.replace({ path: '/places', query })
}

const fetchPlaces = async () => {
  loading.value = true
  error.value = ''
  try {
    const { items, total: totalCount } = await getPlaces({
      keyword: keyword.value,
      category: category.value,
      limit: pageSize,
      offset: (page.value - 1) * pageSize
    })
    places.value = items
    total.value = totalCount
  } catch (err) {
    error.value = err.message || '장소 조회에 실패했습니다.'
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  updateQuery()
}

const handleReset = () => {
  keyword.value = ''
  category.value = '전체'
  page.value = 1
  updateQuery()
}

const changePage = (newPage) => {
  if (newPage < 1 || newPage > pageCount.value || newPage === page.value) return
  page.value = newPage
  updateQuery()
}

watch(
  () => route.query,
  (newQuery) => {
    keyword.value = newQuery.keyword ?? ''
    category.value = newQuery.category ?? '전체'
    page.value = Number(newQuery.page ?? 1) || 1
    fetchPlaces()
  },
  { immediate: true }
)
</script>