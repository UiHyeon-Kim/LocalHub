<template>
  <div class="space-y-4">
    <!-- 로딩 스켈레톤 -->
    <template v-if="loading">
      <!-- 주소 카드 스켈레톤 -->
      <div
        class="animate-pulse rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm"
      >
        <div class="h-4 w-10 rounded bg-gray-200" />
        <div class="mt-4 h-5 w-4/5 rounded bg-gray-200" />
      </div>

      <!-- 전화 / 운영시간 카드 스켈레톤 -->
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div
          v-for="index in 2"
          :key="index"
          class="animate-pulse rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm"
        >
          <div class="h-4 w-14 rounded bg-gray-200" />
          <div class="mt-4 h-5 w-2/3 rounded bg-gray-200" />
        </div>
      </div>
    </template>

    <!-- 실제 데이터 -->
    <template v-else>
      <!-- 주소: 항상 전체 폭 -->
      <div
        v-if="addressItem"
        class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm"
      >
        <h3 class="text-sm font-semibold text-[var(--color-text-muted)]">
          {{ addressItem.label }}
        </h3>

        <p
          class="mt-3 whitespace-pre-line break-words text-base font-medium text-[var(--color-text)]"
        >
          {{ addressItem.value }}
        </p>
      </div>

      <!-- 전화, 운영시간, 요금 -->
      <div
        v-if="otherItems.length > 0"
        class="grid grid-cols-1 gap-4 md:grid-cols-2"
      >
        <div
          v-for="(item, index) in otherItems"
          :key="item.key"
          class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm"
          :class="{
            'md:col-span-2':
              otherItems.length === 1 ||
              (
                otherItems.length % 2 === 1 &&
                index === otherItems.length - 1
              ),
          }"
        >
          <h3 class="text-sm font-semibold text-[var(--color-text-muted)]">
            {{ item.label }}
          </h3>

          <p
            class="mt-3 whitespace-pre-line break-words text-base font-medium text-[var(--color-text)]"
          >
            {{ item.value }}
          </p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { getTourismCommon } from '@/api/placeApi'

const props = defineProps({
  place: {
    type: Object,
    required: true,
  },
})

const tourismInfo = ref({})
const loading = ref(false)

const removeHtml = (value) => {
  if (!value) {
    return ''
  }

  return String(value)
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .trim()
}

const firstNonEmpty = (...values) => {
  return values.find(
    (value) =>
      value !== null &&
      value !== undefined &&
      String(value).trim() !== '',
  )
}

const loadTourismInfo = async () => {
  if (!props.place?.contentId) {
    tourismInfo.value = {}
    loading.value = false
    return
  }

  loading.value = true

  try {
    tourismInfo.value = await getTourismCommon(
      props.place.contentId,
      props.place.contentTypeId,
    )
  } catch (error) {
    console.error('관광 상세 정보 조회 실패:', error)
    tourismInfo.value = {}
  } finally {
    loading.value = false
  }
}

const infoItems = computed(() => {
  const info = tourismInfo.value
  const place = props.place

  const address = firstNonEmpty(
    info.address,
    place.address,
  )

  const phone = firstNonEmpty(
    info.phone,
    place.phone,
  )

  const operatingHours = firstNonEmpty(
    info.operating_hours,
    place.operatingHours,
  )

  const fee = firstNonEmpty(
    info.fee,
    place.fee,
  )

  return [
    {
      key: 'address',
      label: '주소',
      value: removeHtml(address),
    },
    {
      key: 'phone',
      label: '전화',
      value: removeHtml(phone),
    },
    {
      key: 'operatingHours',
      label: '운영시간',
      value: removeHtml(operatingHours),
    },
    {
      key: 'fee',
      label: '요금',
      value: removeHtml(fee),
    },
  ].filter((item) => item.value)
})

const addressItem = computed(() => {
  return (
    infoItems.value.find(
      (item) => item.key === 'address',
    ) || null
  )
})

const otherItems = computed(() => {
  return infoItems.value.filter(
    (item) => item.key !== 'address',
  )
})

watch(
  () => [
    props.place?.contentId,
    props.place?.contentTypeId,
  ],
  loadTourismInfo,
  {
    immediate: true,
  },
)
</script>