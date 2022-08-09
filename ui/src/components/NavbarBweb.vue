<template>
  <div id="navbarbweb">
    <nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link class="navbar-item" :to="'/'">BRUCOŠIJADA FER-A</router-link>
        </div>

       
      

      
      <div class="navbar-end">

        <!-- odkomentirat ovo kad se sredi nabvbar LP -->
        <router-link class="navbar-item" :to="'/'">Naslovnica</router-link>
        <router-link class="navbar-item" :to="'/lineup/'">Izvođači</router-link>
        <router-link class="navbar-item" :to="'/ulaznice/'">Ulaznice</router-link>
        <router-link class="navbar-item" :to="'/sponsors/'">Sponzori</router-link>

        <router-link class="navbar-item" :to="'/kontakt/'">Konakt</router-link>
        <router-link class="navbar-item" :to="'/upis/'">Upis brucoša</router-link>
       
      </div>


    </nav>
  </div>
</template>

<script>
import Dropdown from './DropdownRoute';
import store from '@/store/index.js';
export default {
  name: 'NavbarBweb',
  el: '#app',
  components: {
    Dropdown
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
<style>
body {
  margin: 0;
}

#navbar-item-1 {}

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

.right {
  float: right;
}
</style>


