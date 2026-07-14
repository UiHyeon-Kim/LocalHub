<template>
  <div class="min-h-screen bg-[var(--color-background)]">
    <div class="page-container page-section">
      <div class="mx-auto max-w-3xl">
        <!-- 제목 -->
        <h1 class="text-4xl font-bold text-[var(--color-text)]">
          {{ isEditMode ? '게시글 수정' : '새 게시글 작성' }}
        </h1>

        <!-- 폼 -->
        <form @submit.prevent="handleSubmit" class="mt-8 space-y-6">
          <!-- 카테고리 -->
          <div>
            <label class="block text-sm font-semibold text-[var(--color-text)] mb-2">
              카테고리 *
            </label>
            <select
              v-model="form.category"
              class="w-full rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] bg-white transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
            >
              <option value="">선택하세요</option>
              <option value="관광">관광</option>
              <option value="맛집">맛집</option>
              <option value="생활">생활</option>
              <option value="질문">질문</option>
              <option value="행사">행사</option>
              <option value="자유">자유</option>
            </select>
            <div v-if="errors.category" class="mt-2 text-sm text-red-600">
              {{ errors.category }}
            </div>
          </div>

          <!-- 제목 -->
          <div>
            <label class="block text-sm font-semibold text-[var(--color-text)] mb-2">
              제목 *
            </label>
            <input
              v-model="form.title"
              type="text"
              placeholder="2자 이상 60자 이하"
              maxlength="60"
              class="w-full rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] placeholder-[var(--color-text-muted)] transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
            />
            <div class="mt-2 flex items-center justify-between">
              <div v-if="errors.title" class="text-sm text-red-600">
                {{ errors.title }}
              </div>
              <div class="text-xs text-[var(--color-text-muted)]">
                {{ form.title.length }} / 60
              </div>
            </div>
          </div>

          <!-- 내용 -->
          <div>
            <label class="block text-sm font-semibold text-[var(--color-text)] mb-2">
              내용 *
            </label>
            <textarea
              v-model="form.content"
              placeholder="5자 이상 2000자 이하"
              maxlength="2000"
              rows="12"
              class="w-full rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] placeholder-[var(--color-text-muted)] transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
            ></textarea>
            <div class="mt-2 flex items-center justify-between">
              <div v-if="errors.content" class="text-sm text-red-600">
                {{ errors.content }}
              </div>
              <div class="text-xs text-[var(--color-text-muted)]">
                {{ form.content.length }} / 2000
              </div>
            </div>
          </div>

          <!-- 연관 장소명 -->
          <div>
            <label class="block text-sm font-semibold text-[var(--color-text)] mb-2">
              연관 장소 (선택사항)
            </label>
            <input
              v-model="form.locationName"
              type="text"
              placeholder="예: 금오산 도립공원"
              class="w-full rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] placeholder-[var(--color-text-muted)] transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
            />
          </div>

          <!-- 비밀번호 (작성 모드만) -->
          <div v-if="!isEditMode" class="space-y-6">
            <div>
              <label class="block text-sm font-semibold text-[var(--color-text)] mb-2">
                수정·삭제용 비밀번호 *
              </label>
              <input
                v-model="form.password"
                type="password"
                placeholder="4자 이상 20자 이하"
                maxlength="20"
                class="w-full rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] placeholder-[var(--color-text-muted)] transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
              />
              <div v-if="errors.password" class="mt-2 text-sm text-red-600">
                {{ errors.password }}
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-[var(--color-text)] mb-2">
                비밀번호 확인 *
              </label>
              <input
                v-model="form.passwordConfirm"
                type="password"
                placeholder="비밀번호를 다시 입력하세요"
                maxlength="20"
                class="w-full rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] placeholder-[var(--color-text-muted)] transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
              />
              <div v-if="errors.passwordConfirm" class="mt-2 text-sm text-red-600">
                {{ errors.passwordConfirm }}
              </div>
            </div>
          </div>

          <!-- 버튼 -->
          <div class="flex gap-3 pt-6">
            <button
              type="submit"
              :disabled="isSubmitting"
              class="flex-1 rounded-lg bg-[var(--color-primary)] px-6 py-3 font-semibold text-white transition-all hover:bg-[var(--color-primary-hover)] disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {{ isSubmitting ? '처리 중...' : (isEditMode ? '수정 완료' : '게시글 등록') }}
            </button>
            <button
              type="button"
              @click="handleCancel"
              class="flex-1 rounded-lg border-2 border-[var(--color-border)] px-6 py-3 font-semibold text-[var(--color-text)] transition-all hover:border-[var(--color-primary)] hover:text-[var(--color-primary)]"
            >
              취소
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPostById, createMockPost, updateMockPost } from '@/data/mockPosts'

const route = useRoute()
const router = useRouter()

const isEditMode = computed(() => !!route.params.id)
const postId = route.params.id

const form = ref({
  category: '',
  title: '',
  content: '',
  locationName: '',
  password: '',
  passwordConfirm: ''
})

const errors = ref({})
const isSubmitting = ref(false)

onMounted(() => {
  if (isEditMode.value) {
    const verifyKey = sessionStorage.getItem(`localhub-post-edit-${postId}`)
    if (!verifyKey) {
      router.push(`/posts/${postId}`)
      return
    }

    const post = getPostById(postId)
    if (post) {
      form.value = {
        category: post.category,
        title: post.title,
        content: post.content,
        locationName: post.locationName || '',
        password: '',
        passwordConfirm: ''
      }
    }
  }
})

const validateForm = () => {
  errors.value = {}

  if (!form.value.category) {
    errors.value.category = '카테고리를 선택해주세요.'
  }

  if (!form.value.title.trim()) {
    errors.value.title = '제목을 입력해주세요.'
  } else if (form.value.title.trim().length < 2) {
    errors.value.title = '제목은 2자 이상 입력해주세요.'
  } else if (form.value.title.length > 60) {
    errors.value.title = '제목은 60자 이하여야 합니다.'
  }

  if (!form.value.content.trim()) {
    errors.value.content = '내용을 입력해주세요.'
  } else if (form.value.content.trim().length < 5) {
    errors.value.content = '내용은 5자 이상 입력해주세요.'
  } else if (form.value.content.length > 2000) {
    errors.value.content = '내용은 2000자 이하여야 합니다.'
  }

  if (!isEditMode.value) {
    if (!form.value.password) {
      errors.value.password = '비밀번호를 입력해주세요.'
    } else if (form.value.password.length < 4) {
      errors.value.password = '비밀번호는 4자 이상 입력해주세요.'
    } else if (form.value.password.length > 20) {
      errors.value.password = '비밀번호는 20자 이하여야 합니다.'
    }

    if (!form.value.passwordConfirm) {
      errors.value.passwordConfirm = '비밀번호 확인을 입력해주세요.'
    } else if (form.value.password !== form.value.passwordConfirm) {
      errors.value.passwordConfirm = '비밀번호가 일치하지 않습니다.'
    }
  }

  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    if (isEditMode.value) {
      await updateMockPost(postId, {
        category: form.value.category,
        title: form.value.title,
        content: form.value.content,
        locationName: form.value.locationName
      })
      sessionStorage.removeItem(`localhub-post-edit-${postId}`)
      await router.push(`/posts/${postId}`)
    } else {
      const newPost = await createMockPost({
        title: form.value.title,
        content: form.value.content,
        category: form.value.category,
        password: form.value.password,
        locationName: form.value.locationName
      })
      await router.push(`/posts/${newPost.id}`)
    }
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  if (isEditMode.value) {
    router.push(`/posts/${postId}`)
  } else {
    router.push('/posts')
  }
}
</script>