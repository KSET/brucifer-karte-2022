<template>
    <section id="sadrzaj" class="bw-sadrzaj bw-textured">
        <img class="bw-ray bw-sadrzaj-ray bw-sadrzaj-ray--tl" :src="rayBlue" alt="" aria-hidden="true" />
        <img class="bw-ray bw-sadrzaj-ray bw-sadrzaj-ray--tr" :src="rayYellow" alt="" aria-hidden="true" />
        <img class="bw-ray bw-sadrzaj-ray bw-sadrzaj-ray--ml" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray bw-sadrzaj-ray bw-sadrzaj-ray--bl" :src="rayYellow" alt="" aria-hidden="true" />
        <img class="bw-ray bw-sadrzaj-ray bw-sadrzaj-ray--br" :src="rayBlue" alt="" aria-hidden="true" />

        <div class="bw-sadrzaj-content">
            <div class="bw-sadrzaj-head">
                <h2 class="bw-section-title">Sadržaj</h2>
                <h4 class="bw-section-subtitle">Brucifer 2026.</h4>
            </div>

            <div class="bw-sadrzaj-strips">
                <div v-for="strip in strips" :key="strip.key" class="bw-sadrzaj-strip"
                    :style="{ '--bw-strip-color': strip.color, '--bw-strip-tag': strip.tagColor, '--bw-strip-tilt': strip.tilt }">
                    <div class="bw-sadrzaj-band">
                        <div class="bw-sadrzaj-track" :class="`bw-sadrzaj-track--${strip.direction}`">
                            <div class="bw-sadrzaj-group">
                                <img v-for="(photo, i) in strip.photos" :key="`${strip.key}a-${i}`" :src="photo.src"
                                    :alt="photo.alt" class="bw-sadrzaj-photo" :style="{ aspectRatio: photo.ratio }"
                                    :width="photo.width" :height="photo.height" decoding="async" />
                            </div>
                            <div class="bw-sadrzaj-group" aria-hidden="true">
                                <img v-for="(photo, i) in strip.photos" :key="`${strip.key}b-${i}`" :src="photo.src"
                                    alt="" class="bw-sadrzaj-photo" :style="{ aspectRatio: photo.ratio }"
                                    :width="photo.width" :height="photo.height" decoding="async" />
                            </div>
                        </div>
                    </div>

                    <div class="bw-sadrzaj-tags">
                        <span v-for="tag in strip.tags" :key="tag.label" class="bw-sadrzaj-tag"
                            :class="`bw-sadrzaj-tag--${tag.edge}`"
                            :style="{ '--bw-tag-x': tag.left, '--bw-tag-dir': tag.dir }">
                            {{ tag.label }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import rayPurple from '@/assets/design-elements/zraka-ljubicasta.webp'
import rayBlue from '@/assets/design-elements/zraka-plava.webp'
import rayYellow from '@/assets/design-elements/zraka-zuta.webp'

const DIMENSIONS = {
    '20251108_brucosijada_atmosfera_d_filip_trbara_02.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_filip_trbara_07.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_lucija_kostelac_05.webp': [751, 600],
    '20251108_brucosijada_atmosfera_d_marko_juric_01.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_marko_juric_08.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_marko_juric_11.webp': [901, 600],
    '20251108_brucosijada_votafak_d_filip_trbara_07.webp': [901, 600],
    '20251108_brucosijada_vrh_d_andro_anic_milic_04.webp': [600, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_17.webp': [600, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_48.webp': [901, 600],
    '20241110_brucosijada_atmosfera_d_paula_fanton_01.webp': [817, 600],
    '20241110_brucosijada_atmosfera_d_paula_fanton_02.webp': [901, 600],
    '20241110_brucosijada_atmosfera_d_paula_fanton_03.webp': [901, 600],
    '20241110_brucosijada_atmosfera_d_paula_fanton_04.webp': [901, 600],
    '20241110_brucosijada_atmosfera_d_paula_fanton_05.webp': [489, 600],
    '20241110_brucosijada_atmosfera_d_paula_fanton_06.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_lucija_kostelac_07.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_lucija_kostelac_10.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_lucija_kostelac_11.webp': [751, 600],
    '20251108_brucosijada_atmosfera_d_lucija_kostelac_19.webp': [751, 600],
    '20251108_brucosijada_atmosfera_d_lucija_kostelac_20.webp': [751, 600],
    '20251108_brucosijada_atmosfera_d_marko_juric_02.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_marko_juric_03.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_marko_juric_20.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_marko_juric_21.webp': [901, 600],
    '20251108_brucosijada_atmosfera_d_marko_juric_22.webp': [901, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_20.webp': [901, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_21.webp': [901, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_22.webp': [901, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_23.webp': [777, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_24.webp': [600, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_25.webp': [901, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_26.webp': [840, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_27.webp': [901, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_28.webp': [751, 600],
    '20251108_burcosijada_atmosfera_d_andro_anic_milic_29.webp': [777, 600],
}

const DEFAULT_DIMENSIONS = [901, 600]

const load = (context, alt) => context.keys()
    .sort((a, b) => a.localeCompare(b, 'en', { numeric: true }))
    .map((key, index) => {
        const [width, height] = DIMENSIONS[key.replace('./', '')] || DEFAULT_DIMENSIONS

        return {
            src: context(key),
            alt: `${alt} ${index + 1}`,
            width,
            height,
            ratio: `${width} / ${height}`,
        }
    })

const repeat = (photos, times) => Array.from({ length: times }, () => photos).flat()

const strips = [
    {
        key: 'atmosfera',
        photos: load(require.context('@/assets/sadrzaj/atmosfera', false, /\.webp$/), 'Atmosfera na Bruciferu'),
        color: '#8a3a92',
        tagColor: '#6a2a72',
        direction: 'left',
        tilt: '-1.5deg',
        tags: [
            { label: '3 pozornice', edge: 'top', left: '7%', dir: -1 },
            { label: '14 izvođača', edge: 'bottom', left: '78%', dir: 1 },
        ],
    },
    {
        key: 'silent-disco',
        photos: load(require.context('@/assets/sadrzaj/silent-disco', false, /\.webp$/), 'Silent disco'),
        color: 'var(--bw-teal)',
        tagColor: '#1d5f66',
        direction: 'right',
        tilt: '1deg',
        tags: [
            { label: 'Silent disco', edge: 'bottom', left: '10%', dir: -1 },
        ],
    },
    {
        key: 'votafak',
        photos: load(require.context('@/assets/sadrzaj/votafak', false, /\.webp$/), 'Votafak'),
        color: '#d6cf2c',
        tagColor: '#cfa936',
        direction: 'left',
        tilt: '-1deg',
        tags: [
            { label: 'Votafak', edge: 'top', left: '72%', dir: 1 },
        ],
    },
    {
        key: 'brucistar',
        // Only 6 photos, so repeat them to keep one group wider than the screen
        photos: repeat(load(require.context('@/assets/sadrzaj/brucistar', false, /\.webp$/), 'Brucistar'), 2),
        color: '#2fb6c4',
        tagColor: 'var(--bw-teal-ink)',
        direction: 'right',
        tilt: '1deg',
        tags: [
            { label: 'Brucistar', edge: 'top', left: '66%', dir: -1 },
            { label: 'Kino', edge: 'bottom', left: '84%', dir: -1 },
        ],
    },
]

export default {
    name: 'BwSadrzaj',

    data() {
        return {
            rayPurple,
            rayBlue,
            rayYellow,
            strips,
        }
    },
}
</script>

<style scoped>
.bw-sadrzaj {
    padding: 6vw 0 8vw;
    --bw-sadrzaj-photo-h: clamp(110px, 13vw, 220px);
    --bw-sadrzaj-gap: clamp(12px, 1.4vw, 24px);
}

.bw-sadrzaj-ray {
    width: 26vw;
}

.bw-sadrzaj-ray--tl {
    top: 4vw;
    left: 2vw;
}

.bw-sadrzaj-ray--tr {
    top: -2vw;
    right: 8vw;
}

.bw-sadrzaj-ray--ml {
    top: 42%;
    left: 14vw;
    width: 20vw;
}

.bw-sadrzaj-ray--bl {
    bottom: 14%;
    left: 10vw;
    width: 18vw;
}

.bw-sadrzaj-ray--br {
    bottom: 12%;
    right: 20vw;
    width: 20vw;
}

.bw-sadrzaj-content {
    position: relative;
    z-index: 1;
}

.bw-sadrzaj-head {
    text-align: center;
    padding: 0 4vw;
}

.bw-sadrzaj-strips {
    display: flex;
    flex-direction: column;
    gap: clamp(48px, 6vw, 96px);
    padding-top: clamp(48px, 6vw, 96px);
}

.bw-sadrzaj-strip {
    position: relative;
    width: 106%;
    margin-left: -3%;
    transform: rotate(var(--bw-strip-tilt));
}

.bw-sadrzaj-band {
    overflow: hidden;
    padding: var(--bw-sadrzaj-gap) 0;
    background-color: var(--bw-strip-color);
}

.bw-sadrzaj-track {
    display: flex;
    width: max-content;
    will-change: transform;
    animation: bw-sadrzaj-scroll 60s linear infinite;
}

.bw-sadrzaj-track--right {
    animation-direction: reverse;
}

.bw-sadrzaj-group {
    display: flex;
    gap: var(--bw-sadrzaj-gap);
    padding-right: var(--bw-sadrzaj-gap);
    flex: 0 0 auto;
}

.bw-sadrzaj-photo {
    display: block;
    height: var(--bw-sadrzaj-photo-h);
    width: auto;
    flex-shrink: 0;
    background-color: var(--bw-ink);
}

/* Strip is 106% wide, so the visible viewport starts ~2.83% in on each side */
.bw-sadrzaj-tags {
    position: absolute;
    z-index: 2;
    top: 0;
    bottom: 0;
    left: calc(2.83% + 24px);
    right: calc(2.83% + 24px);
    pointer-events: none;
}

/* Shifting by the same % of its own width keeps the tag inside the viewport at any x */
.bw-sadrzaj-tag {
    position: absolute;
    left: var(--bw-tag-x);
    --bw-tag-angle: 7.72deg;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    box-sizing: border-box;
    height: 51px;
    padding: 16px 24px;
    border: 2px solid white;
    border-radius: 8px;
    background-color: var(--bw-strip-tag);
    box-shadow: 0 0 0 10px var(--bw-strip-tag);
    color: white;
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 600;
    font-size: 24px;
    text-align: center;
    line-height: 1;
    text-transform: uppercase;
    white-space: nowrap;
    pointer-events: none;
    user-select: none;
}

.bw-sadrzaj-tag--top {
    top: 0;
    transform: translate(calc(var(--bw-tag-x) * -1), -60%) rotate(calc(var(--bw-tag-angle) * var(--bw-tag-dir)));
}

.bw-sadrzaj-tag--bottom {
    bottom: 0;
    transform: translate(calc(var(--bw-tag-x) * -1), 60%) rotate(calc(var(--bw-tag-angle) * var(--bw-tag-dir)));
}

@keyframes bw-sadrzaj-scroll {
    from {
        transform: translateX(0);
    }

    to {
        transform: translateX(-50%);
    }
}

@media (prefers-reduced-motion: reduce) {
    .bw-sadrzaj-track {
        animation: none;
        will-change: auto;
    }
}

@media screen and (max-width: 980px) {
    .bw-sadrzaj {
        padding: 12vw 0 16vw;
    }

    .bw-sadrzaj-ray {
        width: 40vw;
    }
}

@media screen and (max-width: 550px) {
    .bw-sadrzaj {
        padding: 18vw 0 22vw;
        --bw-sadrzaj-photo-h: 180px;
        --bw-sadrzaj-gap: 10px;
    }

    .bw-sadrzaj-strips {
        gap: 88px;
        padding-top: 72px;
    }

    .bw-sadrzaj-track {
        animation-duration: 45s;
    }

    .bw-sadrzaj-tag {
        --bw-tag-angle: 2.13deg;
    }
}
</style>
