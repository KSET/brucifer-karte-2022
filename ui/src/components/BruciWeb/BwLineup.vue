<template>
    <section id="lineup" class="bw-lineup bw-textured">
        <img class="bw-ray bw-lineup-ray bw-lineup-ray--tl" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray bw-lineup-ray bw-lineup-ray--br" :src="rayPurple" alt="" aria-hidden="true" />

        <div class="bw-lineup-content">
            <div class="bw-lineup-head">
                <h2 class="bw-section-title">Izvođači</h2>
                <h4 class="bw-section-subtitle">Brucifer 2026.</h4>
            </div>

            <p v-if="error" class="bw-fetch-error">
                Trenutno nije moguće dohvatiti izvođače.
                <button type="button" class="bw-fetch-retry" @click="loadLineups">Pokušaj ponovno</button>
            </p>

            <ul v-else class="bw-lineup-list" ref="list">
                <li v-for="(item, index) in lineups" :key="item.id ?? index" class="bw-lineup-row">
                    <button type="button" class="bw-lineup-entry" @click="openDialog(item)">
                        <span v-if="item.image" class="bw-lineup-thumb">
                            <img :src="item.image" :alt="`${item.name} image`" loading="lazy" decoding="async" />
                        </span>
                        <span class="bw-lineup-bar">
                            <span class="bw-lineup-name" ref="names">{{ item.name }}</span>
                        </span>
                    </button>
                </li>
            </ul>
        </div>

        <BwArtistModal v-model:visible="showDialog" :artist="selectedLineup" />
    </section>
</template>

<script>
import lineupStore from '@/store/lineupStore'
import BwArtistModal from '@/components/BruciWeb/BwArtistModal.vue'
import rayPurple from '@/assets/design-elements/zraka-ljubicasta.webp'

export default {
    name: 'BwLineup',
    components: { BwArtistModal },

    data() {
        return {
            showDialog: false,
            selectedLineup: null,
            rayPurple,
        }
    },

    computed: {
        lineups() {
            return lineupStore.state.list
        },
        error() {
            return lineupStore.state.error
        },
    },

    watch: {
        lineups: {
            flush: 'post',
            handler() {
                this.scheduleNameFit()
            },
        },
    },

    created() {
        this._fitFrame = null
        this._observedList = null
        this._lastListWidth = null
        this._resizeObserver = null
        this._destroyed = false
    },

    async mounted() {
        await this.loadLineups()

        if (this._destroyed) return

        this.scheduleNameFit()

        if (document.fonts?.ready) {
            document.fonts.ready.then(() => {
                if (!this._destroyed) this.scheduleNameFit()
            })
        }
    },

    beforeUnmount() {
        this._destroyed = true
        this._resizeObserver?.disconnect()
        this._resizeObserver = null
        this._observedList = null
        if (this._fitFrame) {
            cancelAnimationFrame(this._fitFrame)
            this._fitFrame = null
        }
    },

    methods: {
        observeList() {
            const list = this.$refs.list

            if (!list) {
                this._resizeObserver?.disconnect()
                this._observedList = null
                this._lastListWidth = null
                return
            }
            if (this._observedList === list || typeof ResizeObserver === 'undefined') return

            if (this._resizeObserver) this._resizeObserver.disconnect()
            else {
                this._resizeObserver = new ResizeObserver(entries => {
                    const width = entries[entries.length - 1].contentRect.width
                    if (width === this._lastListWidth) return
                    this._lastListWidth = width
                    this.scheduleNameFit()
                })
            }

            this._lastListWidth = list.getBoundingClientRect().width
            this._observedList = list
            this._resizeObserver.observe(list)
        },

        updateNameFit() {
            this.observeList()

            const refs = this.$refs.names
            if (!refs) return
            const names = Array.isArray(refs) ? refs : [refs]

            const rows = []
            for (const el of names) {
                const bar = el.parentElement
                const entry = bar?.parentElement
                const row = entry?.parentElement
                if (!bar || !entry || !row) continue

                const barStyle = getComputedStyle(bar)
                const thumb = entry.querySelector('.bw-lineup-thumb')
                rows.push({
                    el,
                    available:
                        row.clientWidth -
                        (thumb ? thumb.getBoundingClientRect().width : 0) -
                        parseFloat(barStyle.paddingLeft) -
                        parseFloat(barStyle.paddingRight),
                })
            }
            if (!rows.length) return

            for (const r of rows) r.el.style.removeProperty('--bw-name-scale')

            for (const r of rows) r.el.classList.add('is-measuring')
            for (const r of rows) r.oneLine = r.el.getBoundingClientRect().width
            for (const r of rows) r.el.classList.remove('is-measuring')

            for (const r of rows) r.el.classList.toggle('is-nowrap', r.oneLine <= r.available)

            for (const r of rows) {
                const scale = r.oneLine > 0 ? Math.min(1, r.available / r.oneLine) : 1
                if (scale < 1 && this.isUnbreakable(r.el.textContent)) {
                    r.el.style.setProperty('--bw-name-scale', Math.max(scale, 0.5).toFixed(3))
                }
            }
        },

        isUnbreakable(text) {
            return !/[\s\u00AD\u200B/\-\u2010\u2012\u2013\u2014]/.test((text ?? '').trim())
        },

        scheduleNameFit() {
            if (this._fitFrame) return
            this._fitFrame = requestAnimationFrame(() => {
                this._fitFrame = null
                if (!this._destroyed) this.updateNameFit()
            })
        },

        async loadLineups() {
            try {
                await lineupStore.dispatch('fetchVisible')
            } catch (e) {
                console.error('Failed to fetch lineup:', e)
            }
        },

        openDialog(lineup) {
            this.selectedLineup = lineup
            this.showDialog = true
        },
    },
}
</script>

