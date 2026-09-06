<template>
    <section id="lineup" class="bw-lineup bw-textured">
        <img class="bw-ray bw-lineup-ray bw-lineup-ray--tl" :src="rayPurple" alt="" aria-hidden="true" />
        <img class="bw-ray bw-lineup-ray bw-lineup-ray--br" :src="rayTeal" alt="" aria-hidden="true" />

        <div class="bw-lineup-content">
            <div class="bw-lineup-head">
                <h2 class="bw-section-title">Izvođači</h2>
                <h4 class="bw-section-subtitle">Brucifer 2026.</h4>
            </div>

            <p v-if="error" class="bw-fetch-error">
                Trenutno nije moguće dohvatiti izvođače.
                <button type="button" class="bw-fetch-retry" @click="loadLineups">Pokušaj ponovno</button>
            </p>

            <ul v-else class="bw-lineup-list">
                <li v-for="(item, index) in lineups" :key="item.id ?? index" class="bw-lineup-row">
                    <button type="button" class="bw-lineup-entry" @click="openDialog(item)">
                        <span v-if="item.image" class="bw-lineup-thumb">
                            <img :src="item.image" :alt="`${item.name} image`" loading="lazy" decoding="async" />
                        </span>
                        <span class="bw-lineup-bar">
                            <span class="bw-lineup-name">{{ item.name }}</span>
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
import rayPurple from '@/assets/design-elements/zraka-ljubicasta.png'
import rayTeal from '@/assets/design-elements/zraka-plava.png'

export default {
    name: 'BwLineup',
    components: { BwArtistModal },

    data() {
        return {
            showDialog: false,
            selectedLineup: null,
            rayPurple,
            rayTeal,
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

    async mounted() {
        await this.loadLineups()
    },

    methods: {
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
    scroll-margin-top: var(--bw-sticky-header-h);
}

.bw-lineup-ray {
    width: 34vw;
}

.bw-lineup-ray--tl {
    top: -12vw;
    left: -11vw;
}

.bw-lineup-ray--br {
    bottom: -12vw;
    right: -11vw;
    transform: scale(-1);
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
    transition: filter 0.2s ease;
}

.bw-fetch-retry:hover {
    filter: brightness(1.15);
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
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 800;
    font-size: clamp(24px, 4.4vw, 64px);
    line-height: 1.08;
    text-transform: uppercase;
    color: white;
    overflow-wrap: normal;
    word-break: normal;
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
        width: min-content;
        max-width: 100%;
        font-size: 32px;
        line-height: 1;
        letter-spacing: 0;
        text-align: center;
    }

    .bw-lineup-list {
        --bw-lineup-row-h: 56px;
    }
}
</style>
