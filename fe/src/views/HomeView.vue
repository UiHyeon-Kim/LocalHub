<template>
  <div>
    <!-- Hero Section -->
    <HeroSection />

    <!-- Category Section -->
    <div class="page-section">
      <CategorySection />
    </div>

    <!-- Featured Places Section -->
    <FeaturedPlacesSection :places="places" />

    <!-- Mood Section -->
    <div class="page-section">
      <MoodSection />
    </div>

    <!-- Map Explorer Section (API로 받아온 places 전달) -->
    <MapExplorerSection :places="places" />

    <!-- Community Preview Section -->
    <CommunityPreviewSection />

    <!-- Region Banner Section -->
    <RegionBannerSection />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import HeroSection from '@/components/home/HeroSection.vue'
import CategorySection from '@/components/home/CategorySection.vue'
import FeaturedPlacesSection from '@/components/home/FeaturedPlacesSection.vue'
import MoodSection from '@/components/home/MoodSection.vue'
import MapExplorerSection from '@/components/home/MapExplorerSection.vue'
import CommunityPreviewSection from '@/components/home/CommunityPreviewSection.vue'
import RegionBannerSection from '@/components/home/RegionBannerSection.vue'
import { getPlaces } from '@/api/placeApi'

const places = ref([])
const loading = ref(false)
const error = ref('')

const loadPlaces = async () => {
  loading.value = true
  error.value = ''
  try {
    // 간단 조회: limit(=12) 등 필요하면 인자로 넘기세요
    const { items } = await getPlaces({ limit: 12, offset: 0 })
    places.value = items
  } catch (e) {
    error.value = e.message || '장소를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPlaces()
})
</script>