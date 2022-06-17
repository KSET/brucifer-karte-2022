<template>

  <nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <a class="navbar-item" href="https://bulma.io">
      "#BRUCIFER"
    </a>

    <a @click="toggleBurger" role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">
        <a  class="navbar-item" v-if="privilege=='1' || privilege=='3'|| privilege=='4'" href="guests">Brucoši</a>

<div class="navbar-item has-dropdown is-hoverable" v-if="privilege=='1' || privilege=='2'|| privilege=='4'">
        <a class="navbar-link">
          Ulaz
        </a>

        <div class="navbar-dropdown">
          <router-link class="navbar-item" :to="'/guest_tag/Brucoši'">Brucoši</router-link>

          <a href="guest_tag/KSET" class="navbar-item">
            KSET
          </a>
          <a href="guest_tag/VIP" class="navbar-item">
            VIP
          </a>
        </div>
      </div>


 
 <a class="navbar-item" v-if="privilege=='1'" href="tags">Tags</a>
 <a class="navbar-item" v-if="privilege=='1'" href="privileges">Privileges</a>
 <a class="navbar-item" v-if="privilege=='1'" href="users">Users</a>
  <a class="navbar-item" v-if="privilege=='1'" href="import">Import</a>
 <a class="navbar-item" v-if="privilege=='1'" href="export">Export</a>

        
      </div>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        
      <div v-if="name!=''" class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          {{name}}
        </a>

        <div class="navbar-dropdown">
         <a href="logout" class="navbar-item">
            Logout
          </a>
          
        </div>
      </div>
          
          <a v-else class="button is-light">
            Log in
          </a>
        </div>
    </div>

      
</nav>

</template>

<script>
import Dropdown from './DropdownRoute';
import store from '@/store/index.js';
export default {
  name: 'Navbar',
  components: {
    Dropdown
  },
  computed: {
    privilege() {
      return store.state.privilege;
    },
    name(){
      return store.state.name;
    }
  },
  data () {
    return {
      services: ['Brucoši','KSET','VIP'],
      logoutlist: ['logout']
    }
  },
  methods: {
    toggleBurger(){
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");
    }
  }}
  

</script>
<style>
body {margin:0;}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #9e9e9e;
  position: fixed;
  top: 0;
  width: 100%;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

li a:hover:not(.active) {
  background-color: #8e8e8e;
}

.active {
  background-color: #fb8c04;
}
.right{float: right;}
</style>


