<template>
  <div class="guestss" style="margin-top: 3.75rem;">
    <div class="header guests">

      <input class="nosubmit search" @input="searchGuest" type="form" v-model="search" placeholder="Unesi JMBAG">


      <h1 class="textfield" style="display: inline-block; margin-left: 12rem">{{this.nomatch}} </h1>
    </div>

    <div class="grid-container guests">
      <h1 class="textfield">Ime </h1>
      <input class="inputfield" :disabled="this.id==''" type="text" @input="changevalue" v-model="name">

      <h1 class="textfield">Prezime </h1>
      <input class="inputfield" :disabled="this.id==''" type="text" @input="changevalue" v-model="surname">

      <h1 class="textfield">JMBAG </h1>
      <input class="inputfield" readonly type="text" v-model="jmbag">

      <h1 class="textfield">Karta </h1>

      <button class="button change" :disabled="this.id==''" v-if="guest.bought == '1'"
        @click="changebought(guest, '0')">
        <img src="../../assets/icons/yes-icon.svg">
      </button>
      <button class="button change" :disabled="this.id==''" v-else @click="changebought(guest, '1') "
        style="background-color: white;">
        <img class="image1" src="../../assets/icons/no-icon.svg">
      </button>

      <h1 class="textfield">Potvrda </h1>
      <h1 class="textfield">{{this.confCode}} </h1>
    </div>

  </div>

</template>




