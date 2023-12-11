<template>
    <div class="grid1-container" id="flex" style="margin-top: 3.75rem">
        <div class="grid-item grid1-item1" id="a">
            <div class="grid2-container" style="width: 100%">
                <div class="grid-item grid1-item">
                    <input class="nosubmit search entry" @input="prepSearchGuest" type="form" v-model="search"
                        placeholder="Unesi Ime" style="width: 100% !important" />
                </div>
                <div class="showMobile qr-scan">
                    <MobileEntry />
                </div>
                <div class="grid-item grid1-item" style="position: relative">
                    <select id="selector" class="inputfield entry" v-model="selectedTag" @change="searchGuest">
                        <option v-for="(item, i) in items" :key="i" class="menu-item">
                            {{ item }}
                        </option>
                    </select>
                    <div class="dropdown-arrow"></div>
                </div>
            </div>
        </div>
        <div class="grid-item grid1-item2" id="b" style="padding: 0px;">
            <v-progress-circular v-if="loading == true" size="90px" indeterminate color="black"></v-progress-circular>

            <button class="person" :class="$style.person" v-bind:style="[
                this.guest.id == guest.id
                    ? { backgroundColor: '#D9D9D9' }
                    : { backgroundColor: 'white' },
            ]" v-for="guest in guests" :key="guest.class" @click="chooseGuest(guest)">
                <p>
                    <strong>{{ guest.name }} {{ guest.surname }}</strong>
                </p>
                <p>{{ guest.tag }}</p>
            </button>
        </div>
        <div class="hideMobile">
            <GuestInfo :guest="guest"></GuestInfo>
        </div>
        <div class="overlayEntry showMobile" v-if="overlayEntry">
            <div class="overlayEntry-container">
                <GuestInfo :guest="guest"></GuestInfo>
                <div class="closeBtn" @click="overlayEntry = false">
                    Zatvori
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import GuestInfo from '../../components/Bruckarte/GuestInfo.vue';
import MobileEntry from '@/components/Bruckarte/MobileEntry.vue'
import debounce from 'lodash/debounce';


export default {
    name: 'GuestsAdd',
    components: {
        GuestInfo,
        MobileEntry
    },
    data() {
        return {
            items: [],
            selectedTag: '',
            id: '',

            guests: [],
            guest: {},
            search: '',

            overlayEntry: false,

            loading: false,
        }
    },
    mounted() {
        this.searchGuest = debounce(this.searchGuest, 1000);

        axios.get(process.env.VUE_APP_BASE_URL + '/tags/',)
            .then(response => {
                var itemss = response.data;
                this.items.push("...");
                itemss.forEach(element => {
                    this.items.push(element.name);
                });

            })
    },
    methods: {
        prepSearchGuest() {
            if (this.selectedTag == "...") {
                this.selectedTag = " ";
            }

            this.guests = [];
            this.guest = {};

            if (this.search != '' && this.search.length > 2) {
                this.loading = true;
            }
            this.searchGuest()
        },
        async searchGuest() {
            if (this.search != '' && this.search.length > 2) {
                console.log("SEARCHING", this.search)

                axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=' + this.search + ' ' + this.selectedTag + "&search_fields=tag&search_fields=name&search_fields=surname",)
                    .then(response => {
                        this.guests = response.data;

                        this.guests.forEach(element => {
                            if (element.tag.includes("Sponzor")) {
                                element.tag = (element.tag).slice(36, element.tag.length)
                            }
                        });

                        if (this.guests.length == 1) {
                            this.overlayEntry = true
                            this.guest = this.guests[0];
                            this.id = this.guest.id;
                        } else if (this.guests.length < 1) {
                            this.guest = {}
                            if (this.search != '') {
                                this.guests = [];
                            }
                        }

                    })
            }
            this.loading = false;
        },
        chooseGuest(guest) {
            this.guest = guest;
            this.overlayEntry = true
        },
    }
}
</script>

<style module lang="scss">
.person {
    p {
        font-size: 0.6em;
        font-family: "Montserrat";
    }
}

.span2Sm {
    @media screen and (max-width: 550px) {
        grid-column: span 2;
    }
}

:global(#flex) .cFix {
    @media screen and (max-width: 550px) {
        display: flex !important;
        flex-direction: column;
        height: fit-content;
        justify-content: flex-start;

        &.cFixExpanded {
            height: 100%;
        }
    }
}
</style>

<style>
.dropdown-arrow {
    position: absolute;
    right: 10px;
    top: 55%;
    transform: translateY(-50%);
    cursor: pointer;
    background-image: url('../../assets/icons/dopdwn-notopen-icon.svg');
    background-size: contain;
    background-repeat: no-repeat;
    width: 16px;
    height: 16px;
}

