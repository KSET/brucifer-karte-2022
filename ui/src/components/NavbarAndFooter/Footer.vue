<template>
    <div ref="root" class="footer">
        <div v-if="SPONSORS_VISIBILITY == 1" class="footer-sponsors-list">
            <sponsors-caroucel />
        </div>

        <div class="footery">
            <div class="footer-container">
                <p id="text1" class="footer-text"> © KSET {{ year }}</p>

                <div class="footer-socials-container-desktop">
                    <div class="footer-socials">
                        <a :href="facebookUrl" aria-label="Facebook" target="_blank" rel="noopener">
                            <img class="footer-icon" src="../../assets/icons/facebook.svg" />
                        </a>
                        <a :href="instagramUrl" aria-label="Instagram" target="_blank" rel="noopener">
                            <img class="footer-icon" src="../../assets/icons/instagram.svg" />
                        </a>
                        <a :href="websiteUrl" aria-label="Website" target="_blank" rel="noopener">
                            <img class="footer-icon" src="../../assets/icons/web.svg" />
                        </a>
                    </div>

                    <span class="footer-separator">•</span>

                    <div>
                        <a href="mailto:press@kset.org" class="footer-mail">press@kset.org</a>
                        <span class="footer-separator">•</span>

                        <a href="mailto:info@kset.org" class="footer-mail">info@kset.org</a>
                    </div>

                </div>

                <div class="footer-left-container">
                    <div v-if="IGRICA_VISIBILITY != 0">
                        <router-link class="footer-text" to="/uvjeti-koristenja">
                            <p class="footer-text">Uvjeti korištenja</p>
                        </router-link>
                    </div>
                    <router-link class="footer-text" to="/pravila-ponasanja">
                        <p class="footer-text">Pravila ponašanja</p>
                    </router-link>
                </div>
            </div>

            <div class="footer-socials-container-mobile">
                <div class="footer-socials">
                    <a :href="facebookUrl" aria-label="Facebook" target="_blank" rel="noopener">
                        <img class="footer-icon" src="../../assets/icons/facebook.svg" />
                    </a>
                    <a :href="instagramUrl" aria-label="Instagram" target="_blank" rel="noopener">
                        <img class="footer-icon" src="../../assets/icons/instagram.svg" />
                    </a>
                    <a :href="websiteUrl" aria-label="Website" target="_blank" rel="noopener">
                        <img class="footer-icon" src="../../assets/icons/web.svg" />
                    </a>
                </div>

                <div>
                    <a href="mailto:press@kset.org" class="footer-mail">press@kset.org</a>
                    <span class="footer-separator">•</span>

                    <a href="mailto:info@kset.org" class="footer-mail">info@kset.org</a>
                </div>

            </div>
        </div>
    </div>

</template>

<script>
import SponsorsCaroucel from '../BruciWeb/SponsorsCaroucel.vue';
import visibilityStore from '@/store/visibilityStore';

export default {
    name: "Footer",
    components: { SponsorsCaroucel },
    data() {
        return {
            year: new Date().getFullYear(),
            facebookUrl: 'https://web.facebook.com/BrucosijadaFER',
            instagramUrl: 'https://www.instagram.com/brucifer_fer/',
            websiteUrl: 'https://www.kset.org/',
            observer: null,
            overlayHost: null,
            frame: null,
            lastMeasured: 0,
        }
    },
    computed: {
        IGRICA_VISIBILITY() {
            return visibilityStore.state.IGRICA_VISIBILITY;
        },
        SPONSORS_VISIBILITY() {
            return visibilityStore.state.SPONSORS_VISIBILITY;
        }
    },

    mounted() {
        this.overlayHost = this.$refs.root?.closest('.bw-overlay-footer') || null;
        if (!this.overlayHost) return;

        this.measure();
        if (typeof ResizeObserver !== 'undefined') {
            this.observer = new ResizeObserver(this.schedule);
            this.observer.observe(this.$refs.root);
        }
    },

    beforeUnmount() {
        this.observer?.disconnect();
        this.observer = null;
        if (this.frame !== null) {
            cancelAnimationFrame(this.frame);
            this.frame = null;
        }
        this.overlayHost?.style.removeProperty('--bw-footer-measured-h');
        this.overlayHost = null;
    },

    methods: {
        schedule() {
            if (this.frame !== null) return;
            this.frame = requestAnimationFrame(() => {
                this.frame = null;
                this.measure();
            });
        },

        measure() {
            const root = this.$refs.root;
            if (!root || !this.overlayHost) return;

            const height = root.getBoundingClientRect().height;
            if (height <= 0) return;

            if (Math.abs(height - this.lastMeasured) < 1) return;

            this.lastMeasured = height;
            this.overlayHost.style.setProperty('--bw-footer-measured-h', `${Math.ceil(height)}px`);
        },
    },
}

