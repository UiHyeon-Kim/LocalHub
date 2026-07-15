<template>
  <section class="py-12">
    <div class="page-container">
      <div
        class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
      >
        <h2 class="text-3xl font-semibold text-[var(--color-text)]">
          어떤 장소를 찾고 있나요?
        </h2>

        <p class="max-w-xl text-sm text-[var(--color-text-muted)]">
          원하는 카테고리를 선택하면 관련 장소를 빠르게 탐색할 수 있습니다.
        </p>
      </div>

      <div class="overflow-x-auto pb-2">
        <div class="flex min-w-[720px] gap-3">
          <button
            v-for="categoryItem in categories"
            :key="categoryItem.id"
            type="button"
            :class="[
              'rounded-full px-4 py-3 text-sm font-medium transition',
              selectedCategory === categoryItem.id
                ? 'bg-[var(--color-primary)] text-white'
                : 'border border-[var(--color-border)] bg-white text-[var(--color-text)] hover:border-[var(--color-primary)]',
            ]"
            @click="selectCategory(categoryItem.id)"
          >
            {{ categoryItem.name }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedCategory = ref('전체')

const categories = [
  { id: '전체', name: '전체' },
  { id: '관광지', name: '관광지' },
  { id: '문화시설', name: '문화시설' },
  { id: '축제공연행사', name: '축제·행사' },
  { id: '여행코스', name: '여행 코스' },
  { id: '레포츠', name: '레포츠' },
  { id: '숙박', name: '숙박' },
  { id: '쇼핑', name: '쇼핑' },
  { id: '음식점', name: '음식점' },
]

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId

  const query =
    categoryId === '전체'
      ? {}
      : {
          category: categoryId,
        }

  router.push({
    path: '/places',
    query,
  })
}
</script>