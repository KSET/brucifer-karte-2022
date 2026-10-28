<template>
    <div class="bw-page-container tlocrt-page bw-overlay-footer bw-textured">
        <img class="bw-ray tlocrt-ray tlocrt-ray--tl" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray tlocrt-ray tlocrt-ray--tr" :src="rayYellow" alt="" aria-hidden="true" />

        <BwBackButton />

        <section class="tlocrt">
            <div class="tlocrt-head">
                <h1 class="bw-section-title">Tlocrt</h1>
                <h4 class="bw-section-subtitle">Brucifer <strong>2026.</strong></h4>
            </div>

            <div ref="mapEl" class="tlocrt-map" aria-label="Location map"></div>

            <img class="tlocrt-main" :src="tlocrt" alt="Brucifer tlocrt" />

            <div class="tlocrt-venues">
                <img v-for="venue in venues" :key="venue.alt" :src="venue.src" :alt="venue.alt" />
            </div>
        </section>

        <Footer></Footer>
    </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwBackButton from '@/components/BruciWeb/BwBackButton.vue'
import tlocrt from '@/assets/tlocrt/tlocrt.svg'
import scMenzaKino from '@/assets/tlocrt/sc-menza-kino.svg'
import galerijaSc from '@/assets/tlocrt/galerija-sc.svg'
import mmCentar from '@/assets/tlocrt/mm-centar.svg'
import teatarTd from '@/assets/tlocrt/teatar-td.svg'
import rayPurple from '@/assets/design-elements/zraka-ljubicasta.webp'
import rayYellow from '@/assets/design-elements/zraka-zuta.webp'

import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// the site outline in tlocrt.svg is placed over the SC block on the map
const OVERLAY_BOUNDS = [
    [45.802764, 15.965103],
    [45.80507, 15.96972],
]

export default {
    name: 'TlocrtView',
    components: { Footer, BwBackButton },

    data() {
        return {
            tlocrt,
            venues: [
                { src: scMenzaKino, alt: 'SC menza i kino' },
                { src: galerijaSc, alt: 'Galerija SC' },
                { src: teatarTd, alt: 'Teatar & TD' },
                { src: mmCentar, alt: 'MM centar' },
            ],
            rayPurple,
            rayYellow,
            map: null,
        }
    },

    mounted() {
        this.$nextTick(() => {
            this.map = L.map(this.$refs.mapEl, {
                scrollWheelZoom: false,
                zoomControl: true,
            })

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; OpenStreetMap contributors',
            }).addTo(this.map)

            this.map.getPane('tilePane').style.filter = 'brightness(0.45) contrast(1.55)'

            // Center and bounds (SC area), clamped so users don't drag too far
            const scBounds = L.latLng(45.804, 15.9673).toBounds(1000)
            const clamped = scBounds.pad(0.15)
            this.map.fitBounds(scBounds, { padding: [30, 30] })
            this.map.setMaxBounds(clamped)
            this.map.setMinZoom(this.map.getBoundsZoom(clamped, true))

            L.imageOverlay(this.tlocrt, L.latLngBounds(OVERLAY_BOUNDS), {
                opacity: 1,
                interactive: false,
            }).addTo(this.map)

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
    },
}
</script>

<style scoped>
.tlocrt-page {
    justify-content: flex-start;
    background-image: none;
}

.tlocrt-ray {
    width: 30vw;
    top: -12vw;
    -webkit-mask-image: radial-gradient(circle at 0% 0%, #000 40%, transparent 74%);
    mask-image: radial-gradient(circle at 0% 0%, #000 40%, transparent 74%);
}

.tlocrt-ray--tl {
    left: -11vw;
}

.tlocrt-ray--tr {
    right: -11vw;
    -webkit-mask-image: radial-gradient(circle at 100% 0%, #000 40%, transparent 74%);
    mask-image: radial-gradient(circle at 100% 0%, #000 40%, transparent 74%);
}

.tlocrt {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(24px, 4vw, 56px);
    width: 100%;
    padding: clamp(88px, 11vw, 132px) 4vw calc(4vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
}

.tlocrt-head {
    text-align: center;
}

.tlocrt-head strong {
    font-weight: 800;
}

.tlocrt-main {
    display: block;
    width: 100%;
    max-width: 960px;
}

.tlocrt-venues {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 2vw;
    width: 100%;
}

.tlocrt-venues img {
    display: block;
    width: 100%;
}

.tlocrt-map {
    width: 100%;
    height: 60vh;
    border-radius: 12px;
    overflow: hidden;
}

@media screen and (max-width: 980px) {
    .tlocrt {
        padding: clamp(88px, 11vw, 132px) 6vw calc(6vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
    }

    .tlocrt-ray {
        width: 52vw;
        top: -18vw;
    }

    .tlocrt-ray--tl {
        left: -17vw;
    }

    .tlocrt-ray--tr {
        right: -17vw;
    }

    .tlocrt-venues {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 4vw;
    }
}

@media screen and (max-width: 550px) {
    .tlocrt {
        padding: clamp(88px, 11vw, 132px) 6vw calc(8vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
    }

    .tlocrt-ray {
        width: 68vw;
        top: -24vw;
    }

    .tlocrt-ray--tl {
        left: -22vw;
    }

    .tlocrt-ray--tr {
        right: -22vw;
    }

    .tlocrt-venues {
        grid-template-columns: 1fr;
    }

    .tlocrt-map {
        height: 50vh;
    }
}
</style>
