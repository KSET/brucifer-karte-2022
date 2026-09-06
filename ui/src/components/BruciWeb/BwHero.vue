<template>
    <section class="bw-hero bw-textured">
        <img class="bw-ray bw-hero-ray bw-hero-ray--tl" :src="rayYellow" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--tr" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--tc" :src="rayTeal" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--left" :src="rayTeal" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--right" :src="rayTeal" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--bl" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray bw-hero-ray bw-hero-ray--br" :src="rayYellow" alt="" aria-hidden="true" />

        <div class="bw-hero-content">
            <img class="bw-hero-mark" :src="heroIcon" alt="" aria-hidden="true" />

            <h1 class="bw-hero-title bw-display-1">Brucifer</h1>
            <p class="bw-hero-subtitle bw-body" :class="{ 'bw-hero-subtitle--wrapped': subtitleWrapped }" ref="subtitle"><span ref="subtitlePlace">Studentski centar u Zagrebu</span><span class="bw-hero-sep" aria-hidden="true"></span><span class="bw-hero-date" ref="subtitleDate">7. 11. 2026.</span></p>

            <div class="bw-hero-actions">
                <router-link v-if="ULAZNICA_VISIBILITY === true"
                    class="bw-hero-btn bw-hero-btn--primary bw-body-upper" to="/ulaznice">Kupi karte</router-link>
                <router-link v-if="BRUCOSI_VISIBILITY === true"
                    class="bw-hero-btn bw-hero-btn--primary bw-body-upper" to="/brucosi">Brucoši</router-link>
            </div>

            <nav class="bw-hero-links">
                <a v-if="LINEUP_VISIBILITY === true" class="bw-hero-btn bw-hero-btn--ghost bw-label"
                    href="#lineup" @click="scrollToSection($event, 'lineup')">Izvođači</a>
                <router-link v-if="SATNICA_VISIBILITY === true" class="bw-hero-btn bw-hero-btn--ghost bw-label"
                    to="/satnica">Satnica</router-link>
                <router-link v-if="TLOCRT_VISIBILITY === true" class="bw-hero-btn bw-hero-btn--ghost bw-label"
                    to="/tlocrt">Tlocrt</router-link>
                <a v-if="SPONSORS_VISIBILITY === true" class="bw-hero-btn bw-hero-btn--ghost bw-label"
                    href="#sponzori" @click="scrollToSection($event, 'sponzori')">Sponzori</a>
            </nav>
        </div>

    </section>
</template>

<script>
import heroIcon from '@/assets/design-elements/hero-icon.svg'
import rayYellow from '@/assets/design-elements/zraka-zuta.webp'
import rayPurple from '@/assets/design-elements/zraka-ljubicasta.webp'
import rayTeal from '@/assets/design-elements/zraka-plava.webp'
import visibilityStore from '@/store/visibilityStore.js'

