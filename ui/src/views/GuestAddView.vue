<template>
    <div id="guests-add">
        <br><br><br>
        <h2 id="page-title">Dodavanje gosta</h2>
        <form @submit="postGuest">
            <h1 id="textfield1">Ime: </h1>
            <input id="inputfield1" type="text" @input="changevalue" v-model="name" placeholder="Surname">
            <br>
            <br>
            <h id="textfield2">Prezime: </h>
            <input id="inputfield2" type="text" @input="changevalue" v-model="surname" placeholder="Surname">
            <br><br>
            <h id="textfield3">Tag: </h>

            <select id="inputfield3" v-model="selectedTag" name={{selectedTag}}>
                <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
            </select>
            <br>
            <br>
            <h id="textfield4">JMBAG: </h>
            <input id="inputfield4" type="text" v-model="jmbag" placeholder="JMBAG">
            <br><br>
            <h id="textfield5">Karta: </h>

            <button id="button1" v-if="karta == '1'" class="btn btn-xs btn-success" type="button"
                @click="changeKarta()">
                <font-awesome-icon icon="fa-solid fa-check" />
            </button>
            <button id="button1" v-else @click="changeKarta()" type="button" class="btn btn-xs btn-danger" >
                <font-awesome-icon icon="fa-solid fa-xmark" />
            </button><br><br>

            <h id="textfield6">Ulaz: </h>

            <button v-if="ulaz == '1'" type="button" class="btn btn-xs btn-success" id="button2" @click="changeUlaz()">
                <font-awesome-icon icon="fa-solid fa-check" />
            </button>
            <button v-else @click="changeUlaz()" type="button" class="btn btn-xs btn-danger" id="button2">
                <font-awesome-icon icon="fa-solid fa-xmark" />
            </button><br><br>
            <button id="submit-button">Dodaj</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

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
            guests: [],
            karta: '0',
            ulaz: '0',
            guest: '',
            id: '',
            name: '',
            surname: '',
            jmbag: '',
            phone: '',
            tag: '',
            bought: '',
            entered: '',
            deleted: '',
            len: '',
            services: ['Brucoši', 'KSET', 'VIP'],
            selectedTag: '',

        }
    },

    created() {
        axios.get('http://127.0.0.1:8000/guests/',)
            .then(response => {
                this.guests = response.data;
                this.len = this.guests.length;
                axios.get('http://127.0.0.1:8000/tags/',)
                    .then(response => {
                        var itemss = response.data;
                        itemss.forEach(element => {
                            this.items.push(element.name);
                        });

                    })
            })
    },
    methods: {
        changeKarta() {
            if (this.karta == '1') {
                this.karta = '0';
            } else {
                this.karta = '1';
            }
        },
        changeUlaz() {
            if (this.ulaz == '1') {
                this.ulaz = '0';
            } else {
                this.ulaz = '1';
            }
        },
        postGuest() {

            var ids = [];
            this.guests.forEach(element => {
                ids.push(element.id);
            });
            for (let index = 0; index < ids.length; index++) {
                if (ids.includes(String(index)) == false) {
                    this.nextId = index;
                    break;
                }
            }
            if (this.nextId == '') {
                this.nextId = ids.length;
            }
            console.log(this.nextId);
            console.log(this.name)
            console.log(this.surname)
            console.log(this.jmbag)
            console.log(this.selectedTag)
            console.log(this.karta)
            console.log(this.ulaz)

            axios.post('http://127.0.0.1:8000/guests/',
                { id: this.nextId, name: this.name, surname: this.surname, jmbag: this.jmbag, tag: this.selectedTag, bought: this.karta, entered: this.ulaz },
                { auth: { username: process.env.VUE_APP_AUTH_USER, password: process.env.VUE_APP_AUTH_PASS } }
            )
                .then(() => {
                })

        }
    }
}
</script>

<style lang="scss">
@import url(../assets/scss/GuestAddView.scss);
</style>