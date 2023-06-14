<template>
    <div id="firme">
        <Sidebar />
        <div class="admin-page-container">
            <h1 class="page-title">Visibility</h1>

            <div class="visibility-grid">
                <div class="textfield">
                    Prikaz stranice Coming soon
                </div>
                <button v-if="COMINGSOON_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('COMINGSOON_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('COMINGSOON_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <div class="textfield">
                    Prikaz stranice Izvođača
                </div>
                <button v-if="LINEUP_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('LINEUP_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('LINEUP_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <div class="textfield">
                    Prikaz stranice Sponzora
                </div>
                <button v-if="SPONSORS_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('SPONSORS_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('SPONSORS_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <div class="textfield">
                    Prikaz stranice Cjenik
                </div>
                <button v-if="CJENIK_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('CJENIK_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('CJENIK_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <div class="textfield">
                    Prikaz stranice Tlocrt
                </div>
                <button v-if="TLOCRT_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('TLOCRT_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('TLOCRT_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <div class="textfield">
                    Prikaz stranice Satnica
                </div>
                <button v-if="SATNICA_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('SATNICA_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('SATNICA_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <div class="textfield">
                    Prikaz stranice Ulaznica
                </div>
                <button v-if="ULAZNICA_VISIBILITY == 1" class="button change"
                    @click="changeVisibility('ULAZNICA_VISIBILITY', '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else class="button change" @click="changeVisibility('ULAZNICA_VISIBILITY', '1')"
                    style="background-color: white;">
                    <img class="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <div class="textfield">
                    Prikaz stranice Timera
                </div>
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
    name: 'GuestsTable',
    props: {
        msg: String
    },
    components: {
        Sidebar
    },
    data() {
        return {
            COMINGSOON_VISIBILITY: store.state.COMINGSOON_VISIBILITY,
            LINEUP_VISIBILITY: store.state.LINEUP_VISIBILITY,
            SPONSORS_VISIBILITY: store.state.SPONSORS_VISIBILITY,
            CJENIK_VISIBILITY: store.state.CJENIK_VISIBILITY,
            SATNICA_VISIBILITY: store.state.SATNICA_VISIBILITY,
            TLOCRT_VISIBILITY: store.state.TLOCRT_VISIBILITY,
            ULAZNICA_VISIBILITY: store.state.ULAZNICA_VISIBILITY,
            TIMER_VISIBILITY: store.state.TIMER_VISIBILITY,
        }
    },
    methods: {
        changeVisibility(changeField, val) {
            console.log(process.env.AUTH_USER)
            axios.put(process.env.VUE_APP_BASE_URL + '/visibility/' + changeField + '/',
                { visible: val },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
                .then(() => {
                    location.reload();
                })

        }
    }

}
</script>


<style>
.visibility-grid {
    display: grid;
    grid-template-columns: 70% 30%;
    row-gap: 20px;
}
</style>

  
  
  