</script>

<style>
.footer-sponsors-list {
    display: flex;
    align-items: center;
}

.footer {
    background: var(--bw-footer-color);
}

.footery {
    bottom: 0;
    left: 0;
    width: 100%;
    min-height: 4rem;

    display: flex;
    align-items: center;

    background: var(--bw-footer-color);
    padding: 0 3%;

    flex-direction: column;
    justify-content: space-around;
}

.footer-container {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-left-container {
    display: flex;
    align-items: center;
    gap: 30px;
}

.footer .footer-text {
    margin: 0;
    font: 400 16px/1 Rubik, sans-serif;
    letter-spacing: 0;
    text-align: center;
    color: #fff;
    text-decoration: none;
    vertical-align: middle;
    padding: 0;
    transition: color .15s ease;
}

.footer .footer-text:hover,
.footer a:hover .footer-text {
    color: #dbe9f4;
}

.footer-socials-container-desktop {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 4px;
}

.footer-socials-container-mobile {
    display: none;
}

.footer-socials {
    display: flex;
    align-items: center;
    gap: 14px;
}

.footer-icon {
    width: 1.75rem;
    height: 1.75rem;
    display: block;
    filter: invert(1);
    opacity: 0.9;
    transition: opacity .15s ease, filter .15s ease;
}

.footer-icon:hover {
    opacity: 1;
    filter: invert(1) sepia(1) saturate(0.55) hue-rotate(170deg) brightness(1.06);
}

.footer .footer-mail {
    color: white;
    font: 400 16px/1 Rubik, sans-serif;
    letter-spacing: 0;
    text-align: center;
    text-decoration: none;
    transition: color .15s ease;
}

.footer .footer-mail:hover {
    color: #dbe9f4;
}

.footer .footer-separator {
    color: white;
    opacity: 0.7;
    margin: 0 6px;
    font: 400 16px/1 Rubik, sans-serif;
    letter-spacing: 0;
}

@media (max-width: 640px) {
    .footer-socials-container-desktop {
        display: none;
    }

    .footer-socials-container-mobile {
        width: 100%;
        display: flex;
        justify-content: space-between;
    }

    .footer-icon {
        width: 1.5rem;
        height: 1.5rem;
    }

    .footery {
        justify-content: flex-start;
        gap: 12px;
        padding: 12px 3%;
    }
}

.bw-overlay-footer .footer {
    display: flex;
    flex-direction: column;
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    min-height: var(--bw-footer-h);
    z-index: 2;
    background-color: rgba(255, 255, 255, 0.05);
}

.bw-overlay-footer .footery {
    background-color: transparent;
    flex: 1;
    justify-content: center;
}

.naslovnica-page .footer-sponsors-list {
    display: none;
}

@media screen and (max-width: 550px) {
    .bw-overlay-footer .footer-container {
        flex-direction: column;
        justify-content: center;
        gap: 32px;
    }

    .bw-overlay-footer .footer-socials-container-mobile {
        display: none;
    }

    .bw-overlay-footer .footer-socials-container-desktop {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 32px;
    }

    .bw-overlay-footer .footer-socials-container-desktop .footer-separator {
        display: none;
    }

    .bw-overlay-footer .footer-socials-container-desktop>div:not(.footer-socials) {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 24px;
    }

    .bw-overlay-footer .footer-left-container {
        flex-direction: column;
        gap: 32px;
    }

    .bw-overlay-footer .footery {
        gap: 14px;
        padding: 20px 3%;
    }

    .bw-overlay-footer .footer .footer-text,
    .bw-overlay-footer .footer .footer-mail,
    .bw-overlay-footer .footer .footer-separator {
        font-weight: 300;
    }
}
</style>
