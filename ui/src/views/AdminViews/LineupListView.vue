<template>
  <div class="lineupp">
    <Sidebar />
    <div class="admin-page-container">
      
        <div class="header">
        <h1 class="page-title">Izvođači</h1>
        <router-link class="icon7" to="/bruckarte/lineup-add/0">
          <img src="../../assets/icons/add-icon.svg">
        </router-link>
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

</style>