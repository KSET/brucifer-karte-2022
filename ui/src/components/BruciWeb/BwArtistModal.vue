<template>
    <Teleport to="body">
        <Transition name="bw-artist-modal">
            <div v-if="visible" class="bw-artist-overlay" role="presentation" @click.self="close">
                <div ref="panel" class="bw-artist-panel bw-textured" role="dialog" aria-modal="true"
                    :aria-label="artist ? artist.name : 'Izvođač'" tabindex="-1" @keydown.tab="trapFocus">
                    <button ref="closeBtn" type="button" class="bw-artist-close" aria-label="Zatvori" @click="close">
                        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
                            <path d="M5 5 L19 19 M19 5 L5 19" />
                        </svg>
                    </button>

                    <div class="bw-artist-body">
                        <img v-if="artist && artist.image" class="bw-artist-image" :src="artist.image"
                            :alt="`${artist.name} image`" />

                        <h2 v-if="artist" class="bw-artist-name">{{ artist.name }}</h2>

                        <p v-if="subtitle" class="bw-artist-meta">{{ subtitle }}</p>

                        <p v-if="biography" class="bw-artist-bio">{{ biography }}</p>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script>
export default {
    name: 'BwArtistModal',

    props: {
        visible: { type: Boolean, default: false },
        artist: { type: Object, default: null },
    },

    emits: ['update:visible'],

    data() {
        return {
            previousOverflow: null,
        }
    },

    computed: {
        biography() {
            const bio = this.artist?.biography
            return bio && bio.trim().length ? bio : ''
        },

        subtitle() {
            const stage = this.artist?.stage?.trim()
            const time = this.artist?.time?.trim()
            if (stage && time) return `${stage} u ${time}`
            return stage || time || ''
        },
    },

    watch: {
        visible(open) {
            this.applyVisibility(open)
        },
    },

    mounted() {
        if (this.visible) this.applyVisibility(true)
    },

    beforeUnmount() {
        document.removeEventListener('keydown', this.onKeydown)
        this.unlockScroll()
    },

    methods: {
        applyVisibility(open) {
            if (open) {
                this.lockScroll()
                document.addEventListener('keydown', this.onKeydown)
                this.$nextTick(() => this.$refs.panel?.focus())
            } else {
                this.unlockScroll()
                document.removeEventListener('keydown', this.onKeydown)
            }
        },

        close() {
            this.$emit('update:visible', false)
        },

        lockScroll() {
            if (this.previousOverflow !== null) return
            this.previousOverflow = document.body.style.overflow
            document.body.style.overflow = 'hidden'
        },

        unlockScroll() {
            if (this.previousOverflow === null) return
            document.body.style.overflow = this.previousOverflow
            this.previousOverflow = null
        },

        onKeydown(e) {
            if (e.key === 'Escape') this.close()
        },

        focusables() {
            const panel = this.$refs.panel
            if (!panel) return []
            const selector = 'a[href], button:not([disabled]), input:not([disabled]),'
                + ' select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
            return Array.from(panel.querySelectorAll(selector))
                .filter((el) => el.getClientRects().length > 0 || el === document.activeElement)
        },

        trapFocus(e) {
            const items = this.focusables()
            if (!items.length) {
                e.preventDefault()
                this.$refs.panel?.focus()
                return
            }

            const first = items[0]
            const last = items[items.length - 1]
            const active = document.activeElement

            if (e.shiftKey && (active === first || !this.$refs.panel?.contains(active))) {
                e.preventDefault()
                last.focus()
            } else if (!e.shiftKey && active === last) {
                e.preventDefault()
                first.focus()
            }
        },
    },
}
</script>

<style scoped>
.bw-artist-overlay {
    position: fixed;
    inset: 0;
    z-index: 1100;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.72);
    backdrop-filter: blur(4px);
}

.bw-artist-panel {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 80vw;
    max-width: 80vw;
    max-height: 80vh;
    overflow: hidden;
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 54px 0 0 0;
    outline: none;
}

.bw-artist-close {
    position: absolute;
    top: clamp(16px, 2vw, 28px);
    right: clamp(16px, 2vw, 28px);
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    padding: 0;
    border: 0;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.12);
    color: white;
    cursor: pointer;
    transition: background 0.2s ease;
}

.bw-artist-close:hover {
    background: rgba(255, 255, 255, 0.22);
}

.bw-artist-close svg {
    width: 20px;
    height: 20px;
    stroke: currentColor;
    stroke-width: 1.75;
    stroke-linecap: round;
    fill: none;
}

.bw-artist-body {
    position: relative;
    z-index: 1;
    min-height: 0;
    overflow-y: auto;
    padding: clamp(72px, 4vw, 84px) clamp(16px, 2.5vw, 36px) clamp(36px, 5vw, 64px);
    text-align: center;
}

.bw-artist-image {
    display: block;
    max-width: 80%;
    height: clamp(160px, 32vw, 300px);
    object-fit: contain;
    margin: 0 auto;
}

.bw-artist-name {
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 800;
    font-size: clamp(32px, 6vw, 72px);
    line-height: 1;
    text-transform: uppercase;
    color: white;
    margin: clamp(20px, 2.5vw, 34px) 0 0;
}

.bw-artist-name::after {
    content: "";
    display: block;
    margin-bottom: -0.25em;
}

.bw-artist-meta {
    font-family: 'Cobya', sans-serif;
    font-weight: 400;
    font-size: clamp(18px, 2.6vw, 32px);
    line-height: 1;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.55);
    margin: clamp(12px, 1.4vw, 18px) 0 0;
}

.bw-artist-bio {
    font-family: 'Rubik', sans-serif;
    font-weight: 300;
    font-size: clamp(15px, 1.5vw, 20px);
    line-height: 1.9;
    color: white;
    text-align: justify;
    white-space: pre-line;
    margin: clamp(28px, 3.5vw, 48px) 0 0;
}

.bw-artist-modal-enter-active,
.bw-artist-modal-leave-active {
    transition: opacity 0.22s ease;
}

.bw-artist-modal-enter-active .bw-artist-panel,
.bw-artist-modal-leave-active .bw-artist-panel {
    transition: transform 0.22s ease;
}

.bw-artist-modal-enter-from,
.bw-artist-modal-leave-to {
    opacity: 0;
}

.bw-artist-modal-enter-from .bw-artist-panel,
.bw-artist-modal-leave-to .bw-artist-panel {
    transform: translateY(12px) scale(0.98);
}

@media (prefers-reduced-motion: reduce) {

    .bw-artist-modal-enter-active,
    .bw-artist-modal-leave-active,
    .bw-artist-modal-enter-active .bw-artist-panel,
    .bw-artist-modal-leave-active .bw-artist-panel {
        transition: none;
    }
}

@media screen and (max-width: 550px) {
    .bw-artist-panel {
        border-radius: 32px 0 0 0;
    }

    .bw-artist-bio {
        text-align: left;
        line-height: 1.7;
    }
}
</style>
