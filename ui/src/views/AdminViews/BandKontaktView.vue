<template>
  <div>
    <Sidebar />

    <div class="admin-page-container" style="padding-top: 0px;">
      <div class="grid-container-contact" style="padding-top: 0px;">
        <div style="border-right: 1px solid black; width: 100% !important">
          <div style="display: flex;">
            <h1 class="page-title lineup-title" style="padding-top: 20px">Popis kontakata</h1>

            <img v-if="this.showContactForm == false" style="margin-top: 15px;" class="dropdown-icon showMobile"
              src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleContactForm">
            <img v-else class="dropdown-icon  showMobile" style="margin-top: 15px;"
              src="@/assets/icons/dopdwn-open-icon.svg" @click="toggleContactForm">
          </div>
          <form v-if="showHid" id="hid" class="inputfields" @submit.prevent="postBandContact">

            <h1 class="textfield">Ime Benda </h1>
            <input required class="inputfield kontakt" type="text" v-model="bandName">

            <h1 class="textfield">Ime i prezime bookera </h1>
            <input required class="inputfield kontakt" type="text" v-model="bookerName">

            <h1 class="textfield">Broj mobitela bookera </h1>
            <input required class="inputfield kontakt" type="text" v-model="bookerPhone">

            <button type="submit" class="button submit">Dodaj</button>

          </form>
        </div>

        <div class="kontakt-table" style="padding-top: 20px">
          <div class=row style="border-left: 0px;">
            <table id="guests">
              <thead>
                <th>Bend</th>
                <th>Booker</th>
                <th>Kontakt</th>
                <th>Opcije</th>
              </thead>
              <tbody :class="{ [$style.tbodyHigh]: this.tbodyHigh }" class="tbody">
                <tr v-for="bandcontact in bandcontacts" :key="bandcontact.id">
                  <td>{{ bandcontact.bandName }}</td>
                  <td>{{ bandcontact.bookerName }}</td>
                  <td @click="call(bandcontact)"><a>{{ bandcontact.bookerPhone }}</a></td>
                  <td style="padding-left: 30px"><button class="button-icon" @click="deleteBandContact(bandcontact)">
                      <img src="@/assets/icons/trash-icon.svg"></button>
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
    Sidebar,
  },
  props: {
    msg: String
  },
  data() {
    return {
      bandcontacts: [],
      bandName: '',
      bookerName: '',
      bookerPhone: '',
      showContactForm: true,
      showHid: false,
      tbodyHigh: false,
    }
  },
  mounted() {
    this.showHid = true;

    this.created();
  },

  methods: {
    call(bandcontact) {
      let tel = "tel:" + bandcontact.bookerPhone
      window.open(tel);
    },
    created() {
      axios.get(process.env.VUE_APP_BASE_URL + '/contact/',)
        .then(response => {
          this.bandcontacts = response.data;
          this.len = this.bandcontacts.length;
        })
    },
    toggleContactForm() {
      this.showContactForm = !this.showContactForm;
      if (this.showContactForm) {
        this.showHid = true;
        this.tbodyHigh = false;
      } else {
        this.showHid = false;
        this.tbodyHigh = true;
      }
    },

    postBandContact() {
      if (this.bandName && this.bookerName && this.bookerPhone) {
        axios.post(process.env.VUE_APP_BASE_URL + '/contact/',
          { bandName: this.bandName, bookerName: this.bookerName, bookerPhone: this.bookerPhone },
          { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
        )
          .then(() => {
            this.bookerName = "";
            this.bookerPhone = "";
            this.bandName = "";
            this.created();
          })
      }
    },
    deleteBandContact(bandcontact) {
      axios.delete(process.env.VUE_APP_BASE_URL + '/contact/' + bandcontact.id + '/',
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created();
        })
    }

  }
}
</script>

<style module scoped>
:global(#app) .tbodyHigh {
  height: 100%;
}
</style>

<style>
.tbody {
  height: 100%;
  overflow: auto;
}

.grid-container-contact {
  display: grid;
  grid-template-columns: 30% 70%;
  width: 100%;
  height: 87vh;
  align-content: stretch;
  justify-items: center;
}

.kontakt-table {
  position: relative;
  width: 100%;
  margin-left: 0px;
  height: 100%;
}

.inputfield.kontakt {
  margin-top: 10px;
  margin-bottom: 30px;
  display: block;
  width: 90%;
}

.row {
  --bs-gutter-x: 0rem !important;
  padding: 0px;
  border-left: 0px solid;
  height: 100%;
}

#guests {
  height: 100%;
}

@media screen and (max-width: 900px) {

  .grid-container-contact {
    display: grid;
    grid-template-columns: 40% 60%;
    padding: 10px;
  }
}

@media screen and (max-width: 550px) {
  .grid-container-contact {
    display: flex !important;
    flex-direction: column;
  }

  .inputfield.kontakt {
    margin: 2px;
  }

  .page-title.lineup-title {
    padding-bottom: 5px;
  }

  .tbody {
    position: relative;
    height: 21.875rem;
  }



  @media screen and (max-width: 550px) {


    .page-title {
      font-size: 26px;
    }

    .textfield {
      font-size: 12px;
    }
  }
}
</style>