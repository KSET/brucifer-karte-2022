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
          <RouterElement class="overlay-element" @click="toggleNav()" :name="'Tagovi'" :link="'/bruckarte/tags'"></RouterElement>
          <RouterElement class="overlay-element" @click="toggleNav()" :name="'Privilegije'" :link="'/bruckarte/privileges'"></RouterElement>
          <RouterElement class="overlay-element" @click="toggleNav()" :name="'Korisnici'" :link="'/bruckarte/users'"></RouterElement>
          <RouterElement class="overlay-element" @click="toggleNav()" :name="'Uvoz'" :link="'/bruckarte/import'"></RouterElement>
          <button class="overlay-element" @click="toggleNav()" >
            <download-csv :data=this.users separator-excel=true encoding='utf-8
        ' name="export.csv">

              Izvoz
            </download-csv>
          </button>

          <div class="sidbar-element">
            <RouterElement class="overlay-element" @click="toggleNav()" style="display: inline-block; width: 30%; border-bottom: none; text-align: right;"
                :name="'Izvođači'">
            </RouterElement>
            <img v-if="this.showDropdownLineup==false" class="dropdown-icon" src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleDropdownLineup">
            <img v-else class="dropdown-icon" src="@/assets/icons/dopdwn-open-icon.svg" @click="toggleDropdownLineup">

        </div>
        <RouterElement id="dpL1" class="overlay-element" @click="toggleNav()" :name="'Pregled Izvođača'" :link="'/bruckarte/lineup-list'">
        </RouterElement>
        <RouterElement id="dpL2" class="overlay-element" @click="toggleNav()" :name="'Dodavanje Izvođača'" :link="'/bruckarte/lineup-add/0'">
        </RouterElement>

        <div class="sidbar-element" >
            <RouterElement class="overlay-element" @click="toggleNav()" style="display: inline-block; width: 30%; border-bottom: none; text-align: right;"
                :name="'Sponzori'">
            </RouterElement>
            <img v-if="this.showDropdownSponsors==false" class="dropdown-icon" src="@/assets/icons/dopdwn-notopen-icon.svg" @click="toggleDropdownSponsors">
            <img v-else class="dropdown-icon" src="@/assets/icons/dopdwn-open-icon.svg" @click="toggleDropdownSponsors">

        </div>
            <RouterElement id="dpS1" class="overlay-element" @click="toggleNav()" :name="'Pregled Sponzora'" :link="'/bruckarte/sponsors-list'">
            </RouterElement>
            <RouterElement id="dpS2" class="overlay-element" @click="toggleNav()" :name="'Dodavanje Sponzora'" :link="'/bruckarte/sponsors-add/0'">
            </RouterElement>

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
    document.getElementById("dpL1").style.display = "none";
    document.getElementById("dpL2").style.display = "none";
    document.getElementById("dpS1").style.display = "none";
    document.getElementById("dpS2").style.display = "none";
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
    toggleDropdownLineup() {
            this.showDropdownLineup = !this.showDropdownLineup;
            if (this.showDropdownLineup) {
                console.log(this.showDropdownLineup);

                document.getElementById("dpL1").style.display = "block";
                document.getElementById("dpL2").style.display = "block";
            } else {
                document.getElementById("dpL1").style.display = "none";
                document.getElementById("dpL2").style.display = "none";
            }
        },
        toggleDropdownSponsors() {
            this.showDropdownSponsors = !this.showDropdownSponsors;
            if (this.showDropdownSponsors) {
                console.log(this.showDropdownSponsors);

                document.getElementById("dpS1").style.display = "block";
                document.getElementById("dpS2").style.display = "block";
            } else {
                document.getElementById("dpS1").style.display = "none";
                document.getElementById("dpS2").style.display = "none";
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

.page-title{
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

@media screen and (max-width: 980px) {
  .navbar-element.hide {
    display: none;
  }
  .textfield{
  font-size: 14px;
}

}

@media screen and (max-width: 400px) {
  .page-title {
  font-size: 16px;
}

.textfield{
  font-size: 12px;
}
}
</style>


