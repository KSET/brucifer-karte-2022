<template>
    <Transition name="bw-sticky">
        <header v-show="visible" class="bw-sticky-header">
            <router-link class="bw-sticky-title" to="/">Brucifer</router-link>

            <router-link v-if="ULAZNICA_VISIBILITY === true" class="bw-sticky-cta bw-body-upper" to="/ulaznice">
                Kupi karte
            </router-link>
        </header>
    </Transition>
</template>

<script>
import visibilityStore from '@/store/visibilityStore.js'

export default {
    name: 'BwStickyHeader',

    data() {
        return {
            visible: false,
            threshold: 0,
            frame: null,
            observer: null,
            lastScrollHeight: 0,
        }
    },

    computed: {
        ULAZNICA_VISIBILITY() {
            return visibilityStore.state.ULAZNICA_VISIBILITY;
        },
    },

    mounted() {
        window.addEventListener('scroll', this.schedule, { passive: true });
        window.addEventListener('resize', this.schedule, { passive: true });

        if (typeof ResizeObserver !== 'undefined') {
            this.observer = new ResizeObserver(this.onDocumentResize);
            this.observer.observe(document.documentElement);
        }

        this.update();
    },

    beforeUnmount() {
        window.removeEventListener('scroll', this.schedule);
        window.removeEventListener('resize', this.schedule);
        this.observer?.disconnect();
        if (this.frame !== null) {
            cancelAnimationFrame(this.frame);
        }
    },

    methods: {
        onDocumentResize() {
            const height = document.documentElement.scrollHeight;
            if (height === this.lastScrollHeight) return;
            this.lastScrollHeight = height;
            this.schedule();
        },

        schedule() {
            if (this.frame !== null) return;
            this.frame = requestAnimationFrame(() => {
                this.frame = null;
                this.update();
            });
        },

        update() {
            this.lastScrollHeight = document.documentElement.scrollHeight;
            const scrollable = this.lastScrollHeight - window.innerHeight;

            this.threshold = Math.min(window.innerHeight * 0.6, Math.max(scrollable, 0));
            this.visible = scrollable > 0 && window.scrollY >= this.threshold;
        },
    },
}
</script>

<style scoped>
.bw-sticky-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 90;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 12px 4vw;
    background: var(--bw-ink);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.bw-sticky-title {
    font-family: 'GC Epic Pro Cro', sans-serif;
    font-weight: 800;
    font-size: 40px;
    line-height: 1;
    text-transform: uppercase;
    text-decoration: none;
    color: white;
}

.bw-sticky-cta.bw-sticky-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 20px;
    border-radius: 20px 0px 0px 0px;
    border: 2px solid var(--bw-primary-yellow);
    background: var(--bw-primary-yellow);
    color: var(--bw-outline);
    font-size: 16px;
    line-height: 1;
    text-decoration: none;
    transition: filter 0.2s ease;
}

.bw-sticky-cta:hover {
    filter: brightness(1.15);
}

.bw-sticky-enter-active,
.bw-sticky-leave-active {
    transition: transform 0.3s ease, opacity 0.3s ease;
}

.bw-sticky-enter-from,
.bw-sticky-leave-to {
    transform: translateY(-100%);
    opacity: 0;
}

@media screen and (max-width: 980px) {
    .bw-sticky-header {
        padding: 10px 6vw;
    }

    .bw-sticky-title {
        font-size: 32px;
    }

    .bw-sticky-cta.bw-sticky-cta {
        padding: 11px 17px;
        font-size: 15px;
    }
}

@media screen and (max-width: 550px) {
    .bw-sticky-header {
        padding: 8px 5vw;
    }

    .bw-sticky-title {
        font-size: 24px;
    }

    .bw-sticky-cta.bw-sticky-cta {
        padding: 10px 14px;
        border-radius: 16px 0px 0px 0px;
        font-size: 13px;
    }
}

@media (prefers-reduced-motion: reduce) {

    .bw-sticky-enter-active,
    .bw-sticky-leave-active {
        transition: none;
    }
}
</style>