export default {
    name: 'BwHero',

    computed: {
        ULAZNICA_VISIBILITY() {
            return visibilityStore.state.ULAZNICA_VISIBILITY;
        },
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
            subtitleWrapped: false,
        }
    },

    mounted() {
        this.updateSubtitleWrap();

        if (typeof ResizeObserver !== 'undefined' && this.$refs.subtitle) {
            this.subtitleObserver = new ResizeObserver(() => this.updateSubtitleWrap());
            this.subtitleObserver.observe(this.$refs.subtitle);
        } else {
            window.addEventListener('resize', this.updateSubtitleWrap);
        }

        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(() => {
                if (!this.isUnmounted) this.updateSubtitleWrap();
            });
        }
    },

    beforeUnmount() {
        this.isUnmounted = true;
        this.stopScrollFollow();

        if (this.subtitleObserver) {
            this.subtitleObserver.disconnect();
            this.subtitleObserver = null;
        }
        window.removeEventListener('resize', this.updateSubtitleWrap);
    },

    methods: {
        updateSubtitleWrap() {
            const place = this.$refs.subtitlePlace;
            const date = this.$refs.subtitleDate;
            if (!place || !date) return;

            this.subtitleWrapped = date.offsetTop > place.offsetTop;
        },

        scrollToSection(event, id) {
            if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            if (event.button !== undefined && event.button !== 0) return;

            const target = document.getElementById(id);
            if (!target) return;

            event.preventDefault();
            this.stopScrollFollow();

            const scrollToTarget = () => {
                const top = target.getBoundingClientRect().top + window.scrollY;
                window.scrollTo({ top, left: 0, behavior: 'auto' });
            };

            scrollToTarget();

            if (typeof ResizeObserver === 'undefined') return;

            this.scrollFollow = new ResizeObserver(() => {
                scrollToTarget();
                clearTimeout(this.scrollFollowSettle);
                this.scrollFollowSettle = setTimeout(() => this.stopScrollFollow(), 250);
            });
            this.scrollFollow.observe(document.documentElement);

            this.scrollFollowCap = setTimeout(() => this.stopScrollFollow(), 2000);
            this.scrollFollowRelease = () => this.stopScrollFollow();
            window.addEventListener('wheel', this.scrollFollowRelease, { once: true, passive: true });
            window.addEventListener('touchstart', this.scrollFollowRelease, { once: true, passive: true });

            window.history.replaceState(null, '', `#${id}`);
        },

        stopScrollFollow() {
            if (this.scrollFollow) {
                this.scrollFollow.disconnect();
                this.scrollFollow = null;
            }
            clearTimeout(this.scrollFollowSettle);
            clearTimeout(this.scrollFollowCap);
            if (this.scrollFollowRelease) {
                window.removeEventListener('wheel', this.scrollFollowRelease);
                window.removeEventListener('touchstart', this.scrollFollowRelease);
                this.scrollFollowRelease = null;
            }
        },
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
    width: 32.4vw;
    -webkit-mask-image: radial-gradient(circle at 0% 0%, #000 45%, transparent 78%);
    mask-image: radial-gradient(circle at 0% 0%, #000 45%, transparent 78%);
}

.bw-hero-ray--tl {
    top: -13vw;
    left: -13vw;
}

.bw-hero-ray--tc {
    display: none;
}

.bw-hero-ray--tr {
    top: -13vw;
    right: -13vw;
    -webkit-mask-image: radial-gradient(circle at 100% 0%, #000 45%, transparent 78%);
    mask-image: radial-gradient(circle at 100% 0%, #000 45%, transparent 78%);
}

.bw-hero-ray--bl {
    bottom: -13vw;
    left: -13vw;
    -webkit-mask-image: radial-gradient(circle at 0% 100%, #000 45%, transparent 78%);
    mask-image: radial-gradient(circle at 0% 100%, #000 45%, transparent 78%);
}

.bw-hero-ray--br {
    bottom: -13vw;
    right: -13vw;
    -webkit-mask-image: radial-gradient(circle at 100% 100%, #000 45%, transparent 78%);
    mask-image: radial-gradient(circle at 100% 100%, #000 45%, transparent 78%);
}

.bw-hero-ray--left,
.bw-hero-ray--right {
    top: 50%;
    width: 24vw;
    --bw-ray-ratio: 1072 / 1400;
    -webkit-mask-image: radial-gradient(circle at 0% 50%, #000 45%, transparent 80%);
    mask-image: radial-gradient(circle at 0% 50%, #000 45%, transparent 80%);
}

.bw-hero-ray--left {
    left: -10vw;
    transform: translateY(-50%);
}

.bw-hero-ray--right {
    right: -10vw;
    transform: translateY(-50%);
    -webkit-mask-image: radial-gradient(circle at 100% 50%, #000 45%, transparent 80%);
    mask-image: radial-gradient(circle at 100% 50%, #000 45%, transparent 80%);
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
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.5em;
    margin: 0;
    padding-top: 24px;
}

.bw-hero-date {
    white-space: nowrap;
}

.bw-hero-sep {
    flex: 0 0 auto;
    width: 4px;
    height: 4px;
    background-color: currentColor;
}

.bw-hero-subtitle--wrapped .bw-hero-sep {
    visibility: hidden;
}

.bw-hero-actions,
.bw-hero-links {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 24px;
}

.bw-hero-actions {
    margin-top: 4vw;
}

.bw-hero-links {
    margin-top: 24px;
}

.bw-hero-btn.bw-hero-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 18px;
    border-radius: 24px 0px 0px 0px;
    line-height: 1;
    text-decoration: none;
    transition: border-color 0.2s ease, background-color 0.2s ease,
        box-shadow 0.2s ease, border-width 0.2s ease, padding 0.2s ease;
}

.bw-hero-btn.bw-hero-btn--primary {
    padding: 24px 32px;
    background: var(--bw-primary-yellow);
    color: var(--bw-outline);
    border: 2px solid var(--bw-primary-yellow);
}

.bw-hero-btn.bw-hero-btn--primary:hover {
    border-width: 4px;
    border-color: rgba(255, 255, 255, 0.25);
    padding: 22px 30px;
}

.bw-hero-btn.bw-hero-btn--primary:active {
    box-shadow: inset 0 0 0 100vmax rgba(255, 255, 255, 0.25);
}

.bw-hero-btn.bw-hero-btn--ghost {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.1);
}

.bw-hero-btn.bw-hero-btn--ghost:hover {
    border-color: rgba(255, 255, 255, 0.2);
}

.bw-hero-btn.bw-hero-btn--ghost:active {
    background-color: rgba(255, 255, 255, 0.4);
}

@media screen and (max-width: 980px) {
    .bw-hero {
        padding-inline: 6vw;
    }

    .bw-hero-ray {
        width: 50.4vw;
    }

    .bw-hero-ray--tl,
    .bw-hero-ray--tr {
        top: -20vw;
    }

    .bw-hero-ray--bl,
    .bw-hero-ray--br {
        bottom: -20vw;
    }

    .bw-hero-ray--tl,
    .bw-hero-ray--bl {
        left: -20vw;
    }

    .bw-hero-ray--tr,
    .bw-hero-ray--br {
        right: -20vw;
    }

    .bw-hero-ray--left,
    .bw-hero-ray--right {
        width: 38.4vw;
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
        gap: 24px;
    }

    .bw-hero-links {
        margin-top: 24px;
        gap: 24px;
    }

    .bw-hero-btn.bw-hero-btn {
        min-width: 0;
        font-size: 18px;
        line-height: 1;
    }

    .bw-hero-btn.bw-hero-btn--primary {
        padding: 24px 32px;
    }

    .bw-hero-btn.bw-hero-btn--primary:hover {
        padding: 22px 30px;
    }

    .bw-hero-btn.bw-hero-btn--ghost {
        padding: 18px;
    }

}

@media screen and (max-width: 550px) {
    .bw-hero-ray {
        width: 66vw;
    }

    .bw-hero-ray--bl,
    .bw-hero-ray--br,
    .bw-hero-ray--left,
    .bw-hero-ray--right {
        display: none;
    }

    .bw-hero-ray--tl,
    .bw-hero-ray--tr {
        top: calc(-25vw - 50px);
    }

    .bw-hero-ray--tl {
        left: -25vw;
    }

    .bw-hero-ray--tr {
        right: -25vw;
    }

    .bw-hero-ray--tc {
        display: block;
        top: calc(-25vw - 50px);
        left: 50%;
        transform: translateX(-50%);
        -webkit-mask-image: radial-gradient(circle at 50% 0%, #000 45%, transparent 78%);
        mask-image: radial-gradient(circle at 50% 0%, #000 45%, transparent 78%);
    }

    .bw-hero-subtitle.bw-hero-subtitle {
        font-size: 16px;
        padding-top: 12px;
    }

    .bw-hero-actions {
        margin-top: 12vw;
        gap: 24px;
    }

    .bw-hero-links {
        margin-top: 24px;
        gap: 24px;
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
        padding: 24px 32px;
        font-size: 24px;
        line-height: 1;
    }

    .bw-hero-btn.bw-hero-btn--primary:hover {
        padding: 22px 30px;
    }

    .bw-hero-btn.bw-hero-btn--ghost {
        padding: 18px;
        font-size: 20px;
        line-height: 1;
    }

}
</style>
