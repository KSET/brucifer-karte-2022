<template>
  <div id="app">
    <template v-if="visibilityLoaded">
      <NavbarAdmin v-if="navType === 'bruckarte'"></NavbarAdmin>
      <NavbarBweb v-if="navType === 'brucweb' && comingSoonVisible && !hideNavbar"></NavbarBweb>
      <router-view />
    </template>
  </div>
</template>

<script>
import NavbarAdmin from './components/NavbarAndFooter/NavbarAdmin.vue';
import NavbarBweb from './components/NavbarAndFooter/NavbarBweb.vue';
import visibilityStore from '@/store/visibilityStore.js';
import translationsStore from '@/store/translationsStore.js';

export default {
  name: 'app',
  components: {
    NavbarAdmin,
    NavbarBweb,
  },
  async beforeCreate() {
    await translationsStore.dispatch('fetchTranslations');
  },
  created() {
    this.syncAppClass();
  },
  watch: {
    $route() {
      this.syncAppClass();
    },
  },
  methods: {
    syncAppClass() {
      const isAdmin = window.location.pathname.split('/')[1] === 'admin';
      document.documentElement.classList.toggle('bw-app', !isAdmin);
    },
  },
  computed: {
    navType() {
      if (window.location.href.split('/')[3] == 'admin') {
        return 'bruckarte';
      } else {
        return 'brucweb';
      }
    },
    comingSoonVisible() {
      return visibilityStore.state.COMINGSOON_VISIBILITY == 0;
    },
    visibilityLoaded() {
      return visibilityStore.state.VISIBILITY_LOADED;
    },
    hideNavbar() {
      return this.$route.meta.hideNavbar === true;
    },
  },
};
</script>

<style>


:root{
  --bw-navbar-color: #004069;
  --bw-footer-color: #004069;
  --bw-page-color: #1E275D;
}

@import '~bootstrap/dist/css/bootstrap.css';
@import './assets/fonts/antonio/antonio.css';
@import './assets/fonts/GCEpicProCro/gcepicprocro.css';
@import './assets/fonts/Rubik/rubik.css';
@import './assets/scss/Admin-scss/global.scss';
@import './bruciweb.css';
</style>
