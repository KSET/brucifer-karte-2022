<template>
  <div class="sponsorss">
    <Sidebar />
    <div class="admin-page-container">
      <h1 class="page-title">Sponzori</h1>
      <sponsors-table></sponsors-table>
    </div>
  </div>

</template>




<script>
import SponsorsAdd from '@/components/Sponsors/SponsorsAdd.vue'
import SponsorsTable from '@/components/Sponsors/SponsorsTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import store from '@/store/index.js';
export default {
  name: 'SponsorsView',
  components: {
    SponsorsAdd,
    SponsorsTable,
    Sidebar

  }
}
</script>

<style scoped>

</style>