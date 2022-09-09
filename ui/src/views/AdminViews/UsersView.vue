<template>
  <div class="users">
    <Sidebar />
    <div class="admin-page-container">
      <h1 class="page-title">Korisnici</h1>
      <users-table id="users-table"></users-table>
    </div>
  </div>

</template>


<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import UsersTable from '@/components/Users/UsersTable.vue'
export default {
  name: 'UsersView',
  components: {
    UsersTable,
    Sidebar
  }
}
</script>

<style scoped>

</style>


<style scoped>
#users-table {
  position: relative;
}

@import url(../../bruckarte.css);
</style>