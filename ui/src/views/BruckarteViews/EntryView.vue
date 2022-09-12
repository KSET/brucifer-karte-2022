<template>
    <div class="grid1-container">
        <div class="grid-item grid1-item1">
            <div class="grid2-container">
                <div class="grid-item grid-item2">
                    <input  class="inputfield" @input="searchGuest" type="form" v-model="search"
                        placeholder="Unesi Ime">
                </div>
                <div class="grid-item grid-item3">
                    <select class="inputfield" v-model="selectedTag" name={{selectedTag}} @updated="searchGuest">
                        <option v-for="(item, i) in items" :key="i" class="menu-item">{{  item  }}</option>
                    </select>
                </div>
            </div>
        </div>
        <div class="grid-item grid1-item2">
            <button class="person" v-bind:style= "[(this.id==guest.id) ? {backgroundColor:'#D9D9D9'}: { backgroundColor:'white'}]" v-for="guest in guests" :key="guest.class" @click="chooseGuest(guest)">
                <p><strong>{{  guest.name  }} {{  guest.surname  }}</strong></p> 
                <p>{{  guest.tag  }} </p>
            </button>
        </div>
        <div class="grid-item grid1-item3">
            <div class="grid3-container">
                <h1 class="textfield">Ime </h1>
                <input readonly class="inputfield" :disabled="this.id==''" type="text" @input="changevalue" v-model="name">

                <h1 class="textfield">Prezime </h1>
                <input readonly class="inputfield" :disabled="this.id==''" type="text" @input="changevalue" v-model="surname">

                <h1 v-if="this.jmbag != ''" class="textfield">JMBAG </h1>
                <input v-if="this.jmbag != ''" class="inputfield" readonly type="text" v-model="jmbag">

                <h1 v-if="this.jmbag != ''" class="textfield">Karta </h1>

                <button disabled v-if="this.jmbag != '' &&  this.bought == '1'"  class="button2-yes" @click="changeBought(guest, '0')">
                    <img  class="va" src="../../assets/icons/yes-icon.svg">
                </button>
                <button disabled class="button2-no" v-if="this.jmbag != '' && this.bought == '0'" @click="changeBought(guest, '1')">
                    <img class="va"  src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield">Ulaz </h1>

                <button v-if="this.entered == '1'" type="button" :disabled="this.id==''" class="button2-yes" @click="changeEntered(guest, '0')">
                    <img class="va" src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else @click="changeEntered(guest, '1')" :disabled="this.id==''" type="button" class="button2-no">
                    <img class="va" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 v-if="this.jmbag != ''" class="textfield">Potvrda </h1>
                <h1 v-if="this.jmbag != ''" class="textfield">kod123456789 </h1>
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
            id: '',
            bought: '',
            entered: '',
            guests: [],
            guest: '',
            search: '',
            name: '',
            surname: '',
            jmbag: '',
            bought: '',
            entered: '',


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
            axios.get('http://127.0.0.1:8000/guests/?search=' + this.search + ' ' + this.selectedTag + "&search_fields=tag&search_fields=name&search_fields=surname",)
                .then(response => {
                    if (this.search != '' && this.search.length > 2) {
                        this.guests = response.data;
                        if (this.guests.length == 1) {
                            this.guest = this.guests[0];
                            this.name = this.guest.name;
                            this.id = this.guest.id;
                            this.bought = this.guest.bought;
                            this.entered = this.guest.entered;
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
        chooseGuest(guest) {
            this.guest = guest;
            this.name = guest.name;
            this.id = guest.id;

            this.surname = guest.surname;
            this.jmbag = guest.jmbag;
            this.bought = guest.bought;
            this.entered = guest.entered;
        },
        changeEntered(guest, changenum) {
            axios.put('http://127.0.0.1:8000/guests/' + guest.id + '/',
                { entered: changenum },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
                .then(() => {
                    this.entered = changenum;
                    this.guest.entered = changenum;
                })
        },
        changeBought(guest, changenum) {
            axios.put('http://127.0.0.1:8000/guests/' + guest.id + '/',
                { bought: changenum },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
                .then(() => {
                    this.bought = changenum;
                    this.guest.bought = changenum;
                })
        },
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
    height: 87vh;
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
    overflow: auto;
    margin-right: 5px;
}

.inputfield {
    left: 6%;
    width: 25.6%;
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 700;
    font-size: 16px;
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
    width: 100%;
    box-sizing: border-box;
background-color: white;
border-bottom: 1px solid #000000;
}

.menu-item{
    width: 35%;
}

.p{
    font-size: 16px;
}

.button2-yes {
    box-sizing: border-box;

    width: 50%;


    background: #000000;
    border: 1px solid #000000;
    border-radius: 6px;
}

.button2-no{
    box-sizing: border-box;
    width: 50%;


border: 1px solid #000000;
border-radius: 6px;

}

.va{
position: relative;
top:-6%;
}
</style>