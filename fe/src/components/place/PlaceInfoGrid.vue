<template>
  <div class="space-y-4">
    <!-- 주소: 항상 전체 폭 -->
    <div
      v-if="addressItem"
      class="rounded-2xl border border-[var(--color-border)] bg-white p-6 shadow-sm"
    >
      <h3 class="text-sm font-semibold text-[var(--color-text-muted)]">
        {{ addressItem.label }}
      </h3>
      <p class="mt-3 whitespace-pre-line break-words text-base font-medium text-[var(--color-text)]">
        {{ addressItem.value }}
      </p>
    </div>

    <!-- 나머지 정보 -->
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
            (otherItems.length % 2 === 1 && index === otherItems.length - 1),
        }"
      >
        <h3 class="text-sm font-semibold text-[var(--color-text-muted)]">
          {{ item.label }}
        </h3>
        <p class="mt-3 whitespace-pre-line break-words text-base font-medium text-[var(--color-text)]">
          {{ item.value }}
        </p>
      </div>
    </div>
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

const removeHtml = (value) => {
  if (!value) return ''

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
    return
  }

  try {
    tourismInfo.value = await getTourismCommon(
      props.place.contentId,
      props.place.contentTypeId,
    )
  } catch (error) {
    console.error('관광 상세 정보 조회 실패:', error)
    tourismInfo.value = {}
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
  return infoItems.value.find((item) => item.key === 'address') || null
})

const otherItems = computed(() => {
  return infoItems.value.filter((item) => item.key !== 'address')
})

watch(
  () => [props.place?.contentId, props.place?.contentTypeId],
  loadTourismInfo,
  { immediate: true },
)
</script>