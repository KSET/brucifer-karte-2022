<template>
<div id="app">
  <NavbarAdmin v-if="this.navtype=='bruckarte'"></NavbarAdmin>
  <NavbarBweb v-if="this.navtype=='brucweb'"></NavbarBweb>
  <Footer v-if="this.navtype=='brucweb'"></Footer>
<router-view/>
</div>
</template>

<script>
import NavbarAdmin from './components/NavbarAndFooter/NavbarAdmin.vue'
import NavbarBweb from './components/NavbarAndFooter/NavbarBweb.vue'
import Footer from './components/NavbarAndFooter/Footer.vue'


export default {
  name: 'app',
  components: {
    NavbarAdmin,
    NavbarBweb,
    Footer
},
  data() {
      return {
        navtype:'brucweb',
      }

    },
  mounted(){
    if(((String(window.location.href).split("/"))[3])=="bruckarte"){
      this.navtype="bruckarte"
    }else{
      this.navtype="brucweb"
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

@import '~bootstrap/dist/css/bootstrap.css'
</style>
