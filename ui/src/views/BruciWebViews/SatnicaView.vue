<template>
    <div class="bw-page-container satnica-page bw-overlay-footer bw-textured">
        <img class="bw-ray satnica-ray satnica-ray--tl" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray satnica-ray satnica-ray--tr" :src="rayYellow" alt="" aria-hidden="true" />

        <BwBackButton />

        <section class="satnica">
            <div class="satnica-head">
                <h1 class="bw-section-title">Satnica</h1>
                <h4 class="bw-section-subtitle">Brucifer <strong>2026.</strong></h4>
            </div>

            <p v-if="error" class="bw-fetch-error">
                Trenutno nije moguće dohvatiti satnicu.
                <button type="button" class="bw-fetch-retry" @click="loadLineups">Pokušaj ponovno</button>
            </p>

            <div class="satnica-table" :style="{ '--stage-count': columns.length, '--span': span }">
                <div class="satnica-heads-bar" ref="headsBar">
                    <div class="satnica-heads-viewport">
                        <div class="satnica-heads" ref="heads">
                            <div v-for="stage in columns" :key="`head-${stage.key}`" class="satnica-stage-head">
                                <span class="satnica-stage-label">{{ stage.label }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="satnica-vscroll">
                    <div class="satnica-axis" aria-hidden="true">
                        <span v-for="hour in hours" :key="hour.offset" class="satnica-hour"
                            :style="{ '--m': hour.offset }">{{ hour.label }}</span>                    </div>

                    <div class="satnica-scroll" @scroll.passive="syncHeads">
                        <div class="satnica-grid">
                            <div class="satnica-lines" aria-hidden="true"></div>

                            <div v-for="(stage, index) in columns" :key="`col-${stage.key}`" class="satnica-column"
                                :class="{ 'satnica-column--sticky': stage.sticky }"
                                :style="{ '--block-color': stage.color, gridColumn: index + 1 }" :aria-label="stage.label">
                                <button v-for="act in stage.acts" :key="act.key" type="button" class="satnica-block"
                                    :style="{ '--m': act.offset, '--d': act.duration }"
                                    @click="openArtist(act, stage)">
                                    <span class="satnica-block-label">
                                        <span class="satnica-block-name">{{ act.name }}</span>
                                        <span class="satnica-block-time">{{ act.time }}</span>
                                    </span>
                                </button>
                            </div>

                            <div v-if="nowVisible" class="satnica-now" :style="{ '--m': nowOffset }" aria-hidden="true"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <BwArtistModal v-model:visible="showDialog" :artist="selectedArtist" />

        <Footer></Footer>
    </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwBackButton from '@/components/BruciWeb/BwBackButton.vue'
import BwArtistModal from '@/components/BruciWeb/BwArtistModal.vue'
import lineupStore from '@/store/lineupStore'
import { parseStored, zagrebMinutes } from '@/utils/datetime'
import { EVENT_START, EVENT_END, SATNICA_STAGES, HARDCODED_ACTS, eventNightDate, pad, formatTime } from '@/utils/satnica'
import rayPurple from '@/assets/design-elements/zraka-ljubicasta.webp'
import rayYellow from '@/assets/design-elements/zraka-zuta.webp'
import { gsap } from 'gsap'

const MINUTE = 60000
const BLOCK_PAD = 8
const STATIC_LABEL_STAGES = ['menza', 'kino']
const STAGE_KEYS = SATNICA_STAGES.map(s => s.key)
// the frozen stage names follow horizontal scroll via a CSS scroll timeline where supported
const SCROLL_TIMELINE = typeof CSS !== 'undefined' && CSS.supports('timeline-scope', '--a')

const offsetOf = (date) => (date - EVENT_START) / MINUTE

export default {
    name: 'SatnicaView',
    components: { Footer, BwBackButton, BwArtistModal },

    data() {
        return {
            now: new Date(),
            showDialog: false,
            selectedArtist: null,
            rayPurple,
            rayYellow,
        }
    },

    computed: {
        error() {
            return lineupStore.state.error
        },

        currentTime() {
            const q = this.$route.query.now
            return eventNightDate(Array.isArray(q) ? q[0] : q) || this.now
        },

        acts() {
            const fromDb = lineupStore.state.list
                .map(item => ({
                    name: item.name,
                    image: item.image,
                    biography: item.biography,
                    stage: item.stage,
                    start: parseStored(item.startTime),
                    end: parseStored(item.endTime),
                }))
                .filter(a => STAGE_KEYS.includes(a.stage) && a.start && a.end && a.end > a.start)

            return [...fromDb, ...HARDCODED_ACTS]
                .map(a => {
                    const start = Math.max(a.start, EVENT_START)
                    const end = Math.min(a.end, EVENT_END)
                    return {
                        key: `${a.stage}-${a.name}-${a.start.getTime()}`,
                        name: a.name,
                        image: a.image,
                        biography: a.biography,
                        stage: a.stage,
                        offset: offsetOf(start),
                        duration: (end - start) / MINUTE,
                        time: `${formatTime(a.start)} – ${formatTime(a.end)}`,
                    }
                })
                .filter(a => a.duration > 0)
                .sort((a, b) => a.offset - b.offset)
        },

        columns() {
            return SATNICA_STAGES.map(stage => ({
                ...stage,
                sticky: !STATIC_LABEL_STAGES.includes(stage.key),
                acts: this.acts.filter(a => a.stage === stage.key),
            }))
        },

        span() {
            return offsetOf(EVENT_END)
        },

        hours() {
            const startMin = zagrebMinutes(EVENT_START)
            return Array.from({ length: Math.floor(this.span / 60) + 1 }, (_, i) => ({
                offset: i * 60,
                label: pad(Math.floor((startMin + i * 60) % 1440 / 60)),
            }))
        },

        nowVisible() {
            return EVENT_START <= this.currentTime && this.currentTime < EVENT_END
        },

        nowOffset() {
            return offsetOf(this.currentTime)
        },
    },

    watch: {
        acts: {
            handler: 'setupStickyLabels',
            flush: 'post',
        },
    },

    mounted() {
        this.loadLineups()
        this._clock = setInterval(() => { this.now = new Date() }, 30000)
        this.setupStickyLabels()
        window.addEventListener('scroll', this.updateStickyLabels, { passive: true })
        window.addEventListener('resize', this.updateStickyLabels)
        document.fonts?.ready.then(this.updateStickyLabels)
    },

    beforeUnmount() {
        clearInterval(this._clock)
        window.removeEventListener('scroll', this.updateStickyLabels)
        window.removeEventListener('resize', this.updateStickyLabels)
    },

    methods: {
        setupStickyLabels() {
            this._labels = [...this.$el.querySelectorAll('.satnica-column--sticky .satnica-block')].map(block => {
                const label = block.querySelector('.satnica-block-label')
                return { block, label, setY: gsap.quickSetter(label, 'y', 'px') }
            })
            this.updateStickyLabels()
        },

        updateStickyLabels() {
            if (!this._labels || !this.$refs.headsBar) return
            const lineTop = Math.max(0, this.$refs.headsBar.getBoundingClientRect().bottom)

            const ys = this._labels.map(({ block, label }) => {
                const maxY = Math.max(0, block.clientHeight - 2 * BLOCK_PAD - label.offsetHeight)
                return gsap.utils.clamp(0, maxY, lineTop - block.getBoundingClientRect().top - block.clientTop)
            })
            this._labels.forEach(({ setY }, i) => setY(ys[i]))
        },

        syncHeads(e) {
            if (SCROLL_TIMELINE) return
            this.$refs.heads.style.transform = `translateX(${-e.target.scrollLeft}px)`
        },

        async loadLineups() {
            try {
                await lineupStore.dispatch('fetchVisible')
            } catch (e) {
                console.error('Failed to fetch lineup:', e)
            }
        },

        openArtist(act, stage) {
            this.selectedArtist = {
                name: act.name,
                image: act.image,
                biography: act.biography,
                stage: stage.label,
                time: act.time,
                color: stage.color,
            }
            this.showDialog = true
        },
    },
}
</script>

<style scoped>
.satnica-page {
    --satnica-now: #e3262f;
    --satnica-hour-line: rgba(255, 255, 255, 0.75);
    --satnica-quarter-line: rgba(255, 255, 255, 0.28);
    justify-content: flex-start;
    background-image: none;
}

.satnica-ray {
    width: 30vw;
    top: -12vw;
    -webkit-mask-image: radial-gradient(circle at 0% 0%, #000 40%, transparent 74%);
    mask-image: radial-gradient(circle at 0% 0%, #000 40%, transparent 74%);
}

.satnica-ray--tl {
    left: -11vw;
}

.satnica-ray--tr {
    right: -11vw;
    -webkit-mask-image: radial-gradient(circle at 100% 0%, #000 40%, transparent 74%);
    mask-image: radial-gradient(circle at 100% 0%, #000 40%, transparent 74%);
}

.satnica {
    position: relative;
    z-index: 1;
    width: 100%;
    padding: clamp(88px, 11vw, 132px) 4vw calc(4vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
}

.satnica-head {
    text-align: center;
}

.satnica-head strong {
    font-weight: 800;
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

.satnica-table {
    --px-per-min: 2.4px;
    --pad: 20px;
    --hour-w: 88px;
    --col-min: 0px;
    --col-gap: 14px;
    --axis-gap: 30px;
    --label-gap: 24px;
    --head-h: 150px;
    --track-h: calc(var(--span) * var(--px-per-min) + 1px);
    --stage-cols: repeat(var(--stage-count), minmax(var(--col-min), 1fr));
    timeline-scope: --satnica-x;
    margin-top: clamp(24px, 4vw, 56px);
}

.satnica-heads-viewport {
    margin-left: calc(var(--hour-w) + var(--axis-gap));
}

.satnica-heads,
.satnica-grid {
    display: grid;
    grid-template-columns: var(--stage-cols);
    column-gap: var(--col-gap);
    width: max-content;
    min-width: 100%;
}

.satnica-heads {
    height: var(--head-h);
}

.satnica-vscroll {
    display: grid;
    grid-template-columns: var(--hour-w) minmax(0, 1fr);
    column-gap: var(--axis-gap);
}

.satnica-scroll {
    scroll-timeline: --satnica-x x;
}

.satnica-grid {
    grid-template-rows: calc(var(--track-h) + 2 * var(--pad));
}

.satnica-stage-head {
    position: relative;
}

.satnica-stage-label {
    position: absolute;
    left: 14%;
    bottom: calc(var(--label-gap) - var(--pad));
    transform-origin: left bottom;
    transform: rotate(-45deg);
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 800;
    font-size: 20px;
    line-height: 1;
    text-box: trim-both cap alphabetic;
    text-transform: uppercase;
    white-space: nowrap;
    color: white;
}

.satnica-axis {
    position: relative;
    z-index: 4;
    height: calc(var(--track-h) + 2 * var(--pad));
}

.satnica-hour {
    position: absolute;
    top: calc(var(--pad) + var(--m) * var(--px-per-min));
    transform: translateY(-50%);
    left: 0;
    right: 0;
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 600;
    font-size: 32px;
    line-height: 1;
    text-box: trim-both cap alphabetic;
    font-variant-numeric: slashed-zero;
    text-align: center;
    text-transform: uppercase;
    color: white;
}

.satnica-lines {
    position: relative;
    grid-column: 1 / -1;
    grid-row: 1;
}

.satnica-lines::before,
.satnica-lines::after {
    content: "";
    position: absolute;
    inset: var(--pad) 0;
}

.satnica-lines::before {
    background: repeating-linear-gradient(to bottom,
            var(--satnica-quarter-line) 0 1px,
            transparent 1px calc(15 * var(--px-per-min)));
    -webkit-mask-image: repeating-linear-gradient(to right, #000 0 3px, transparent 3px 6px);
    mask-image: repeating-linear-gradient(to right, #000 0 3px, transparent 3px 6px);
}

.satnica-lines::after {
    background: repeating-linear-gradient(to bottom,
            var(--satnica-hour-line) 0 1px,
            transparent 1px calc(60 * var(--px-per-min)));
}

.satnica-column {
    position: relative;
    grid-row: 1;
    z-index: 1;
}

.satnica-block {
    position: absolute;
    top: calc(var(--pad) + var(--m) * var(--px-per-min));
    left: 0;
    right: 0;
    height: calc(var(--d) * var(--px-per-min) - 2px);
    display: flex;
    flex-direction: column;
    padding: 8px;
    overflow: hidden;
    border: 2px solid rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    background: var(--block-color);
    color: white;
    font: inherit;
    text-align: left;
    cursor: pointer;
    transition: filter 0.2s ease;
}

.satnica-block:hover {
    filter: brightness(1.15);
}

.satnica-block:focus-visible {
    outline: 2px solid white;
    outline-offset: 2px;
}

.satnica-block-label {
    display: flex;
    flex-direction: column;
    gap: 8px;
    will-change: transform;
}

.satnica-block-name {
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 800;
    font-size: 16px;
    line-height: 1;
    text-box: trim-both cap alphabetic;
    text-transform: uppercase;
    font-variant-numeric: slashed-zero;
    overflow-wrap: break-word;
}

.satnica-block-time {
    font-family: 'Rubik', sans-serif;
    font-weight: 400;
    font-size: 16px;
    line-height: 1.15;
    white-space: nowrap;
}

.satnica-now {
    grid-column: 1 / -1;
    grid-row: 1;
    align-self: start;
    position: relative;
    z-index: 3;
    height: 2px;
    margin-top: calc(var(--pad) + var(--m) * var(--px-per-min) - 1px);
    background: var(--satnica-now);
    box-shadow: 0 0 8px rgba(227, 38, 47, 0.6);
    pointer-events: none;
}

@keyframes satnica-heads-x {
    to {
        transform: translateX(calc(100cqw - 100%));
    }
}

@media screen and (max-width: 1550px) {
    .satnica-table {
        --px-per-min: 2px;
        --hour-w: 72px;
        --col-gap: 12px;
        --head-h: 128px;
    }

    .satnica-block-time {
        font-size: 14px;
    }
}

@media screen and (max-width: 1280px) {
    .satnica-table {
        --hour-w: 60px;
        --col-gap: 10px;
    }

    .satnica-block-time {
        font-size: 13px;
    }
}

@media screen and (max-width: 980px) {
    .satnica {
        padding: clamp(88px, 11vw, 132px) 0 calc(6vw + var(--bw-footer-measured-h, var(--bw-footer-total-h))) 6vw;
    }

    .satnica-head {
        padding-right: 6vw;
    }

    .satnica-ray {
        width: 52vw;
        top: -18vw;
    }

    .satnica-ray--tl {
        left: -17vw;
    }

    .satnica-ray--tr {
        right: -17vw;
    }

    .satnica-page {
        overflow: clip;
    }

    .satnica-heads-bar {
        position: sticky;
        top: 0;
        z-index: 5;
        background:
            linear-gradient(rgba(15, 16, 17, 0.75), rgba(15, 16, 17, 0.75)),
            var(--bw-texture) center / cover,
            var(--bw-ink);
    }

    .satnica-heads-viewport {
        overflow: hidden;
        container-type: inline-size;
        margin-left: calc(var(--hour-w) + var(--axis-gap) - 4px);
    }

    .satnica-heads {
        padding: 0 4px;
    }

    @supports (timeline-scope: --a) {
        .satnica-heads {
            animation: satnica-heads-x linear both;
            animation-timeline: --satnica-x;
        }
    }

    .satnica-scroll {
        overflow-x: auto;
        overscroll-behavior-x: contain;
        margin-left: -4px;
        padding: 0 4px;
    }

    .satnica-table {
        --col-min: 140px;
        --col-gap: 8px;
        --axis-gap: 8px;
        --hour-w: 56px;
        --head-h: 40px;
        --pad: 14px;
    }

    .satnica-stage-head {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .satnica-stage-label {
        position: static;
        transform: none;
        font-size: 15px;
    }

    .satnica-hour {
        font-size: 22px;
    }
}

@media screen and (max-width: 550px) {
    .satnica {
        padding: clamp(88px, 11vw, 132px) 0 calc(8vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
    }

    .satnica-head {
        padding: 0 6vw;
    }

    .satnica-ray {
        width: 68vw;
        top: -24vw;
    }

    .satnica-ray--tl {
        left: -22vw;
    }

    .satnica-ray--tr {
        right: -22vw;
    }

    .satnica-table {
        --hour-w: 46px;
    }

    .satnica-hour {
        font-size: 18px;
    }

    .satnica-block-name {
        font-size: 13px;
    }

    .satnica-block-time {
        font-size: 12px;
    }
}
</style>
