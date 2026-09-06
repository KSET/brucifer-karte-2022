<template>
  <div class="lineup-table" :class="{ filtering: isFiltering }" @mousedown="onRowDragStart"
    @dragend="onRowDragEnd">
    <Toast />

    <div class="table-toolbar">
      <IconField>
        <InputIcon class="pi pi-search" />
        <InputText v-model="filters.global.value" placeholder="Pretraži po imenu" />
      </IconField>

      <small class="reorder-hint">
        {{ isFiltering
          ? 'Redoslijed se ne može mijenjati dok je pretraga aktivna.'
          : 'Povuci redak za promjenu redoslijeda. Klikni ćeliju za uređivanje (Ctrl/Cmd + Enter za spremanje biografije).' }}
      </small>
    </div>

    <DataTable :value="lineups" dataKey="id" :loading="loading" editMode="cell"
      @cell-edit-complete="onCellEditComplete" :reorderableRows="canReorder" @row-reorder="onRowReorder"
      v-model:filters="filters" :globalFilterFields="['name']" :rowClass="rowClass" scrollable
      scrollHeight="flex" size="small" tableStyle="table-layout: fixed; width: 100%; min-width: 40rem">
      <template #empty>
        <div class="empty">Nema izvođača.</div>
      </template>

      <Column :rowReorder="true" :reorderableColumn="false" style="width: 3rem" bodyClass="handle-cell center-cell" />

      <Column header="Slika" style="width: 14rem" bodyClass="center-cell" headerClass="center-head">
        <template #body="{ data }">
          <img class="lineup-thumb" :class="{ dimmed: !data.visible }" :src="data.image" :alt="data.name">
        </template>
      </Column>

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
          <span class="cell-text bio-cell" :title="data.biography">{{ data.biography || '—' }}</span>
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

      <Column header="" style="width: 6rem" bodyClass="center-cell">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" text rounded size="small" title="Uredi sliku"
            @click="editLineup(data)" />
          <Button icon="pi pi-trash" text rounded size="small" severity="danger" title="Obriši izvođača"
            @click="confirmDelete(data)" />
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import { useToast } from 'primevue/usetoast'
import { FilterMatchMode } from '@primevue/core/api'

import lineupStore from '@/store/lineupStore'

export default {
  name: 'LineupTable',
  components: {
    DataTable, Column, InputText, Textarea,
    Checkbox, Button, Toast, IconField, InputIcon,
  },

  setup() {
    return { toast: useToast() }
  },

  data() {
    return {
      savingCounts: {},
      saveSeq: {},
      dragArmed: false,
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
    }
  },

  computed: {
    lineups() {
      return lineupStore.state.list
    },
    loading() {
      return lineupStore.state.loading
    },
    isFiltering() {
      return (this.filters.global.value || '').trim().length > 0
    },
    canReorder() {
      return !this.isFiltering
    },
  },

  watch: {
    isFiltering() {
      this.dragArmed = false
    },
  },

  async mounted() {
    await lineupStore.dispatch('fetchAll')
  },

  methods: {
    isSaving(id) {
      return (this.savingCounts[id] || 0) > 0
    },

    rowClass(row) {
      return this.isSaving(row.id) ? 'row-saving' : ''
    },

    editLineup(lineup) {
      this.$router.push({ path: `/admin/lineup-add/${lineup.slug}` })
    },

    notifyError(detail) {
      this.toast.add({ severity: 'error', summary: 'Greška', detail, life: 3000 })
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

    async savePatch(row, changes) {
      const current = lineupStore.state.list.find(x => x.id === row.id)
      if (!current) return

      const previous = {}
      const tickets = {}
      Object.keys(changes).forEach(k => {
        previous[k] = current[k]
        const key = `${row.id}:${k}`
        const ticket = (this.saveSeq[key] || 0) + 1
        this.saveSeq[key] = ticket
        tickets[k] = ticket
      })

      lineupStore.commit('PATCH_LIST_ITEM', { id: row.id, changes })
      this.savingCounts[row.id] = (this.savingCounts[row.id] || 0) + 1

      try {
        await lineupStore.dispatch('patch', { id: row.id, changes })
      } catch (e) {
        const revert = {}
        Object.keys(previous).forEach(k => {
          if (this.saveSeq[`${row.id}:${k}`] === tickets[k]) revert[k] = previous[k]
        })
        if (Object.keys(revert).length) {
          lineupStore.commit('PATCH_LIST_ITEM', { id: row.id, changes: revert })
        }
        this.notifyError('Promjena nije spremljena.')
      } finally {
        const next = (this.savingCounts[row.id] || 1) - 1
        if (next > 0) this.savingCounts[row.id] = next
        else delete this.savingCounts[row.id]
      }
    },

    onRowDragStart(event) {
      const el = event.target instanceof Element
        ? event.target
        : event.target?.parentElement
      const fromHandle = !!el?.closest?.('.p-datatable-reorderable-row-handle')
      this.dragArmed = fromHandle && this.canReorder
    },

    onRowDragEnd() {
      this.dragArmed = false
    },

    async onRowReorder(event) {
      const armed = this.dragArmed
      this.dragArmed = false
      if (!armed || this.isFiltering) return

      try {
        await lineupStore.dispatch('reorder', event.value)
      } catch (e) {
        this.notifyError(e?.stale
          ? 'Popis je u međuvremenu promijenjen; osvježen je, pokušaj ponovno.'
          : 'Redoslijed nije spremljen.')
      }
    },

    async confirmDelete(row) {
      if (!window.confirm(`Obrisati izvođača "${row.name}"?`)) return

      try {
        await lineupStore.dispatch('remove', row.id)
      } catch (e) {
        this.notifyError('Brisanje nije uspjelo.')
      }
    },
  },
}
</script>

<style scoped>
.lineup-table {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  min-width: 0;
  font-family: 'Montserrat', sans-serif;
}

:deep(.p-datatable) {
  display: flex;
  flex-direction: column;
  min-height: 0;
  flex: 1;
}

:deep(.p-datatable-table-container) {
  flex: 1;
  min-height: 0;
  overflow: auto;
}

.table-toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  flex-shrink: 0;
}

