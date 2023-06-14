<template>
  <div class="lineupp">
    <Sidebar />
    <div class="admin-page-container" style="overflow: auto;">

      <div class="header">
        <h1 class="page-title">Izvođači</h1>
        <router-link class="icon7" to="/admin/lineup-add/0">
          <img src="../../assets/icons/add-icon.svg">
        </router-link>

      </div>

      <lineup-table></lineup-table>
    </div>
  </div>
</template>



<script>
import LineupTable from '@/components/AdminPanel/LineupTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import axios from 'axios'

export default {
  name: 'SponsorsView',
  components: {
    LineupTable,
    Sidebar
  }
}
</script>

<style >
.switchdiv {
  display: inline;
  margin-right: 2%;
  position: absolute;
  overflow: hidden;
  vertical-align: middle;
  right: 0%;
  top: 3%;


  margin-top: auto;
}

.switch {
  position: relative;
  vertical-align: middle;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #D9D9D9;
  ;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked+.slider {
  background-color: black;
}

input:focus+.slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked+.slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>

<style lang="scss" module>
:global(#app) .forceNewLine {
  @media screen and (max-width: 550px) {
    display: block;
    position: relative;
    text-align: right;
  }
}
</style>