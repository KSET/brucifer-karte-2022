<template>
  <div class="users">
    <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
          <div class="card-header">Users</div>
          <div class="card-body">
    <users-table id="users-table"></users-table>
  </div></div></div></div></div>
</template>


<script>
import UsersTable from '../components/Users/UsersTable.vue'
export default {
  name: 'UsersView',
  components: {
    UsersTable

  }
}
</script>


<style scoped>
#users-table{
  position: relative;
}

@import url(../bruckarte.css);
</style>