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

    <Column field="stage" header="Stage" style="width: 9rem; min-width: 9rem">
      <template #body="{ data }">
        <span class="cell-text">{{ stageLabel(data.stage) || '—' }}</span>
      </template>
      <template #editor="{ data, field }">
        <Select v-model="data[field]" :options="stageOptions" optionLabel="label" optionValue="value"
          placeholder="—" showClear fluid @clear="data[field] = ''" />
      </template>
    </Column>

    <Column field="startTime" header="Početak" style="width: 11rem; min-width: 11rem">
      <template #body="{ data }">
        <span class="cell-text">{{ formatTime(data.startTime) || '—' }}</span>
      </template>
      <template #editor="{ data, field }">
        <InputText type="datetime-local" :modelValue="toLocalInput(data[field])" autofocus fluid
          @change="data[field] = toIso($event.target.value)" />
      </template>
    </Column>

    <Column field="endTime" header="Kraj" style="width: 11rem; min-width: 11rem">
      <template #body="{ data }">
        <span class="cell-text">{{ formatTime(data.endTime) || '—' }}</span>
      </template>
      <template #editor="{ data, field }">
        <InputText type="datetime-local" :modelValue="toLocalInput(data[field])" autofocus fluid
          @change="data[field] = toIso($event.target.value)" />
      </template>
    </Column>

    <Column field="biography" header="Biografija" style="width: 50%; min-width: 12rem">
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
import Select from 'primevue/select'
import Toast from 'primevue/toast'

import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { useOptimisticList } from '@/composables/useOptimisticList'
import lineupStore from '@/store/lineupStore'
import { zagrebLocalToDate, dateToZagrebLocalInput, formatZagreb, parseStored } from '@/utils/datetime'
import { STAGE_OPTIONS, stageLabel } from '@/utils/stages'

const TIME_FIELDS = ['startTime', 'endTime']

export default {
  name: 'LineupTable',
  components: { AdminTable, Column, InputText, Textarea, Checkbox, Select, Toast },

  setup() {
    return useOptimisticList(lineupStore)
  },

  data() {
    return {
      hint: 'Povuci redak za promjenu redoslijeda. Klikni ćeliju za uređivanje (Ctrl/Cmd + Enter za spremanje biografije).',
      stageOptions: STAGE_OPTIONS,
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

    stageLabel,

    formatTime(value) {
      return formatZagreb(parseStored(value))
    },

    toLocalInput(value) {
      return dateToZagrebLocalInput(parseStored(value))
    },

    toIso(localValue) {
      const date = zagrebLocalToDate(localValue)
      return date ? date.toISOString() : null
    },

    timeOf(value) {
      return parseStored(value)?.getTime() ?? null
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

      if (TIME_FIELDS.includes(field)) {
        if (this.timeOf(value) === this.timeOf(data[field])) return

        const start = this.timeOf(field === 'startTime' ? value : data.startTime)
        const end = this.timeOf(field === 'endTime' ? value : data.endTime)
        if (start !== null && end !== null && end <= start) {
          return this.rejectEdit(event, 'Kraj nastupa mora biti nakon početka.')
        }
      }

      if (this.isUnchanged(value, data[field])) return

      await this.savePatch(data, { [field]: value })
    },
  },
}
</script>
