<template>
  <div class="guestss">
    <div class="header guests">
    <h1 class="textfield"></h1>
    <h1 class="line1"></h1>
    <input class="inputfield search" @input="searchGuest" type="form"  v-model="search" placeholder="Unesi JMBAG">
    <img class="icon1" src="../../assets/icons/search-icon.svg">
    <h1 class="textfield">{{this.nomatch}} </h1>
  </div>

  <div class="grid-container guests">
    <h1 class="textfield">Ime </h1>
    <input class="inputfield" :disabled="this.id==''" type="text" @input="changevalue"  v-model="name" >
    
    <h1 class="textfield">Prezime </h1>
    <input class="inputfield" :disabled="this.id==''" type="text"  @input="changevalue"  v-model="surname">
    
    <h1 class="textfield">JMBAG </h1>
    <input class="inputfield" readonly  type="text" v-model="jmbag">
    
    <h1 class="textfield">Karta </h1>
    
    <button class="button change" :disabled="this.id==''" v-if="guest.bought == '1'"  @click="changebought(guest, '0')">
      <img src="../../assets/icons/yes-icon.svg">
    </button> 
    <button class="button change" :disabled="this.id==''" v-else @click="changebought(guest, '1') " style="background-color: white;" >
      <img class="image1" src="../../assets/icons/no-icon.svg">
    </button>
    
  </div>

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
      nomatch: '',
      
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
            this.nomatch="";
            this.guest = this.guests[0];
            this.id=this.guest.id;
            this.name = this.guest.name;
            this.surname = this.guest.surname;
            this.jmbag = this.guest.jmbag;
          } else if (this.guests.length == 0) {
            this.nomatch="JMBAG nije pronađen!";
            this.id="";
            this.name = "";
            this.surname = '';
            this.jmbag = '';
          }
          else {
            this.nomatch="";
            this.id = '';
            this.name = '';
            this.surname = '';
            this.jmbag = '';
            this.bought='0';
          }
        })
    },
    sendMail() {
      
    }
  }

}
</script>

<style lang="scss" scope>
@import '../../assets/scss/Admin-scss/gird-view.scss';


.header.guests{
  height: 7.188rem;
  width: 100%;
  border-bottom: 1px solid black;
}

.inputfield.search{
  margin-top: 2.5%;
  margin-left: 4%;
  width: 20%;
  padding-left: 3%;
}

.grid-container.guests{
  margin-top: 3.5%;
  margin-left: 5%;
  row-gap: 45%;

}
</style>

