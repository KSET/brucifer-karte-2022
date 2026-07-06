<template>
  <div class="bw-page-container">
    <div class="tlocrt">
      <div class="map-wrapper">
        <div ref="mapEl" class="map-container" aria-label="Location map"></div>
      </div>
      <div class="image">
        <BwResponsiveImage :desktop-src="tlocrtDesktop" :tablet-src="tlocrtTablet" :mobile-src="tlocrtMobile"
          alt="Brucifer Tlocrt" />
        <div class="tlocrt-grid">
          <img src="../../assets/tlocrt/menza-desktop.svg" alt="Brucifer Tlocrt" />
          <img src="../../assets/tlocrt/galerija-desktop.svg" alt="Brucifer Tlocrt" />
          <img src="../../assets/tlocrt/mm-desktop.svg" alt="Brucifer Tlocrt" />
          <img src="../../assets/tlocrt/teatar-desktop.svg" alt="Brucifer Tlocrt" />
        </div>
      </div>

    </div>
    <Footer></Footer>

  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwResponsiveImage from '@/components/BruciWeb/BwResponsiveImage.vue'
import tlocrtDesktop from '@/assets/tlocrt/tlocrt-desktop.svg'
import tlocrtTablet from '@/assets/tlocrt/tlocrt-tablet.svg'
import tlocrtMobile from '@/assets/tlocrt/tlocrt-mobile.svg'

import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'TlocrtView',
  components: { Footer, BwResponsiveImage },
  data() {
    return {
      tlocrtDesktop,
      tlocrtTablet,
      tlocrtMobile,
      map: null
    }
  },
  mounted() {
    this.$nextTick(() => {
      // --- Basic map ---
      this.map = L.map(this.$refs.mapEl, {
        scrollWheelZoom: false,
        zoomControl: true
      })

      // Base tiles
      // Simple, no-labels basemap
      // Base dark-gray layer:
      const base = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(this.map)

      this.map.getPane('tilePane').style.filter = 'brightness(0.45) contrast(1.55)'



      // Center and bounds (SC area)
      const scCenter = L.latLng(45.804, 15.9673)
      const scBounds = scCenter.toBounds(1000) // ~1km box

      // Fit to area and clamp a bit so users don't drag too far
      const clamped = scBounds.pad(0.15)
      this.map.fitBounds(scBounds, { padding: [30, 30] })
      this.map.setMaxBounds(clamped)
      const minZoom = this.map.getBoundsZoom(clamped, true)
      this.map.setMinZoom(minZoom)

      // --- SVG overlay (tlocrt) ---
      const overlayBounds = L.latLngBounds(
        [45.8027, 15.9647],
        [45.8053, 15.9699]
      )
      L.imageOverlay(
        this.tlocrtDesktop,
        overlayBounds,
        { opacity: 1, interactive: false }
      ).addTo(this.map)

      // Final size fix in case container animates in
      setTimeout(() => this.map && this.map.invalidateSize(), 150)
    })
  },
  beforeUnmount() {
    if (this.map) {
      this.map.off()
      this.map.remove()
      this.map = null
    }
  }
}
</script>

<style scoped>
.map-wrapper {
  position: relative;
}

.map-container {
  width: 100%;
  height: 60vh;
  border-radius: 12px;
  overflow: hidden;
}

.tlocrt {
  width: 100%;
  min-height: 93vh;
  padding-top: 3rem;
}

.image {
  width: 100%;
  height: 100%;
}

.tlocrt-grid {
  display: grid;
  grid-template-columns: 25% 25% 25% 25%;
}

.tlocrt-grid img {
  width: 100%;
  display: block;
}

@media screen and (max-width: 980px) {
  .tlocrt-grid {
    grid-template-columns: 100%;
  }
}
</style>
