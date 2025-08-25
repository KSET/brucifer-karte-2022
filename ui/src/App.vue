<template>
  <div id="app">
    <NavbarAdmin v-if="navType === 'bruckarte'"></NavbarAdmin>
    <NavbarBweb v-if="navType === 'brucweb' && comingSoonVisible"></NavbarBweb>
    <router-view />
  </div>
</template>

<script>
import NavbarAdmin from './components/NavbarAndFooter/NavbarAdmin.vue';
import NavbarBweb from './components/NavbarAndFooter/NavbarBweb.vue';
import Footer from './components/NavbarAndFooter/Footer.vue';
import visibilityStore from '@/store/visibilityStore.js';
import translationsStore from '@/store/translationsStore.js';

export default {
  name: 'app',
  components: {
    NavbarAdmin,
    NavbarBweb,
    Footer,
  },
  data() {
    return {};
  },
  async beforeCreate() {
    await visibilityStore.dispatch('fetchVisibilityData');
    await translationsStore.dispatch('fetchTranslations');
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
  },
};
</script>

<style>


:root{
  --bw-navbar-color: #004069;
  --bw-footer-color: #004069;
  --bw-page-color: #004069;
}

@import '~bootstrap/dist/css/bootstrap.css';
@import './assets/fonts/antonio/antonio.css';
@import './assets/scss/Admin-scss/global.scss';
</style>
