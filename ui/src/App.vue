<template>
  <div id="app">
    <NavbarAdmin v-if="this.navtype == 'bruckarte'"></NavbarAdmin>
    <NavbarBweb v-if="this.navtype == 'brucweb'"></NavbarBweb>
    <router-view />
  </div>
</template>

<script>
import NavbarAdmin from './components/NavbarAndFooter/NavbarAdmin.vue'
import NavbarBweb from './components/NavbarAndFooter/NavbarBweb.vue'
import Footer from './components/NavbarAndFooter/Footer.vue'
import axios from 'axios'

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
    }

  },
  created() {
    this.setupVisibilityStore();
  },
  mounted() {
    if (((String(window.location.href).split("/"))[3]) == "admin") {
      this.navtype = "bruckarte"
    } else {
      this.navtype = "brucweb"
    }
  },
  methods: {
    setupVisibilityStore() {
      axios.get(process.env.VUE_APP_BASE_URL + '/visibility/',)
        .then(response => {
          console.log(response.data)
        })
    }
  }
}
</script>

<style>
@import '~bootstrap/dist/css/bootstrap.css'
</style>
