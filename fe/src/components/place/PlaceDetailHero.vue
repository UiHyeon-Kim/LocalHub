<template>
  <div class="relative w-full overflow-hidden rounded-2xl">
    <div
      class="h-[420px] w-full bg-gray-900"
      :style="place.imageUrl ? { backgroundImage: `url('${place.imageUrl}')`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}"
    >
      <div class="absolute inset-0 bg-gradient-to-b from-black/30 via-black/10 to-black/60"></div>

      <div class="relative z-10 flex h-full items-end p-8">
        <div class="max-w-3xl">
          <div class="mb-4 flex items-center gap-3">
            <span class="inline-flex items-center rounded-full bg-[var(--color-primary)] px-3 py-1 text-sm font-semibold text-white">
              {{ place.category }}
            </span>
            <span class="text-sm text-white/80">· {{ place.district || '' }}</span>
          </div>

          <h1 class="text-4xl font-extrabold leading-tight text-white">
            {{ place.name }}
          </h1>

          <p class="mt-3 max-w-2xl text-lg text-white/90">
            {{ place.shortDescription }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  place: { type: Object, required: true }
})
</script>