<template>
  <div id="admin-navbar">

        <router-link id="navbar-title" to="/bruckarte/home">
          #BRUCIFER
        </router-link>

        <router-link id="navbar-item1"  to="/bruckarte/guests">
          Brucoši
        </router-link>

        <router-link id="navbar-item2" to="/bruckarte/ulaz">
          Ulaz
        </router-link>

        <router-link id="navbar-item3" to="/bruckarte/admin-panel">
          Admin
        </router-link>

  </div>
</template>

<script>
import store from '@/store/index.js';
export default {
  name: 'Navbar',
  el: '#app',
  components: {

  },
  data() {
    return {
      showNav: false,
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
    }
  }
}


</script>
<style lang="scss">
#admin-navbar{
  position: absolute;
width: 100%;
height: 3.75rem;
left: 0px;
top: 0px;

background: #FFFFFF;
border-bottom: 1px solid #000000;
}

#navbar-title{
position: absolute;
width: 24.563rem;
height: 2.25rem;
left: calc(50% - 293px/2 - 337.5px);
top: calc(50% - 36px/2);

font-family: 'Montserrat';
font-style: normal;
font-weight: 700;
font-size: 2rem;
line-height: 2.25rem;
/* identical to box height, or 112% */

letter-spacing: -0.015em;

color: #000000;

}

#navbar-item1{
position: absolute;
width: 62px;
height: 36px;
left: 690px;
top: 10px;

font-family: 'Montserrat';
font-style: normal;
font-weight: 700;
font-size: 16px;
line-height: 36px;
/* identical to box height, or 225% */

display: flex;
align-items: center;
text-align: center;
letter-spacing: -0.015em;

color: #000000;
}

#navbar-item2{
  position: absolute;
width: 62px;
height: 36px;
left: 776px;
top: 10px;

font-family: 'Montserrat';
font-style: normal;
font-weight: 400;
font-size: 16px;
line-height: 36px;
/* identical to box height, or 225% */

display: flex;
align-items: center;
text-align: center;
letter-spacing: -0.015em;

color: #000000;
}

#navbar-item3{
position: absolute;
width: 62px;
height: 36px;
left: 862px;
top: 10px;

font-family: 'Montserrat';
font-style: normal;
font-weight: 400;
font-size: 16px;
line-height: 36px;
/* identical to box height, or 225% */

display: flex;
align-items: center;
text-align: center;
letter-spacing: -0.015em;

color: #000000;
}
</style>


