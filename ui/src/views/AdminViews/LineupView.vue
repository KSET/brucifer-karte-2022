<template>
  <div class="lineupp">
    <Sidebar />
    <div class="admin-page-container">
      <Sidebar />
      <div class="admin-page-container">
        <h1 class="page-title">Izvođači</h1>
        <router-link class="icon7" to="/bruckarte/lineup-add/0">
          <img src="../../assets/icons/add-icon.svg">
        </router-link>

        <lineup-table></lineup-table>
      </div>
    </div>
  </div>
</template>

<script>
import LineupAdd from "@/components/Lineup/LineupTable.vue"
import LineupTable from '@/components/Lineup/LineupTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import store from '@/store/index.js';
export default {
  name: 'SponsorsView',
  components: {
    LineupAdd,
    LineupTable,
    Sidebar
  }
}
</script>

<style >
.page-title7 {
  position: absolute;
  left: 2.83%;
  right: 68.55%;
  top: 14.71%;
  bottom: 80.6%;

  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-size: 32px;
  line-height: 36px;
  /* identical to box height, or 112% */

  letter-spacing: -0.015em;

  color: #000000;
}

.icon7 {
  position: absolute;
  left: 19.73%;
  right: 74.41%;
  top: 13.15%;
  bottom: 79.04%;
  border: 0px;
  background-color: #ffffffff;
}
</style>