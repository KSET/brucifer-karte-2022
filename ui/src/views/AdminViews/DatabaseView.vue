<template>
    <div id="database">
        <Sidebar />
        <div class="admin-page-container admin-table-page">
            <div class="admin-table-header">
                <h1 class="page-title">Baza podataka</h1>
            </div>
            <AdminTable :key="table" :rows="rows" :loading="loading" :dataKey="pk" :searchFields="columns"
                :minWidth="`${Math.max(columns.length, 4) * 10}rem`" :hint="truncatedHint"
                :emptyText="table ? 'Tablica je prazna.' : 'Odaberi tablicu.'">
                <template #toolbar-start>
                    <Select v-model="table" :options="tableOptions" optionLabel="name" optionValue="table" filter
                        placeholder="Odaberi tablicu" :loading="tablesLoading" :dt="pickerTokens"
                        class="table-picker" />
                </template>
                <Column v-for="c in columns" :key="c" :field="c" :header="c" style="width: 10rem">
                    <template #body="{ data }">
                        <span class="cell-text" :title="fmt(data[c])">{{ fmt(data[c]) }}</span>
                    </template>
                </Column>
            </AdminTable>
        </div>
    </div>
</template>

<script>
import Column from 'primevue/column'
import Select from 'primevue/select'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { api } from '@/plugins/api';

export default {
    name: 'DatabaseView',
    components: { Sidebar, AdminTable, Column, Select },
    data() {
        return {
            tables: [],
            tablesLoading: false,
            table: this.$route.query.table || null,
            columns: [],
            pk: 'id',
            rows: [],
            total: 0,
            truncated: false,
            loading: false,
            pickerTokens: {
                option: {
                    selectedBackground: '#ececec',
                    selectedFocusBackground: '#e0e0e0',
                    selectedColor: '#000',
                    selectedFocusColor: '#000',
                },
            },
        }
    },
    computed: {
        tableOptions() {
            return this.tables.map(t => ({ ...t, name: `${t.table.replace(/^bruc_/, '')} (${t.count})` }));
        },
        truncatedHint() {
            return this.truncated ? `Prikazano prvih ${this.rows.length} od ${this.total} redaka.` : null;
        },
    },
    watch: {
        table(value) {
            if (value !== this.$route.query.table) {
                this.$router.replace({ query: value ? { table: value } : {} });
            }
            this.fetchRows();
        },
    },
    async mounted() {
        this.tablesLoading = true;
        try {
            const response = await api.get('/db/tables/');
            this.tables = response.data;
        } catch (error) {
            if (error.response?.status === 403) return;
            console.error('Failed to fetch tables:', error);
        } finally {
            this.tablesLoading = false;
        }
        if (this.table) this.fetchRows();
    },
    methods: {
        async fetchRows() {
            const table = this.table;
            if (!table) {
                this.columns = [];
                this.rows = [];
                this.truncated = false;
                return;
            }
            this.loading = true;
            try {
                const { data } = await api.get(`/db/tables/${encodeURIComponent(table)}/`);
                if (table !== this.table) return;
                this.columns = data.columns;
                this.pk = data.pk;
                this.rows = data.rows;
                this.total = data.total;
                this.truncated = data.truncated;
            } catch (error) {
                console.error('Failed to fetch table:', error);
                if (table === this.table) {
                    this.columns = [];
                    this.rows = [];
                    this.truncated = false;
                }
            } finally {
                if (table === this.table) this.loading = false;
            }
        },
        fmt(value) {
            if (value === null || value === undefined || value === '') return '—';
            if (typeof value === 'object') return JSON.stringify(value);
            return String(value);
        },
    },
}
</script>

<style scoped>
.table-picker {
    min-width: 18rem;
}
</style>
