<template>
  <div class="navbar bw" :class="$style.page">
    <router-link class="navbar-title" to="/">
      {{ translations?.navbar.title ? translations.navbar.title : "navbar.title" }} </router-link>
    <div class="routes">

      <RouterElement :class="{ [$style.selected]: isCurrentPage('bwlineup') }" v-if="this.LINEUP_VISIBILITY == '1'"
        class="navbar-element hideTablet" :name="'Izvođači'" :link="'/lineup'">
      </RouterElement>

      <RouterElement :class="{ [$style.selected]: isCurrentPage('ulaznice') }" v-if="this.ULAZNICA_VISIBILITY == '1'"
        class="navbar-element hideTablet" :name="'Ulaznice'" :link="'/ulaznice'">
      </RouterElement>

      <RouterElement :class="{ [$style.selected]: isCurrentPage('bwsponsors') }" v-if="this.SPONSORS_VISIBILITY == '1'"
        class="navbar-element hideTablet" :name="'Sponzori'" :link="'/sponsors'"></RouterElement>

      <!-- MAKNUTI KADA IGRICA KRENE U PRODUKCIJU

      <RouterElement :class="{ [$style.selected]: isCurrentPage('igrica') }" v-if="this.IGRICA_VISIBILITY == '1'"
        class="navbar-element hideTablet" :name="'Igrica'" :link="'/igrica'">
      </RouterElement>

       -->

      <RouterElement :class="{ [$style.selected]: isCurrentPage('kontakt') }" class="navbar-element hideTablet"
        :name="'Kontakt'" :link="'/kontakt'">
      </RouterElement>

      <RouterElement :class="{ [$style.selected]: isCurrentPage('cjenik') }" v-if="this.CJENIK_VISIBILITY == '1'"
        class="navbar-element hideTablet" :name="'Cjenik'" :link="'/cjenik'">
      </RouterElement>

      <div id="nav-icon3" class="hideDesktop" @click="toggleNav">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>

      <div id="myNav" class="overlay bw">
        <div class="overlay-content bw">

          <RouterElement :class="{ [$style.selected]: isCurrentPage('bwlineup') }" v-if="this.LINEUP_VISIBILITY == '1'"
            class="overlay-element " :name="'Izvođači'" :link="'/lineup'" @click="toggleNav()">
          </RouterElement>

          <RouterElement :class="{ [$style.selected]: isCurrentPage('ulaznice') }"
            v-if="this.ULAZNICA_VISIBILITY == '1'" class="overlay-element " :name="'Ulaznice'" :link="'/ulaznice'"
            @click="toggleNav()">
          </RouterElement>

          <RouterElement :class="{ [$style.selected]: isCurrentPage('bwsponsors') }"
            v-if="this.SPONSORS_VISIBILITY == '1'" class="overlay-element " :name="'Sponzori'" :link="'/sponsors'"
            @click="toggleNav()">
          </RouterElement>

          <!-- MAKNUTI KADA IGRICA KRENE U PRODUKCIJU

          <RouterElement :class="{ [$style.selected]: isCurrentPage('igrica') }" v-if="this.IGRICA_VISIBILITY == '1'"
            class="overlay-element " :name="'Igrica'" :link="'/igrica'" @click="toggleNav()">
          </RouterElement>

        -->

          <RouterElement :class="{ [$style.selected]: isCurrentPage('kontakt') }" class="overlay-element "
            :name="'Kontakt'" :link="'/kontakt'" @click="toggleNav()">
          </RouterElement>

          <RouterElement :class="{ [$style.selected]: isCurrentPage('cjenik') }" v-if="this.CJENIK_VISIBILITY == '1'"
            class="overlay-element " :name="'Cjenik'" :link="'/cjenik'" @click="toggleNav()">
          </RouterElement>

        </div>
      </div>

    </div>
  </div>
</template>

<style module>
.page .selected {
  text-decoration: underline;
  font-weight: 700;
}
</style>

<script>
import axios from 'axios';
import RouterElement from '@/components/AdminPanel/RouterElement.vue'
import store from '@/store/visibilityStore';
import translationsStore from "@/store/translationsStore.js";

