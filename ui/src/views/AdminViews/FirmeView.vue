<template>
    <div id="firme">
        <Sidebar />
        <div class="admin-page-container admin-table-page">
            <div class="admin-table-header">
                <h1 class="page-title">Firme</h1>
            </div>
            <AdminTable :rows="firms" :loading="loading" :searchFields="['name']"
                searchPlaceholder="Pretraži po imenu firme" emptyText="Nema firmi.">
                <Column field="name" header="Firma">
                    <template #body="{ data }">
                        <span class="cell-text" :title="data.name">{{ data.name }}</span>
                    </template>
                </Column>
                <Column field="guestCap" header="Odobreno" style="width: 8rem" bodyClass="center-cell"
                    headerClass="center-head">
                    <template #body="{ data }">{{ data.guestCap ?? '—' }}</template>
                </Column>
                <Column field="guestsAdded" header="Upisano" style="width: 8rem" bodyClass="center-cell"
                    headerClass="center-head" />
                <Column field="guestsEntered" header="Ušlo" style="width: 8rem" bodyClass="center-cell"
                    headerClass="center-head" />
            </AdminTable>
        </div>
    </div>
</template>

<script>
import Column from 'primevue/column'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { api } from '@/plugins/api';

export default {
    name: 'FirmeView',
    components: { Sidebar, AdminTable, Column },
    data() {
        return {
            firms: [],
            loading: false,
        }
    },
    async mounted() {
        this.loading = true;
        try {
            const response = await api.get('/sponsors/');

            this.firms = await Promise.all(response.data.map(async sponsor => {
                const guests = await api.get('/guests/?search=' + sponsor.slug + "&search_fields=tag")
                    .then(r => r.data)
                    .catch(() => []);
                return {
                    ...sponsor,
                    guestsAdded: guests.length,
                    guestsEntered: guests.filter(g => g.entered === true).length,
                };
            }));
        } finally {
            this.loading = false;
        }
    },
}
</script>
