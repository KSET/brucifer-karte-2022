<template>
  <div class="admin-table" :class="{ filtering: isFiltering }" @mousedown="onRowDragStart"
    @dragend="onRowDragEnd">
    <div v-if="hasToolbar" class="table-toolbar">
      <slot name="toolbar-start"></slot>

      <IconField v-if="searchFields.length">
        <InputIcon class="pi pi-search" />
        <InputText v-model="filters.global.value" :placeholder="searchPlaceholder" />
      </IconField>

      <slot name="toolbar"></slot>

      <small v-if="hintText" class="table-hint">{{ hintText }}</small>
    </div>

    <DataTable :value="rows" :dataKey="dataKey" :loading="loading" :editMode="editable ? 'cell' : undefined"
      @cell-edit-complete="e => $emit('cell-edit-complete', e)" :reorderableRows="canReorder"
      @row-reorder="onRowReorder" v-model:filters="filters" :globalFilterFields="searchFields"
      :rowClass="rowClass" scrollable scrollHeight="flex" size="small"
      :tableStyle="`table-layout: fixed; width: 100%; min-width: ${minWidth}`">
      <template #empty>
        <slot name="empty">
          <div class="empty">{{ emptyText }}</div>
        </slot>
      </template>

      <Column v-if="reorderable" :rowReorder="true" :reorderableColumn="false" style="width: 3rem"
        bodyClass="handle-cell center-cell" />

      <Column v-if="image" header="Slika" :style="{ width: imageSize === 'lg' ? '14rem' : '9rem' }"
        bodyClass="center-cell" headerClass="center-head">
        <template #body="{ data }">
          <img class="table-thumb" :class="[`thumb-${imageSize}`, { dimmed: isDimmed(data) }]"
            :src="imageSrc(data)" :alt="data.name">
        </template>
      </Column>

      <slot></slot>

      <Column v-if="hasActions" header="" style="width: 6rem" bodyClass="center-cell">
        <template #body="{ data }">
          <slot name="actions" :data="data">
            <Button v-if="onEdit" icon="pi pi-pencil" text rounded size="small" :title="editTitle"
              @click="onEdit(data)" />
            <Button v-if="onDelete" icon="pi pi-trash" text rounded size="small" severity="danger"
              :title="deleteTitle" @click="onDelete(data)" />
          </slot>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import { FilterMatchMode } from '@primevue/core/api'

export default {
  name: 'AdminTable',
  components: { DataTable, Column, InputText, Button, IconField, InputIcon },

  props: {
    rows: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    dataKey: { type: String, default: 'id' },
    searchFields: { type: Array, default: () => [] },
    searchPlaceholder: { type: String, default: 'Pretraži' },
    reorderable: { type: Boolean, default: false },
    image: { type: [String, Function], default: null },
    imageSize: { type: String, default: 'sm', validator: v => ['sm', 'lg'].includes(v) },
    imageDimmedField: { type: String, default: 'visible' },
    editable: { type: Boolean, default: false },
    isRowBusy: { type: Function, default: null },
    hint: { type: String, default: null },
    emptyText: { type: String, default: 'Nema podataka.' },
    minWidth: { type: String, default: '40rem' },
    editTitle: { type: String, default: 'Uredi' },
    deleteTitle: { type: String, default: 'Obriši' },
    onEdit: { type: Function, default: null },
    onDelete: { type: Function, default: null },
  },

  emits: ['reorder', 'cell-edit-complete'],

  data() {
    return {
      dragArmed: false,
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
    }
  },

  computed: {
    isFiltering() {
      return (this.filters.global.value || '').trim().length > 0
    },
    canReorder() {
      return this.reorderable && !this.isFiltering
    },
    hasActions() {
      return !!(this.onEdit || this.onDelete || this.$slots.actions)
    },
    hintText() {
      if (this.reorderable && this.isFiltering) {
        return 'Redoslijed se ne može mijenjati dok je pretraga aktivna.'
      }
      if (this.hint) return this.hint
      const parts = []
      if (this.reorderable) parts.push('Povuci redak za promjenu redoslijeda.')
      if (this.editable) parts.push('Klikni ćeliju za uređivanje.')
      return parts.join(' ')
    },
    hasToolbar() {
      return !!(this.searchFields.length || this.$slots['toolbar-start'] || this.$slots.toolbar || this.hintText)
    },
  },

  watch: {
    isFiltering() {
      this.dragArmed = false
    },
  },

  methods: {
    rowClass(row) {
      return this.isRowBusy?.(row) ? 'row-saving' : ''
    },

    imageSrc(row) {
      return typeof this.image === 'function' ? this.image(row) : row[this.image]
    },

    isDimmed(row) {
      return !!this.imageDimmedField && row[this.imageDimmedField] === false
    },
    
    onRowDragStart(event) {
      if (!this.reorderable) return
      const el = event.target instanceof Element
        ? event.target
        : event.target?.parentElement
      const fromHandle = !!el?.closest?.('.p-datatable-reorderable-row-handle')
      this.dragArmed = fromHandle && this.canReorder
    },

    onRowDragEnd() {
      this.dragArmed = false
    },

    onRowReorder(event) {
      const armed = this.dragArmed
      this.dragArmed = false
      if (!armed || this.isFiltering) return
      this.$emit('reorder', event.value)
    },
  },
}
</script>

<style scoped>
.admin-table {
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

.table-hint {
  color: #777;
  font-size: 12px;
}

.empty {
  padding: 2rem 0;
  text-align: center;
  color: #777;
}

.table-thumb {
  display: inline-block;
  vertical-align: middle;
  object-fit: contain;
  background-color: #cfcfcf;
  border-radius: 3px;
  padding: 2px;
  box-sizing: border-box;
}

.table-thumb.thumb-sm {
  width: 7rem;
  height: 2.75rem;
}

.table-thumb.thumb-lg {
  width: 12rem;
  height: 7rem;
}

.table-thumb.dimmed {
  opacity: 0.3;
}

/* Cell helpers for slot content rendered by the parent page. */
.admin-table :deep(.cell-text) {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.admin-table :deep(.cell-clamp) {
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
