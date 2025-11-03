<template>
  <div class="bw-page-container">
    <!-- Map section -->
    <div class="map-wrapper">
      <div ref="mapEl" class="map-container" aria-label="Location map"></div>
    </div>

    <!-- Your existing content -->
    <div class="tlocrt">
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

    <Footer />
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import NavbarBweb from '@/components/NavbarAndFooter/NavbarBweb.vue'

// Leaflet imports
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix marker icons in bundlers (Vite/Webpack)
// These imports ensure the default icon files are bundled correctly.
import marker2x from 'leaflet/dist/images/marker-icon-2x.png'
import marker1x from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

// Set default icon globally
const DefaultIcon = L.icon({
  iconRetinaUrl: marker2x,
  iconUrl: marker1x,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
})
L.Marker.prototype.options.icon = DefaultIcon

export default {
  name: 'Naslovnica',
  components: { Footer, NavbarBweb },
  props: { msg: String },
  data() {
    return {
      map: null
    }
  },
  // Leaflet setup stays the same … then inside mounted():
  mounted() {
    this.$nextTick(() => {
      // Initialize map
      this.map = L.map(this.$refs.mapEl, {
        scrollWheelZoom: false,
        zoomControl: true,
        zoomAnimation: false,
        markerZoomAnimation: false
      })

      // Base layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map)

      // SC center and bounds
      const scCenter = L.latLng(45.8035519, 15.9672823)
      let scBounds = scCenter.toBounds(1000)
      this.map.fitBounds(scBounds, { padding: [30, 30] })

      const clampedBounds = scBounds.pad(0.15)
      this.map.setMaxBounds(clampedBounds)
      this.map.options.maxBoundsViscosity = 1.0
      const minZoomForSC = this.map.getBoundsZoom(clampedBounds, true)
      this.map.setMinZoom(minZoomForSC)

      // Overlay image
      const scOverlayBounds = L.latLngBounds(
        [45.8027, 15.9647],
        [45.8053, 15.9699]
      )

      const tlocrtOverlay = L.imageOverlay(
        require('@/assets/tlocrt/tlocrt-desktop.svg'),
        scOverlayBounds,
        { opacity: 1, interactive: false }
      )
      tlocrtOverlay.addTo(this.map)

      // Optional guides
      L.rectangle(scBounds, { weight: 1, fillOpacity: 0.05 }).addTo(this.map)
      L.marker(scCenter).addTo(this.map).bindPopup('Studentski centar')

      // ---- Geolocation (robust) ----
      let userMarker = null
      let retryMs = 1500 // start small
      const retryMax = 60000

      const updateUserMarker = (latlng) => {
        if (!userMarker) {
          userMarker = L.marker(latlng, { icon: DefaultIcon, zIndexOffset: 1000 })
            .addTo(this.map)
            .bindPopup('Vaša lokacija')
        } else {
          userMarker.setLatLng(latlng)
        }
        this.map.panInsideBounds(clampedBounds, { animate: true })
      }

      const startLocate = () => {
        this.map.locate({
          setView: false,
          watch: false,              // one fix first
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 1000
        })
      }

      const scheduleRetry = () => {
        const delay = Math.min(retryMs, retryMax)
        console.warn(`Retrying geolocation in ${delay}ms…`)
        setTimeout(startLocate, delay)
        retryMs = Math.min(retryMs * 2, retryMax)
      }

      this.map.on('locationfound', (e) => {
        if (!clampedBounds.contains(e.latlng)) return
        updateUserMarker(e.latlng)

        // After first fix, switch to continuous watch
        this.map.stopLocate()
        this.map.locate({
          setView: false,
          watch: true,
          enableHighAccuracy: true,
          timeout: 20000,
          maximumAge: 2000
        })

        retryMs = 1500 // reset backoff after success
      })

      this.map.on('locationerror', (err) => {
        const code = err.code
        const msg = (err && err.message) || ''
        console.warn('Geolocation failed:', code, msg)

        // Show only once
        if (!this._geoToastShown) {
          this._geoToastShown = true
          alert(
            'Ne možemo trenutno odrediti lokaciju. Provjerite dozvole i pokušat ćemo ponovno.'
          )
        }

        if (code === 1) {
          // Permission denied: stop retries, offer manual
          console.warn('Permission denied — stopping retries.')
          addManualPinHelper()
          return
        }

        // Transient/timeout → retry
        scheduleRetry()
      })

      // Manual fallback
      const addManualPinHelper = () => {
        if (this._manualPinMsg) return
        this._manualPinMsg = true
        const onClick = (e) => {
          if (!clampedBounds.contains(e.latlng)) return
          updateUserMarker(e.latlng)
        }
        this.map.on('click', onClick)
        console.info('Manual pin mode enabled: click the map to set your location.')
      }

      // Kick off first locate
      startLocate()

      // Final resize correction
      setTimeout(() => this.map && this.map.invalidateSize(), 200)
    })
  }
  ,
  beforeUnmount() {
    if (this.map) {
      this.map.stopLocate()
      this.map.off()
      this.map.remove()
      this.map = null
    }
  }
  ,
}
</script>
