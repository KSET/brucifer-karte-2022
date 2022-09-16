<template>
  <div class="navbar bw">
        <router-link class="navbar-title" to="/">
          BRUCOŠIJADA FER-A
        </router-link>
        <div class="routes">

        <RouterElement class="navbar-element hide"
        :name="'Naslovnica'" :link="'/'"></RouterElement>

        <RouterElement class="navbar-element hide"
        :name="'Izvođači'" :link="'/lineup'"></RouterElement>

        <RouterElement class="navbar-element hide"
        :name="'Ulaznice'" :link="'/ulaznice'"></RouterElement>

        <RouterElement class="navbar-element hide"
        :name="'Sponzori'" :link="'/sponsors'"></RouterElement>

        <RouterElement class="navbar-element hide"
        :name="'Kontakt'" :link="'/kontakt'"></RouterElement>

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
      page: '',
    }
  },
  mounted() {
    this.page = this.$route.path;
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
      tagsList: ['Brucoši', 'KSET', 'VIP'],
      logoutlist: ['logout']
    }
  },
  methods: {
    toggleBurger() {
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");
    },
    refresh() {
      if (!window.location.hash) {
        window.location = window.location + '#loaded';
        window.location.reload();
      }
    },
    changenav(){
      this.showNav=!this.showNav;
    }
  }
}


</script>
<style lang="css">
@import "@fontsource/antonio";

#bw-navbar{
  position: absolute;
width: 100%;
height: 3.75rem;
left: 0px;
top: 0px;

background: #DC5E88;
}


</style>


