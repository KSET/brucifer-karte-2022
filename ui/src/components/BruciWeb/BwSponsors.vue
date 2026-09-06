<template>
    <section id="sponzori" class="bw-sponsors bw-textured">
        <img class="bw-ray bw-sponsors-ray bw-sponsors-ray--tl" :src="rayTeal" alt="" aria-hidden="true" />
        <img class="bw-ray bw-sponsors-ray bw-sponsors-ray--tr" :src="rayTeal" alt="" aria-hidden="true" />

        <div class="bw-sponsors-content">
            <div class="bw-sponsors-head">
                <h2 class="bw-section-title">Sponzori</h2>
                <h4 class="bw-section-subtitle">Brucifer 2026.</h4>
            </div>

            <p v-if="error" class="bw-fetch-error">
                Trenutno nije moguće dohvatiti sponzore.
            </p>

            <BwCardGrid v-else :items="sponsors">
                <template #default="{ item }">
                    <a :href="item.url" rel="noreferrer noopener" target="_blank">
                        <div class="card-image-container">
                            <div class="card-image-sizer"></div>
                            <img class="card-image-frame" :src="item.image" :alt="item.name ? `${item.name} logo` : 'sponsor'"
                                loading="lazy" decoding="async">
                        </div>
                    </a>
                </template>
            </BwCardGrid>
        </div>
    </section>
</template>

<script>
import BwCardGrid from '@/components/BruciWeb/BwCardGrid.vue'
import sponsorsStore from '@/store/sponsorsStore'
import rayTeal from '@/assets/design-elements/zraka-plava.webp'

export default {
    name: 'BwSponsors',
    components: { BwCardGrid },

    data() {
        return {
            rayTeal,
        }
    },

    mounted() {
        this.loadSponsors()
    },

    computed: {
        sponsors() {
            return sponsorsStore.state.list
        },
        error() {
            return sponsorsStore.state.error
        },
    },

    methods: {
        async loadSponsors() {
            try {
                await sponsorsStore.dispatch('fetchVisible', { force: !!this.error })
            } catch (e) {
                console.error('Failed to fetch sponsors:', e)
            }
        },
    },
}
</script>

<style scoped>
.bw-sponsors {
    padding: 6vw 4vw calc(4vw + var(--bw-footer-measured-h, var(--bw-footer-h)));
    scroll-margin-top: var(--bw-sticky-header-h);
}

.bw-sponsors-ray {
    width: 27vw;
    --bw-ray-ratio: 1072 / 1400;
    -webkit-mask-image: radial-gradient(circle at 0% 0%, #000 32%, transparent 68%);
    mask-image: radial-gradient(circle at 0% 0%, #000 32%, transparent 68%);
}

.bw-sponsors-ray--tl {
    top: -13vw;
    left: -13vw;
}

.bw-sponsors-ray--tr {
    top: -13vw;
    right: -13vw;
    -webkit-mask-image: radial-gradient(circle at 100% 0%, #000 32%, transparent 68%);
    mask-image: radial-gradient(circle at 100% 0%, #000 32%, transparent 68%);
}

.bw-sponsors-content {
    position: relative;
    z-index: 1;
}

.bw-sponsors-head {
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

@media screen and (max-width: 980px) {
    .bw-sponsors {
        padding: 12vw 6vw calc(8vw + var(--bw-footer-measured-h, var(--bw-footer-h)));
    }

    .bw-sponsors-ray {
        width: 42vw;
    }

    .bw-sponsors-ray--tl {
        top: -20vw;
        left: -20vw;
    }

    .bw-sponsors-ray--tr {
        top: -20vw;
        right: -20vw;
    }
}

@media screen and (max-width: 550px) {
    .bw-sponsors {
        padding: clamp(48px, 14vw, 72px) 6vw calc(clamp(28px, 8vw, 42px) + var(--bw-footer-measured-h, var(--bw-footer-h)));
    }

    .bw-sponsors-ray {
        width: 55vw;
    }

    .bw-sponsors-ray--tl {
        top: -26vw;
        left: -26vw;
    }

    .bw-sponsors-ray--tr {
        top: -26vw;
        right: -26vw;
    }
}
</style>
