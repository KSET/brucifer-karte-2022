<template>
  <div class="guestss">
    <h1 id="textfield0"></h1>
    <h1 id="line1"></h1>
    <input id="search-field" @input="searchGuest" type="form"  v-model="search" placeholder="Unesi JMBAG">
    <img id="icon1" src="../../assets/icons/search-icon.svg">
    <h1 id="textfield1">Ime </h1>
    <input id="inputfield1" type="text" @input="changevalue"  v-model="name" >
    
    <h1 id="textfield2">Prezime </h1>
    <input id="inputfield2" type="text"  @input="changevalue"  v-model="surname">
    
    <h1 id="textfield3">JMBAG </h1>
    <input id="inputfield3" readonly  type="text" v-model="jmbag">
    
    <h1 id="textfield4">Karta </h1>
    
    <button id="button1-yes" v-if="guest.bought == '1'"  @click="changebought(guest, '0')">
      <img src="../../assets/icons/yes-icon.svg">
    </button> 
    <button id="button1-no" v-else @click="changebought(guest, '1')" >
      <img id="image1" src="../../assets/icons/no-icon.svg">
    </button>
    


  </div>

</template>




<script>
import emailjs from 'emailjs-com';
import GuestsAdd from '@/components/Guests/GuestsAdd.vue'
import GuestsTable from '@/components/Guests/GuestsTable.vue'
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
          { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
        )
      }
    },
    changebought(guest, changenum) {
      axios.put('http://127.0.0.1:8000/guests/' + guest.id + '/',
        { bought: changenum },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          guest.bought=changenum;
          if(changenum==1){
            this.sendConfMail(guest);
          }
        })
    }, 
    sendConfMail(guest){
      var jmbagslice = guest.jmbag;
      if(jmbagslice.slice(0,2)=="00"){
        jmbagslice= jmbagslice.slice(4,9);
      }else{
        jmbagslice=jmbagslice.slice(2,7);
      }

      var email= guest.name[0].toLowerCase() + guest.surname[0].toLowerCase() + jmbagslice +"@fer.hr";

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

<style lang="scss" scope>
@import '../../assets/scss/GuestsView.scss';
</style>

