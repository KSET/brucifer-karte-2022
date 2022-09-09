<template>
  <div class="tagss">
    <Sidebar />
    <div class="admin-page-container">
      <h1 class="page-title">Tagovi</h1>
      <tags-add></tags-add>
      <tags-table></tags-table>
    </div>
  </div>

</template>




<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import TagsTable from '@/components/Tags/TagsTable.vue'
import store from '@/store/index.js';
import TagsAdd from '@/components/Tags/TagsAdd.vue';
export default {
  name: 'SponsorsView',
  components: {
    TagsTable,
    TagsAdd,
    Sidebar
  }
}
</script>


<style scoped>

</style>