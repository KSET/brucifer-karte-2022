<template>
  <div id="navbar">
    <nav class="navbar is-fixed-top" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link class="navbar-item" :to="'/bruckarte/home/'">#BRUCIFER</router-link>
      </div>

        <a v-on:click="showNav = !showNav" v-bind:class="{ 'is-active': showNav }" role="button" class="navbar-burger"
          aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      

      <div id="navbarBasicExample" class="navbar-menu" v-bind:class="{ 'is-active': showNav }">
        <div class="navbar-start">

          <router-link class="navbar-item" v-if="privilege == '1' || privilege == '3' || privilege == '4'"
            :to="'/bruckarte/guests/'">Brucoši</router-link>


          <div class="navbar-item has-dropdown is-hoverable"
            v-if="privilege == '1' || privilege == '2' || privilege == '4'">
            <a class="navbar-link">
              Ulaz
            </a>

            <div class="navbar-dropdown">
              <a href="/bruckarte/guest_tag/Brucoši" class="navbar-item">
                Brucoši
              </a>
              <a href="/bruckarte/guest_tag/KSET" class="navbar-item">
                KSET
              </a>
              <a href="/bruckarte/guest_tag/VIP" class="navbar-item">
                VIP
              </a>
            </div>
          </div>


          <div class="navbar-item has-dropdown is-hoverable"
            v-if="privilege == '1'">
            <a class="navbar-link">
              Admin
            </a>

            <div class="navbar-dropdown">
          <router-link class="navbar-item" v-if="privilege == '1'" :to="'/bruckarte/tags/'">Tags</router-link>
          <router-link class="navbar-item" v-if="privilege == '1'" :to="'/bruckarte/privileges/'">Privileges
          </router-link>
          <router-link class="navbar-item" v-if="privilege == '1'" :to="'/bruckarte/users/'">Users</router-link>
          <router-link class="navbar-item" v-if="privilege == '1'" :to="'/bruckarte/import/'">Import</router-link>
          <router-link class="navbar-item" v-if="privilege == '1'" :to="'/bruckarte/export/'">Export</router-link>
          </div></div>
          <router-link class="navbar-item" v-if="privilege == '1'" :to="'/bruckarte/'">|</router-link>

            

          <div class="navbar-item has-dropdown is-hoverable" v-if="privilege == '1'">
            <a class="navbar-link">
              Bruciweb
            </a>

            <div class="navbar-dropdown">
              <a href="/bruckarte/lineup" class="navbar-item">
                Lineup
              </a>
              <a href="/bruckarte/sponsors" class="navbar-item">
                Sponsors
              </a>

            </div>
          </div>

        </div>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">

          <div v-if="name != ''" class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              {{ name }}
            </a>

            <div class="navbar-dropdown">

              <router-link class="navbar-item" :to="'/bruckarte/logout'">Logout</router-link>

            </div>
          </div>

          <a v-else class="button is-light">
            Log in
          </a>
        </div>
      </div>


    </nav>
  </div>
</template>

<script>
import Dropdown from './DropdownRoute';
import store from '@/store/index.js';
export default {
  name: 'Navbar',
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


