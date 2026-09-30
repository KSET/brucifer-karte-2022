<template>
  <Toast />
  <AdminTable :rows="lineups" :loading="loading" :searchFields="['name']" searchPlaceholder="Pretraži po imenu"
    image="image" imageSize="lg" reorderable editable :isRowBusy="row => isSaving(row.id)" :hint="hint"
    emptyText="Nema izvođača." editTitle="Uredi sliku" deleteTitle="Obriši izvođača"
    @cell-edit-complete="onCellEditComplete" @reorder="reorder" @edit="editLineup"
    @delete="confirmDelete">
    <Column field="name" header="Ime" style="width: 25%; min-width: 8rem">
      <template #body="{ data }">
        <span class="cell-text" :title="data.name">{{ data.name || '—' }}</span>
      </template>
      <template #editor="{ data, field }">
        <InputText v-model="data[field]" maxlength="49" autofocus fluid />
      </template>
    </Column>

    <Column field="biography" header="Biografija" style="width: 75%; min-width: 12rem">
      <template #body="{ data }">
        <span class="cell-text cell-clamp" :title="data.biography">{{ data.biography || '—' }}</span>
      </template>
      <template #editor="{ data, field }">
        <Textarea v-model="data[field]" rows="3" autoResize autofocus fluid
          @keydown.enter="onBioEnter" />
      </template>
    </Column>

    <Column field="visible" header="Vidljivo" style="width: 5.5rem" bodyClass="center-cell" headerClass="center-head">
      <template #body="{ data }">
        <Checkbox :modelValue="data.visible" binary :disabled="isSaving(data.id)"
          @update:modelValue="v => savePatch(data, { visible: v })" />
      </template>
    </Column>
  </AdminTable>
</template>

<script>
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'
import Toast from 'primevue/toast'

import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { useOptimisticList } from '@/composables/useOptimisticList'
import lineupStore from '@/store/lineupStore'

export default {
  name: 'LineupTable',
  components: { AdminTable, Column, InputText, Textarea, Checkbox, Toast },

  setup() {
    return useOptimisticList(lineupStore)
  },

  data() {
    return {
      hint: 'Povuci redak za promjenu redoslijeda. Klikni ćeliju za uređivanje (Ctrl/Cmd + Enter za spremanje biografije).',
    }
  },

  computed: {
    lineups() {
      return lineupStore.state.list
    },
    loading() {
      return lineupStore.state.loading
    },
  },

  async mounted() {
    await lineupStore.dispatch('fetchAll')
  },

  methods: {
    confirmDelete(row) {
      return this.remove(row, `Obrisati izvođača "${row.name}"?`)
    },

    editLineup(lineup) {
      this.$router.push({ path: `/admin/lineup-add/${lineup.slug}` })
    },

    rejectEdit(event, detail) {
      event.preventDefault()
      this.notifyError(detail)
    },

    isUnchanged(a, b) {
      const norm = v => (v === null || v === undefined ? '' : v)
      return norm(a) === norm(b)
    },

    onBioEnter(event) {
      if (event.ctrlKey || event.metaKey) return
      event.stopPropagation()
    },

    async onCellEditComplete(event) {
      const { data, newValue, field } = event

      const value = newValue

      if (field === 'name' && (!value || value.length > 49)) {
        return this.rejectEdit(event, 'Ime je obavezno (max 49 znakova).')
      }

      if (this.isUnchanged(value, data[field])) return

      await this.savePatch(data, { [field]: value })
    },
  },
}
</script>
