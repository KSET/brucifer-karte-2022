<template>
  <div class="navbar admin">
    <router-link style="left:  1.7rem !important;" class="navbar-title" to="/admin/">
      #BRUCIFER
    </router-link>

    <div class="routes">

      <RouterElement v-if="privilege == '1' || privilege == '3' || privilege == '4'" class="navbar-element hidemobile"
        :name="'Brucoši'" :link="'/admin/guests'"></RouterElement>

      <RouterElement v-if="privilege == '1' || privilege == '2' || privilege == '4'" class="navbar-element hidemobile"
        :name="'Ulaz'" :link="'/admin/entry'"></RouterElement>

      <router-link v-if="privilege == '1'" class="navbar-element hidetablet" to="/admin/admin-panel">
        <img src="../../assets/icons/nav-burger.svg">
      </router-link>
      <div id="nav-icon3" style="  margin-left: 70px;" v-if="privilege != ''" class="navbar-element hidedesktop"
        @click="toggleNav">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
      <router-link v-if="privilege != '' && privilege != '0'" class="navbar-element lg" to="/admin/logout">
        <img src="../../assets/icons/logout-icon.svg">
      </router-link>



      <div id="myNav" class="overlay admin">
        <div class="overlay-content admin">
          <RouterElement class="overlay-element hidetablet showmobile"
            v-if="privilege == '1' || privilege == '3' || privilege == '4'" @click="toggleNav()" :name="'Brucoši'"
            :link="'/admin/guests'">
          </RouterElement>
          <RouterElement class="overlay-element hidetablet showmobile"
            v-if="privilege == '1' || privilege == '2' || privilege == '4'" @click="toggleNav()" :name="'Ulaz'"
            :link="'/admin/entry'">
          </RouterElement>
          <RouterElement class="overlay-element" v-if="privilege == '1'" @click="toggleNav()" :name="'Tagovi'"
            :link="'/admin/tags'">
          </RouterElement>
          <RouterElement class="overlay-element" v-if="privilege == '1'" @click="toggleNav()" :name="'Privilegije'"
            :link="'/admin/privileges'"></RouterElement>
          <RouterElement class="overlay-element" v-if="privilege == '1'" @click="toggleNav()" :name="'Korisnici'"
            :link="'/admin/users'">
          </RouterElement>
          <RouterElement class="overlay-element" v-if="privilege == '1'" @click="toggleNav()" :name="'Uvoz'"
            :link="'/admin/import'">
          </RouterElement>

          <button class="overlay-element" v-if="privilege == '1'" @click="ExportData()">
            Izvoz
          </button>


          <div class="sidbar-element" v-if="privilege == '1'" @click="toggleDropdownLineup">
            <RouterElement class="overlay-element" style="left: 0%; position: abosolute; display: inline-block;"
              :name="'Izvođači'">
            </RouterElement>
            <img v-if="this.showDropdownLineup==false" class="dropdown-icon"
              src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleDropdownLineup">
            <img v-else class="dropdown-icon" src="@/assets/icons/dopdwn-open-icon.svg" @click="toggleDropdownLineup">

          </div>
          <RouterElement id="dpL11" class="overlay-element" @click="toggleNav()" :name="'Pregled Izvođača'"
            style="margin-left: 30px;" :link="'/admin/lineup-list'">
          </RouterElement>
          <RouterElement id="dpL21" class="overlay-element" @click="toggleNav()" :name="'Dodavanje Izvođača'"
            style="margin-left: 30px;" :link="'/admin/lineup-add/0'">
          </RouterElement>

          <div class="sidbar-element" v-if="privilege == '1'" @click="toggleDropdownSponsors">
            <RouterElement class="overlay-element" style="left: 0%; position: abosolute; display: inline-block;"
              :name="'Sponzori'">
            </RouterElement>
            <img v-if="this.showDropdownSponsors==false" class="dropdown-icon" style="display: inline-block"
              src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleDropdownSponsors">
            <img v-else class="dropdown-icon" src="@/assets/icons/dopdwn-open-icon.svg" @click="toggleDropdownSponsors">

          </div>
          <RouterElement id="dpS11" class="overlay-element" @click="toggleNav()" :name="'Pregled Sponzora'"
            style="margin-left: 30px;" :link="'/admin/sponsors-list'">
          </RouterElement>
          <RouterElement id="dpS21" class="overlay-element" @click="toggleNav()" :name="'Dodavanje Sponzora'"
            style="margin-left: 30px;" :link="'/admin/sponsors-add/0'">
          </RouterElement>

          <RouterElement class="overlay-element" v-if="privilege == '1'" :name="'Dodaj Gosta'" @click="toggleNav()"
            :link="'/admin/guests-add'"></RouterElement>
          <RouterElement class="overlay-element" v-if="privilege == '1'" :name="'Kontakt'" @click="toggleNav()"
            :link="'/admin/band-kontakt'"></RouterElement>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from '@/store/index.js';
