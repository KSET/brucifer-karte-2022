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

        <router-link id="navbar-item4" to="/bruckarte/logout">
          <img src="../../assets/icons/logout-icon.svg">
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

#navbar-item1{
position: absolute;
left: 67.38%;
right: 26.56%;
top: 16.67%;
bottom: 23.33%;

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
left: 75.78%;
right: 18.16%;
top: 16.67%;
bottom: 23.33%;

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
left: 84.18%;
right: 9.77%;
top: 16.67%;
bottom: 23.33%;

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

#navbar-item4{
position: absolute;
left: 94.34%;
right: 2.54%;
top: 20%;
bottom: 26.67%;
}

@media screen and (max-width: 900px) {

#admin-navbar{
bottom: 96.15%;
}
  

#navbar-item1{
left: 47.42%;
right: 42.26%;
top: 2.7%;
bottom: 0%;


color: #000000;
}

#navbar-item2{
left: 62%;
right: 35%;
top: 2.7%;
bottom: 0%;
}

#navbar-item3{
left: 76.04%;
right: 13.64%;
top: 2.7%;
bottom: 0%;

}

#navbar-item4{
left: 92.18%;
right: 3.83%;
top: 23%;
bottom: 16.22%;
}
}
</style>