.grid1-container {
    display: grid;
    grid-template-columns: auto 34.47%;
    grid-template-rows: auto 80.76%;
    width: 100vw;
    height: 93vh;
}

.grid3-container {
    left: 6%;
    display: grid;
    grid-template-columns: 23.6% auto;
    padding: 10px;
    grid-gap: 6%;
}

.grid-item {
    padding: 20px;
    font-size: 30px;
    text-align: left;
}

.grid1-item1 {
    display: flex;
    align-items: center;
    border-bottom: 1px solid #000000;
}

.grid2-container {
    display: grid;
    grid-template-columns: 50% 50%;
}

.grid1-item2 {
    grid-row: span 2;
    border-left: 1px solid #000000;
    overflow: auto;
    margin-right: 5px;
}

.grid1-item3 {
    overflow: visible;
}

.inputfield {
    border: 1px solid;
    left: 6%;
}

#inputfield {
    width: 50.6%;
}

.nosubmit.search {
    height: 39px;
    position: relative;
    width: 20%;
    margin-left: 6%;
}

.person {
    display: block;
    width: 100%;
    box-sizing: border-box;
    background-color: white;
    border: 0px;
    border-bottom: 1px solid #000000 !important;
}

.qr-scan {
    grid-row: span 2;
    display: none;
    align-items: center;
    justify-content: center;
    border: 1px solid black;
    margin: 5px;
    border-radius: 5px;
}

.menu-item {
    width: 35%;
}

.p {
    font-size: 16px;
}

.button2-yes {
    box-sizing: border-box;

    width: 25%;

    background: #000000;
    border: 1px solid #000000;
    border-radius: 6px;
}

.button2-no {
    box-sizing: border-box;
    width: 25%;

    background-color: white !important;
    border: 1px solid #000000;
    border-radius: 6px;
}

.va {
    margin-bottom: 5px;
}

.nosubmit.search.entry {
    width: 100%;
    left: 0px;
    margin: 0px;
}

.inputfield.entry {
    width: 100%;
}

.grid1-item {
    width: 95%;
    display: block !important;
    padding: 10px 0px;
    align-items: center;
}

.grid-container2 {
    left: 6%;
    display: grid;
    grid-template-columns: 15% auto;
    padding: 10px;
    grid-gap: 15%;
    row-gap: 3rem;
    align-items: center;
}

.overlayEntry {
    display: none;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 100;
    background-color: rgba(0, 0, 0, 0.5);
}

.overlayEntry-container {
    background-color: white;
    width: 80%;
    height: fit-content;
    border-radius: 15px;
}

.showMobile {
    display: none;
}

.closeBtn {
    width: 93%;
    text-align: center;
    height: 30px;
    border: 1px solid black;
    margin: -10px 10px 10px 10px;
    border-radius: 10px;
}

@media screen and (max-width: 980px) {
    .hideDesktop {
        display: inline-block !important;
    }

    .hideTablet {
        display: none;
    }

    .textfield {
        font-size: 14px;
    }

    .showMobile {
        display: none !important;
    }
}

@media screen and (max-width: 550px) {
    .dropdown-arrow {
        top: 50%
    }

    .grid1-container {
        display: block !important;
    }

    .grid1-container {
        display: block !important;
    }

    .grid3-container {
        display: block !important;
    }

    .grid-item {
        display: block !important;
    }

    .grid1-item1 {
        border-bottom: 1px solid #000000;
    }

    .grid1-item2 {
        display: block !important;
    }

    #flex {
        display: flex !important;
        flex-direction: column;
    }

    #a {
        order: 1;
    }

    #b {
        order: 3;
        height: 100%;
    }

    #c {
        order: 2;
    }
}

@media screen and (max-width: 550px) {
    .grid1-item {
        display: flex !important;
        margin: 0px;
        padding: 7px 0px;
        width: 95% !important;
    }

    .nosubmit.search.entry {
        width: 100% !important;
        font-size: 12px;
    }

    .inputfield.entry {
        width: 100% !important;
    }

    .grid1-item2 {
        border-left: none;
    }

    .textfield {
        font-size: 5px;
    }

    .bttn {
        width: 76px;
        height: 25px;
    }

    .va {
        width: 19px;
        height: 19px;
        margin-top: 3px;
        vertical-align: top;
    }

    .span2 {
        grid-column: 1/2;
    }

    .span3 {
        grid-column: 3/6;
        height: 35px !important;
    }

    .grid-container2 {
        left: 6%;
        display: grid;
        grid-template-columns: 5% 1% 5% 10% 30%;
        padding: 10px;
        padding-top: 3px;

        grid-gap: 15%;
        row-gap: 1rem;
        align-items: center;
    }

    .showMobile {
        display: block !important;
    }

    .qr-scan {
        display: flex !important;
    }

    .overlayEntry {
        display: flex !important;
    }
}
</style>