<style scoped>
.bw-lineup {
    padding: 6vw 4vw 8vw;
}

.bw-lineup-ray {
    width: 34vw;
    -webkit-mask-image: radial-gradient(circle at 0% 0%, #000 40%, transparent 74%);
    mask-image: radial-gradient(circle at 0% 0%, #000 40%, transparent 74%);
}

.bw-lineup-ray--tl {
    top: -12vw;
    left: -11vw;
}

.bw-lineup-ray--br {
    bottom: -12vw;
    right: -11vw;
    -webkit-mask-image: radial-gradient(circle at 100% 100%, #000 40%, transparent 74%);
    mask-image: radial-gradient(circle at 100% 100%, #000 40%, transparent 74%);
}

.bw-lineup-content {
    position: relative;
    z-index: 1;
}

.bw-lineup-head {
    text-align: center;
}

.bw-fetch-error {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding-top: clamp(32px, 6vw, 64px);
    text-align: center;
    color: white;
}

.bw-fetch-retry {
    padding: 12px 20px;
    border: 2px solid var(--bw-primary-yellow);
    border-radius: 20px 0 0 0;
    background: var(--bw-primary-yellow);
    color: var(--bw-outline);
    font: inherit;
    line-height: 1;
    cursor: pointer;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.bw-fetch-retry:hover {
    border-width: 4px;
    border-color: rgba(255, 255, 255, 0.25);
    padding: 10px 18px;
}

.bw-fetch-retry:active {
    box-shadow: inset 0 0 0 100vmax rgba(255, 255, 255, 0.25);
}

.bw-lineup-list {
    --bw-lineup-row-h: clamp(44px, 6.2vw, 88px);
    list-style: none;
    margin: 0 auto;
    padding: 0;
    padding-top: 4vw;
    max-width: 68rem;
}

.bw-lineup-row {
    display: flex;
    justify-content: center;
    max-width: 100%;
}

.bw-lineup-entry {
    display: flex;
    align-items: stretch;
    width: fit-content;
    max-width: 100%;
    border: 0;
    background: none;
    font: inherit;
    color: inherit;
    text-align: left;
    cursor: pointer;
    transition: filter 0.2s ease, transform 0.2s ease;
}

.bw-lineup-entry:hover {
    filter: brightness(1.15);
    transform: translateX(-0.5rem);
}

.bw-lineup-thumb {
    flex: 0 0 var(--bw-lineup-row-h);
    width: var(--bw-lineup-row-h);
    height: var(--bw-lineup-row-h);
    align-self: flex-start;
    overflow: hidden;
}

.bw-lineup-thumb img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top center;
}

.bw-lineup-bar {
    display: flex;
    align-items: center;
    flex: 0 1 auto;
    min-height: var(--bw-lineup-row-h);
    padding: clamp(8px, 1vw, 14px) clamp(16px, 2.2vw, 34px);
    background: var(--bw-lineup-bar-bg);
}

.bw-lineup-name {
    --bw-name-scale: 1;
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 800;
    font-size: calc(clamp(24px, 4.4vw, 64px) * var(--bw-name-scale));
    line-height: 1.08;
    text-transform: uppercase;
    color: white;
    overflow-wrap: normal;
    word-break: normal;
    display: block;
    width: min-content;
    max-width: 100%;
}

.bw-lineup-name.is-nowrap {
    width: max-content;
}

.bw-lineup-name.is-measuring {
    width: max-content;
    max-width: none;
    white-space: nowrap;
}

.bw-lineup-name::after {
    content: "";
    display: block;
    margin-bottom: -0.19em;
}

@media screen and (max-width: 980px) {
    .bw-lineup {
        padding: 12vw 6vw 16vw;
    }

    .bw-lineup-ray {
        width: 52vw;
    }

    .bw-lineup-ray--tl {
        top: -18vw;
        left: -17vw;
    }

    .bw-lineup-ray--br {
        bottom: -18vw;
        right: -17vw;
    }
}

@media screen and (max-width: 550px) {
    .bw-lineup {
        padding: 18vw 6vw 22vw;
    }

    .bw-lineup-ray {
        width: 68vw;
    }

    .bw-lineup-ray--tl {
        top: -24vw;
        left: -22vw;
    }

    .bw-lineup-ray--br {
        bottom: -24vw;
        right: -22vw;
    }

    .bw-lineup-name {
        font-size: calc(32px * var(--bw-name-scale));
        line-height: 1;
        letter-spacing: 0;
        text-align: center;
    }

    .bw-lineup-list {
        --bw-lineup-row-h: 56px;
    }
}
</style>
