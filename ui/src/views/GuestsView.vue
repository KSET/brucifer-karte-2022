<template>
  <div class="guestss">
    <br>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Brucoši</div>
          <div class="card-body">
            <guests-add></guests-add>
            <guests-table></guests-table>
          </div>
        </div>
      </div>
    </div>
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
</style>

