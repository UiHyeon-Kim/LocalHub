<template>
  <div class="relative w-full overflow-hidden rounded-2xl border border-[var(--color-border)]">
    <div ref="mapContainer" class="w-full" :style="{ height: mapHeight }"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  places: {
    type: Array,
    default: () => []
  },
  selectedPlaceId: {
    type: [String, Number],
    default: null
  },
  center: {
    type: Array,
    default: () => [36.1088, 128.4136] // 구미 중심
  },
  zoom: {
    type: Number,
    default: 13
  },
  interactive: {
    type: Boolean,
    default: true
  },
  mapHeight: {
    type: String,
    default: '480px'
  }
})

const emit = defineEmits(['select-place'])

const mapContainer = ref(null)
let map = null
let markerLayer = null
let markers = {}

const createMap = () => {
  if (!mapContainer.value) return

  map = L.map(mapContainer.value).setView(props.center, props.zoom)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map)

  markerLayer = L.layerGroup().addTo(map)
  updateMarkers()
}

const isValidCoordinate = (place) => {
  return (
    place &&
    typeof place.latitude === 'number' &&
    typeof place.longitude === 'number' &&
    !isNaN(place.latitude) &&
    !isNaN(place.longitude)
  )
}

const createMarkerIcon = (isSelected = false) => {
  const bgColor = isSelected ? '#0f4c3a' : '#007c78'
  const html = `
    <div style="
      width: 32px;
      height: 40px;
      background-color: ${bgColor};
      border: 2px solid white;
      border-radius: 50% 50% 50% 0;
      position: relative;
      transform: rotate(-45deg);
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    ">
      <div style="
        width: 10px;
        height: 10px;
        background-color: white;
        border-radius: 50%;
        position: absolute;
        top: 6px;
        left: 11px;
      "></div>
    </div>
  `

  return L.divIcon({
    html,
    iconSize: [32, 40],
    iconAnchor: [16, 40],
    popupAnchor: [0, -40],
    className: ''
  })
}

const createPopupContent = (place) => {
  const div = L.DomUtil.create('div')
  div.innerHTML = `
    <div style="padding: 4px; font-size: 12px;">
      <div style="font-weight: bold; font-size: 14px; margin-bottom: 4px;">${escapeHtml(place.name)}</div>
      <div style="color: #666; margin-bottom: 4px;">${escapeHtml(place.category)}</div>
      <div style="color: #999; font-size: 11px; word-wrap: break-word; max-width: 200px;">${escapeHtml(place.address || '')}</div>
    </div>
  `
  return div
}

const escapeHtml = (text) => {
  if (!text) return ''
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

const updateMarkers = () => {
  if (!map || !markerLayer) return

  markerLayer.clearLayers()
  markers = {}

  const validPlaces = props.places.filter(isValidCoordinate)

  validPlaces.forEach((place) => {
    const isSelected = String(place.id) === String(props.selectedPlaceId)
    const marker = L.marker(
      [place.latitude, place.longitude],
      { icon: createMarkerIcon(isSelected) }
    )

    const popupContent = createPopupContent(place)
    marker.bindPopup(popupContent)

    marker.on('click', () => {
      emit('select-place', place.id)
    })

    markerLayer.addLayer(marker)
    markers[place.id] = marker
  })

  if (validPlaces.length === 0) {
    map.setView(props.center, props.zoom)
  } else if (validPlaces.length === 1) {
    const place = validPlaces[0]
    map.setView([place.latitude, place.longitude], 15)
  } else {
    const group = new L.featureGroup(
      validPlaces.map((p) => L.marker([p.latitude, p.longitude]))
    )
    map.fitBounds(group.getBounds(), { padding: [50, 50], maxZoom: 16 })
  }
}

const handleSelectedPlaceChange = async () => {
  if (!props.selectedPlaceId || !markers[props.selectedPlaceId] || !map) return

  const place = props.places.find((p) => p.id === props.selectedPlaceId)
  if (!isValidCoordinate(place)) return

  updateMarkers()
  await nextTick()
  map.flyTo([place.latitude, place.longitude], 15, { duration: 1 })
}

watch(() => props.places, updateMarkers, { deep: true })
watch(() => props.selectedPlaceId, handleSelectedPlaceChange)

onMounted(async () => {
  await nextTick()
  createMap()
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
    markerLayer = null
    markers = {}
  }
})
</script>

<style scoped>
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

:deep(.leaflet-popup-tip) {
  background-color: white;
}

:deep(.leaflet-control-attribution) {
  background-color: rgba(255, 255, 255, 0.8);
  font-size: 11px;
}
</style>