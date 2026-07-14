<template>
  <div class="flex gap-2">
    <!-- 검색 레이블 (접근성) -->
    <label class="sr-only">검색 키워드</label>
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @keyup.enter="$emit('search')"
      type="text"
      placeholder="제목 또는 내용으로 검색..."
      class="flex-1 rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] placeholder-[var(--color-text-muted)] transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
    />

    <!-- 카테고리 선택 레이블 (접근성) -->
    <label class="sr-only">카테고리</label>
    <select
      :value="selectedCategory"
      @change="$emit('update:selectedCategory', $event.target.value)"
      class="rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] bg-white transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
    >
      <option value="전체">전체</option>
      <option value="관광">관광</option>
      <option value="맛집">맛집</option>
      <option value="생활">생활</option>
      <option value="질문">질문</option>
      <option value="행사">행사</option>
      <option value="자유">자유</option>
    </select>

    <!-- 검색 버튼 -->
    <button
      @click="$emit('search')"
      class="rounded-lg bg-[var(--color-primary)] px-6 py-3 font-semibold text-white transition-all hover:bg-[var(--color-primary-hover)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
    >
      검색
    </button>

    <!-- 초기화 버튼 -->
    <button
      @click="$emit('reset')"
      class="rounded-lg border-2 border-[var(--color-border)] px-6 py-3 font-semibold text-[var(--color-text)] transition-all hover:border-[var(--color-primary)] hover:text-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
    >
      초기화
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  selectedCategory: {
    type: String,
    default: '전체'
  }
})

defineEmits(['update:modelValue', 'update:selectedCategory', 'search', 'reset'])
</script>