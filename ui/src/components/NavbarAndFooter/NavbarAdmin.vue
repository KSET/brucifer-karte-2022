<template>
  <div id="admin-navbar">

        <router-link id="navbar-title" to="/bruckarte/">
          #BRUCIFER
        </router-link>

        <router-link v-if="privilege == '1' || privilege == '3' || privilege == '4'"
        
        class="navbar-item1"  to="/bruckarte/guests">
          Brucoši
        </router-link>

        <router-link v-if="privilege == '1' || privilege == '2' || privilege == '4'" id="navbar-item2" to="/bruckarte/entry">
          Ulaz
        </router-link>

        <router-link v-if="privilege == '1'" id="navbar-item3" to="/bruckarte/admin-panel">
          <img src="../../assets/icons/nav-burger.svg">
        </router-link>

        <router-link id="navbar-icon2" to="/bruckarte/logout">
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
    console.log(this.route);
  },
  methods: {
    toggleBurger() {
      
      
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

.navbar-item1{
position: absolute;
left: 67.38%;
right: 26.56%;
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

#navbar-item2{
position: absolute;
left: 76.46%;
right: 17.48%;
top: 20%;
bottom: 20%;

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

#navbar-item3{
position: absolute;
left: 86.91%;
right: 9.96%;
top: 20%;
bottom: 26.67%;

background: #FFFFFF;

}

#navbar-icon2{
position: absolute;
left: 94.34%;
right: 2.54%;
top: 20%;
bottom: 26.67%;
}

.current{
  font-weight: 800;
}

@media screen and (max-width: 900px) {

#admin-navbar{
bottom: 96.15%;
}
  

#navbar-item1{
left: 52.42%;
right: 42.26%;
top: 2.7%;
bottom: 0%;

}

#navbar-item2{
left: 67%;
top: 2%;
bottom: 0%;
}

#navbar-item3{
left: 80.2%;
right: 15.81%;
top: 23%;
bottom: 96.78%;


}

#navbar-icon2{
left: 92.18%;
right: 3.83%;
top: 23%;
bottom: 16.22%;
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

@media screen and (max-width: 414px) {

#admin-navbar{
bottom: 95.78%;}
  

#navbar-item1{
display: none;

}

#navbar-item2{
display: none;
}

#navbar-item3{
left: 80.2%;
right: 15.81%;
top: 23%;
bottom: 96.78%;


}

#navbar-icon2{
left: 92.18%;
right: 3.83%;
top: 23%;
bottom: 16.22%;
}}




}
</style>


