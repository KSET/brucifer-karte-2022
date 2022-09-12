<template>
  <div id="admin-navbar">
        <router-link id="navbar-title" to="/bruckarte/">
          #BRUCIFER
        </router-link>

        <div class="routes">

        <RouterElement v-if="privilege == '1' || privilege == '3' || privilege == '4'" class="navbar-element hide" :name="'Brucoši'" :link="'/bruckarte/guests'"></RouterElement>

        <RouterElement v-if="privilege == '1' || privilege == '2' || privilege == '4'" class="navbar-element hide" :name="'Ulaz'" :link="'/bruckarte/entry'"></RouterElement>


        <router-link v-if="privilege == '1'" class="navbar-element" to="/bruckarte/admin-panel">
          <img src="../../assets/icons/nav-burger.svg">
        </router-link>

        <router-link class="navbar-element hide" to="/bruckarte/logout">
          <img src="../../assets/icons/logout-icon.svg">
        </router-link></div>

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
      route: '',
    }
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
  mounted(){
    this.route = this.$route.path;
  },
  methods: {
    toggleBurger() {
      
      
    }
  }
}


</script>
<style lang="scss">
#admin-navbar{
  overflow: hidden;
  position: fixed; /* Set the navbar to fixed position */
  top: 0; /* Position the navbar at the top of the page */
  width: 100%; /* Full width */
  height: 3.75rem;

background: #FFFFFF;
border-bottom: 1px solid #000000;
}

#navbar-title{
position: absolute;
left: 2.73%;
right: 68.65%;
top: 20%;
bottom: 20%;

font-family: 'Montserrat';
font-style: normal;
font-weight: 700;
font-size: 32px;
line-height: 36px;
/* identical to box height, or 112% */

letter-spacing: -0.015em;

color: #000000;
}

.routes{
  margin-right: 2%;
  position: absolute;
  overflow: hidden;
  right: 0%;
}

.navbar-element{
    padding-left: 70px;
    font-size: 20px;
    
    border: none;
    background: none;
    text-align: left;
    cursor: pointer;
    outline: none;

    height: 60px;
    text-align: left;
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 500;
    font-size: 16px;
    line-height: 36px;
    border-bottom: black;
}

@media screen and (max-width: 980px) {
    .navbar-element.hide {
        display: none;
    }
}
</style>


