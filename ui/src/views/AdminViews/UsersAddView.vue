<template>
    <div class="guests-add">
        <Sidebar />
        <div class="admin-page-container">

            <h1 class="page-title" style="margin-bottom: 40px;">Dodavanje Korisnka</h1>

            <div class="grid-container" style="row-gap: 3rem;">
                <h1 class="textfield">Ime i prezime </h1>
                <input required class="inputfield" type="text" @input="changeValue" v-model="name">

                <h1 class="textfield">KSET e-adresa </h1>
                <input required class="inputfield" type="text" @input="changeValue" v-model="email">

                <h1 class="textfield">Privilegija </h1>

                <div class="users-elements">

                    <div class="users-element add"> <button class="button-priv"
                            v-bind:style="[(this.privilege == NONE) ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                            @click="changeprivilege(NONE)">X</button></div>
                    <div class="users-element add"> <button class="button-priv"
                            v-bind:style="[(this.privilege == TICKETS) ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                            @click="changeprivilege(TICKETS)">Karte</button></div>
                    <div class="users-element add"><button class="button-priv"
                            v-bind:style="[(this.privilege == ENTRY) ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                            @click="changeprivilege(ENTRY)">Ulaz</button></div>
                    <div class="users-element add"><button class="button-priv"
                            v-bind:style="[(this.privilege == ENTRY_TICKETS) ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                            @click="changeprivilege(ENTRY_TICKETS)">Ulaz <br>+Karte</button></div>
                    <div class="users-element add"><button class="button-priv"
                            v-bind:style="[(this.privilege == ADMIN) ? { backgroundColor: 'black', color: 'white' } : { backgroundColor: 'white', color: 'black' }]"
                            @click="changeprivilege(ADMIN)">Admin</button></div>

                </div>





                <button class="button submit" @click="postUser">Dodaj</button>
            </div>

        </div>
    </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import { api } from "@/plugins/api";
import { NONE, ADMIN, ENTRY, TICKETS, ENTRY_TICKETS } from "@/plugins/roles";

export default {
    name: 'UsersAdd',
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
            NONE,
            ADMIN,
            ENTRY,
            TICKETS,
            ENTRY_TICKETS,
        }
    },

    mounted() {
        this.created();
    },
    methods: {
        created() {
            api.get('/users/',)
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

                await api.post('/users/',
                    { name: this.name, email: this.email, privilege: this.privilege },
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