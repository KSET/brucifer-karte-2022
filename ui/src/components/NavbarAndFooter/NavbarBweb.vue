<template>
  <div class="navbar bw" :class="$style.page">
    <router-link class="navbar-title" to="/">
      {{ translations?.navbar?.title ? translations.navbar.title : "navbar.title" }}
    </router-link>

    <div class="routes">
      <RouterElement v-if="LINEUP_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('bwlineup') }"
        class="navbar-element hideTablet" name="Izvođači" link="/lineup" />

      <RouterElement v-if="ULAZNICA_VISIBILITY == '1'"
        :class="{ ['ulaznice-button-selected']: isCurrentPage('ulaznice') }"
        class="navbar-element hideTablet ulaznice-button" name="Kupi karte" link="/ulaznice" icon="pi-arrow-right" />

      <RouterElement v-if="SATNICA_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('satnica') }"
        class="navbar-element hideTablet" name="Satnica" link="/satnica" />

      <RouterElement v-if="TLOCRT_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('tlocrt') }"
        class="navbar-element hideTablet" name="Tlocrt" link="/tlocrt" />

      <RouterElement v-if="SPONSORS_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('bwsponsors') }"
        class="navbar-element hideTablet" name="Sponzori" link="/sponsors" />

      <RouterElement v-if="IGRICA_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('igrica') }"
        class="navbar-element hideTablet" name="Igrica" link="/igrica" />

      <!-- <RouterElement :class="{ [$style.selected]: isCurrentPage('kontakt') }" class="navbar-element hideTablet"
        name="Kontakt" link="/kontakt" /> -->

      <RouterElement v-if="CJENIK_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('cjenik') }"
        class="navbar-element hideTablet" name="Cjenik" link="/cjenik" />

      <div id="nav-icon3" class="hideDesktop" @click="toggleNav">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>

      <div id="myNav" class="overlay bw">
        <div class="overlay-content bw">
          <RouterElement v-if="LINEUP_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('bwlineup') }"
            class="overlay-element" name="Izvođači" link="/lineup" @click="toggleNav" />

          <RouterElement v-if="ULAZNICA_VISIBILITY == '1'"
            :class="{ ['ulaznice-button-selected']: isCurrentPage('ulaznice') }" class="overlay-element ulaznice-button"
            name="Kupi karte" link="/ulaznice" icon="pi-arrow-right" @click="toggleNav" />

          <RouterElement v-if="SATNICA_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('satnica') }"
            class="overlay-element" name="Satnica" link="/satnica" @click="toggleNav" />

          <RouterElement v-if="TLOCRT_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('tlocrt') }"
            class="overlay-element" name="Tlocrt" link="/tlocrt" @click="toggleNav" />

          <RouterElement v-if="SPONSORS_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('bwsponsors') }"
            class="overlay-element" name="Sponzori" link="/sponsors" @click="toggleNav" />

          <RouterElement v-if="IGRICA_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('igrica') }"
            class="overlay-element" name="Igrica" link="/igrica" @click="toggleNav" />

          <!-- <RouterElement :class="{ [$style.selected]: isCurrentPage('kontakt') }" class="overlay-element" name="Kontakt"
            link="/kontakt" @click="toggleNav" /> -->

          <RouterElement v-if="CJENIK_VISIBILITY == '1'" :class="{ [$style.selected]: isCurrentPage('cjenik') }"
            class="overlay-element" name="Cjenik" link="/cjenik" @click="toggleNav" />
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
    SATNICA_VISIBILITY() {
      return store.state.SATNICA_VISIBILITY;
    },
    TLOCRT_VISIBILITY() {
      return store.state.TLOCRT_VISIBILITY;
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
  font-size: 2rem;
  z-index: 101;
  text-decoration: none;
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

.arrow-icon {
  font-size: 1rem;
  margin-left: 6px;
  color: white;
  vertical-align: middle;
}

.ulaznice-button {
  border: 1px solid white;
  border-radius: 8px;
  padding: 8px 10px;
  height: fit-content;
  transition: background-color 0.5s ease, color 0.5s ease;
  transition: color 0.5s ease, color 0.5s ease;

}

.ulaznice-button:hover,
.ulaznice-button-selected {
  background-color: white !important;
  color: var(--bw-navbar-color) !important;
}
</style>

<style lang="css">
.overlay {
  height: 0%;
  width: 100%;
  position: fixed;
  z-index: 100;
  top: 0;
  left: 0;
  background-color: var(--bw-navbar-color);
  overflow-x: hidden;
  transition: 0.5s;
}

.overlay-content {
  position: relative;
  width: 100%;
  text-align: left;
  margin-top: 4rem;
  top: 17%;
  padding-left: 3%;
}

.overlay-element {
  padding-left: 5%;
  font-size: 22px;
  color: #FFFFFF;
  display: block;
  transition: 0.3s;
  border: none;
  background: none;
  cursor: pointer;
  outline: none;
  height: 60px;
  font-weight: 500;
  font-style: normal;
}

#nav-icon3 {
  display: inline-block;
  width: 32px;
  height: 20px;
  position: relative;
  margin: 20px 0px;
  transition: 0.5s ease-in-out;
  cursor: pointer;
  z-index: 101;
}

#nav-icon3 span {
  display: block;
  position: absolute;
  height: 1px;
  width: 100%;
  background: #FFFFFF;
  border-radius: 6px;
  left: 0;
  transition: 0.25s ease-in-out;
}

#nav-icon3 span:nth-child(1) {
  top: 0;
}

#nav-icon3 span:nth-child(2),
#nav-icon3 span:nth-child(3) {
  top: 8px;
}

#nav-icon3 span:nth-child(4) {
  top: 16px;
}

#nav-icon3.open span:nth-child(1),
#nav-icon3.open span:nth-child(4) {
  top: 8px;
  width: 0%;
  left: 50%;
}

#nav-icon3.open span:nth-child(2) {
  transform: rotate(45deg);
}

#nav-icon3.open span:nth-child(3) {
  transform: rotate(-45deg);
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

  .navbar-title {
    font-size: 1.5rem !important;
  }
}
</style>
