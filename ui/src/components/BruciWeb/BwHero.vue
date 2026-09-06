<template>
    <section class="bw-hero bw-textured">
        <img class="bw-ray bw-hero-ray bw-hero-ray--tl" :src="rayYellow" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--tr" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--left" :src="rayTeal" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--right" :src="rayTeal" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--bl" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--br" :src="rayYellow" alt="" aria-hidden="true" />

        <div class="bw-hero-content">
            <img class="bw-hero-mark" :src="heroIcon" alt="" aria-hidden="true" />

            <h1 class="bw-hero-title bw-display-1">Brucifer</h1>
            <p class="bw-hero-subtitle bw-body">Studentski centar u Zagrebu &middot; 7. 11. 2026.</p>

            <div class="bw-hero-actions">
                <router-link class="bw-hero-btn bw-hero-btn--primary bw-body-upper" to="/ulaznice">Kupi karte</router-link>
                <router-link v-if="BRUCOSI_VISIBILITY === true"
                    class="bw-hero-btn bw-hero-btn--primary bw-body-upper" to="/brucosi">Brucoši</router-link>
            </div>

            <nav class="bw-hero-links">
                <a v-if="LINEUP_VISIBILITY === true" class="bw-hero-btn bw-hero-btn--ghost bw-label"
                    href="#lineup">Izvođači</a>
                <router-link v-if="SATNICA_VISIBILITY === true" class="bw-hero-btn bw-hero-btn--ghost bw-label"
                    to="/satnica">Satnica</router-link>
                <router-link v-if="TLOCRT_VISIBILITY === true" class="bw-hero-btn bw-hero-btn--ghost bw-label"
                    to="/tlocrt">Tlocrt</router-link>
                <a v-if="SPONSORS_VISIBILITY === true" class="bw-hero-btn bw-hero-btn--ghost bw-label"
                    href="#sponzori">Sponzori</a>
            </nav>
        </div>

    </section>
</template>

<script>
import heroIcon from '@/assets/design-elements/hero-icon.svg'
import rayYellow from '@/assets/design-elements/zraka-zuta.png'
import rayPurple from '@/assets/design-elements/zraka-ljubicasta.png'
import rayTeal from '@/assets/design-elements/zraka-plava.png'
import visibilityStore from '@/store/visibilityStore.js'

export default {
    name: 'BwHero',

    computed: {
        BRUCOSI_VISIBILITY() {
            return visibilityStore.state.BRUCOSI_VISIBILITY;
        },
        LINEUP_VISIBILITY() {
            return visibilityStore.state.LINEUP_VISIBILITY;
        },
        SATNICA_VISIBILITY() {
            return visibilityStore.state.SATNICA_VISIBILITY;
        },
        TLOCRT_VISIBILITY() {
            return visibilityStore.state.TLOCRT_VISIBILITY;
        },
        SPONSORS_VISIBILITY() {
            return visibilityStore.state.SPONSORS_VISIBILITY;
        },
    },

    data() {
        return {
            heroIcon,
            rayYellow,
            rayPurple,
            rayTeal,
        }
    },
}
</script>

<style scoped>
.bw-hero {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    height: 100svh;
    padding-inline: 4vw;
    padding-block: 4vh;
}

