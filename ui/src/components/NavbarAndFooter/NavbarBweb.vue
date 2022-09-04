<template>
  <div id="bw-navbar">

        <router-link id="navbar-title1" to="/">
          Brucošijada FER-a
        </router-link>

        <router-link 
        
        id="navbar-item4"  to="/">
          Naslovnica
        </router-link>

        <router-link  id="navbar-item5" to="/lineup">
          Izvođači
        </router-link>

        <router-link  id="navbar-item6" to="/ulaznice">
          Ulaznice
        </router-link>

        <router-link id="navbar-item7" to="/sponsors">
          Sponzori
        </router-link>

        <router-link  id="navbar-item8" to="/kontakt">
          Kontakt
        </router-link>

        <div v-if="this.showNav==true" class="navi">slay</div>

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
      page: '',
    }
  },
  mounted() {
    this.page = this.$route.path;
console.log(this.page);

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
    },
    changenav(){
      this.showNav=!this.showNav;
      console.log(this.showNav);
    }
  }
}


</script>
<style lang="css">
@import "@fontsource/antonio";

#bw-navbar{
  position: absolute;
width: 100%;
height: 3.75rem;
left: 0px;
top: 0px;

background: #DC5E88;
}

#navbar-title1{
position: absolute;
left: 2.73%;
right: 68.65%;
top: 20%;
bottom: 20%;

font-family: 'Antonio';
font-style: normal;
font-weight: 700;
font-size: 20px;
line-height: 36px;
/* identical to box height, or 480% */

text-align: center;
letter-spacing: -0.022em;

color: #000000;
}

#navbar-item4{
position: absolute;
left: 54.69%;
right: 39.75%;
top: 20%;
bottom: 20%;

font-family: 'Antonio';
font-style: normal;
font-weight: 400;
font-size: 14px;
line-height: 36px;
/* identical to box height, or 686% */

text-align: center;
letter-spacing: -0.022em;
color: #000000;

color: #000000;
}

#navbar-item5{
position: absolute;
left: 64.75%;
right: 31.35%;
top: 20%;
bottom: 20%;

font-family: 'Antonio';
font-style: normal;
font-weight: 400;
font-size: 14px;
line-height: 36px;
/* identical to box height, or 686% */

text-align: center;
letter-spacing: -0.022em;
color: #000000;
}

#navbar-item6{
position: absolute;
left: 73.24%;
right: 22.75%;
top: 20%;
bottom: 20%;

font-family: 'Antonio';
font-style: normal;
font-weight: 400;
font-size: 14px;
line-height: 36px;
/* identical to box height, or 686% */

text-align: center;
letter-spacing: -0.022em;

color: #000000;

}

#navbar-item7{
position: absolute;
left: 81.84%;
right: 14.06%;
top: 20%;
bottom: 20%;

font-family: 'Antonio';
font-style: normal;
font-weight: 400;
font-size: 14px;
line-height: 36px;
/* identical to box height, or 686% */

text-align: center;
letter-spacing: -0.022em;

color: #000000;
}

#navbar-item8{
position: absolute;
left: 90.43%;
right: 5.86%;
top: 20%;
bottom: 20%;

font-family: 'Antonio';
font-style: normal;
font-weight: 400;
font-size: 14px;
line-height: 36px;
/* identical to box height, or 686% */

text-align: center;
letter-spacing: -0.022em;

color: #000000;
color: #000000;
}

#nav-burger{
}

.navi{
  height: 100vh;
}


@media screen and (max-width: 900px) {

#admin-navbar{
bottom: 96.15%;
}
  

#navbar-item4{
display: none;

}

#navbar-item5{
display: none;
}

#navbar-item6{
display: none;
}

#navbar-item7{
display: none;
}

#navbar-item8{
display: none;
}

#nav-burger{
  position: absolute;
width: 32px;
height: 32px;
left: 536px;
top: 19px;
}
}
</style>


