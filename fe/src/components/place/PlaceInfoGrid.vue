<template>
  <div class="grid grid-cols-4 gap-4">
    <!-- 주소 -->
    <div v-if="place.address" class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm">
      <h3 class="text-sm font-semibold text-[var(--color-text-muted)]">주소</h3>
      <p class="mt-3 text-base font-medium text-[var(--color-text)] line-clamp-3">
        {{ place.address }}
      </p>
    </div>

    <!-- 전화번호 -->
    <div v-if="place.phone" class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm">
      <h3 class="text-sm font-semibold text-[var(--color-text-muted)]">전화</h3>
      <p class="mt-3 text-base font-medium text-[var(--color-text)]">
        {{ place.phone }}
      </p>
    </div>

    <!-- 운영 시간 -->
    <div v-if="place.operatingHours" class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm">
      <h3 class="text-sm font-semibold text-[var(--color-text-muted)]">운영시간</h3>
      <p class="mt-3 text-base font-medium text-[var(--color-text)]">
        {{ place.operatingHours }}
      </p>
    </div>

    <!-- 요금 -->
    <div v-if="place.fee" class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm">
      <h3 class="text-sm font-semibold text-[var(--color-text-muted)]">요금</h3>
      <p class="mt-3 text-base font-medium text-[var(--color-text)]">
        {{ place.fee }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  place: {
    type: Object,
    required: true
  }
})
</script>