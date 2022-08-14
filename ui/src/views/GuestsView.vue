<template>
  <div class="guestss">
    <br>
    <br>
    <br>
    <br>
    <h>Search: </h>
    <input @input="searchGuest" type="form" id="searchgumb" v-model="search">
    <br><br>

    <br>
    <h>Ime: </h>
    <input type="text"  @input="changevalue" id="inputname" v-model="name" placeholder="Surname">
    <br>
    <br>
    <h>Prezime: </h>
    <input type="text" @input="changevalue" id="inputsurname" v-model="surname" placeholder="Surname">
    <br>
    <br>
    <h>JMBAG: </h>
    <input type="text" readonly id="inputjmbag" v-model="jmbag" placeholder="JMBAG">
    <br>
    <br>
    <h>Karta: </h>
    
    <button v-if="guest.bought == '1'" class="btn btn-xs btn-success" id="gumbary" @click="changebought(guest, '0')">
      <font-awesome-icon icon="fa-solid fa-check" />
    </button> 
    <button v-else @click="changebought(guest, '1')"  class="btn btn-xs btn-danger" id="gumbarn">
      <font-awesome-icon icon="fa-solid fa-xmark" />
    </button><br>
    <br>


  </div>

</template>




<script>
import GuestsAdd from '../components/Guests/GuestsAdd.vue'
import GuestsTable from '../components/Guests/GuestsTable.vue'
import axios from 'axios'
export default {
  name: 'GuestsView',
  components: {

    GuestsTable,
    GuestsAdd

  },
  data() {
    return {
      guest: '',
      guests: [],
      id: '',
      name: '',
      surname: '',
      jmbag: '',
      phone: '',
      tag: '',
      bought: '',
      entered: '',
      deleted: '',
    }
  },
  methods: {
    loggg() {
      console.log(document.getElementById("contentedit").getAttribute('value'))
    },
    created() {
      axios.get('http://127.0.0.1:8000/guests/?search=Brucoši&search_fields=tag',)

        .then(response => {
          this.guests = response.data;
        })
    },
    changevalue() {
      if (this.guest != '') {
        axios.put('http://127.0.0.1:8000/guests/' + this.guest.id + '/',
          { name: this.name, surname: this.surname },
          { auth: { username: process.env.VUE_APP_AUTH_USER, password: process.env.VUE_APP_AUTH_PASS } }
        )
      }
    },
    changebought(guest, changenum) {
      axios.put('http://127.0.0.1:8000/guests/' + guest.id + '/',
        { bought: changenum },
        { auth: { username: process.env.VUE_APP_AUTH_USER, password: process.env.VUE_APP_AUTH_PASS } }
      )
        .then(() => {
          guest.bought=changenum;
        })
    },
    searchGuest() {
      axios.get('http://127.0.0.1:8000/guests/?search=Brucoši ' + this.search + "&search_fields=tag&search_fields=jmbag",)
        .then(response => {
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
          else {
            this.name = '';
            this.surname = '';
            this.jmbag = '';
            this.bought='0';
          }
        })
    }
  }

}
</script>

<style scoped>
</style>

