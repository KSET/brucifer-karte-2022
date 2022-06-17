<template>
  <div class="guest">
     <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card-header">Brucoši</div>
          <div class="card-body">
    <guests-add></guests-add>
    <guests-table></guests-table>
    </div></div></div>
  </div>
</template>




<script>
import GuestsAdd from '../components/Guests/GuestsAdd.vue'
import GuestsTable from '../components/Guests/GuestsTable.vue'
export default {
  name: 'GuestsView',
  components: {
    
    GuestsTable,
    GuestsAdd

  }
}
</script>

<style scoped>
.card-header {
  padding: 0.75rem 1.25rem;
  margin-bottom: 0;
  background-color: rgba(0, 0, 0, 0.03);
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.col-md-8{
position: relative;
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
}
.card-body {
  flex: 1 1 auto;
  min-height: 1px;
  padding: 1.25rem;
}
</style>

