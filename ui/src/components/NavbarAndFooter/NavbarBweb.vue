<template>
  <div class="navbar bw" :class="$style.page">
    <router-link class="navbar-title" to="/">
      {{ translations.navbar.title ? translations.navbar.title : "navbar.title" }} </router-link>
    <div class="routes">

      <RouterElement :class="{ [$style.selected]: isCurrentPage('naslovnica') }" class="navbar-element hidetablet"
        :name="'Naslovnica'" :link="'/'">
      </RouterElement>

      <RouterElement :class="{ [$style.selected]: isCurrentPage('bwlineup') }" v-if="this.LINEUP_VISIBILITY == '1'"
        class="navbar-element hidetablet" :name="'Izvođači'" :link="'/lineup'">
      </RouterElement>

      <RouterElement :class="{ [$style.selected]: isCurrentPage('ulaznice') }" v-if="this.ULAZNICA_VISIBILITY == '1'"
        class="navbar-element hidetablet" :name="'Ulaznice'" :link="'/ulaznice'">
      </RouterElement>

      <RouterElement :class="{ [$style.selected]: isCurrentPage('bwsponsors') }" v-if="this.SPONSORS_VISIBILITY == '1'"
        class="navbar-element hidetablet" :name="'Sponzori'" :link="'/sponsors'"></RouterElement>

      <RouterElement :class="{ [$style.selected]: isCurrentPage('kontakt') }" class="navbar-element hidetablet"
        :name="'Kontakt'" :link="'/kontakt'">
      </RouterElement>

      <RouterElement :class="{ [$style.selected]: isCurrentPage('cjenik') }" v-if="this.CJENIK_VISIBILITY == '1'"
        class="navbar-element hidetablet" :name="'Cjenik'" :link="'/cjenik'">
      </RouterElement>

      <div id="nav-icon3" class="hidedesktop" @click="toggleNav">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>

      <div id="myNav" class="overlay bw">
        <div class="overlay-content bw">
          <RouterElement :class="{ [$style.selected]: isCurrentPage('naslovnica') }" class=" overlay-element"
            :name="'Naslovnica'" :link="'/'" @click="toggleNav()">
          </RouterElement>

          <RouterElement :class="{ [$style.selected]: isCurrentPage('bwlineup') }" v-if="this.LINEUP_VISIBILITY == '1'"
            class="overlay-element " :name="'Izvođači'" :link="'/lineup'" @click="toggleNav()">
          </RouterElement>

          <RouterElement :class="{ [$style.selected]: isCurrentPage('ulaznice') }" v-if="this.ULAZNICA_VISIBILITY == '1'"
            class="overlay-element " :name="'Ulaznice'" :link="'/ulaznice'" @click="toggleNav()">
          </RouterElement>

          <RouterElement :class="{ [$style.selected]: isCurrentPage('bwsponsors') }"
            v-if="this.SPONSORS_VISIBILITY == '1'" class="overlay-element " :name="'Sponzori'" :link="'/sponsors'"
            @click="toggleNav()">
          </RouterElement>

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
      LINEUP_VISIBILITY: store.state.LINEUP_VISIBILITY,
      SPONSORS_VISIBILITY: store.state.SPONSORS_VISIBILITY,
      ULAZNICA_VISIBILITY: store.state.ULAZNICA_VISIBILITY,
      CJENIK_VISIBILITY: store.state.CJENIK_VISIBILITY,

      translations: translationsStore.state.translations,

    }
  },
  created() {
    this.showNav = false;
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
<style lang="css">
@import "@fontsource/antonio";


.overlay {
  height: 0%;
  width: 100%;
  position: fixed;
  z-index: -1;
  top: 0;
  left: 0;
  background-color: #DC5E88;
  overflow-x: hidden;
  transition: 0.5s;
}

.overlay.bw {
  background-color: #DC5E88;

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
  color: black;
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
.overlay-element:focus {
  color: #f1f1f1;
}

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
  height: 6px;
  width: 100%;
  background: black;
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
  top: 10px;
}

#nav-icon3 span:nth-child(4) {
  top: 20px;
}

#nav-icon3.open span:nth-child(1) {
  top: 10px;
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

.hidedesktop {
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

}

@media screen and (max-width: 550px) {
  .lineup-form {
    width: 100%;
  }

  .hidemobile {
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


