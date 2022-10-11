<template>
    <div class="guests-add">
        <Sidebar />
        <div class="admin-page-container">

            <h1 class="page-title" style="margin-bottom: 40px;">Dodavanje Korisnka</h1>

            <div class="grid-container" style="row-gap: 5%;">
                <h1 class="textfield">Ime i prezime </h1>
                <input required class="inputfield" type="text" @input="changevalue" v-model="name">

                <h1 class="textfield">KSET e-adresa </h1>
                <input required class="inputfield" type="text" @input="changevalue" v-model="email">

                <h1 class="textfield">Privilegija </h1>

                <div class="users-elements">

                    <div class="users-element add"> <button class="button-priv"
                            v-bind:style="[(this.privilege=='3') ? {backgroundColor: 'black', color:'white'}: {backgroundColor: 'white', color:'black'}]"
                            @click="changeprivilege('3')">Karte</button></div>
                    <div class="users-element add"><button class="button-priv"
                            v-bind:style="[(this.privilege=='2') ? {backgroundColor: 'black', color:'white'}: {backgroundColor: 'white', color:'black'}]"
                            @click="changeprivilege('2')">Ulaz</button></div>
                    <div class="users-element add"><button class="button-priv"
                            v-bind:style="[(this.privilege=='4') ? {backgroundColor: 'black', color:'white'}: {backgroundColor: 'white', color:'black'}]"
                            @click="changeprivilege('4')">Ulaz <br>+Karte</button></div>
                    <div class="users-element add"><button class="button-priv"
                            v-bind:style="[(this.privilege=='1') ? {backgroundColor: 'black', color:'white'}: {backgroundColor: 'white', color:'black'}]"
                            @click="changeprivilege('1')">Admin</button></div>

                </div>





                <button class="button submit" @click="postUser">Dodaj</button>
            </div>

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
            users: [],
            privilege: '',
            nextId: '',
        }
    },

    mounted() {
        this.created();
    },
    methods: {
        created() {
            axios.get(process.env.VUE_APP_BASE_URL + '/users/',)
                .then(response => {
                    this.users = response.data;
                })
        },
        changeprivilege(changenum) {
            this.privilege = changenum
        },
        async postUser() {
            if (this.name == "" || this.email == "" || this.privilege == "") {
                window.alert("Unesite sve podatke");
            } else {

                var ids = [];

                this.users.forEach(element => {
                    ids.push(element.id);
                });
                for (let index = 0; index < ids.length; index++) {
                    if (ids.includes(String(index)) == false) {
                        this.nextId = index;
                        break;
                    }
                }
                if (this.nextId === '') {
                    this.nextId = ids.length;
                }

                await axios.post(process.env.VUE_APP_BASE_URL + '/users/',
                    { id: this.nextId, name: this.name, email: this.email, privilege: this.privilege },
                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                )
                    .then(() => {
                        this.created()
                    })

                this.$router.push({ path: '/admin/users/' });
            }
        }
    }
}
</script>

<style lang="scss" scope>
.users-element.add {
    display: inline-block;
    border: 0px;
}

@media screen and (max-width: 550px) {
    .users-elements {
        display: grid;
        grid-template-columns: 50% 50%;
        width: 80%;
    }

    .button-priv {
        height: 70px;
        width: 70px;
        font-size: 16px;
        
    }
}

@import '../../assets/scss/Admin-scss/gird-view.scss';
</style>