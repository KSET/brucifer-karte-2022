<template>
    <section class="bw-gallery" v-if="photos.length"
        :style="{ '--bw-gallery-bg-image': `url(${galleryBg})`, '--bw-gallery-grain': `url(${texture})` }">
        <div class="bw-gallery-bg" aria-hidden="true"></div>

        <div class="bw-gallery-tilt">
            <div class="bw-gallery-marquee-wrapper">
                <div class="bw-gallery-marquee-track bw-gallery-marquee-left">
                    <div class="bw-gallery-marquee-group">
                        <img v-for="(photo, i) in row1" :key="`r1a-${i}`" :src="photo.src" :alt="photo.alt"
                            class="bw-gallery-marquee-image" :style="{ aspectRatio: photo.ratio }" :width="photo.width"
                            :height="photo.height" decoding="async" />
                    </div>
                    <div class="bw-gallery-marquee-group" aria-hidden="true">
                        <img v-for="(photo, i) in row1" :key="`r1b-${i}`" :src="photo.src" alt=""
                            class="bw-gallery-marquee-image" :style="{ aspectRatio: photo.ratio }" :width="photo.width"
                            :height="photo.height" decoding="async" />
                    </div>
                </div>
            </div>

            <div class="bw-gallery-marquee-wrapper">
                <div class="bw-gallery-marquee-track bw-gallery-marquee-right">
                    <div class="bw-gallery-marquee-group">
                        <img v-for="(photo, i) in row2" :key="`r2a-${i}`" :src="photo.src" :alt="photo.alt"
                            class="bw-gallery-marquee-image" :style="{ aspectRatio: photo.ratio }" :width="photo.width"
                            :height="photo.height" decoding="async" />
                    </div>
                    <div class="bw-gallery-marquee-group" aria-hidden="true">
                        <img v-for="(photo, i) in row2" :key="`r2b-${i}`" :src="photo.src" alt=""
                            class="bw-gallery-marquee-image" :style="{ aspectRatio: photo.ratio }" :width="photo.width"
                            :height="photo.height" decoding="async" />
                    </div>
                </div>
            </div>

            <div class="bw-gallery-marquee-wrapper bw-gallery-marquee-wrapper--mobile">
                <div class="bw-gallery-marquee-track bw-gallery-marquee-left bw-gallery-marquee-slow">
                    <div class="bw-gallery-marquee-group">
                        <img v-for="(photo, i) in row3" :key="`r3a-${i}`" :src="photo.src" :alt="photo.alt"
                            class="bw-gallery-marquee-image" :style="{ aspectRatio: photo.ratio }" :width="photo.width"
                            :height="photo.height" decoding="async" />
                    </div>
                    <div class="bw-gallery-marquee-group" aria-hidden="true">
                        <img v-for="(photo, i) in row3" :key="`r3b-${i}`" :src="photo.src" alt=""
                            class="bw-gallery-marquee-image" :style="{ aspectRatio: photo.ratio }" :width="photo.width"
                            :height="photo.height" decoding="async" />
                    </div>
                </div>
            </div>
        </div>

        <img :src="znak" alt="" aria-hidden="true" class="bw-gallery-znak" />
        <img :src="strelica" alt="" aria-hidden="true" class="bw-gallery-strelica" />
    </section>
</template>

<script>
import galleryBg from '@/assets/design-elements/gallery-background.webp'
import texture from '@/assets/design-elements/tekstura.png'
import znak from '@/assets/design-elements/galerija-znak.svg'
import strelica from '@/assets/design-elements/galerija-strelica.svg'

const context = require.context('@/assets/galerija', false, /^\.\/[^/]+\.webp$/)

const DIMENSIONS = {
    '20251108_brucosijada_ignor_d_ela_kumer_2.webp': [1600, 900],
    '20251108_brucosijada_ignor_d_ela_kumer_7.webp': [1600, 1000],
    '20251108_brucosijada_repetitor_d_katarina_pesic_13.webp': [1600, 2240],
    '20251108_brucosijada_repetitor_d_katarina_pesic_18.webp': [1600, 1067],
    '20251108_brucosijada_rtificial_red_d_Barbara_Kralj_09.webp': [1600, 1067],
    '20251108_brucosijada_svemirko_d_ana_madunic_01.webp': [1600, 2401],
    '20251108_brucosijada_zevin_d_paula_fanton_01.webp': [1600, 1171],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_08.webp': [1600, 1237],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_09.webp': [1600, 1067],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_14.webp': [1600, 900],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_41.webp': [1600, 1280],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_45.webp': [1600, 1067],
    '20251108_d_d_ana_marija_devcic_12.webp': [1600, 1067],
}

const DEFAULT_DIMENSIONS = [1600, 1067]

const photos = context.keys()
    .sort((a, b) => a.localeCompare(b, 'en', { numeric: true }))
    .map((key, index) => {
        const [width, height] = DIMENSIONS[key.replace('./', '')] || DEFAULT_DIMENSIONS

        return {
            src: context(key),
            alt: `Brucifer fotografija ${index + 1}`,
            width,
            height,
            ratio: `${width} / ${height}`,
        }
    })

