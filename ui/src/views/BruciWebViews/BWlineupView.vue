<template>
    <div class="bw-page-container">
        <BwCardGrid :items="lineups" variant="lineup">
            <template #default="{ item }">
                <div class="card-image-container">
                    <div class="card-image-sizer"></div>
                    <img class="card-image-frame artist-image" :src="item.image" :alt="`${item.name} image`"
                        loading="lazy" decoding="async" @click="openDialog(item)" />
                </div>
                <h3 class="artist-name">{{ item.name }}</h3>
            </template>
        </BwCardGrid>

        <Footer />

        <Dialog v-model:visible="showDialog" modal :header="selectedLineup ? selectedLineup.name : ''"
            class="artist-dialog">
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
import BwCardGrid from '@/components/BruciWeb/BwCardGrid.vue'
import lineupStore from '@/store/lineupStore'
import Dialog from 'primevue/dialog'

export default {
    name: 'BWLineup',
    components: { Footer, BwCardGrid, Dialog },

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

<style scoped>
.artist-image {
    cursor: pointer;
}

.artist-name {
    text-align: center;
    font-style: normal;
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
    .artist-name {
        font-size: 1.85rem;
    }
}

@media screen and (max-width: 980px) {
    .artist-name {
        font-size: 1.4rem;
    }
}

@media screen and (max-width: 635px) {
    .artist-name {
        font-size: 1.1rem;
    }
}
</style>
