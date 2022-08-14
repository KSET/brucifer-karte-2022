<template>
  <div class="lineupp">
    <br>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Lineup</div>
          <div class="card-body">
            <lineup-add></lineup-add>
            <lineup-table></lineup-table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>




<script>
import LineupAdd from '../components/Lineup/LineupAdd.vue'
import LineupTable from '../components/Lineup/LineupTable.vue'
import store from '@/store/index.js';
export default {
  name: 'SponsorsView',
  components: {
    LineupAdd,
    LineupTable

  }
}
</script>

<style scoped>
</style>