const ROWS = 3
const rowLength = photos.length ? Math.ceil(photos.length / ROWS) : 0

const buildRow = (row) => Array.from(
    { length: rowLength },
    (unused, i) => photos[(row * rowLength + i) % photos.length],
)

export default {
    name: 'BwGallery',

    data() {
        return {
            galleryBg,
            texture,
            znak,
            strelica,
            photos,
            row1: buildRow(0),
            row2: buildRow(1),
            row3: buildRow(2),
        }
    },
}
</script>

<style scoped>
.bw-gallery {
    position: relative;
    overflow: hidden;
    box-sizing: border-box;
    height: 100vh;
    height: 100svh;
    --bw-gallery-gap: 20px;
    --bw-gallery-padding: 70px;
    --bw-gallery-tilt-height: calc((100vh - var(--bw-gallery-padding) * 2) * 1.0625);
}

@supports (height: 100svh) {
    .bw-gallery {
        --bw-gallery-tilt-height: calc((100svh - var(--bw-gallery-padding) * 2) * 1.0625);
    }
}

.bw-gallery-tilt {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 120%;
    height: var(--bw-gallery-tilt-height);
    display: flex;
    flex-direction: column;
    gap: var(--bw-gallery-gap);
    transform: translate(-50%, -50%) rotate(-4deg);
    transform-origin: center;
}

.bw-gallery-marquee-wrapper {
    position: relative;
    z-index: 1;
    display: flex;
    flex: 1 1 0;
    min-height: 0;
    width: 100%;
    overflow: hidden;
}

.bw-gallery-marquee-wrapper--mobile {
    display: none;
}

.bw-gallery-bg {
    position: absolute;
    inset: 0;
    background-image: var(--bw-gallery-bg-image);
    background-size: cover;
    background-position: center;
    pointer-events: none;
}

.bw-gallery-bg::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image: var(--bw-gallery-grain);
    background-size: cover;
    background-position: center;
    opacity: 0.18;
    mix-blend-mode: overlay;
}

.bw-gallery-marquee-track {
    display: flex;
    width: max-content;
    height: 100%;
    flex: 0 0 auto;
    will-change: transform;
    animation: bw-gallery-scroll 40s linear infinite;
}

.bw-gallery-marquee-group {
    display: flex;
    gap: var(--bw-gallery-gap);
    padding-right: var(--bw-gallery-gap);
    height: 100%;
    flex: 0 0 auto;
}

.bw-gallery-marquee-left {
    align-items: flex-end;
}

.bw-gallery-marquee-right {
    align-items: flex-start;
    animation-direction: reverse;
}

.bw-gallery-marquee-slow {
    animation-duration: 52s;
}

.bw-gallery-marquee-image {
    height: 100%;
    width: auto;
    flex-shrink: 0;
}

.bw-gallery-znak,
.bw-gallery-strelica {
    position: absolute;
    pointer-events: none;
    user-select: none;
}

.bw-gallery-znak {
    z-index: 2;
    top: 3vh;
    left: 4%;
    width: clamp(80px, 9vw, 160px);
    height: auto;
    transform: rotate(-8deg);
}

.bw-gallery-strelica {
    z-index: 0;
    right: 0;
    bottom: 3vh;
    width: clamp(140px, 18vw, 320px);
    height: auto;
}

@keyframes bw-gallery-scroll {
    from {
        transform: translateX(0);
    }

    to {
        transform: translateX(-50%);
    }
}

@media (prefers-reduced-motion: reduce) {
    .bw-gallery-marquee-track {
        animation: none;
        width: 100%;
        will-change: auto;
    }

    .bw-gallery-marquee-group {
        width: 100%;
        overflow: hidden;
    }

    .bw-gallery-marquee-group[aria-hidden="true"] {
        display: none;
    }
}

@media screen and (min-width: 981px) {
    .bw-gallery {
        --bw-gallery-gap: 28px;
    }
}

@media screen and (max-width: 980px) {
    .bw-gallery-znak {
        width: clamp(56px, 16vw, 90px);
    }

    .bw-gallery-strelica {
        width: clamp(100px, 34vw, 180px);
    }
}

@media screen and (max-width: 550px) {
    .bw-gallery {
        --bw-gallery-tilt-height: calc(100vh - var(--bw-gallery-padding) * 2);
    }

    .bw-gallery-tilt {
        width: 100%;
        box-sizing: border-box;
        transform: translate(-50%, -50%);
    }

    .bw-gallery-marquee-wrapper--mobile {
        display: flex;
    }

    .bw-gallery-marquee-left,
    .bw-gallery-marquee-right {
        align-items: stretch;
    }
}

@supports (height: 100svh) {
    @media screen and (max-width: 550px) {
        .bw-gallery {
            --bw-gallery-tilt-height: calc(100svh - var(--bw-gallery-padding) * 2);
        }
    }
}
</style>