<script>
import { uuid } from 'vue-uuid';
import GuestsAdd from '@/components/Bruckarte/GuestsAdd.vue'
import GuestsTable from '@/components/Bruckarte/GuestsTable.vue'
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
      mails: [],
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
      confCode: '',

      uuid: uuid.v1(),

    }
  },
  mounted() {
    this.created();
  },
  methods: {
    loggg() {
    },
    created() {
      axios.get(process.env.VUE_APP_BASE_URL + '/mailer/',)
        .then(response => {
          this.mails = response.data;
        })
    },
    changevalue() {
      if (this.guest != '') {
        axios.put(process.env.VUE_APP_BASE_URL + '/guests/' + this.guest.id + '/',
          { name: this.name, surname: this.surname },
          { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
        )
      }
    },
    changebought(guest, changenum) {

      if (this.name == "" || this.surname == "") {
        window.alert("Ispunite polja ime i prezime!")
      } else {
        if (changenum == 1) {
          var confCode = this.$uuid.v1();

        } else {
          var confCode = "";
        }
        axios.put(process.env.VUE_APP_BASE_URL + '/guests/' + guest.id + '/',
          { bought: changenum, confCode: confCode },
          { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
        )
          .then(() => {
            guest.bought = changenum;
            guest.confCode = confCode;
            this.confCode = confCode;

            if (changenum == 1) {
              this.sendMail(guest);
            }
          })
      }
    },
    searchGuest() {
      axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=Brucoši ' + this.search + "&search_fields=tag&search_fields=jmbag",)
        .then(response => {
          this.guests = response.data;
          if (this.guests.length == 1) {
            this.nomatch = "";
            this.guest = this.guests[0];
            this.id = this.guest.id;
            this.name = this.guest.name;
            this.surname = this.guest.surname;
            this.jmbag = this.guest.jmbag;
            this.jmbag = this.guest.jmbag;
            this.confCode = this.guest.confCode;

          } else if (this.guests.length == 0) {
            this.nomatch = "JMBAG nije pronađen!";
            this.id = "";
            this.name = "";
            this.surname = '';
            this.jmbag = '';
            this.confCode = '';

          }
          else {
            this.nomatch = "";
            this.id = '';
            this.name = '';
            this.surname = '';
            this.jmbag = '';
            this.confCode = '';

            this.bought = '0';
          }
        })
    },
    sendMail(guest) {
      var ids = [];
      var nextId = '';
      this.mails.forEach(element => {
        ids.push(element.id);
      });
      for (let index = 0; index < ids.length; index++) {
        if (ids.includes(String(index)) == false) {
          nextId = index;
          break;
        }
      }
      if (nextId == '') {
        nextId = ids.length;
      }
      console.log("send mail attempt")

      var jmbagslice = guest.jmbag;
      if (jmbagslice.slice(0, 2) == "00") {
        jmbagslice = jmbagslice.slice(4, 9);
      } else {
        jmbagslice = jmbagslice.slice(2, 7);
      }

      var e_name= this.name[0].toLowerCase()
      if(e_name=="č"){
        e_name="c";
      }else if(e_name=="š"){
        e_name="s";
      }else if(e_name=="ž"){
        e_name="z";
      }else if(e_name=="đ"){
        e_name="d";
      }else if(e_name=="ć"){
        e_name="c";
      }

      var e_surname= this.surname[0].toLowerCase()
      if(e_surname=="č"){
        e_surname="c";
      }else if(e_surname=="š"){
        e_surname="s";
      }else if(e_surname=="ž"){
        e_surname="z";
      }else if(e_surname=="đ"){
        e_surname="d";
      }else if(e_surname=="ć"){
        e_surname="c";
      }


      var email = e_name + e_surname + jmbagslice + "@fer.hr";

      var msg=this.name+" "+this.surname+" "+guest.confCode

      axios.post(process.env.VUE_APP_BASE_URL + '/mailer/',
        {
          id: nextId, subject: "[#BRUCIFER22] Potvrda za kupljenu kartu",
          message: msg,
          name: this.name,
          confCode: guest.confCode,
          to_mail: email
        },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      ).then(response => {
        axios.post(process.env.VUE_APP_BASE_URL + '/mailer/' + nextId + '/send_mail/',
          {
            subject: "[#BRUCIFER22] Potvrda za kupljenu kartu",
            message: msg,
            name: this.name,
            confCode: guest.confCode,
            to_mail: email
          },
          { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
        )
      }).then(response => {
        this.created();
      })
    },
  }

}
</script>

<style lang="scss" scope>
@import url('https://fonts.cdnfonts.com/css/montserrat');
@import '../../assets/scss/Admin-scss/gird-view.scss';

.header.guests {
  height: 7.188rem;
  width: 100%;
  border-bottom: 1px solid black;
}

.nosubmit.search {
  position: absolute;
  margin-top: 2.375rem;
  width: 20%;
  left:6%;
}

.grid-container.guests {
  margin-top: 3.5%;
  margin-left: 5%;
  row-gap: 18%;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}



input[type="search"] {
  border: none;
  background: transparent;
  margin: 0;
  padding: 7px 8px;
  font-size: 14px;
  color: inherit;
  border: 1px solid transparent;
  border-radius: inherit;
}

input[type="search"]::placeholder {
  color: #bbb;
}

button[type="submit"] {
  text-indent: -999px;
  overflow: hidden;
  width: 40px;
  padding: 0;
  margin: 0;
  border: 1px solid transparent;
  border-radius: inherit;
  background: transparent url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' class='bi bi-search' viewBox='0 0 16 16'%3E%3Cpath d='M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z'%3E%3C/path%3E%3C/svg%3E") no-repeat center;
  cursor: pointer;
  opacity: 0.7;
}

button[type="submit"]:hover {
  opacity: 1;
}

button[type="submit"]:focus,
input[type="search"]:focus {
  box-shadow: 0 0 3px 0 #1183d6;
  border-color: #1183d6;
  outline: none;
}

form.nosubmit {
  border: none;
  padding: 0;
}

input.nosubmit {
  left: 6%;
  width: 40.6%;
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  border: 1px solid #555;
  padding: 9px 4px 9px 40px;
  background: transparent url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' class='bi bi-search' viewBox='0 0 16 16'%3E%3Cpath d='M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z'%3E%3C/path%3E%3C/svg%3E") no-repeat 13px center;
}

@media screen and (max-width: 980px) {
  .nosubmit.search {
    width: 40%;
    font-size: 12px;
  }

  .inputfield {
    width: 80% !important;
  }
}
</style>

