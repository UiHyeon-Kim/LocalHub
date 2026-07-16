<template>
  <div class="flex flex-wrap gap-2">
    <button
      v-for="suggestion in suggestions"
      :key="suggestion.id"
      @click="$emit('select', suggestion.message)"
      class="rounded-full border border-[var(--color-border)] bg-white px-3 py-2 text-sm font-medium text-[var(--color-primary)] transition-all hover:border-[var(--color-primary)] hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
    >
      {{ suggestion.label }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  suggestions: {
    type: Array,
    required: true
  }
})

defineEmits(['select'])
</script>