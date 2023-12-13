<template>
  <div>
    <Sidebar />
    <div class="admin-page-container" style="padding-top: 0px;">
      <div class="grid-container-contact" style="padding-top: 0px;">
        <div style="border-right: 1px solid black; width: 100%">
          <div style="display: flex;">

            <h1 class="page-title lineup-title" style="padding-top: 20px">Popis Artikala</h1>

            <img v-if="this.showContactForm == false" style="margin-top: 15px;" class="dropdown-icon showMobile"
              src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleContactForm">
            <img v-else class="dropdown-icon  showMobile" style="margin-top: 15px;"
              src="@/assets/icons/dopdwn-open-icon.svg" @click="toggleContactForm">
          </div>

          <form v-if="showHid" id="hid" class="inputfields" @submit.prevent="postArtikl">

            <div class="form-group">
              <h1 class="textfield">Ime Artikla</h1>
              <input required class="inputfield kontakt" type="text" v-model="name">
            </div>

            <div class="form-group">
              <h1 class="textfield">Kategorija Artikla</h1>
              <div style="position:relative; width: 90%; margin-bottom:30px">
                <select id="selector" class="inputfield entry" v-model="selectedTag" @input="searchGuest">
                  <option v-for="(item, index) in tags" :key="index">{{ item }}</option>
                </select>
                <div class="dropdownTab-icon"></div>
              </div>
            </div>

            <div class="form-group">
              <h1 class="textfield">Cijena u EUR</h1>
              <input required class="inputfield kontakt" type="text" v-model="priceEUR">
            </div>

            <div class="form-group">
              <h1 class="textfield">Količina u L</h1>
              <input required class="inputfield kontakt" type="text" v-model="volume">
            </div>

            <button type="submit" class="button submit">Dodaj</button>

          </form>
        </div>

        <div class="kontakt-table" style="padding-top: 20px">
          <div class=row style="border-left: 0px;">
            <table id="guests">
              <div class="thead-artikli">
                <p>Artikl</p>
                <p>Cijena EUR</p>
                <p>Količina</p>
                <p>Opcije</p>
              </div>
              <tbody :class="{ [$style.tbodyHigh]: this.tbodyHigh }" style="overflow:auto; " class="tbody">
                <div class="grid-artikli" v-for="artikl in artikli" :key="artikl.id">
                  <p>{{ artikl.name }}</p>
                  <p v-if="artikl.tag != 'OSTALO'">{{ artikl.volume }} L</p>
                  <p v-else>{{ artikl.volume }}</p>
                  <p>{{ artikl.priceEUR }}</p>
                  <p><button class="button-icon" @click="orderUp(artikl)">
                      <img src="@/assets/icons/arrow-up-icon.svg"></button> </p>


                  <p><button class="button-icon" @click="orderDown(artikl)">
                      <img src="@/assets/icons/dopdwn-notopen-icon.svg"></button> </p>




                  <p style="grid-column: 1/4;">{{ artikl.tag }}</p>

                  <p><button class="button-icon" @click="deleteArtikl(artikl)">
                      <img src="@/assets/icons/trash-icon.svg"></button> </p>


                </div>
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
      showContactForm: true,
      showHid: false,
      tbodyHigh: false,

      tags: ["SOK", "PIVO", "DOLJEVI", "ALKOHOL", "OSTALO"],

      selectedTag: '',
      priceEUR: '',
      artikli: [],

    }
  },

  mounted() {
    this.showHid = true;
    this.created();
  },

  methods: {
    async created() {
      this.artikli = [];
      this.tags.forEach(async element => {
        const resp = await axios.get(process.env.VUE_APP_BASE_URL + '/cjenik/?ordering=order&search=' + element + '&search_fields=tag',)
        if (resp.data.length != 0) {
          resp.data.forEach(element => {
            this.artikli.push(element)
          });
        }
      });
    },

    async orderUp(artikl) {
      let curIndex = this.artikli.indexOf(artikl);
      let nextIndex = curIndex - 1;
      let nextArtikl = this.artikli[nextIndex]

      if (curIndex != "0") {
        if (artikl.tag == nextArtikl.tag) {
          await axios.put(process.env.VUE_APP_BASE_URL + '/cjenik/' + artikl.id + '/',
            { order: nextArtikl.order },
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } })

          await axios.put(process.env.VUE_APP_BASE_URL + '/cjenik/' + nextArtikl.id + '/',
            { order: artikl.order },
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } })
        }
        window.location.reload();
      }
    },
    async orderDown(artikl) {
      let curIndex = this.artikli.indexOf(artikl);
      let nextIndex = curIndex + 1;
      let nextArtikl = this.artikli[nextIndex]

      if (nextIndex != this.artikli.length) {
        if (artikl.tag == nextArtikl.tag) {
          await axios.put(process.env.VUE_APP_BASE_URL + '/cjenik/' + artikl.id + '/',
            { order: nextArtikl.order },
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } })

          await axios.put(process.env.VUE_APP_BASE_URL + '/cjenik/' + nextArtikl.id + '/',
            { order: artikl.order },
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } })
        }
        this.created()
      }
    },
    calculateEUR() {
      const tečajEUR = 7.53450;
      this.priceEUR = Math.round(((this.priceHRK / tečajEUR)) * 100) / 100
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

    async postArtikl() {
      const resp = await axios.get(process.env.VUE_APP_BASE_URL + '/cjenik/?ordering=order&search=' + this.selectedTag + '&search_fields=tag',)
      let nextOrder = "00";

      let cjenik = resp.data;

      if ((cjenik.length) != 0) {
        let lastOrder = cjenik[cjenik.length - 1].order;

        if (lastOrder[0] == "0") {
          if (lastOrder == "09") {
            nextOrder = "10"
          }
          else {
            nextOrder = "0" + (parseInt(lastOrder[1]) + 1).toString();
          }
        } else {
          nextOrder = (parseInt(lastOrder) + 1).toString();
        }
      }

      axios.post(process.env.VUE_APP_BASE_URL + '/cjenik/',
        { name: this.name, tag: this.selectedTag, order: nextOrder, priceEUR: this.priceEUR, volume: this.volume },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      ).then(() => {
        this.created()
      })

    },
    deleteArtikl(artikl) {
      axios.delete(process.env.VUE_APP_BASE_URL + '/cjenik/' + artikl.id + '/',
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created()
        })
    }

  }
}
</script>

<style module>
:global(#app) .tbodyHigh {
  height: 100%;
}
</style>

<style>
.dropdownTab-icon {
  position: absolute;
  right: 10px;
  top: 55%;
  transform: translateY(-50%);
  cursor: pointer;
  background-size: contain;
  background-repeat: no-repeat;
  width: 16px;
  height: 16px;
  background-image: url('../../assets/icons/dopdwn-notopen-icon.svg');
}

.tagDropdown-icon {
  background-image: url('../../assets/icons/dopdwn-notopen-icon.svg');
}

.grid-artikli {
  display: grid;
  padding: 10px;
  grid-template-columns: 28% 20% 25% 5% 5%;
  border-bottom: 1px solid black;
  row-gap: 20px;
  padding-left: 5px;
}

.thead-artikli {
  font-family: 'Montserrat';
  display: grid;
  padding: 10px;
  grid-template-columns: 28% 20% 25% 10%;
  border-bottom: 1px solid black;
  row-gap: 20px;
  padding-left: 5px;
}
</style>