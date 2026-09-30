<template>
  <Toast />
  <AdminTable :rows="tags" :loading="loading" :searchFields="['name']" searchPlaceholder="Pretraži po imenu"
    emptyText="Nema tagova." deleteTitle="Obriši tag" @delete="deleteTag">
    <Column field="name" header="Ime">
      <template #body="{ data }">
        <span class="cell-text" :title="data.name">{{ data.name }}</span>
      </template>
    </Column>
    <Column field="count" header="Broj" style="width: 7rem" bodyClass="center-cell" headerClass="center-head" />
    <Column field="bought" header="Karta" style="width: 7rem" bodyClass="center-cell" headerClass="center-head" />
    <Column field="entered" header="Ulaz" style="width: 7rem" bodyClass="center-cell" headerClass="center-head" />
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
        const response = await api.get(`/tags/`);
        await this.processTags(response.data);
      } catch (error) {
        console.error('Failed to fetch tags:', error);
      } finally {
        this.loading = false;
      }
    },
    async processTags(tags) {
      try {
        for (const tag of tags) {
          const response = await api.get(`/guests/?search=${tag.name}&search_fields=tag`);
          let { numc, numb, nume } = { numc: 0, numb: 0, nume: 0 };

          response.data.forEach(guest => {
            numc++;
            if (guest.bought === true) numb++;
            if (guest.entered === true) nume++;
          });

          if (numc != tag.count || numb !== tag.bought || nume !== tag.entered) {
            await api.put(`/tags/${tag.id}/`,
              { count: numc, bought: numb, entered: nume },
            );

            Object.assign(tag, { count: numc, bought: numb, entered: nume });
          }
        }
        this.tags = [...tags];
      } catch (error) {
        console.error('Failed to process tags:', error);
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
