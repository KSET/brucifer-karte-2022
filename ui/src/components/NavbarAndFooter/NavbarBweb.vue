<template>
  <div class="navbar bw">
    <router-link class="navbar-title" to="/">
      BRUCOŠIJADA FER-A
    </router-link>
    <div class="routes">

      <RouterElement class="navbar-element hide" :name="'Naslovnica'" :link="'/'"></RouterElement>

      <RouterElement v-if="this.visible=='1'" class="navbar-element hide" :name="'Izvođači'" :link="'/lineup'"></RouterElement>

      <RouterElement class="navbar-element hide" :name="'Ulaznice'" :link="'/ulaznice'"></RouterElement>

      <RouterElement class="navbar-element hide" :name="'Sponzori'" :link="'/sponsors'"></RouterElement>

      <RouterElement class="navbar-element hide" :name="'Kontakt'" :link="'/kontakt'"></RouterElement>

      <div id="nav-icon3" @click="toggleNav">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>

      <div id="myNav" class="overlay bw">
        <div class="overlay-content bw">
          <RouterElement class=" overlay-element" :name="'Naslovnica'" :link="'/'" @click="toggleNav()">
          </RouterElement>

          <RouterElement v-if="this.visible=='1'" class="overlay-element " :name="'Izvođači'" :link="'/lineup'" @click="toggleNav()">
          </RouterElement>

          <RouterElement class="overlay-element " :name="'Ulaznice'" :link="'/ulaznice'" @click="toggleNav()">
          </RouterElement>

          <RouterElement class="overlay-element " :name="'Sponzori'" :link="'/sponsors'" @click="toggleNav()">
          </RouterElement>

          <RouterElement class="overlay-element " :name="'Kontakt'" :link="'/kontakt'" @click="toggleNav()">
          </RouterElement>


        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import RouterElement from '@/components/AdminPanel/RouterElement.vue'

export default {
  name: 'Navbar',
  el: '#app',
  components: {
    RouterElement
  },
  data() {
    return {
      showNav: false,
      visible: '1',
    }
  },
  created() {
    this.showNav = false;
    axios.get('http://127.0.0.1:8000/lineup/?ordering=order',)
      .then(response => {
        var users = response.data;
        this.visible= users[users.length - 1].visible;
      })
  },
  methods: {
    toggleNav() {
      document.getElementById("nav-icon3").classList.toggle('open');
      if (this.showNav) {
        document.getElementById("myNav").style.height = "0%";
      } else {
        document.getElementById("myNav").style.height = "100%";
      }
      this.showNav = !this.showNav;
    },

  }
}


</script>
<style lang="css">
@import "@fontsource/antonio";


.overlay {
  height: 0%;
  width: 100%;
  position: fixed;
  z-index: -1;
  top: 0;
  left: 0;
  background-color: #DC5E88;
  overflow-x: hidden;
  transition: 0.5s;
}

.overlay.bw{
  background-color: #DC5E88;

}

.overlay.admin{
  background-color: white;

}

.overlay-content {
  position: relative;
  width: 100%;
  text-align: center;
  margin-top: 30px;
}

.overlay-content.bw{
  top: 17%;
}



.overlay-element {
  width: 100%;
  padding: 5%;
  text-decoration: none;
  font-size: 36px;
  color: black;
  display: block;
  transition: 0.3s;

  font-family: inherit;

  border: none;
  background: none;
  cursor: pointer;
  outline: none;

  height: 60px;
  font-style: normal;
  font-weight: 500;
}

.overlay-element:hover,
.overlay-element:focus {
  color: #f1f1f1;
}

.overlay .closebtn {
  position: absolute;
  top: 20px;
  right: 45px;
  font-size: 60px;
}

@media screen and (max-height: 450px) {
  .overlay-element {
    font-size: 20px
  }

  .overlay .closebtn {
    font-size: 40px;
    top: 15px;
    right: 35px;
  }
}


#nav-icon1,
#nav-icon2,
#nav-icon3,
#nav-icon4 {
  width: 32px;
  height: 20px;
  position: relative;
  margin: 20px;
  -webkit-transform: rotate(0deg);
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  transform: rotate(0deg);
  -webkit-transition: .5s ease-in-out;
  -moz-transition: .5s ease-in-out;
  -o-transition: .5s ease-in-out;
  transition: .5s ease-in-out;
  cursor: pointer;
}

#nav-icon1 span,
#nav-icon3 span,
#nav-icon4 span {
  display: block;
  position: absolute;
  height: 6px;
  width: 100%;
  background: black;
  border-radius: 6px;
  opacity: 1;
  left: 0;
  -webkit-transform: rotate(0deg);
  -moz-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  transform: rotate(0deg);
  -webkit-transition: .25s ease-in-out;
  -moz-transition: .25s ease-in-out;
  -o-transition: .25s ease-in-out;
  transition: .25s ease-in-out;
}

#nav-icon1 span:nth-child(1) {
  top: 0px;
}


#nav-icon3 span:nth-child(1) {
  top: 0px;
}

#nav-icon3 span:nth-child(2),
#nav-icon3 span:nth-child(3) {
  top: 10px;
}

#nav-icon3 span:nth-child(4) {
  top: 20px;
}

#nav-icon3.open span:nth-child(1) {
  top: 10px;
  width: 0%;
  left: 50%;
}

#nav-icon3.open span:nth-child(2) {
  -webkit-transform: rotate(45deg);
  -moz-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  transform: rotate(45deg);
}

#nav-icon3.open span:nth-child(3) {
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  transform: rotate(-45deg);
}

#nav-icon3.open span:nth-child(4) {
  top: 10px;
  width: 0%;
  left: 50%;
}
</style>


