<template>
  <Toast />
  <AdminTable :rows="sponsors" :loading="loading" :searchFields="['name', 'email']"
    searchPlaceholder="Pretraži po imenu ili e-mailu" image="image" imageSize="sm" reorderable editable
    :isRowBusy="row => isSaving(row.id)" emptyText="Nema sponzora." minWidth="54rem" editTitle="Uredi sliku"
    deleteTitle="Obriši sponzora" @cell-edit-complete="onCellEditComplete" @reorder="reorder"
    @edit="editSponsor" @delete="confirmDelete">
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
  </AdminTable>
</template>

<script>
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import Checkbox from 'primevue/checkbox'
import Toast from 'primevue/toast'

import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { useOptimisticList } from '@/composables/useOptimisticList'
import sponsorsStore from '@/store/sponsorsStore'
import visibilityStore from '@/store/visibilityStore'

export default {
  name: 'SponsorsTable',
  components: { AdminTable, Column, InputText, InputNumber, Textarea, Checkbox, Toast },

  setup() {
    return useOptimisticList(sponsorsStore)
  },

  computed: {
    sponsors() {
      return sponsorsStore.state.list
    },
    loading() {
      return sponsorsStore.state.loading
    },
  },

  async mounted() {
    await sponsorsStore.dispatch('fetchAll')
  },

  methods: {
    confirmDelete(row) {
      return this.remove(row, `Obrisati sponzora "${row.name}"?`)
    },

    editSponsor(sponsor) {
      this.$router.push({ path: `/admin/sponsors-add/${sponsor.slug}` })
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
  },
}
</script>

<style scoped>
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
</style>
