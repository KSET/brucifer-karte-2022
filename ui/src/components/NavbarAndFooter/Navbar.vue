<template>
  <div id="navbar">
    <ul>
      <li>
        <router-link style="float:right" to="/bruckarte/home">
          #Brucifer
        </router-link>
      </li>
      <li>
        <router-link style="float:right" to="/bruckarte/guests">
          Brucoši
        </router-link>
      </li>
      <li>
        <router-link style="float:right" to="/bruckarte/ulaz">
          Ulaz
        </router-link>
      </li>
      <li>
        <router-link style="float:right" to="/bruckarte/admin-panel">
          Admin
        </router-link>
      </li>
    </ul>
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
<style>
ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

router-link {
  float: left;

}

li router-link {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

li router-link:hover:not(.active) {
  background-color: #111;
}

.active {
  background-color: #04AA6D;
}
</style>


