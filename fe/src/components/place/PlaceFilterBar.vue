<template>
  <div class="rounded-[20px] border border-[var(--color-border)] bg-white p-5 shadow-sm">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div class="relative flex-1">
        <span class="pointer-events-none absolute inset-y-0 left-4 flex items-center text-[var(--color-text-muted)]">
          🔍
        </span>
        <input
          v-model="localKeyword"
          @keyup.enter="emitSearch"
          type="text"
          placeholder="장소명이나 주소를 검색해보세요"
          class="h-12 w-full rounded-[14px] border border-[var(--color-border)] bg-white px-12 pr-4 text-[var(--color-text)] placeholder:text-[var(--color-text-muted)] focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
        />
        <button
          v-if="localKeyword.trim()"
          @click="clearKeyword"
          type="button"
          class="absolute right-3 top-1/2 -translate-y-1/2 rounded-full px-3 py-1 text-sm text-[var(--color-text-muted)] transition hover:text-[var(--color-primary)]"
        >
          지우기
        </button>
      </div>

      <button
        @click="emitSearch"
        type="button"
        class="h-12 rounded-[14px] border border-[var(--color-border)] bg-white px-5 text-sm font-semibold text-[var(--color-primary)] transition hover:border-[var(--color-primary)] hover:bg-[var(--color-primary)]/10"
      >
        검색
      </button>
    </div>

    <div class="mt-4 flex flex-wrap gap-2">
      <button
        v-for="option in categories"
        :key="option.id"
        @click="selectCategory(option.id)"
        type="button"
        :class="[
          'rounded-full px-4 py-2 text-sm font-medium transition',
          selectedCategory === option.id
            ? 'bg-[var(--color-primary)] text-white'
            : 'border border-[var(--color-border)] bg-white text-[var(--color-text)] hover:border-[var(--color-primary)]'
        ]"
      >
        {{ option.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  selectedCategory: {
    type: String,
    default: '전체'
  },
  categories: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'update:selectedCategory', 'search', 'reset'])

const localKeyword = ref(props.modelValue)

watch(
  () => props.modelValue,
  (value) => {
    localKeyword.value = value
  }
)

const emitSearch = () => {
  emit('update:modelValue', localKeyword.value)
  emit('search')
}

const clearKeyword = () => {
  localKeyword.value = ''
  emit('update:modelValue', '')
  emit('search')
}

const selectCategory = (category) => {
  emit('update:selectedCategory', category)
  emit('search')
}
</script>