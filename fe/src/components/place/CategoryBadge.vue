<template>
  <span
    :class="[
      'inline-block whitespace-nowrap rounded-full px-3 py-1 text-sm font-medium',
      getCategoryStyle(category)
    ]"
  >
    {{ category }}
  </span>
</template>

<script setup>
defineProps({
  category: {
    type: String,
    required: true
  }
})

const categoryStyles = {
  '관광지': 'bg-green-700 text-white',
  '문화시설': 'bg-teal-600 text-white',
  '축제·행사': 'bg-purple-600 text-white',
  '여행 코스': 'bg-blue-600 text-white',
  '레포츠': 'bg-orange-500 text-white',
  '숙박': 'bg-pink-500 text-white',
  '쇼핑': 'bg-amber-500 text-gray-900'
}

const getCategoryStyle = (category) => {
  return categoryStyles[category] || 'bg-gray-300 text-gray-700'
}
</script>