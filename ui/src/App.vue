<template>
<div id="app">
  <navbar v-if="this.navtype=='bruckarte'"></navbar>
  <NavbarBweb v-if="this.navtype=='brucweb'"></NavbarBweb>
<router-view/>
</div>
</template>

<script>
import Navbar from './components/NavbarAndFooter/Navbar.vue'
import NavbarBweb from './components/NavbarAndFooter/NavbarBweb.vue'


export default {
  name: 'app',
  components: {
    Navbar,
    NavbarBweb,
    
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
