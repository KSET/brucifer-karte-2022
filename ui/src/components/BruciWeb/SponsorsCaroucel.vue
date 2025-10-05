<template>
    <div v-if="SPONSORS_VISIBILITY == 1" class="sponsorsMarquee">
        <div class="marquee-track" :style="{ '--duration': duration }">
            <div class="marquee-group" v-for="n in 10" :key="n">
                <a v-for="sponsor in sponsors" :key="`${n}-${sponsor.id}`" class="sponsorsIcon" :href="sponsor.url"
                    rel="noreferrer noopener" target="_blank">
                    <img class="sponsorsIconImage" :src="sponsor.image" />
                </a>
            </div>
        </div>
    </div>
</template>


<script>
import store from '@/store/visibilityStore'
import sponsorsStore from '@/store/sponsorsStore'

export default {
    name: 'SponsorsCaroucel',
    data() {
        return {
            sponsors: [],
            duration: '100s',
        }
    },

    async mounted() {
        await this.loadSponsors()
    },

    computed: {
        SPONSORS_VISIBILITY() {
            return store.state.SPONSORS_VISIBILITY
        },
        loading() {
            return sponsorsStore.state.loading
        },
        error() {
            return sponsorsStore.state.error
        }
    },

    methods: {
        async loadSponsors() {
            const data = await sponsorsStore.dispatch('fetchVisible')
            this.sponsors = data
            const speed = Math.max(100, this.sponsors.length * 10)
            this.duration = `${speed}s`
        }
    }
}
</script>


<style scoped>
.sponsorsMarquee {
    position: relative;
    overflow: hidden;
    width: 100%;
    display: block;
    padding-block: 4px;
}

.marquee-track {
    display: flex;
    width: max-content;
    gap: 1rem;
    animation: marquee var(--duration, 30s) linear infinite;
}

.sponsorsMarquee:hover .marquee-track {
    animation-play-state: paused;
}

.marquee-group {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.sponsorsIcon {
    border-radius: 18px;
    padding: 5px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.sponsorsIconImage {
    height: 2rem;
    width: 5.5rem;
    object-fit: contain;
}

@keyframes marquee {
    0% {
        transform: translateX(0);
    }

    100% {
        transform: translateX(-50%);
    }
}

@media (prefers-reduced-motion: reduce) {
    .marquee-track {
        animation: none;
    }
}
</style>