.bw-hero-ray {
    width: 27vw;
    -webkit-mask-image: radial-gradient(circle at 0% 0%, #000 45%, transparent 78%);
    mask-image: radial-gradient(circle at 0% 0%, #000 45%, transparent 78%);
}

.bw-hero-ray--tl {
    top: -8vw;
    left: -8vw;
}

.bw-hero-ray--tr {
    top: -8vw;
    right: -8vw;
    transform: scaleX(-1);
}

.bw-hero-ray--bl {
    bottom: -8vw;
    left: -8vw;
    transform: scaleY(-1);
}

.bw-hero-ray--br {
    bottom: -8vw;
    right: -8vw;
    transform: scale(-1);
}

.bw-hero-ray--left,
.bw-hero-ray--right {
    top: 50%;
    width: 20vw;
    -webkit-mask-image: radial-gradient(circle at 0% 50%, #000 45%, transparent 80%);
    mask-image: radial-gradient(circle at 0% 50%, #000 45%, transparent 80%);
}

.bw-hero-ray--left {
    left: -10vw;
    transform: translateY(-50%);
}

.bw-hero-ray--right {
    right: -10vw;
    transform: translateY(-50%) scaleX(-1);
}

.bw-hero-content {
    position: relative;
    z-index: 1;
    text-align: center;
    width: 100%;
    max-width: 60rem;
}

.bw-hero-mark {
    display: block;
    width: clamp(72px, 20vw, 150px);
    height: clamp(72px, 20vw, 150px);
    object-fit: contain;
    margin: 0 auto 0.6vw;
}

.bw-hero-title.bw-hero-title {
    font-size: clamp(48px, 11vw, 160px);
    line-height: 1;
    text-transform: uppercase;
    margin: 0;
}

.bw-hero-title::after {
    content: "";
    display: block;
    margin-bottom: -0.25em;
}

.bw-hero-subtitle.bw-hero-subtitle {
    margin: 0;
    padding-top: 24px;
}

.bw-hero-subtitle::before {
    content: "";
    display: block;
    margin-top: -0.1425em;
}

.bw-hero-actions,
.bw-hero-links {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 16px;
}

.bw-hero-actions {
    margin-top: 4vw;
}

.bw-hero-links {
    margin-top: 1vw;
}

.bw-hero-btn.bw-hero-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 18px;
    border-radius: 24px 0px 0px 0px;
    line-height: 1;
    text-decoration: none;
    transition: filter 0.2s ease, transform 0.2s ease;
}

.bw-hero-btn:hover {
    filter: brightness(1.15);
    transform: translateX(-0.25rem);
}

.bw-hero-btn.bw-hero-btn--primary {
    padding: 24px 32px;
    background: var(--bw-primary-yellow);
    color: var(--bw-outline);
    border: 2px solid var(--bw-primary-yellow);
}

.bw-hero-btn.bw-hero-btn--ghost {
    background: rgba(255, 255, 255, 0.25);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.25);
}

@media screen and (max-width: 980px) {
    .bw-hero {
        padding-inline: 6vw;
    }

    .bw-hero-ray {
        width: 42vw;
    }

    .bw-hero-ray--tl,
    .bw-hero-ray--tr {
        top: -13vw;
    }

    .bw-hero-ray--bl,
    .bw-hero-ray--br {
        bottom: -13vw;
    }

    .bw-hero-ray--tl,
    .bw-hero-ray--bl {
        left: -13vw;
    }

    .bw-hero-ray--tr,
    .bw-hero-ray--br {
        right: -13vw;
    }

    .bw-hero-ray--left,
    .bw-hero-ray--right {
        width: 32vw;
    }

    .bw-hero-ray--left {
        left: -16vw;
    }

    .bw-hero-ray--right {
        right: -16vw;
    }

    .bw-hero-subtitle.bw-hero-subtitle {
        font-size: 20px;
    }

    .bw-hero-actions {
        margin-top: 8vw;
        gap: 12px;
    }

    .bw-hero-links {
        margin-top: 2vw;
        gap: 12px;
    }

    .bw-hero-btn.bw-hero-btn {
        min-width: 0;
        font-size: 18px;
        line-height: 1;
    }

    .bw-hero-btn.bw-hero-btn--primary {
        padding: 18px 26px;
    }

    .bw-hero-btn.bw-hero-btn--ghost {
        padding: 14px 20px;
    }

}

@media screen and (max-width: 550px) {
    .bw-hero-ray {
        width: 55vw;
    }

    .bw-hero-ray--tl,
    .bw-hero-ray--tr {
        top: -17vw;
    }

    .bw-hero-ray--bl,
    .bw-hero-ray--br {
        bottom: -17vw;
    }

    .bw-hero-ray--tl,
    .bw-hero-ray--bl {
        left: -17vw;
    }

    .bw-hero-ray--tr,
    .bw-hero-ray--br {
        right: -17vw;
    }

    .bw-hero-ray--left,
    .bw-hero-ray--right {
        width: 42vw;
    }

    .bw-hero-ray--left {
        left: -21vw;
    }

    .bw-hero-ray--right {
        right: -21vw;
    }

    .bw-hero-subtitle.bw-hero-subtitle {
        font-size: 16px;
    }

    .bw-hero-actions {
        margin-top: 12vw;
        gap: 12px;
    }

    .bw-hero-links {
        margin-top: 3vw;
        gap: 10px;
    }

    .bw-hero-actions,
    .bw-hero-links {
        flex-direction: column;
        align-items: center;
    }

    .bw-hero-btn.bw-hero-btn {
        min-width: 0;
        border-radius: 18px 0 0 0;
        font-size: 15px;
        line-height: 1;
    }

    .bw-hero-btn.bw-hero-btn--primary {
        padding: 14px 20px;
    }

    .bw-hero-btn.bw-hero-btn--ghost {
        padding: 11px 16px;
    }

}
</style>
