<template>
  <div class="navbar bw">
    <router-link class="navbar-title" to="/">
      BRUCOŠIJADA FER-A
    </router-link>
    <div class="routes">

      <RouterElement class="navbar-element hide" :name="'Naslovnica'" :link="'/'"></RouterElement>

      <RouterElement class="navbar-element hide" :name="'Izvođači'" :link="'/lineup'"></RouterElement>

      <RouterElement class="navbar-element hide" :name="'Ulaznice'" :link="'/ulaznice'"></RouterElement>

      <RouterElement class="navbar-element hide" :name="'Sponzori'" :link="'/sponsors'"></RouterElement>

      <RouterElement class="navbar-element hide" :name="'Kontakt'" :link="'/kontakt'"></RouterElement>

      <button class="navbar-element" to="/bruckarte/admin-panel">
        <img src="../../assets/icons/nav-burger.svg">
      </button>

      <div id="myNav" class="overlay">
        <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&times;</a>
        <div class="overlay-content">
          <a href="lineup">Izvođači</a>
          <RouterElement class="oberlay-elem" :name="'Naslovnica'" :link="'/'"></RouterElement>

          <RouterElement class="navbar-element " :name="'Izvođači'" :link="'/lineup'"></RouterElement>

          <RouterElement class="navbar-element " :name="'Ulaznice'" :link="'/ulaznice'"></RouterElement>

          <RouterElement class="navbar-element " :name="'Sponzori'" :link="'/sponsors'"></RouterElement>

          <RouterElement class="navbar-element " :name="'Kontakt'" :link="'/kontakt'"></RouterElement>
        </div>
      </div>

      <span style="font-size:30px;cursor:pointer" @click="openNav()">&#9776; open</span>
    </div>
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
      page: '',
    }
  },
  mounted() {
    this.page = this.$route.path;
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
    openNav() {
      document.getElementById("myNav").style.width = "100%";
    },
    closeNav() {
      document.getElementById("myNav").style.width = "0%";
    },
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
    changenav() {
      this.showNav = !this.showNav;
    }
  }
}


</script>
<style lang="css">
@import "@fontsource/antonio";


.overlay {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: rgb(0, 0, 0);
  background-color: rgba(0, 0, 0, 0.9);
  overflow-x: hidden;
  transition: 0.5s;
}

.overlay-content {
  position: relative;
  top: 25%;
  width: 100%;
  text-align: center;
  margin-top: 30px;
}

.overlay.elem {
  padding: 8px;
  text-decoration: none;
  font-size: 36px;
  color: #818181;
  display: block;
  transition: 0.3s;
}

.overlay-elem:hover,
.overlay-elem:focus {
  color: #f1f1f1;
}

.overlay .closebtn {
  position: absolute;
  top: 20px;
  right: 45px;
  font-size: 60px;
}

@media screen and (max-height: 450px) {
  .overlay-elem {
    font-size: 20px
  }

  .overlay .closebtn {
    font-size: 40px;
    top: 15px;
    right: 35px;
  }
}
</style>


