<template>
    <div class="bw-page-container">
        <div class="lineup">
            <div v-for="lineup in lineups" :key="lineup.id">
                <div class="artist">
                    <div class="image-container">
                        <div class="image-sizer2"></div>
                        <img class="image-frame2" :src="lineup.image" :alt="`${lineup.name} image`"
                            style="cursor:pointer" @click="openDialog(lineup)" />
                    </div>
                    <h3>{{ lineup.name }}</h3>
                </div>
            </div>
        </div>

        <Footer />

        <Dialog v-model:visible="showDialog" modal :header="selectedLineup ? selectedLineup.name : ''"
            class="artist-dialog" style="max-width: 25rem">
            <template #default>
                <img v-if="selectedLineup && selectedLineup.image" :src="selectedLineup.image"
                    :alt="`${selectedLineup.name} image`" class="artist-dialog-image" />
                <p v-if="selectedLineup && selectedLineup.biography && selectedLineup.biography.trim().length"
                    style="white-space: pre-line;">
                    {{ selectedLineup.biography }}
                </p>
            </template>
        </Dialog>
    </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import lineupStore from '@/store/lineupStore'
import Dialog from 'primevue/dialog'

export default {
    name: 'BWLineup',
    components: { Footer, Dialog },

    data() {
        return {
            showDialog: false,
            selectedLineup: null, // { id, name, image, biography }
        }
    },

    computed: {
        lineups() {
            return lineupStore.state.list
        },
        loading() {
            return lineupStore.state.loading
        },
        error() {
            return lineupStore.state.error
        },
    },

    async mounted() {
        await lineupStore.dispatch('fetchVisible')
    },

    methods: {
        openDialog(lineup) {
            this.selectedLineup = lineup
            this.showDialog = true
        },
    },
}
</script>

<!-- Only dialog-related styles -->
<style>
.p-dialog-close-button,
.p-dialog {}

.p-dialog-close-button:not(:disabled):hover {
    color: black !important;
}

.p-dialog-close-button {
    color: #fff !important;
}

.p-dialog-header {
    padding-top: 25.5rem !important;
    padding-bottom: 0rem;
}

.p-dialog-title {
    color: white !important;
    text-transform: uppercase;
}

.artist-dialog {
    width: 95%;
    max-width: 30rem;
    height: fit-content;
    margin: auto;

    display: flex;
    flex-direction: column;
    gap: 0rem;

    background-color: rgba(7, 72, 120, 0.7) !important;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(6px) !important;
}

.artist-dialog-image {
    aspect-ratio: 1;
    width: 100%;
    object-fit: cover;
    max-width: 100%;

    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;

    border-radius: 12px;
}

@media screen and (max-width: 450px) {
    .p-dialog-header {
        padding-top: 97vw !important;
    }

    .artist-dialog {
        max-width: 97vw;
        max-height: 97vw;
    }
}
</style>


<style>
.bw-page-container {
    margin-top: 0;
    flex: 1;

    position: relative;
    background-repeat: repeat;
    background-size: cover;
    background-color: linear-gradient(red, var(--bw-footer-color));
    min-height: 100vh;
    padding-bottom: 0px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.lineup {
    padding: 3.14159em;

    padding-top: 5.5em;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    grid-row-gap: 3.45rem;
    grid-column-gap: 5.25rem;
    will-change: grid-row-gap, grid-column-gap;
    transition-duration: .2s;
    transition-timing-function: ease;
    transition-property: grid-row-gap, grid-column-gap;
}

.image-container {
    position: relative;
}

.image-container .image-sizer2 {
    padding-bottom: calc(0.86 * 100%);
    transition: padding-bottom .3s ease;
    will-change: padding-bottom;
}

.image-container .image-frame2 {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-repeat: no-repeat;
    background-position: center center;
    background-size: contain;
    object-fit: contain;
}

.artist {
    background: rgba(0, 0, 0, .3);
    border-radius: 18px;
    padding: 15px 30px;
}

.artist h3 {
    text-align: center;
    font-style: normal;
    font-weight: normal;
    font-size: 2.25rem;
    color: white;
    text-transform: uppercase;
    margin-top: .3em;
    will-change: font-size;
    transition-duration: .2s;
    transition-timing-function: ease;
    transition-property: font-size;
    font-weight: 700;
}

@media screen and (max-width: 1550px) {
    .lineup {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        grid-column-gap: 3rem;
    }

    .artist {
        padding: 15px 30px;
    }

    .artist h3 {
        font-size: 1.85rem;
    }
}

@media screen and (max-width: 980px) {
    .lineup {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        grid-column-gap: 2.85rem;
    }

    .artist {
        padding: 10px 20px;
    }

    .artist h3 {
        font-size: 1.4rem;
    }
}

@media screen and (max-width: 635px) {
    .lineup {
        grid-template-columns: repeat(1, minmax(0, 1fr));
        grid-column-gap: 2rem;
    }

    .artist h3 {
        font-size: 1.1rem;
    }
}

@media screen and (max-width: 21.875rem) {
    .lineup {
        grid-template-columns: repeat(1, minmax(0, 1fr));
        grid-row-gap: 1.2rem;
    }


    .artist {
        padding: 8px 12px;
    }
}
</style>
