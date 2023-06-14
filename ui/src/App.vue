<template>
  <div id="app">
    <NavbarAdmin v-if="this.navtype == 'bruckarte'"></NavbarAdmin>
    <NavbarBweb v-if="this.navtype == 'brucweb' && COMINGSOON_VISIBILITY == 0"></NavbarBweb>
    <router-view />
  </div>
</template>

<script>
import NavbarAdmin from './components/NavbarAndFooter/NavbarAdmin.vue'
import NavbarBweb from './components/NavbarAndFooter/NavbarBweb.vue'
import Footer from './components/NavbarAndFooter/Footer.vue'
import axios from 'axios'
import store from "@/store/visibilityStore.js";

export default {
  name: 'app',
  components: {
    NavbarAdmin,
    NavbarBweb,
    Footer
  },
  data() {
    return {
      navtype: 'brucweb',
      COMINGSOON_VISIBILITY: store.state.COMINGSOON_VISIBILITY
    }

  },
  created() {
    store.dispatch("fetchVisibilityData")
  },
  mounted() {
    if (((String(window.location.href).split("/"))[3]) == "admin") {
      this.navtype = "bruckarte"
    } else {
      this.navtype = "brucweb"
    }
  },
}
</script>

<style>
@import '~bootstrap/dist/css/bootstrap.css'
</style>
