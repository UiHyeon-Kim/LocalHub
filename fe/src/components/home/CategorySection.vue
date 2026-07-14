<template>
  <section class="py-12">
    <div class="page-container">
      <!-- 제목 -->
      <h2 class="mb-10 text-3xl font-bold text-[var(--color-text)]">
        어떤 장소를 찾고 있나요?
      </h2>

      <!-- 카테고리 카드 그리드 -->
      <div class="grid grid-cols-7 gap-4">
        <button
          v-for="category in categories"
          :key="category.id"
          @click="selectedCategory = category.id"
          :class="[
            'group relative flex flex-col items-center gap-3 rounded-2xl border-2 px-4 py-8 transition-all duration-300',
            selectedCategory === category.id
              ? 'border-[var(--color-primary)] bg-green-50 shadow-lg'
              : 'border-[var(--color-border)] bg-white hover:border-[var(--color-primary)] hover:-translate-y-1 hover:shadow-md'
          ]"
        >
          <!-- 원형 아이콘 -->
          <div
            :class="[
              'flex h-12 w-12 items-center justify-center rounded-full text-xl font-bold text-white transition-colors',
              selectedCategory === category.id
                ? 'bg-[var(--color-primary)]'
                : 'bg-[var(--color-secondary)] group-hover:bg-[var(--color-primary)]'
            ]"
          >
            {{ category.initial }}
          </div>

          <!-- 카테고리명 -->
          <span
            :class="[
              'text-center text-sm font-medium transition-colors',
              selectedCategory === category.id
                ? 'text-[var(--color-primary)]'
                : 'text-[var(--color-text)]'
            ]"
          >
            {{ category.name }}
          </span>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const selectedCategory = ref('all')

const categories = [
  { id: 'all', name: '전체', initial: '전' },
  { id: 'attraction', name: '관광지', initial: '관' },
  { id: 'culture', name: '문화시설', initial: '문' },
  { id: 'festival', name: '축제·행사', initial: '축' },
  { id: 'sports', name: '레포츠', initial: '레' },
  { id: 'lodging', name: '숙박', initial: '숙' },
  { id: 'shopping', name: '쇼핑', initial: '쇼' }
]
</script>