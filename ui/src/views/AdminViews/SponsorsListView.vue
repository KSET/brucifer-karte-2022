<template>
  <div class="lineupp">
    <Sidebar />
    <div class="admin-page-container">
      
        <div class="header">
        <h1 class="page-title">Sponzori</h1>
        <router-link class="icon7" to="/bruckarte/sponsors-add/0">
          <img src="../../assets/icons/add-icon.svg">
        </router-link>
      </div>

        <sponsors-table></sponsors-table>
      </div>
    </div>
</template>

<script>
import SponsorsTable from '@/components/Sponsors/SponsorsTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import store from '@/store/index.js';
export default {
  name: 'SponsorsView',
  components: {
    SponsorsTable,
    Sidebar
  }
}
</script>

<style >

</style>