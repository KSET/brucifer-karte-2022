<template>
  <div class="bw-page-container">
    <div class="tlocrt">
      <div class="map-wrapper">
        <div ref="mapEl" class="map-container" aria-label="Location map"></div>
      </div>
      <div class="image">
        <img class="tlocrt-desktop" src="../../assets/tlocrt/tlocrt-desktop.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-tablet" src="../../assets/tlocrt/tlocrt-tablet.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-mobile" src="../../assets/tlocrt/tlocrt-mobile.svg" alt="Brucifer Tlocrt" />
        <div class="tlocrt-grid">
          <img class="tlocrt-desktop" src="../../assets/tlocrt/menza-desktop.svg" alt="Brucifer Tlocrt" />
          <img class="tlocrt-desktop" src="../../assets/tlocrt/galerija-desktop.svg" alt="Brucifer Tlocrt" />
          <img class="tlocrt-desktop" src="../../assets/tlocrt/mm-desktop.svg" alt="Brucifer Tlocrt" />
          <img class="tlocrt-desktop" src="../../assets/tlocrt/teatar-desktop.svg" alt="Brucifer Tlocrt" />
        </div>
        <img class="tlocrt-tablet" src="../../assets/tlocrt/menza-desktop.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-tablet" src="../../assets/tlocrt/galerija-desktop.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-tablet" src="../../assets/tlocrt/mm-desktop.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-tablet" src="../../assets/tlocrt/teatar-desktop.svg" alt="Brucifer Tlocrt" />

        <img class="tlocrt-mobile" src="../../assets/tlocrt/menza-desktop.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-mobile" src="../../assets/tlocrt/galerija-desktop.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-mobile" src="../../assets/tlocrt/mm-desktop.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-mobile" src="../../assets/tlocrt/teatar-desktop.svg" alt="Brucifer Tlocrt" />
      </div>

    </div>
    <Footer></Footer>

  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import NavbarBweb from '@/components/NavbarAndFooter/NavbarBweb.vue'

import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  name: 'Naslovnica',
  components: { Footer, NavbarBweb },
  data() {
    return {
      map: null,
      params: {
        zoom: 0,
        center: { lat: 0, lng: 0 },
        bounds: { sw: { lat: 0, lng: 0 }, ne: { lat: 0, lng: 0 } }
      }
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
      L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution:
          '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, © OpenMapTiles, © OpenStreetMap contributors'
      }).addTo(this.map)




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
        // if using Vite/Webpack with file-loader, require() keeps bundling intact
        require('@/assets/tlocrt/tlocrt-desktop.svg'),
        overlayBounds,
        { opacity: 1, interactive: false }
      ).addTo(this.map)

      // Keep the “Parameters” panel in sync
      const updateParams = () => {
        const c = this.map.getCenter()
        const b = this.map.getBounds()
        this.params.zoom = this.map.getZoom()
        this.params.center = { lat: c.lat, lng: c.lng }
        this.params.bounds = {
          sw: { lat: b.getSouthWest().lat, lng: b.getSouthWest().lng },
          ne: { lat: b.getNorthEast().lat, lng: b.getNorthEast().lng }
        }
      }
      this.map.on('moveend zoomend', updateParams)
      updateParams()

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

.params {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.4;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.tlocrt {
  width: 100%;
  min-height: 93vh;
  padding-top: 3rem;
}

.tlocrt-desktop {
  width: 100%;
  height: 100%;
  display: block;
}

.tlocrt-tablet {
  display: none !important;
}

.tlocrt-mobile {
  display: none !important;
}

.image {
  width: 100%;
  height: 100%;
}

.navbar.bw {
  background: var(--bw-navbar-color);
}

.navbar.bw::after {
  background: var(--bw-navbar-color);
}

.tlocrt-grid {
  display: grid;
  grid-template-columns: 25% 25% 25% 25%;
}

@media screen and (max-width: 980px) {
  .tlocrt-desktop {
    display: none !important;
  }

  .tlocrt-tablet {
    height: 100%;
    display: block !important;
  }

  .tlocrt-mobile {
    display: none !important;
  }
}

@media screen and (max-width: 550px) {
  .tlocrt-desktop {
    display: none !important;
  }

  .tlocrt-tablet {
    display: none !important;
  }

  .tlocrt-mobile {
    height: 100%;
    display: block !important;
  }

}

@import url(../../bruciweb.css);
</style>
