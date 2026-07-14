<template>
  <footer class="bg-[var(--color-primary)]">
    <div class="page-container py-12">
      <!-- 메인 콘텐츠 -->
      <div class="grid grid-cols-2 gap-12 pb-8">
        <!-- 왼쪽: 로고 및 설명 -->
        <div>
          <div class="text-2xl font-bold text-white">
            LocalHub
          </div>
          <p class="mt-2 text-white/70">
            구미의 지역 정보와 이야기를 한곳에서 만나보세요.
          </p>
        </div>

        <!-- 오른쪽: 메뉴 -->
        <div>
          <nav class="flex gap-6">
            <RouterLink
              to="/"
              class="text-white/80 transition-colors hover:text-white"
            >
              홈
            </RouterLink>
            <RouterLink
              to="/"
              class="text-white/80 transition-colors hover:text-white"
            >
              장소 둘러보기
            </RouterLink>
            <RouterLink
              to="/posts"
              class="text-white/80 transition-colors hover:text-white"
            >
              커뮤니티
            </RouterLink>
          </nav>
        </div>
      </div>

      <!-- 구분선 -->
      <div class="border-t border-white/20"></div>

      <!-- 하단 안내 -->
      <div class="space-y-2 pt-6">
        <p class="text-sm text-white/60">
          제공되는 정보는 공공데이터를 기반으로 하며 실제 운영 정보와 다를 수 있습니다.
        </p>
        <p class="text-sm text-white/60">
          SSAFY 팀 프로젝트
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>