<template>
  <div class="navbar admin">
    <router-link class="navbar-title" to="/bruckarte/">
      #BRUCIFER
    </router-link>

    <div class="routes">

      <RouterElement v-if="privilege == '1' || privilege == '3' || privilege == '4'" class="navbar-element hide"
        :name="'Brucoši'" :link="'/bruckarte/guests'"></RouterElement>

      <RouterElement v-if="privilege == '1' || privilege == '2' || privilege == '4'" class="navbar-element hide"
        :name="'Ulaz'" :link="'/bruckarte/entry'"></RouterElement>

      <router-link v-if="privilege == '1'" class="navbar-element hide" to="/bruckarte/admin-panel">
        <img src="../../assets/icons/nav-burger.svg">
      </router-link>

      <router-link v-if="privilege != '' && privilege != '0'" class="navbar-element hide" to="/bruckarte/logout">
        <img src="../../assets/icons/logout-icon.svg">
      </router-link>


      <div id="nav-icon3" @click="toggleNav">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>

      <div id="myNav" class="overlay admin">
        <div class="overlay-content admin">
          <RouterElement class="overlay-element" :name="'Tagovi'" :link="'/bruckarte/tags'"></RouterElement>
          <RouterElement class="overlay-element" :name="'Privilegije'" :link="'/bruckarte/privileges'"></RouterElement>
          <RouterElement class="overlay-element" :name="'Korisnici'" :link="'/bruckarte/users'"></RouterElement>
          <RouterElement class="overlay-element" :name="'Uvoz'" :link="'/bruckarte/import'"></RouterElement>
          <button class="overlay-element" @click="exportCSV">
            <download-csv :data=this.users separator-excel=true encoding='utf-8
        ' name="export.csv">

              Izvoz
            </download-csv>
          </button>

          <button class="dropdown-btn">Izvođači
            <img class="dropdown-icon" src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleDropdown">
          </button>
          <div class="dropdown-container">
            <RouterElement class="overlay-element" :name="'Pregled Izvođača'" :link="'/bruckarte/lineup-list'">
            </RouterElement>
            <RouterElement class="overlay-element" :name="'Dodavanje Izvođača'" :link="'/bruckarte/lineup-add/0'">
            </RouterElement>
          </div>
          <button class="dropdown-btn" @click="toggleDropdown">Sponzori
            <img class="dropdown-icon" src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleDropdown">
          </button>
          <div class="dropdown-container">
            <RouterElement class="overlay-element" :name="'Pregled Sponzora'" :link="'/bruckarte/sponsors-list'">
            </RouterElement>
            <RouterElement class="overlay-element" :name="'Dodavanje Sponzora'" :link="'/bruckarte/sponsors-add/0'">
            </RouterElement>

          </div>
          <RouterElement class="overlay-element" :name="'Dodaj Gosta'" :link="'/bruckarte/guests-add'"></RouterElement>
          <RouterElement class="overlay-element" :name="'Kontakt'" :link="'/bruckarte/band-kontakt'"></RouterElement>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from '@/store/index.js';
import RouterElement from '@/components/AdminPanel/RouterElement.vue'

export default {
  name: 'Navbar',
  el: '#app',
  components: {
    RouterElement
  },
  data() {
    return {
      route: '',
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
  data() {
    return {
      showNav: false,
      tagsList: ['Brucoši', 'KSET', 'VIP'],
      logoutlist: ['logout']
    }
  },
  mounted() {
    this.route = this.$route.path;
  },
  methods: {
    toggleNav() {
      document.getElementById("nav-icon3").classList.toggle('open');
      if (this.showNav) {
        document.getElementById("myNav").style.height = "0%";
      } else {
        document.getElementById("myNav").style.height = "100%";
      }
      this.showNav = !this.showNav;
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

@media screen and (max-width: 980px) {
  .navbar-element.hide {
    display: none;
  }
}
</style>


