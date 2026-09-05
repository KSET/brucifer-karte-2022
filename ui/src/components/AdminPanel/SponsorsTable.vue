<template>
  <div class="sponsors-table" :class="{ filtering: isFiltering }" @mousedown="onRowDragStart"
    @dragend="onRowDragEnd">
    <Toast />

    <div class="table-toolbar">
      <IconField>
        <InputIcon class="pi pi-search" />
        <InputText v-model="filters.global.value" placeholder="Pretraži po imenu ili e-mailu" />
      </IconField>

      <small class="reorder-hint">
        {{ isFiltering
          ? 'Redoslijed se ne može mijenjati dok je pretraga aktivna.'
          : 'Povuci redak za promjenu redoslijeda. Klikni ćeliju za uređivanje.' }}
      </small>
    </div>

    <DataTable :value="sponsors" dataKey="id" :loading="loading" editMode="cell"
      @cell-edit-complete="onCellEditComplete" :reorderableRows="canReorder" @row-reorder="onRowReorder"
      v-model:filters="filters" :globalFilterFields="['name', 'email']" :rowClass="rowClass" scrollable
      scrollHeight="flex" size="small" tableStyle="table-layout: fixed; width: 100%; min-width: 54rem">
      <template #empty>
        <div class="empty">Nema sponzora.</div>
      </template>

      <Column :rowReorder="true" :reorderableColumn="false" style="width: 3rem" bodyClass="handle-cell center-cell" />

      <Column header="Slika" style="width: 9rem" bodyClass="center-cell" headerClass="center-head">
        <template #body="{ data }">
          <img class="sponsor-thumb" :class="{ dimmed: !data.visible }" :src="data.image" :alt="data.name">
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

      <Column field="url" header="Link" style="width: 37.5%; min-width: 10rem">
        <template #body="{ data }">
          <a class="cell-text url-cell" :href="data.url" :title="data.url" target="_blank" rel="noopener"
            @click.stop>{{ data.url }}</a>
        </template>
        <template #editor="{ data, field }">
          <InputText v-model="data[field]" autofocus fluid />
        </template>
      </Column>

      <Column field="email" header="E-mail" style="width: 37.5%; min-width: 10rem">
        <template #body="{ data }">
          <span class="cell-text" :title="data.email">{{ data.email || '—' }}</span>
        </template>
        <template #editor="{ data, field }">
          <Textarea v-model="data[field]" rows="2" autoResize autofocus fluid />
        </template>
      </Column>

      <Column field="guestCap" header="Uzvanici" style="width: 6.5rem" bodyClass="center-cell" headerClass="center-head">
        <template #body="{ data }">
          <span class="cell-text">{{ data.guestCap ?? '—' }}</span>
        </template>
        <template #editor="{ data, field }">
          <InputNumber v-model="data[field]" :min="0" autofocus fluid />
        </template>
      </Column>

      <Column field="visible" header="Vidljivo" style="width: 5.5rem" bodyClass="center-cell" headerClass="center-head">
        <template #body="{ data }">
          <Checkbox :modelValue="data.visible" binary :disabled="isSaving(data.id)"
            @update:modelValue="v => savePatch(data, { visible: v })" />
        </template>
      </Column>

      <Column field="guestsEnabled" header="Popis" style="width: 5.5rem" bodyClass="center-cell" headerClass="center-head">
        <template #body="{ data }">
          <Checkbox :modelValue="data.guestsEnabled !== 0" binary
            :disabled="isSaving(data.id)"
            :title="guestsLabel(data.guestsEnabled)"
            @update:modelValue="v => toggleGuests(data, v)" />
          <i v-if="data.guestsEnabled === 2" class="pi pi-lock closed-badge"
            :title="guestsLabel(data.guestsEnabled)"></i>
        </template>
      </Column>

      <Column header="" style="width: 6rem" bodyClass="center-cell">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" text rounded size="small" title="Uredi sliku"
            @click="editSponsor(data)" />
          <Button icon="pi pi-trash" text rounded size="small" severity="danger" title="Obriši sponzora"
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
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import { useToast } from 'primevue/usetoast'
import { FilterMatchMode } from '@primevue/core/api'

import sponsorsStore from '@/store/sponsorsStore'
import visibilityStore from '@/store/visibilityStore'

