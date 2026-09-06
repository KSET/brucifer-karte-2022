<template>
  <div class="lineupp">
    <Sidebar />
    <div class="admin-page-container lineup-page">

      <div class="header lineup-header">
        <h1 class="page-title">Izvođači</h1>
        <router-link class="add-link" to="/admin/lineup-add/0" title="Dodaj izvođača">
          <img src="../../assets/icons/add-icon.svg">
        </router-link>
      </div>

      <lineup-table></lineup-table>
    </div>
  </div>
</template>

<script>
import LineupTable from '@/components/AdminPanel/LineupTable.vue'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

export default {
  name: 'LineupView',
  components: {
    LineupTable,
    Sidebar
  }
}
</script>

<style scoped>
.lineup-page {
  display: flex;
  flex-direction: column;
  height: 93vh;
  min-height: 0;
  box-sizing: border-box;
  margin-left: 25%;
  margin-right: 0;
  padding-left: 1rem;
  padding-right: 1rem;
}

@media screen and (max-width: 900px) {
  .lineup-page {
    margin-left: 0;
  }
}

.lineup-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.lineup-header .page-title {
  margin: 0;
}

.add-link {
  display: inline-flex;
  align-items: center;
}

.add-link img {
  width: 2rem;
  height: 2rem;
  display: block;
}
</style>
