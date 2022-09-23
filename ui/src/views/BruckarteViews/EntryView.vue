<template>
    <div class="grid1-container" id="flex">
        <div class="grid-item grid1-item1" id="a">
            <div class="grid2-container">
                <div class="grid-item grid1-item">
                    <input class="nosubmit search entry" @input="searchGuest" type="form" v-model="search"
                        placeholder="Unesi Ime">

                </div>
                <div class="grid-item grid1-item">
                    <select class="inputfield entry" v-model="selectedTag" name={{selectedTag}} @updated="searchGuest">
                        <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
                    </select>
                </div>
            </div>
        </div>
        <div class="grid-item grid1-item2" id="b">
            <button class="person"
                v-bind:style="[(this.id==guest.id) ? {backgroundColor:'#D9D9D9'}: { backgroundColor:'white'}]"
                v-for="guest in guests" :key="guest.class" @click="chooseGuest(guest)">
                <p><strong>{{ guest.name }} {{ guest.surname }}</strong></p>
                <p>{{ guest.tag }} </p>
            </button>
        </div>
        <div class="grid-item grid1-item3" id="c">
            <div class="grid-container2">
                <h1 class="textfield span2">Ime </h1>
                <input readonly class="inputfield span3" :disabled="this.id==''" type="text" @input="changevalue"
                    v-model="name">

                <h1 class="textfield span2">Prezime </h1>
                <input readonly class="inputfield span3" :disabled="this.id==''" type="text" @input="changevalue"
                    v-model="surname">

                <h1 v-if="this.tag == 'Brucoši'" class="textfield">Karta </h1>

                <button disabled v-if="this.tag == 'Brucoši' &&  this.bought == '1'" class="bttn button2-yes"
                    @click="changeBought(guest, '0')">
                    <img class="va" src="../../assets/icons/yes-icon.svg">
                </button>
                <button disabled class="bttn button2-no" v-if="this.tag == 'Brucoši' && this.bought == '0'"
                    @click="changeBought(guest, '1')">
                    <img class="va" src="../../assets/icons/no-icon.svg">
                </button>
<br v-if="this.tag == 'Brucoši'">
                <h1 class="textfield">Ulaz </h1>

                <button v-if="this.entered == '1'" type="button" :disabled="this.id==''" class="bttn button2-yes"
                    @click="changeEntered(guest, '0')">
                    <img class="va" src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else @click="changeEntered(guest, '1')" :disabled="this.id==''" type="button"
                    class="bttn button2-no">
                    <img class="va" src="../../assets/icons/no-icon.svg">
                </button>

                <h1 v-if="this.tag == 'Brucoši'" class="textfield span2">Potvrda </h1>
                <h1 v-if="this.tag == 'Brucoši'" class="textfield span3">{{this.confCode}} </h1>
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
            tag: '',
            confCode: '',



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
                            this.tag = this.guest.tag;
                            this.confCode = this.guest.confCode;

                        } else if (this.guests.length == 0) {
                            this.name = "";
                            this.surname = '';
                            this.jmbag = '';
                            this.tag = '';
                            this.confCode = '';


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
            this.tag = guest.tag;
            this.confCode = guest.confCode;


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

.grid1-item3 {
    border-bottom: 1px solid #000000;
    overflow:visible;
}

.inputfield {
    left: 6%;

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

.menu-item {
    width: 35%;
}

.p {
    font-size: 16px;
}

.button2-yes {
    box-sizing: border-box;

    width: 50%;


    background: #000000;
    border: 1px solid #000000;
    border-radius: 6px;
}

.button2-no {
    box-sizing: border-box;
    width: 50%;


    border: 1px solid #000000;
    border-radius: 6px;

}

.va {
    position: relative;
    top: -6%;
}

.nosubmit.search.entry {
    width: 60%;
    left: 0px;
    margin: 0px;
}

.inputfield.entry {
    width: 60% !important;
}

.grid1-item {
    width: 60% !important;
}
.grid-container2{
    left: 6%;
    display: grid;
    grid-template-columns: 15% auto;
    padding: 10px;
    grid-gap: 15%;
    row-gap: 15%;
    align-items: center;
}

@media screen and (max-width: 980px) {
    .hidedesktop {
        display: inline-block !important;
    }

    .hidetablet {
        display: none;
    }

    .textfield {
        font-size: 14px;
    }

}

@media screen and (max-width: 550px) {
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
        height: 50%
    }

    #c {
        order: 2;
        height: 50% !important;
    }
}


@media screen and (max-width: 550px) {
    .grid1-item {
        display: inline-block !important;
        margin: 0px;
        padding: 0px;
        width: 50% !important;
    }

    .nosubmit.search.entry {
        width: 90% !important;
    }

    .inputfield.entry {
        width: 90% !important;
    }

    .grid1-item2 {
        border-left: none;

    }

    .textfield {
        font-size: 12px;
    }

    .bttn {
        width: 76px;
        height: 25px;
    }

    .va {
        width: 19px;
        height: 19px;
        margin-top: 4px;
        vertical-align: top;
    }

    .span2{
        grid-column: 1/2;
    }

    .span3{
        grid-column: 3/6;
    }

    .grid-container2{
        left: 6%;
    display: grid;
    grid-template-columns: 5% 1% 5% 10% 30%;
    padding: 10px;
    grid-gap: 15%;
    row-gap: 10%;
    align-items: center;
    }
}
</style>