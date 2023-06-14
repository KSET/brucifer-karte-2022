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

          const visibilittyResp = response.data.reduce((result, obj) => {
            result[obj.name] = obj.visible;
            return result;
          }, {})
          console.log(visibilittyResp)

          for (const key in visibilittyResp) {
            if (Object.prototype.hasOwnProperty.call(visibilittyResp, key)) {
              const value = visibilittyResp[key];
              const mutationName = `set${key}`;
              store.commit(mutationName, value);
            }
          }

          console.log(store.state.COMINGSOON_VISIBILITY)
        })
    }
  }
}
</script>

<style>
@import '~bootstrap/dist/css/bootstrap.css'
</style>
