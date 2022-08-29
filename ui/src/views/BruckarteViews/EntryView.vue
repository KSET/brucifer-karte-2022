<template>
    <div class="grid1-container">
        <div class="grid-item grid1-item1">
            <div class="grid2-container">
                <div class="grid-item grid-item2">
                    <input id="search-field2" class="inputfield" @input="searchGuest" type="form" v-model="search"
                        placeholder="Unesi Ime">
                </div>
                <div class="grid-item grid-item3">
                    <select class="inputfield" v-model="selectedTag" name={{selectedTag}} @select="searchGuest">
                        <option v-for="(item, i) in items" :key="i" class="menu-item">{{  item  }}</option>
                    </select>
                </div>
            </div>
        </div>
        <div class="grid-item grid1-item2">
            <button class="person" v-for="guest in guests" :key="guest.id" @click="chooseGuest">
                <p>{{  guest.name  }} {{ guest.surname }}</p>
                <p>{{  guest.tag  }} </p>
            </button>
        </div>
        <div class="grid-item grid1-item3">
            <div class="grid3-container">
                <h1 id="textfield">Ime </h1>
                <input id="inputfield" type="text" @input="changevalue" v-model="name">

                <h1 id="textfield">Prezime </h1>
                <input id="inputfield" type="text" @input="changevalue" v-model="surname">

                <h1 id="textfield">JMBAG </h1>
                <input id="inputfield" readonly type="text" v-model="jmbag">

                <h1 id="textfield">Karta </h1>
                <button id="button" v-if="guest.bought == '1'" @click="changebought(guest, '0')">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button id="button" v-else @click="changebought(guest, '1')">
                    <img id="image1" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 id="textfield">Ulaz </h1>

                <button v-if="guest.enetered == '1'" type="button" class="button" @click="changeUlaz()">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else @click="changeUlaz()" type="button" class="button">
                    <img src="../../assets/icons/no-icon.svg">
                </button>

                <h1 id="textfield">Potvrda </h1>
                <h1 id="textfield">kod123456789 </h1>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'GuestsAdd',
    components: {

    },
    props: {
        msg: String
    },
    data() {
        return {
            items: [],
            selectedTag: '',
            bought: '',
            entered: '',
            guests: [],
            guest: '',
            search: '',


        }
    },
    mounted() {
        axios.get('http://127.0.0.1:8000/tags/',)
            .then(response => {
                var itemss = response.data;
                itemss.forEach(element => {
                    this.items.push(element.name);
                });

            })
    },
    methods: {
        searchGuest() {
            console.log(this.selectedTag);
            axios.get('http://127.0.0.1:8000/guests/?search=' + this.search + ' ' + this.selectedTag + "&search_fields=tag&search_fields=name&search_fields=surname",)
                .then(response => {
                    if (this.search != '' && this.search.length > 2) {
                        this.guests = response.data;
                        if (this.guests.length == 1) {
                            this.guest = this.guests[0];
                            this.name = this.guest.name;
                            this.surname = this.guest.surname;
                            this.jmbag = this.guest.jmbag;
                        } else if (this.guests.length == 0) {
                            this.name = "NO MATCH!";
                            this.surname = '';
                            this.jmbag = '';
                        }
                    } else {
                        if (this.search != '') {
                            this.guests = [];
                        }

                    }
                })
        },
        chooseGuest() {
            console.log(guest.name);
        }
    }
}
</script>

<style>
.grid1-container {
    display: grid;
    grid-template-columns: auto 34.47%;
    grid-template-rows: auto 70.76%;
    padding: 10px;
    width: 100vw;
    height: 90vh;
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
    border-bottom: 1px solid #000000;
}

.grid1-item2 {
    grid-row: span 2;
    border-left: 1px solid #000000;
}

.inputfield {
    left: 6%;
    width: 25.6%;
}

.textfield {
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 700;
    font-size: 16px;
    line-height: 36px;
    /* identical to box height, or 225% */

    display: flex;
    align-items: center;
    letter-spacing: -0.015em;

    color: #000000;
}

#inputfield {
    width: 50.6%;
}

.person {
    display: block;
    border: 1px solid #000000;
}
</style>