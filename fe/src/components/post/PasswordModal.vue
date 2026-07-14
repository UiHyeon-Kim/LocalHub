<template>
  <!-- Overlay -->
  <Transition name="fade">
    <div
      v-if="open"
      @click="$emit('close')"
      class="fixed inset-0 z-40 bg-black/40"
    ></div>
  </Transition>

  <!-- Modal -->
  <Transition name="modal">
    <div
      v-if="open"
      class="fixed left-1/2 top-1/2 z-50 w-full max-w-md -translate-x-1/2 -translate-y-1/2 rounded-2xl bg-white p-8 shadow-2xl"
      @click.stop
    >
      <!-- 제목 -->
      <h2 class="text-2xl font-bold text-[var(--color-text)]">
        {{ title }}
      </h2>

      <!-- 설명 -->
      <p class="mt-2 text-[var(--color-text-muted)]">
        {{ description }}
      </p>

      <!-- 비밀번호 입력 -->
      <div class="mt-6">
        <label class="sr-only">비밀번호</label>
        <input
          ref="passwordInput"
          v-model="password"
          type="password"
          placeholder="비밀번호를 입력하세요"
          @keyup.enter="handleConfirm"
          @keyup.escape="$emit('close')"
          class="w-full rounded-lg border border-[var(--color-border)] px-4 py-3 text-[var(--color-text)] placeholder-[var(--color-text-muted)] transition-colors focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/20"
        />
      </div>

      <!-- 오류 메시지 -->
      <div v-if="errorMessage" class="mt-3 rounded-lg bg-red-50 p-3 text-sm text-red-700">
        {{ errorMessage }}
      </div>

      <!-- 버튼 -->
      <div class="mt-8 flex gap-3">
        <button
          @click="$emit('close')"
          class="flex-1 rounded-lg border-2 border-[var(--color-border)] px-4 py-3 font-semibold text-[var(--color-text)] transition-all hover:border-[var(--color-primary)] hover:text-[var(--color-primary)]"
        >
          취소
        </button>
        <button
          @click="handleConfirm"
          :disabled="loading || !password.trim()"
          class="flex-1 rounded-lg bg-[var(--color-primary)] px-4 py-3 font-semibold text-white transition-all hover:bg-[var(--color-primary-hover)] disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {{ loading ? '처리 중...' : confirmText }}
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: '확인'
  },
  loading: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close', 'confirm'])

const password = ref('')
const passwordInput = ref(null)

const handleConfirm = () => {
  if (password.value.trim()) {
    emit('confirm', password.value)
  }
}

watch(() => props.open, async (newVal) => {
  if (newVal) {
    await nextTick()
    passwordInput.value?.focus()
  } else {
    password.value = ''
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: translate(-50%, -48%);
}
</style>