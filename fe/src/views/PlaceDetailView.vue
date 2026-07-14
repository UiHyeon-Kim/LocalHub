<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const placeId = computed(() => route.params.id)
</script>

<template>
  <section class="mx-auto max-w-7xl px-6 py-16">
    <h1 class="text-3xl font-bold text-slate-900">
      장소 상세
    </h1>

    <p class="mt-4 text-slate-600">
      장소 ID: {{ placeId }}
    </p>
  </section>
</template>