import RouterElement from '@/components/AdminPanel/RouterElement.vue'
import * as XLSX from 'xlsx'
import axios from 'axios'

export default {
  name: 'Navbar',
  el: '#app',
  components: {
    RouterElement
  },
  data() {
    return {
      route: '',
      showDropdownLineup: false,
      showDropdownSponsors: false,
    }
  },
  computed: {
    privilege() {
      return store.state.privilege;
    },
    name() {
      return store.state.name;
    }
  },
  mounted() {
    this.route = this.$route.path;
    document.getElementById("dpL11").style.display = "none";
    document.getElementById("dpL21").style.display = "none";
    document.getElementById("dpS11").style.display = "none";
    document.getElementById("dpS21").style.display = "none";
  },
  methods: {
    ExportData() {
      var filename = 'export_guests.xlsx';
      axios.get(process.env.VUE_APP_BASE_URL + '/guests/',)
        .then(response => {
          var data = response.data;
          var ws = XLSX.utils.json_to_sheet(data);
          var wb = XLSX.utils.book_new();
          XLSX.utils.book_append_sheet(wb, ws, "People");
          XLSX.writeFile(wb, filename);
        });


    },
    toggleNav() {
      document.getElementById("nav-icon3").classList.toggle('open');
      if (this.showNav) {
        document.getElementById("myNav").style.height = "0%";
      } else {
        document.getElementById("myNav").style.height = "100%";
      }
      this.showNav = !this.showNav;
    },
    toggleDropdownLineup() {
      this.showDropdownLineup = !this.showDropdownLineup;
      if (this.showDropdownLineup) {
        document.getElementById("dpL11").style.display = "block";
        document.getElementById("dpL21").style.display = "block";
      } else {
        document.getElementById("dpL11").style.display = "none";
        document.getElementById("dpL21").style.display = "none";
      }
    },
    toggleDropdownSponsors() {
      this.showDropdownSponsors = !this.showDropdownSponsors;
      if (this.showDropdownSponsors) {
        document.getElementById("dpS11").style.display = "block";
        document.getElementById("dpS21").style.display = "block";
      } else {
        document.getElementById("dpS11").style.display = "none";
        document.getElementById("dpS21").style.display = "none";
      }
    },
  }
}


</script>
<style lang="scss">
.navbar {
  overflow: hidden;
  position: absolute;
  /* Set the navbar to fixed position */
  top: 0px;
  /* Position the navbar at the top of the page */
  width: 100%;
  /* Full width */
  height: 3.75rem;


}

.navbar.admin {
  background: #FFFFFF;
  border-bottom: 1px solid #000000;

  font-family: 'Montserrat';
  font-style: normal;
}

.navbar.bw {
  font-family: 'Antonio';
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  /* identical to box height, or 686% */

  text-align: center;
  letter-spacing: -0.022em;
  font-style: normal;
  background: #DC5E88;

}

.navbar-title {
  position: absolute;
  left: 2.73%;
  top: 20%;
  bottom: 20%;


  font-weight: 700;
  font-size: 32px;
  line-height: 36px;
  /* identical to box height, or 112% */

  letter-spacing: -0.015em;

  color: #000000;
}

.routes {
  margin-right: 2%;
  position: absolute;
  overflow: hidden;
  vertical-align: top;
  right: 0%;
  top: 0%;
}

.navbar-element {
  font-family: inherit;
  margin-left: 70px;
  vertical-align: middle;

  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  outline: none;

  height: 60px;
  text-align: left;
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  border-bottom: black;
}

.page-title {
  vertical-align: middle;
  display: inline-block;
  padding-top: 3%;
  padding-bottom: 3%;
  padding-right: 5%;

  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-size: 32px;
  line-height: 36px;
  /* identical to box height, or 112% */

  letter-spacing: -0.015em;

  color: #000000;
}

.textfield {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  vertical-align: middle;

}

.showmobile {
  display: none !important;
}

@media screen and (max-width: 980px) {
  .hidedesktop {
    display: inline-block !important;
  }

  .hidetablet {
    display: none;
  }

  .textfield {
    font-size: 14px;
  }

  .showmobile {
    display: none !important;
  }

}

@media screen and (max-width: 550px) {
  .lineup-form {
    width: 100%;
  }

  .hidetablet {
    display: none !important;
  }

  .hidemobile {
    display: none;
  }

  .page-title {
    font-size: 16px;
  }

  .textfield {
    font-size: 12px;
  }

  .showmobile {
    display: inline-block !important;
  }

  .dropdown-icon {
    margin-bottom: 7px;

    padding-left: 40px;
    padding-bottom: 10px,
  }

  .navbar-element.lg {
    margin-left: 10px;

  }
}
</style>


