<template>
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
                <router-link class="footer-text" style="margin-left:30px" to="/pravila-ponasanja">
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
</template>


<script>
import visibilityStore from '@/store/visibilityStore';

export default {
    name: "Footer",
    data() {
        return {
            year: new Date().getFullYear(),
            facebookUrl: 'https://web.facebook.com/BrucosijadaFER',
            instagramUrl: 'https://www.instagram.com/brucifer_fer/',
            websiteUrl: 'https://www.kset.org/',
        }
    },
    computed: {
        IGRICA_VISIBILITY() {
            return visibilityStore.state.IGRICA_VISIBILITY;
        }
    }
}

</script>

<style>
.footery {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 60px;

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

.footer-text {
    margin: 0;
    font: 400 14px/14px Ubuntu, sans-serif;
    letter-spacing: -0.022em;
    text-align: right;
    color: #fff;
    text-decoration: none;
    vertical-align: middle;
}

.footer-text:hover {
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
    transition: opacity .15s ease;
}

.footer-icon:hover {
    opacity: 1;
}

.footer-mail {
    color: white;
    font: 400 14px/14px Ubuntu, sans-serif;
}

.footer-mail:hover {
    color: white;
}

.footer-separator {
    color: white;
    opacity: 0.7;
    margin: 0 6px;
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
}
</style>
