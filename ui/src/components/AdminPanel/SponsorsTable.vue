<template>
  <DataTable class="sponsors-table" scrollable :value="sponsors" dataKey="id" editMode="cell" reorderableRows
    @rowReorder="onRowReorder" @cell-edit-complete="onCellEditComplete" stripedRows :pt="{
      table: { style: 'min-width: 64rem' },
      column: { bodycell: ({ state }) => ({ class: [{ '!py-0': state['d_editing'] }] }) }
    }">
    <!-- Drag handle -->
    <Column rowReorder :reorderableColumn="false" style="width: 3rem !important" />

    <!-- Logo (read-only) -->
    <Column header="Logo" style="width:8rem !important">
      <template #body="{ data }">
        <img :src="data.image"
          :style="{ opacity: data.visible === '0' ? 0.25 : 1, height: '5rem', width: '5rem', background: '#D9D9D9', objectFit: 'contain' }"
          alt="logo" />
      </template>
    </Column>

    <!-- Name -->
    <Column field="name" header="Name" frozen alignFrozen="left">
      <template #editor="{ data, field }">
        <InputText v-model="data[field]" autofocus fluid />
      </template>
    </Column>

    <!-- Email -->
    <Column field="email" header="Email" style="min-width:16rem">
      <template #editor="{ data, field }">
        <InputText v-model="data[field]" autofocus fluid />
      </template>
    </Column>

    <!-- URL -->
    <Column field="url" header="URL" style="min-width:18rem">
      <template #body="{ data }">
        <a :href="data.url" target="_blank" rel="noopener">{{ data.url }}</a>
      </template>
      <template #editor="{ data, field }">
        <InputText v-model="data[field]" autofocus fluid />
      </template>
    </Column>

    <!-- guestCap -->
    <Column field="guestCap" header="Guest Cap" style="width:10rem">
      <template #editor="{ data, field }">
        <InputNumber v-model="data[field]" :min="0" :max="9999" :useGrouping="false" autofocus fluid />
      </template>
    </Column>

    <!-- Visible: ALWAYS a checkbox -->
    <Column field="visible" header="Visible" style="width:9rem" :editable="false">
      <template #body="{ data }">
        <div class="flex items-center justify-center">
          <Checkbox v-model="data.visibleBool" :binary="true" @change="onVisibleToggle(data)" />
        </div>
      </template>
    </Column>
  </DataTable>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import sponsorsStore from '@/store/sponsorsStore'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'

export default {
  name: 'SponsorsTable',
  components: { DataTable, Column, InputText, InputNumber, Checkbox },
  data() {
    return {
      buttonEnabled: true,
    }
  },

  computed: {
    sponsors() {
      return sponsorsStore.state.list
    },
    loading() {
      return sponsorsStore.state.loading
    },
    error() {
      return sponsorsStore.state.error
    },
    isBusy() {
      return this.loading || !this.buttonEnabled
    },
  },

  async mounted() {
    await sponsorsStore.dispatch('fetchAll')
  },

  methods: {
    editsponsor(sponsor) {
      this.$router.push({ path: `/admin/sponsors-add/${sponsor.slug}` })
    },

    canMoveBack(sponsor) {
      const idx = this.sponsors.indexOf(sponsor)
      return idx > 0
    },

    canMoveForward(sponsor) {
      const idx = this.sponsors.indexOf(sponsor)
      return idx > -1 && idx < this.sponsors.length - 1
    },

    async changesponsororder(sponsor, direction) {
      if (this.isBusy) return
      this.buttonEnabled = false

      try {
        const idx = this.sponsors.indexOf(sponsor)
        if (idx === -1) return

        let neighbor = null
        if (direction === 'f' && this.canMoveForward(sponsor)) {
          neighbor = this.sponsors[idx + 1]
        } else if (direction !== 'f' && this.canMoveBack(sponsor)) {
          neighbor = this.sponsors[idx - 1]
        }
        if (!neighbor) return

        const payload = [
          { id: sponsor.id, order: neighbor.order },
          { id: neighbor.id, order: sponsor.order },
        ]

        await sponsorsStore.dispatch('reorder', payload)
        await sponsorsStore.dispatch('fetchAll')
      } catch (e) {
        console.error(e)
        alert('Promjena poretka sponzora nije uspjela.')
      } finally {
        this.buttonEnabled = true
      }
    },
  },
}
</script>


<style scoped>
.sponsors-table .ccard-img {
  max-width: 100%;
}
</style>

<style>
.sponsors-table {
  --p-inputtext-focus-border-color: black;
  font-size: 0.85rem !important;
}

.p-datatable .p-cell-editing {
  padding: 0 !important;
}

.sponsors-table .p-datatable-thead>tr>th,
.sponsors-table .p-datatable-tbody>tr>td {
  padding: 0.4rem 0.6rem;
  font-size: 0.85rem;
  vertical-align: middle;
}

.sponsors-table .p-datatable-tbody>tr>td {
  white-space: normal;
  word-break: break-word;
  max-width: 200px;
}

.p-inputtext {
  font-size: 0.85rem !important;
}

thead,
tr {
  width: 100% !important;
}

td {
  width: fit-content !important;
}
</style>
