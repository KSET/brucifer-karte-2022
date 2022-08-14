<template>
    <div id="guests-add">
        <br><br><br>
        <form @submit="postGuest">
            <h>Ime: </h>
            <input type="text" @input="changevalue" id="inputname" v-model="name" placeholder="Surname">
            <br>
            <br>
            <h>Prezime: </h>
            <input type="text" @input="changevalue" id="inputsurname" v-model="surname" placeholder="Surname">
            <br><br>
            <h>Tag: </h>

            <select v-model="selectedTag" name={{selectedTag}} id={{selectedTag}}>
                <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
            </select>
            <br>
            <br>
            <h>JMBAG: </h>
            <input type="text" id="inputjmbag" v-model="jmbag" placeholder="JMBAG">
            <br><br>
            <h>Karta: </h>

            <button v-if="karta == '1'" class="btn btn-xs btn-success" id="gumbary" type="button"
                @click="changeKarta()">
                <font-awesome-icon icon="fa-solid fa-check" />
            </button>
            <button v-else @click="changeKarta()" type="button" class="btn btn-xs btn-danger" id="gumbarn">
                <font-awesome-icon icon="fa-solid fa-xmark" />
            </button><br><br>

            <h>Ulaz: </h>

            <button v-if="ulaz == '1'" type="button" class="btn btn-xs btn-success" id="gumbary" @click="changeUlaz()">
                <font-awesome-icon icon="fa-solid fa-check" />
            </button>
            <button v-else @click="changeUlaz()" type="button" class="btn btn-xs btn-danger" id="gumbarn">
                <font-awesome-icon icon="fa-solid fa-xmark" />
            </button><br><br>
            <button class="btn btn-primary" id="gumb2">Add</button>
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
            console.log( this.name)
            console.log(this.surname)
            console.log(this.jmbag )
            console.log(this.selectedTag)
            console.log(this.karta)
            console.log( this.ulaz)

            axios.post('http://127.0.0.1:8000/guests/',
                { id: this.nextId, name: this.name, surname: this.surname, jmbag: this.jmbag, tag: this.selectedTag, bought: this.karta, entered: this.ulaz },
                { auth: { username: process.env.VUE_APP_AUTH_USER, password: VUE_APP_AUTH_PASS } }
            )
                .then(() => {
                })
                
        }
    }
}
</script>


<style>
#inputname {
    width: 220px;
    margin: 2px;
}

#inputsurname {
    width: 220px;
    margin: 2px;
}


#gumb2 {
    padding: 0px;
    margin: 2px;
    width: 220px;
    height: 30px;
    text-align: center;
}
</style>


