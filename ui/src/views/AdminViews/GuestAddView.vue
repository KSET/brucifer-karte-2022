<template>
    <div class="guests-add">
        <Sidebar />
        <div class="admin-page-container">
            <h1 class="page-title">Dodavanje Gosta</h1>            <form @submit="postGuest">
                <h1 class="textfield7">Ime: </h1>
                <input class="inputfield7" type="text" @input="changevalue" v-model="name" placeholder="Surname">

                <h1 class="textfield8">Prezime: </h1>
                <input class="inputfield8" type="text" @input="changevalue" v-model="surname" placeholder="Surname">

                <h1 class="textfield9">Tag: </h1>

                <select class="inputfield9" v-model="selectedTag" name={{selectedTag}}>
                    <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
                </select>


                <h1 class="textfield10">JMBAG: </h1>
                <input class="inputfield10" type="text" v-model="jmbag" placeholder="JMBAG">

                <h1 class="textfield11">Karta: </h1>

                <button class="btn4" v-if="karta == '1'" type="button" @click="changeKarta()">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button class="btn4" v-else @click="changeKarta()" type="button">
                    <img src="../../assets/icons/no-icon.svg">
                </button>

                <h1 class="textfield12">Ulaz: </h1>

                <button v-if="ulaz == '1'" type="button" class="button5" @click="changeUlaz()">
                    <img src="../../assets/icons/yes-icon.svg">
                </button>
                <button v-else @click="changeUlaz()" type="button" class="button5">
                    <img src="../../assets/icons/no-icon.svg">
                </button>
                <button class="submit-button2">Dodaj</button>
            </form>
        </div>
    </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import axios from 'axios'

export default {
    name: 'GuestsAdd',
    components: {
        Sidebar
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
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
                .then(() => {
                })

        }
    }
}
</script>

<style lang="scss" scope>
@import '../../assets/scss/GuestAddView.scss';
</style>