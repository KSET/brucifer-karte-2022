<template>
  <div class="sponsors">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Sponsors</div>
          <div class="card-body">
            <sponsors-add></sponsors-add>
            <sponsors-table></sponsors-table>
          </div>
        </div>
      </div>
    </div></div>
</template>




<script>
import SponsorsAdd from '../components/Sponsors/SponsorsAdd.vue'
import SponsorsTable from '../components/Sponsors/SponsorsTable.vue'
import store from '@/store/index.js';
export default {
  name: 'SponsorsView',
  components: {
    SponsorsAdd,
    SponsorsTable

  }
}
</script>