export default {
  name: 'Navbar',
  el: '#app',
  components: {
    RouterElement
  },
  data() {
    return {
      showNav: false,
    }
  }, computed: {
    LINEUP_VISIBILITY() {
      return store.state.LINEUP_VISIBILITY;
    },
    SPONSORS_VISIBILITY() {
      return store.state.SPONSORS_VISIBILITY;
    },
    ULAZNICA_VISIBILITY() {
      return store.state.ULAZNICA_VISIBILITY;
    },
    CJENIK_VISIBILITY() {
      return store.state.CJENIK_VISIBILITY;
    },
    IGRICA_VISIBILITY() {
      return store.state.IGRICA_VISIBILITY;
    },
    translations() {
      return translationsStore.state.translations;
    }
  },
  async beforeCreate() {
    await store.dispatch("fetchVisibilityData")
    await translationsStore.dispatch("fetchTranslations")
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
    isCurrentPage(routeName) {
      return this.$route.name == routeName;
    }
  }
}


</script>

<style scoped>
.navbar-title {
  font-family: 'Ubuntu';
  font-size: 20px;
}

.navbar-title:hover {
  color: #dbe9f4;
}

.navbar-element {
  font-family: 'Ubuntu';
}

.overlay-element {
  font-family: 'Ubuntu';
}
</style>

<style lang="css">
.overlay {
  height: 0%;
  width: 100%;
  position: fixed;
  z-index: -1;
  top: 0;
  left: 0;
  background-color: #00142B;
  overflow-x: hidden;
  transition: 0.5s;
}

.overlay.bw {
  background-color: #00142B;

}

.overlay.admin {
  background-color: white;

}

.overlay-content {
  position: relative;
  width: 100%;
  text-align: left;
  margin-top: 4rem;
}

.overlay-content.bw {
  top: 17%;
}



.overlay-element {
  padding-left: 5%;
  text-decoration: none;
  font-size: 22px;
  color: #FFFFFF;
  display: block;
  transition: 0.3s;

  font-family: inherit;

  border: none;
  background: none;
  cursor: pointer;
  outline: none;

  height: 60px;
  font-style: normal;
  font-weight: 500;
}

.overlay-element:hover,
.overlay-element:focus {}

.overlay .closebtn {
  position: absolute;
  top: 20px;
  right: 45px;
  font-size: 60px;
}

@media screen and (max-height: 450px) {
  .overlay-element {
    font-size: 20px
  }

  .overlay .closebtn {
    font-size: 40px;
    top: 15px;
    right: 35px;
  }

  .overlay-element.LS {
    width: 5%;
  }
}


#nav-icon1,
#nav-icon2,
#nav-icon3,
#nav-icon4 {
  display: inline-block;
  width: 32px;
  height: 20px;
  position: relative;
  margin: 20px;
  -webkit-transform: rotate(0deg);
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  transform: rotate(0deg);
  -webkit-transition: .5s ease-in-out;
  -moz-transition: .5s ease-in-out;
  -o-transition: .5s ease-in-out;
  transition: .5s ease-in-out;
  cursor: pointer;
}

#nav-icon1 span,
#nav-icon3 span,
#nav-icon4 span {
  display: block;
  position: absolute;
  height: 1px;
  width: 100%;
  background: #FFFFFF;
  border-radius: 6px;
  opacity: 1;
  left: 0;
  -webkit-transform: rotate(0deg);
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  transform: rotate(0deg);
  -webkit-transition: .25s ease-in-out;
  -moz-transition: .25s ease-in-out;
  -o-transition: .25s ease-in-out;
  transition: .25s ease-in-out;
}

#nav-icon1 span:nth-child(1) {
  top: 0px;
}


#nav-icon3 span:nth-child(1) {
  top: 0px;
}

#nav-icon3 span:nth-child(2),
#nav-icon3 span:nth-child(3) {
  top: 8px;
}

#nav-icon3 span:nth-child(4) {
  top: 16px;
}

#nav-icon3.open span:nth-child(1) {
  top: 8px;
  width: 0%;
  left: 50%;
}

#nav-icon3.open span:nth-child(2) {
  -webkit-transform: rotate(45deg);
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  transform: rotate(45deg);
}

#nav-icon3.open span:nth-child(3) {
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  transform: rotate(-45deg);
}

#nav-icon3.open span:nth-child(4) {
  top: 10px;
  width: 0%;
  left: 50%;
}

.hideDesktop {
  display: none !important;
}

@media screen and (max-width: 980px) {
  .hideDesktop {
    display: inline-block !important;
  }

  .hideTablet {
    display: none;
  }

  .textfield {
    font-size: 14px;
  }

}

@media screen and (max-width: 550px) {
  .lineup-form {
    width: 100%;
  }

  .hideMobile {
    display: none;
  }

  .page-title {
    font-size: 26px;
  }

  .textfield {
    font-size: 12px;
  }
}
</style>
