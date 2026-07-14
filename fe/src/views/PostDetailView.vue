<template>
  <div v-if="post" class="min-h-screen bg-[var(--color-background)]">
    <!-- 게시글 컨테이너 -->
    <div class="page-container page-section">
      <div class="mx-auto max-w-3xl">
        <!-- 뒤로가기 버튼 -->
        <RouterLink
          to="/posts"
          class="mb-6 inline-flex items-center gap-2 text-[var(--color-primary)] font-medium hover:gap-3 transition-all"
        >
          ← 목록으로 돌아가기
        </RouterLink>

        <!-- 게시글 헤더 -->
        <div class="rounded-lg border border-[var(--color-border)] bg-white p-8">
          <!-- 카테고리 -->
          <div class="mb-4">
            <span class="inline-block rounded-md bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700">
              {{ post.category }}
            </span>
          </div>

          <!-- 제목 -->
          <h1 class="text-4xl font-bold text-[var(--color-text)]">
            {{ post.title }}
          </h1>

          <!-- 메타 정보 -->
          <div class="mt-6 flex items-center gap-6 border-b border-[var(--color-border)] pb-6 text-sm text-[var(--color-text-muted)]">
            <div>작성일: {{ formatDateTime(post.createdAt) }}</div>
            <div v-if="post.updatedAt">수정됨: {{ formatDateTime(post.updatedAt) }}</div>
            <div>조회수: {{ post.viewCount }}</div>
            <div v-if="post.locationName">📍 {{ post.locationName }}</div>
          </div>

          <!-- 컨트롤 버튼 -->
          <div class="mt-6 flex gap-3">
            <button
              @click="showEditPasswordModal = true"
              class="rounded-lg border-2 border-[var(--color-primary)] px-4 py-2 font-semibold text-[var(--color-primary)] transition-all hover:bg-[var(--color-primary)] hover:text-white"
            >
              수정
            </button>
            <button
              @click="showDeletePasswordModal = true"
              class="rounded-lg border-2 border-red-500 px-4 py-2 font-semibold text-red-500 transition-all hover:bg-red-500 hover:text-white"
            >
              삭제
            </button>
          </div>
        </div>

        <!-- 본문 -->
        <div class="mt-8 rounded-lg border border-[var(--color-border)] bg-white p-8">
          <div class="prose prose-sm max-w-none whitespace-pre-wrap text-lg leading-relaxed text-[var(--color-text)]">
            {{ post.content }}
          </div>
        </div>
      </div>
    </div>

    <!-- 수정 비밀번호 모달 -->
    <PasswordModal
      :open="showEditPasswordModal"
      title="게시글 수정"
      description="이 게시글을 수정하려면 작성 시 등록한 비밀번호를 입력하세요."
      confirm-text="인증"
      :loading="editLoading"
      :error-message="editError"
      @close="showEditPasswordModal = false"
      @confirm="handleEditPassword"
    />

    <!-- 삭제 비밀번호 모달 -->
    <PasswordModal
      :open="showDeletePasswordModal"
      title="게시글 삭제"
      description="삭제한 게시글은 복구할 수 없습니다. 작성 시 등록한 비밀번호를 입력하세요."
      confirm-text="삭제"
      :loading="deleteLoading"
      :error-message="deleteError"
      @close="showDeletePasswordModal = false"
      @confirm="handleDeletePassword"
    />
  </div>

  <!-- Not Found -->
  <div v-else class="flex h-screen items-center justify-center bg-[var(--color-background)]">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-[var(--color-text)]">
        게시글을 찾을 수 없습니다
      </h1>
      <p class="mt-4 text-[var(--color-text-muted)]">
        요청하신 게시글이 없거나 삭제되었습니다.
      </p>
      <RouterLink
        to="/posts"
        class="mt-8 inline-block rounded-lg bg-[var(--color-primary)] px-6 py-3 text-white font-semibold transition-all hover:bg-[var(--color-primary-hover)]"
      >
        목록으로 돌아가기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPostById, verifyPostPassword, deleteMockPost } from '@/data/mockPosts'
import PasswordModal from '@/components/post/PasswordModal.vue'

const route = useRoute()
const router = useRouter()

const postId = route.params.id
const post = computed(() => getPostById(postId))

const showEditPasswordModal = ref(false)
const showDeletePasswordModal = ref(false)
const editLoading = ref(false)
const editError = ref('')
const deleteLoading = ref(false)
const deleteError = ref('')

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleEditPassword = async (password) => {
  editLoading.value = true
  editError.value = ''

  try {
    verifyPostPassword(postId, password)
    sessionStorage.setItem(`localhub-post-edit-${postId}`, 'verified')
    showEditPasswordModal.value = false
    await router.push(`/posts/${postId}/edit`)
  } catch (error) {
    editError.value = error.message
  } finally {
    editLoading.value = false
  }
}

const handleDeletePassword = async (password) => {
  deleteLoading.value = true
  deleteError.value = ''

  try {
    deleteMockPost(postId, password)
    showDeletePasswordModal.value = false
    await router.push('/posts')
  } catch (error) {
    deleteError.value = error.message
  } finally {
    deleteLoading.value = false
  }
}
</script>

<style scoped>
.prose {
  all: unset;
}
</style>