export default {
  name: 'SponsorsTable',
  components: {
    DataTable, Column, InputText, InputNumber, Textarea,
    Checkbox, Button, Toast, IconField, InputIcon,
  },

  // useToast() wraps inject(), which only resolves during setup(); calling it
  // from a lifecycle hook throws "No PrimeVue Toast provided!".
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
    sponsors() {
      return sponsorsStore.state.list
    },
    loading() {
      return sponsorsStore.state.loading
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
    await sponsorsStore.dispatch('fetchAll')
  },

  methods: {
    isSaving(id) {
      return (this.savingCounts[id] || 0) > 0
    },

    rowClass(row) {
      return this.isSaving(row.id) ? 'row-saving' : ''
    },

    editSponsor(sponsor) {
      this.$router.push({ path: `/admin/sponsors-add/${sponsor.slug}` })
    },

    notifyError(detail) {
      this.toast.add({ severity: 'error', summary: 'Greška', detail, life: 3000 })
    },

    rejectEdit(event, detail) {
      event.preventDefault()
      this.notifyError(detail)
    },

    guestsLabel(value) {
      if (value === 0) return 'Isključeno'
      if (value === 2) return 'Zatvoreno (isteklo vrijeme unosa)'
      return 'Otvoreno'
    },

    toggleGuests(row, checked) {
      if (!checked) {
        return this.savePatch(row, { guestsEnabled: 0 })
      }
      const value = visibilityStore.getters.sponsorsInputClosed ? 2 : 1
      return this.savePatch(row, { guestsEnabled: value })
    },

    isUnchanged(a, b) {
      const norm = v => (v === null || v === undefined ? '' : v)
      return norm(a) === norm(b)
    },

    async onCellEditComplete(event) {
      const { data, newValue, field } = event

      let value = newValue

      if (field === 'guestCap') {
        value = (newValue === '' || newValue === null) ? null : Number(newValue)
        if (value !== null && (!Number.isInteger(value) || value < 0)) {
          return this.rejectEdit(event, 'Broj uzvanika mora biti cijeli broj.')
        }
        if (value === null && data.guestCap !== null && data.guestCap !== undefined) {
          const ok = window.confirm(
            `Ukloniti ograničenje broja uzvanika za "${data.name}"? ` +
            'Sponzor će moći unijeti neograničen broj gostiju.')
          if (!ok) return this.rejectEdit(event, 'Promjena je odbačena.')
        }
      }
      if (field === 'name' && (!value || value.length > 49)) {
        return this.rejectEdit(event, 'Ime je obavezno (max 49 znakova).')
      }
      if (field === 'url' && value && !/^https?:\/\//.test(value)) {
        return this.rejectEdit(event, 'Link mora počinjati s http:// ili https://')
      }

      if (this.isUnchanged(value, data[field])) return

      await this.savePatch(data, { [field]: value })
    },

    async savePatch(row, changes) {
      const current = sponsorsStore.state.list.find(x => x.id === row.id)
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

      sponsorsStore.commit('PATCH_LIST_ITEM', { id: row.id, changes })
      this.savingCounts[row.id] = (this.savingCounts[row.id] || 0) + 1

      try {
        await sponsorsStore.dispatch('patch', { id: row.id, changes })
      } catch (e) {
        const revert = {}
        Object.keys(previous).forEach(k => {
          if (this.saveSeq[`${row.id}:${k}`] === tickets[k]) revert[k] = previous[k]
        })
        if (Object.keys(revert).length) {
          sponsorsStore.commit('PATCH_LIST_ITEM', { id: row.id, changes: revert })
        }
        this.notifyError('Promjena nije spremljena.')
      } finally {
        const next = (this.savingCounts[row.id] || 1) - 1
        if (next > 0) this.savingCounts[row.id] = next
        else delete this.savingCounts[row.id]
      }
    },

    // Must listen on mousedown, not dragstart: PrimeVue flips `draggable` on
    // the <tr> from its own mousedown handler, so by the time dragstart fires
    // the event target is the row, not the handle, and a handle check there
    // can never match -- which left every reorder disarmed. mousedown is the
    // same event PrimeVue keys off, and there the target really is the handle.
    //
    // The handle is an <svg> (BarsIcon); nodes inside an SVG are not always
    // Elements with closest(), so walk up from the nearest element instead.
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
        await sponsorsStore.dispatch('reorder', event.value)
      } catch (e) {
        this.notifyError(e?.stale
          ? 'Popis je u međuvremenu promijenjen; osvježen je, pokušaj ponovno.'
          : 'Redoslijed nije spremljen.')
      }
    },

    async confirmDelete(row) {
      if (!window.confirm(`Obrisati sponzora "${row.name}"?`)) return

      try {
        await sponsorsStore.dispatch('remove', row.id)
      } catch (e) {
        this.notifyError('Brisanje nije uspjelo.')
      }
    },
  },
}
</script>

<style scoped>
.sponsors-table {
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

.sponsor-thumb {
  display: inline-block;
  vertical-align: middle;
  width: 7rem;
  height: 2.75rem;
  object-fit: contain;
  background-color: #cfcfcf;
  border-radius: 3px;
  padding: 2px;
  box-sizing: border-box;
}

.sponsor-thumb.dimmed {
  opacity: 0.3;
}

.cell-text {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.url-cell {
  color: #111;
  text-decoration: none;
}

.url-cell:hover {
  text-decoration: underline;
}

.closed-badge {
  margin-left: 0.4rem;
  font-size: 0.75rem;
  color: #777;
  vertical-align: middle;
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
