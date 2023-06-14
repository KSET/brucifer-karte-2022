<template>
    <div id="firme">
        <Sidebar />
        <div class="admin-page-container">
            <h1 class="page-title">Visibility</h1>

            <div class="visibility-grid">
                <h1 class="textfield">
                    Prikaz stranice Coming soon
                </h1>
                <button v-if="COMINGSOON_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('COMINGSOON_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('COMINGSOON_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Izvođača
                </h1>
                <button v-if="LINEUP_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('LINEUP_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('LINEUP_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Sponzora
                </h1>
                <button v-if="SPONSORS_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('SPONSORS_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('SPONSORS_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Cjenik
                </h1>
                <button v-if="CJENIK_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('CJENIK_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('CJENIK_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Tlocrt
                </h1>
                <button v-if="TLOCRT_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('TLOCRT_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('TLOCRT_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Satnica
                </h1>
                <button v-if="SATNICA_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('SATNICA_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('SATNICA_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Ulaznica
                </h1>
                <button v-if="ULAZNICA_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('ULAZNICA_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('ULAZNICA_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">
                    Prikaz stranice Timera
                </h1>
                <button v-if="TIMER_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('TIMER_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('TIMER_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>
            </div>

        </div>
    </div>
</template>
  
<script>
import axios from 'axios'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import store from "@/store/visibilityStore.js";

export default {
    name: 'VisibilityView',
    components: {
        Sidebar,
    },
    computed: {
        COMINGSOON_VISIBILITY() {
            return store.state.COMINGSOON_VISIBILITY;
        },
        LINEUP_VISIBILITY() {
            return store.state.LINEUP_VISIBILITY;
        },
        SPONSORS_VISIBILITY() {
            return store.state.SPONSORS_VISIBILITY;
        },
        CJENIK_VISIBILITY() {
            return store.state.CJENIK_VISIBILITY;
        },
        SATNICA_VISIBILITY() {
            return store.state.SATNICA_VISIBILITY;
        },
        TLOCRT_VISIBILITY() {
            return store.state.TLOCRT_VISIBILITY;
        },
        ULAZNICA_VISIBILITY() {
            return store.state.ULAZNICA_VISIBILITY;
        },
        TIMER_VISIBILITY() {
            return store.state.TIMER_VISIBILITY;
        },
    },
    methods: {
        async changeVisibility(changeField, val) {
            console.log(process.env.AUTH_USER)
            await axios.put(process.env.VUE_APP_BASE_URL + '/visibility/' + changeField + '/',
                { visible: val },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
            await store.dispatch("fetchVisibilityData")

        }
    }
}
</script>


<style>
.visibility-grid {
    display: grid;
    grid-template-columns: 70% 30%;
    row-gap: 20px;
    align-items: center;
    width: 50%;
}

@media screen and (max-width: 980px) {
    .visibility-grid {
        width: 80%;
    }
}

@media screen and (max-width: 550px) {
    .visibility-grid {
        width: 90%;
    }
}
</style>

  
  
  