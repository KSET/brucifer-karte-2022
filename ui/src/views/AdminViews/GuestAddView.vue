<template>
    <div class="guests-add">
        <Sidebar />
        <div class="admin-page-container">

            <h1 class="page-title">Dodavanje Gosta</h1>

            <form @submit="postGuest">
                <div class="grid-container" style="row-gap: 10%;">
                    <h1 class="textfield">Ime: </h1>
                    <input class="inputfield" type="text" @input="changevalue" v-model="name">

                    <h1 class="textfield">Prezime: </h1>
                    <input class="inputfield" type="text" @input="changevalue" v-model="surname" >

                    <h1 class="textfield">Tag: </h1>

                    <select class="inputfield" v-model="selectedTag" name={{selectedTag}}>
                        <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
                    </select>


                    <h1 class="textfield">JMBAG: </h1>
                    <input class="inputfield" type="text" v-model="jmbag" >

                    <h1 class="textfield">Karta: </h1>

                    <button class="button change" v-if="karta == '1'"  type="button" @click="changeKarta()">
                        <img src="../../assets/icons/yes-icon.svg">
                    </button>
                    <button class="button change" v-else @click="changeKarta()" style="background-color: white;" type="button ">
                        <img src="../../assets/icons/no-icon.svg">
                    </button>

                    <h1 class="textfield">Ulaz: </h1>

                    <button v-if="ulaz == '1'" type="button" class="button change" @click="changeUlaz()">
                        <img src="../../assets/icons/yes-icon.svg">
                    </button>
                    <button v-else @click="changeUlaz()" type="button" style="background-color: white;" class="button change">
                        <img src="../../assets/icons/no-icon.svg">
                    </button>
                    <button class="button submit">Dodaj</button>
                </div>
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
@import '../../assets/scss/Admin-scss/gird-view.scss';
</style>