<template>
  <div class="tags">
    <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card-header">Tags</div>
          <div class="card-body">
    <tags-add></tags-add>
    <tags-table></tags-table>
  </div></div></div></div>
</template>




<script>
import TagsAdd from '../components/Tags/TagsAdd.vue'
import TagsTable from '../components/Tags/TagsTable.vue'
import store from '@/store/index.js';
export default {
  name: 'GuestsView',
  components: {
    TagsTable,
    TagsAdd

  }
}
</script>