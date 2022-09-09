<template>
    <div id="upis">
        <br>
        <h1>Ime: </h1>
        <input type="text" id="inputname" v-model="name" placeholder="Name">
        <br>
        <br>
        <h1>Prezime: </h1>
        <input type="text" id="inputsurname" v-model="surname" placeholder="Surname">
        <br>
        <br>
        <h1>JMBAG: </h1>
        <input type="text" id="inputjmbag" v-model="jmbag" placeholder="JMBAG">
        <br>
        <br>
        <h1>e-mail: </h1>
        <input type="text" id="inputemail" v-model="email" placeholder="email">
        <br>
        <br>

        <button @click="postGuest" class="btn btn-primary" id="gumb3">Upiši se!</button>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Upis',

    props: {
        msg: String
    },
    data() {
        return {
            chosenguest: [],
            id: '',
            name: '',
            surname: '',
            jmbag: '',
            email: '',
            tag: '',
            bought: '',
            entered: '',
            deleted: '',
            len: '',
        }
    },
    created() {


    },
    methods: {
        postGuest() {

            axios.get('http://127.0.0.1:8000/guests/?search=' + this.jmbag + '&search_fields=jmbag',)
                .then(response => {
                    this.chosenguest = response.data;
                    if (response.data.length == 0) {
                        window.alert("kriv jmbag");
                    } else {
                        var osoba = this.chosenguest[0];
                        if (osoba.name != "") {
                            window.alert("podaci već ispunjeni, u slučaju pogreške javiti se na help@kset.org");
                        } else {
                            axios.put('http://127.0.0.1:8000/guests/' + osoba.id + '/',
                                { name: this.name, surname: this.surname, email: this.email },
                                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                            )
                        }

                    }
                })

        }
    }
}
</script>

<style>
</style>