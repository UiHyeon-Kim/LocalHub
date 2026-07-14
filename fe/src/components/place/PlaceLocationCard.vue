<template>
  <div class="sticky top-[calc(var(--header-height)+24px)] space-y-6">
    <!-- 위치 정보 카드 -->
    <div class="rounded-3xl border border-[var(--color-border)] bg-white p-8 shadow-md">
      <h2 class="text-2xl font-bold text-[var(--color-text)]">위치 안내</h2>

      <!-- 지도 placeholder -->
      <div class="mt-6 rounded-2xl bg-gray-100 h-64 flex items-center justify-center">
        <div class="text-center">
          <div class="text-4xl mb-2">🗺️</div>
          <p class="text-[var(--color-text-muted)]">지도를 준비 중입니다</p>
        </div>
      </div>

      <!-- 주소 -->
      <div v-if="place.address" class="mt-6">
        <p class="text-sm text-[var(--color-text-muted)] font-semibold">주소</p>
        <p class="mt-2 text-base text-[var(--color-text)] font-medium">
          {{ place.address }}
        </p>
      </div>

      <!-- 길찾기 버튼 (비활성) -->
      <button
        disabled
        class="mt-6 w-full rounded-xl bg-gray-200 px-4 py-3 text-gray-500 font-semibold cursor-not-allowed"
      >
        길찾기 (준비 중)
      </button>
    </div>

    <!-- 목록으로 돌아가기 -->
    <RouterLink
      to="/"
      class="block w-full rounded-xl border-2 border-[var(--color-primary)] bg-white px-4 py-3 text-center text-[var(--color-primary)] font-semibold transition-all hover:bg-[var(--color-primary)] hover:text-white"
    >
      목록으로 돌아가기
    </RouterLink>
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