<template>
    <section class="bw-gallery" v-if="photos.length"
        :style="{ '--bw-gallery-bg-image': `url(${galleryBg})`, '--bw-gallery-grain': `url(${texture})` }">
        <div class="bw-gallery-bg" aria-hidden="true"></div>

        <div class="bw-gallery-tilt">
            <div class="bw-gallery-marquee-wrapper">
                <div class="bw-gallery-marquee-track bw-gallery-marquee-left">
                    <img v-for="(photo, i) in row1" :key="`r1a-${i}`" :src="photo.src" :alt="photo.alt"
                        class="bw-gallery-marquee-image" decoding="async" />
                </div>
                <div class="bw-gallery-marquee-track bw-gallery-marquee-left" aria-hidden="true">
                    <img v-for="(photo, i) in row1" :key="`r1b-${i}`" :src="photo.src" alt=""
                        class="bw-gallery-marquee-image" decoding="async" />
                </div>
            </div>

            <div class="bw-gallery-marquee-wrapper">
                <div class="bw-gallery-marquee-track bw-gallery-marquee-right">
                    <img v-for="(photo, i) in row2" :key="`r2a-${i}`" :src="photo.src" :alt="photo.alt"
                        class="bw-gallery-marquee-image" decoding="async" />
                </div>
                <div class="bw-gallery-marquee-track bw-gallery-marquee-right" aria-hidden="true">
                    <img v-for="(photo, i) in row2" :key="`r2b-${i}`" :src="photo.src" alt=""
                        class="bw-gallery-marquee-image" decoding="async" />
                </div>
            </div>

            <div class="bw-gallery-marquee-wrapper bw-gallery-marquee-wrapper--mobile">
                <div class="bw-gallery-marquee-track bw-gallery-marquee-left bw-gallery-marquee-slow">
                    <img v-for="(photo, i) in row3" :key="`r3a-${i}`" :src="photo.src" :alt="photo.alt"
                        class="bw-gallery-marquee-image" decoding="async" />
                </div>
                <div class="bw-gallery-marquee-track bw-gallery-marquee-left bw-gallery-marquee-slow" aria-hidden="true">
                    <img v-for="(photo, i) in row3" :key="`r3b-${i}`" :src="photo.src" alt=""
                        class="bw-gallery-marquee-image" decoding="async" />
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

const photos = context.keys()
    .sort((a, b) => a.localeCompare(b, 'en', { numeric: true }))
    .map((key, index) => ({
        src: context(key),
        alt: `Brucifer fotografija ${index + 1}`,
    }))

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
    height: 100vh;
    height: 100svh;
    --bw-gallery-gap: 20px;
}

.bw-gallery-tilt {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 120%;
    height: calc(100svh * 1.25);
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
    gap: var(--bw-gallery-gap);
    padding-right: var(--bw-gallery-gap);
    white-space: nowrap;
    width: max-content;
    height: 100%;
    flex: 0 0 auto;
}

.bw-gallery-marquee-left {
    align-items: flex-end;
    animation: bw-gallery-scroll-left 40s linear infinite;
}

.bw-gallery-marquee-right {
    align-items: flex-start;
    animation: bw-gallery-scroll-right 40s linear infinite;
}

.bw-gallery-marquee-slow {
    animation-duration: 52s;
}

.bw-gallery-marquee-image {
    height: 68%;
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

@keyframes bw-gallery-scroll-left {
    0% {
        transform: translateX(0);
    }

    100% {
        transform: translateX(-100%);
    }
}

@keyframes bw-gallery-scroll-right {
    0% {
        transform: translateX(-100%);
    }

    100% {
        transform: translateX(0);
    }
}

@media (prefers-reduced-motion: reduce) {

    .bw-gallery-marquee-left,
    .bw-gallery-marquee-right {
        animation: none;
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
    .bw-gallery-tilt {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        padding-block: var(--bw-gallery-gap);
        transform: translate(-50%, -50%);
    }

    .bw-gallery-marquee-wrapper--mobile {
        display: flex;
    }

    .bw-gallery-marquee-left,
    .bw-gallery-marquee-right {
        align-items: stretch;
    }

    .bw-gallery-marquee-image {
        height: 100%;
    }
}
</style>
