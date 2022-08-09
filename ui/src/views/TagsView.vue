<template>
  <div class="tagss">
    <br>
<div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
          <div class="card-header">Tags</div>
          <div class="card-body">
    <tags-add></tags-add>
    <tags-table></tags-table>
  </div></div></div></div></div>
</template>




<script>
import TagsTable from '../components/Tags/TagsTable.vue'
import store from '@/store/index.js';
import TagsAdd from '@/components/Tags/TagsAdd.vue';
export default {
  name: 'SponsorsView',
  components: {
    TagsTable,
    TagsAdd
}
}
</script>


<style scoped>

</style>