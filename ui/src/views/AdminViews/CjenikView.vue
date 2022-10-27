<template>
  <div>
    <Sidebar />
    <div class="admin-page-container" style="padding-top: 0px;">
      <div class="grid-container-contact" style="padding-top: 0px;">
        <div style="border-right: 1px solid black; width: 95%">
          <h1 class="page-title lineup-title" style="padding-top: 20px">Popis Artikala</h1>

          <img v-if="this.showContactForm == false" style="margin-top: 15px;" class="dropdown-icon showmobile"
            src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleContactForm">
          <img v-else class="dropdown-icon  showmobile" style="margin-top: 15px;"
            src="@/assets/icons/dopdwn-open-icon.svg" @click="toggleContactForm">

          <form v-if="showHid" id="hid" class="inputfields" onsubmit="return false">

            <h1 class="textfield">Ime Arikla </h1>
            <input required class="inputfield kontakt" type="text" v-model="name">

            <h1 class="textfield">Kategorija Artikla </h1>
            <select id="selector" class="inputfield entry" v-model="selectedTag" name={{selectedTag}}
              @input="searchGuest" style="margin-bottom: 30px;">
              <option v-for="(item, i) in tags" :key="i" class="menu-item">{{ item }}</option>
            </select>


            <div class="grid-container" style="grid-template-columns: 30% 30%; margin-bottom: 20px">
              <h1 class="textfield">Cijena u HRK</h1>
              <h1 class="textfield">Cijena u EUR </h1>

              <input required class="inputfield kontakt" type="text" v-model="priceHRK" @input="calculateEUR">
              <input required class="inputfield kontakt" type="text" v-model="priceEUR">

            </div>
            <h1 class="textfield">Količina u L </h1>
            <input required class="inputfield kontakt" type="text" v-model="volume">
            <button class="button submit" @click="postArtikl">Dodaj</button>

          </form>
        </div>

        <div class="kontakt-table" style="padding-top: 20px">
          <div class=row>
            <table id="guests">
              <thead>
                <th>Artikl</th>
                <th>Cijema HRK</th>
                <th>Cijena EUR</th>
                <th>Opcije</th>
              </thead>
              <tbody :class="{ [$style.tbodyHigh]: this.tbodyHigh }" style="overflow:auto; " class="tbody">
                <div class="grid-artikli" v-for="artikl in artikli" :key="artikl.id">
                  <p>{{ artikl.name }}</p>
                  <p>{{ artikl.priceHRK }}</p>
                  <p>{{ artikl.priceEUR }}</p>
                  <p><button class="button-icon" @click="deleteArtikl(artikl)">
                      <img src="@/assets/icons/arrow-up-icon.svg"></button> </p>


                  <p><button class="button-icon" @click="deleteArtikl(artikl)">
                      <img src="@/assets/icons/dopdwn-notopen-icon.svg"></button> </p>

                  <p style="grid-column: 1/6;">{{ artikl.volume }} L</p>

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

      tags: ["BEZALKOHOLNA PIĆA", "PIVO", "VINO", "ŽESTOKA PIĆA", "OSTALO"],

      selectedTag: '',
      priceHRK: '',
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
      this.artikli=[];
      this.tags.forEach(async element => {
        console.log(element)
        const resp = await axios.get(process.env.VUE_APP_BASE_URL + '/cjenik/?search=' + element + '&search_fields=tag',)
        if(resp.data.length!=0){
          resp.data.forEach(element => {
            console.log(this.artikli)
            this.artikli.push(element)
          });
        }
      });
      console.log(this.artikli)

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



      console.log(nextOrder)
      await axios.post(process.env.VUE_APP_BASE_URL + '/cjenik/',
        { name: this.name, tag: this.selectedTag, order: nextOrder, priceHRK: this.priceHRK, priceEUR: this.priceEUR, volume: this.volume },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
      this.created();

    },
    deleteArtikl(artikl) {
      axios.delete(process.env.VUE_APP_BASE_URL + '/cjenik/' + artikl.id + '/',
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created();
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
.grid-artikli {
  display: grid;
  grid-template-columns: 35% 20% 25% 5% 5%;
  border-bottom: 1px solid black;
  row-gap: 20px;
}

.grid-container-contact {
  display: grid;
  grid-template-columns: 30% 40%;
  width: 100vw;
  height: 87vh;
  align-content: stretch;
  justify-items: center;
}

.kontakt-table {
  position: relative;
  width: 100%;
  margin-left: 0px;
}

.inputfield.kontakt {
  margin-top: 10px;
  margin-bottom: 30px;
  display: block;
  width: 90%;
}

.row {
  padding: 0px;
  border-left: 1px solid;
}

#guests th {
  padding-left: 20px
}

@media screen and (max-width: 900px) {

  .grid-container-contact {
    display: grid;
    grid-template-columns: 40% 60%;
    padding: 10px;
    width: 100vw;
    height: 87vh;
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