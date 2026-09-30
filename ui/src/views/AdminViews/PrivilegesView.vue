<template>
  <div id="privileges">
    <Sidebar />
    <div class="admin-page-container admin-table-page">
      <div class="admin-table-header">
        <h1 class="page-title">Privilegije</h1>
      </div>
      <AdminTable :rows="rows" dataKey="code" :loading="loading" minWidth="20rem">
        <template #toolbar>
          <strong class="privileges-total">Ukupno {{ total }}</strong>
        </template>
        <Column field="code" header="Oznaka" style="width: 7rem" />
        <Column field="name" header="Ime" />
        <Column field="count" header="Broj" style="width: 7rem" bodyClass="center-cell" headerClass="center-head" />
      </AdminTable>
    </div>
  </div>
</template>

<script>
import Column from 'primevue/column'
import { api } from "@/plugins/api";
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { NONE, ADMIN, ENTRY, TICKETS, ENTRY_TICKETS } from "@/plugins/roles";

const PRIVILEGES = [
  { code: 0, role: NONE, name: 'Ništa' },
  { code: 1, role: ADMIN, name: 'Admin' },
  { code: 2, role: ENTRY, name: 'Ulaz' },
  { code: 3, role: TICKETS, name: 'Karte' },
  { code: 4, role: ENTRY_TICKETS, name: 'Ulaz+Karte' },
];

export default {
  name: 'PrivilegesView',
  components: { Sidebar, AdminTable, Column },
  data() {
    return {
      users: [],
      loading: false,
    }
  },
  computed: {
    rows() {
      return PRIVILEGES.map(p => ({
        code: p.code,
        name: p.name,
        count: this.users.filter(u => u.privilege == p.role).length,
      }));
    },
    total() {
      return this.rows.reduce((sum, r) => sum + r.count, 0);
    },
  },
  async mounted() {
    this.loading = true;
    try {
      const response = await api.get('/users/');
      this.users = response.data;
    } finally {
      this.loading = false;
    }
  },
}
</script>

<style scoped>
.privileges-total {
  font-size: 14px;
  word-spacing: 6px;
}
</style>

<style>
#guests {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
  text-align: left;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;

}

#guests td,
#guests th {
  border: 0px;
  border-bottom: 0.5px solid black;
  padding: 8px;
  text-align: left;
  vertical-align: middle;
  font-family: 'Montserrat';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  font-size: 16px;
}

#guests tr {
  overflow: auto;
}



#guests tr:nth-child(even) {
  background-color: white;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
}

#guests tr:hover {
  background-color: white;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
}

#guests th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: white;
  color: black;
}
</style>


