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

                <h1 class="textfield">
                    Vrijeme odbrojavanja Timera
                </h1>
                <label class="datetimePicker">
                    <input @change="changeVisibility('TIMER_TIME', timerTime)" type="datetime-local" v-model="timerTime"
                        class="datetimePickerInput">
                    <span class="placeholderText">{{ formattedTimerTime }}</span>
                </label>

                <h1 class="textfield">
                    Vrijeme sponzorima za unos
                </h1>
                <label class="datetimePicker">
                    <input @change="changeVisibility('SPONSORS_INPUT_TIME', sponsorsInputTime)" type="datetime-local"
                        v-model="sponsorsInputTime" class="datetimePickerInput">
                    <span class="placeholderText">{{ formattedSponsorsInputTime }}</span>
                </label>
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
    data() {
        return {
            timerTime: '',
            sponsorsInputTime: ''
        }
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
        formattedTimerTime() {
            const timerTime = store.state.TIMER_TIME;
            const formattedDate = timerTime.substring(8, 10) + '.' + timerTime.substring(5, 7) + '.' + timerTime.substring(0, 4);
            const formattedTime = timerTime.substring(11, 16);
            return formattedDate + '. ' + formattedTime;
        },
        formattedSponsorsInputTime() {
            const timerTime = store.state.SPONSORS_INPUT_TIME;
            const formattedDate = timerTime.substring(8, 10) + '.' + timerTime.substring(5, 7) + '.' + timerTime.substring(0, 4);
            const formattedTime = timerTime.substring(11, 16);
            return formattedDate + '. ' + formattedTime;
        },
    },
    methods: {
        async changeVisibility(changeField, val) {
            if (changeField == "TIMER_TIME" || changeField == "SPONSORS_INPUT_TIME") {
                if (window.confirm("Pokušavate promijeniti jedno od VREMENA, jeste li sigurni?")) {
                    await axios.put(process.env.VUE_APP_BASE_URL + '/visibility/' + changeField + '/',
                        { visible: val },
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                    )
                    await store.dispatch("fetchVisibilityData")
                }
            } else {
                await axios.put(process.env.VUE_APP_BASE_URL + '/visibility/' + changeField + '/',
                    { visible: val },
                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                )
                await store.dispatch("fetchVisibilityData")
            }

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

.datetimePicker {
    border: 1px solid black;
    font-size: 15px;
    position: relative;
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

.datetimePickerInput {
    width: 20px;

}

.placeholderText {
    position: absolute;
    top: 50%;
    left: 25px;
    transform: translateY(-50%);
}
</style>

  
  
  