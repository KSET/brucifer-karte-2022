<template>
  <div class="lineupp">
    <Sidebar />
    <div class="admin-page-container">

      <div class="header">
        <h1 class="page-title">Izvođači</h1>
        <router-link class="icon7" to="/bruckarte/lineup-add/0">
          <img src="../../assets/icons/add-icon.svg">
        </router-link>

        <h1 class="textfield" style="display: inline;">Prikaz lineupa na brucwebu</h1>

        <label class="switch">
          <input type="checkbox">
          <span class="slider round"></span>
        </label>
      </div>

      <lineup-table></lineup-table>
    </div>
  </div>
</template>

<script>
import LineupTable from '@/components/Lineup/LineupTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import store from '@/store/index.js';
export default {
  name: 'SponsorsView',
  components: {
    LineupTable,
    Sidebar
  }
}
</script>

<style >
.switch {
  float: right;
  position: relative;
  display: flow;
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
  background-color: red;
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
  background-color: green;
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