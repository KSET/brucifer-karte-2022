<template>
  <Toast />
  <AdminTable :rows="tags" :loading="loading" :searchFields="['name']" searchPlaceholder="Pretraži po imenu"
    emptyText="Nema tagova." deleteTitle="Obriši tag" @delete="deleteTag">
    <Column field="name" header="Ime" footer="Ukupno">
      <template #body="{ data }">
        <span class="cell-text" :style="{ paddingLeft: `${data.depth * 1.5}rem` }"
          :title="data.name">{{ data.name }}</span>
      </template>
    </Column>
    <Column field="count" :footer="String(totals.count)" header="Broj" style="width: 7rem" bodyClass="center-cell" headerClass="center-head"
      footerClass="center-cell" />
    <Column field="bought" :footer="String(totals.bought)" header="Karta" style="width: 7rem" bodyClass="center-cell" headerClass="center-head"
      footerClass="center-cell" />
    <Column field="entered" :footer="String(totals.entered)" header="Ulaz" style="width: 7rem" bodyClass="center-cell" headerClass="center-head"
      footerClass="center-cell" />
  </AdminTable>
</template>

<script>
import Column from 'primevue/column'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'

import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { api } from "@/plugins/api";

export default {
  name: 'TagsTable',
  components: { AdminTable, Column, Toast },

  setup() {
    return { toast: useToast() }
  },

  data() {
    return {
      tags: [],
      totals: { count: 0, bought: 0, entered: 0 },
      loading: false,
    };
  },
  created() {
    this.fetchTags();
  },
  methods: {
    async fetchTags() {
      this.loading = true;
      try {
        const { data } = await api.get(`/tags/stats/`);
        this.tags = data.tags;
        this.totals = data.totals;
      } catch (error) {
        console.error('Failed to fetch tags:', error);
      } finally {
        this.loading = false;
      }
    },
    async deleteTag(tag) {
      if (!window.confirm(`Obrisati tag "${tag.name}"?`)) return
      try {
        await api.delete(`/tags/${tag.id}/`);
        this.fetchTags();
      } catch (error) {
        this.toast.add({ severity: 'error', summary: 'Greška', detail: 'Brisanje nije uspjelo.', life: 3000 })
      }
    }
  }
};
</script>

<style>
.button-icon {
  border: 0px;
  background-color: white;
  padding: 0px;
}

tbody {
  display: block;
  height: 80%;
  overflow: auto;
}

thead,
tbody tr {
  display: table;
  width: 80%;
  table-layout: fixed;
}
</style>
