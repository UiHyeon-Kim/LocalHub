<template>
  <div>
    <!-- Hero Section -->
    <HeroSection />

    <!-- Category Section -->
    <div class="page-section">
      <CategorySection />
    </div>

    <!-- Featured Places Section -->
    <FeaturedPlacesSection />

    <!-- Mood Section -->
    <div class="page-section">
      <MoodSection />
    </div>

    <!-- Community Preview Section -->
    <CommunityPreviewSection />

    <!-- Region Banner Section -->
    <RegionBannerSection />
  </div>
</template>

<script setup>
import HeroSection from '@/components/home/HeroSection.vue'
import CategorySection from '@/components/home/CategorySection.vue'
import FeaturedPlacesSection from '@/components/home/FeaturedPlacesSection.vue'
import MoodSection from '@/components/home/MoodSection.vue'
import CommunityPreviewSection from '@/components/home/CommunityPreviewSection.vue'
import RegionBannerSection from '@/components/home/RegionBannerSection.vue'
</script>