.reorder-hint {
  color: #777;
  font-size: 12px;
}

.empty {
  padding: 2rem 0;
  text-align: center;
  color: #777;
}

.lineup-thumb {
  display: inline-block;
  vertical-align: middle;
  width: 12rem;
  height: 7rem;
  object-fit: contain;
  background-color: #cfcfcf;
  border-radius: 3px;
  padding: 2px;
  box-sizing: border-box;
}

.lineup-thumb.dimmed {
  opacity: 0.3;
}

.cell-text {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bio-cell {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
  line-clamp: 4;
  white-space: normal;
}

:deep(.p-datatable-table) {
  border-collapse: collapse;
}

:deep(.p-datatable-thead > tr > th) {
  background-color: #111;
  color: #fff;
  font-weight: 600;
  font-size: 12px;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  padding: 0.6rem 0.75rem;
  border: 0;
  white-space: nowrap;
}

:deep(.p-datatable-tbody > tr > td) {
  font-size: 13px;
  padding: 0.5rem 0.75rem;
  border: 0;
  border-bottom: 1px solid #ececec;
  overflow: hidden;
}

:deep(.p-datatable-tbody > tr:hover) {
  background-color: #fafafa;
}

:deep(.p-datatable-tbody > tr.row-saving) {
  opacity: 0.5;
}

:deep(.p-datatable-tbody > tr > td[data-p-editable-column="true"]:hover) {
  outline: 1px solid #ddd;
  outline-offset: -1px;
  cursor: text;
}

:deep(.p-datatable-tbody > tr > td[data-p-cell-editing="true"]) {
  padding: 0.25rem 0.5rem;
  overflow: visible;
}

:deep(td.center-cell) {
  text-align: center;
}

:deep(th.center-head) {
  text-align: center;
}

:deep(th.center-head .p-datatable-column-header-content) {
  justify-content: center;
}

:deep(td.handle-cell) {
  color: #bbb;
}

:deep(td.handle-cell .p-datatable-reorderable-row-handle) {
  display: inline-block;
}

:deep(.p-datatable-reorderable-row-handle) {
  cursor: grab;
}

.filtering :deep(.p-datatable-reorderable-row-handle) {
  opacity: 0.25;
  cursor: not-allowed;
}

:deep(.p-datatable-table td),
:deep(.p-datatable-table th) {
  background-image: none;
}

:deep(.p-datatable-table tbody) {
  display: table-row-group;
  height: auto;
  overflow: visible;
}

:deep(.p-datatable-table tbody > tr) {
  display: table-row;
  width: auto;
}

:deep(.p-datatable-thead) {
  display: table-header-group;
}

:deep(.p-datatable-thead > tr > th) {
  position: sticky;
  top: 0;
  z-index: 1;
}
</style>
