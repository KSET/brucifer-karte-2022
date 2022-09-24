<template>
  <div>
    <Sidebar />
    <div class="admin-page-container">
      <div class="grid-container-contact">
        <div>
          <h1 class="page-title lineup-title">Dodavanje izvođača</h1>

          <img v-if="this.showContactForm==false" style="margin-top: 15px;" class="dropdown-icon showmobile" src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleContactForm">
            <img v-else class="dropdown-icon  showmobile" style="margin-top: 15px;" src="@/assets/icons/dopdwn-open-icon.svg" @click="toggleContactForm">

          <form id="hid" @submit="postBandContact" class="inputfields">

            <h1 class="textfield">Ime Benda </h1>
            <input required class="inputfield kontakt" type="text" v-model="bandName">

            <h1 class="textfield">Ime i prezime bookera </h1>
            <input required class="inputfield kontakt" type="text" v-model="bookerName">

            <h1 class="textfield">Broj mobitela bookera </h1>
            <input required class="inputfield kontakt" type="text" v-model="bookerPhone">

            <button class="button submit">Dodaj</button>

          </form>
        </div>
        <div class="kontakt-table">
          <div class=row>
            <table id="guests">
              <thead>
                <th>Bend</th>
                <th>Booker</th>
                <th>Kontakt</th>
                <th>Opcije</th>
              </thead>
              <tbody style="overflow:auto;" class="tbody" id="tbody">
                <tr  v-for="bandcontact in bandcontacts" :key="bandcontact.id">
                  <td>{{bandcontact.bandName}}</td>
                  <td>{{bandcontact.bookerName}}</td>
                  <td>{{bandcontact.bookerPhone}}</td>
                  <td><button class="button-icon" @click="deleteBandContact(bandcontact)"> <img
                        src="@/assets/icons/trash-icon.svg"></button>
                  </td>
                </tr>
              </tbody>
            </table>

          </div>
        </div>

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
      bandcontacts: [],
      bandName: '',
      bookeraName: '',
      bookerPhone: '',
      nextId:'',
      showContactForm:true,
    }
  },
  mounted() {
    document.getElementById("hid").style.display = "block";

    this.created();
  },

  methods: {
    created() {
      axios.get('http://127.0.0.1:8000/contact/',)
        .then(response => {
          this.bandcontacts = response.data;
          this.len = this.bandcontacts.length;
        })
    },
    toggleContactForm(){
      this.showContactForm = !this.showContactForm;
            if (this.showContactForm) {
                document.getElementById("hid").style.display = "block";
                document.getElementById("tbody").style.height = "250px";

            } else {
                document.getElementById("hid").style.display = "none";
                document.getElementById("tbody").style.height = "100%";

            }
    },

    postBandContact() {

      var ids = [];
      this.bandcontacts.forEach(element => {
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


      axios.post('http://127.0.0.1:8000/contact/',
        { id: this.nextId, bandName: this.bandName, bookerName: this.bookerName, bookerPhone: this.bookerPhone },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
        })

    },
    deleteBandContact(bandcontact) {
      axios.delete('http://127.0.0.1:8000/contact/' + bandcontact.id + '/',
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created();
        })
    }

  }
}
</script>

<style>
  
.grid-container-contact {
  display: grid;
  grid-template-columns: 30% 40%;
  padding: 10px;
  width: 100vw;
  height: 87vh;
}

.kontakt-table {
  position: relative;
  width: 100%;
  padding-left: 5px;
}

.inputfield.kontakt {
  margin-top: 10px;
  margin-bottom: 30px;
  display: block;
  width: 90%;
}

@media screen and (max-width: 550px) {
    .grid-container-contact{
      display: flex !important;
      flex-direction: column;
    }
    .inputfield.kontakt {
  margin: 2px;
}
.page-title.lineup-title{
  padding-bottom: 5px;
}
.tbody{
  position: relative;
  height: 250px;
}
   


@media screen and (max-width: 550px) {


  .page-title {
    font-size: 16px;
  }

  .textfield {
    font-size: 12px;
  }
}
}
</style>