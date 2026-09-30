<template>
  <div class="tagss">
    <Sidebar />
    <div class="admin-page-container admin-table-page">
      <div class="admin-table-header">
        <h1 class="page-title">Dnevni Izveještaj</h1>
      </div>
      <AdminTable :rows="dateSummary" dataKey="date" :loading="loading" emptyText="Nema prodanih karata.">
        <Column field="date" header="Datum">
          <template #body="{ data }">{{ formatDate(data.date) }}</template>
        </Column>
        <Column field="totalEntries" header="Prodane ukupno u danu" />
        <Column field="ticketsBefore12" header="Prodane smjena prije 12.00" />
        <Column field="ticketsAfter12" header="Prodane smjena poslije 12.00" />
      </AdminTable>
    </div>
  </div>
</template>

<script>
import Column from 'primevue/column'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { api } from "@/plugins/api";

export default {
  name: 'DailyReportView',
  components: { Sidebar, AdminTable, Column },
  data() {
    return {
      dateSummary: [],
      loading: false,
    };
  },
  created() {
    this.fetchGuests();
  },
  methods: {
    async fetchGuests() {
      this.loading = true;
      try {
        const response = await api.get('/guests/?bought=true');
        this.guests = response.data;
        this.processDailyReport();
      } finally {
        this.loading = false;
      }
    },
    processDailyReport() {
      let entries = this.guests;
      const dateSummary = {};

      entries.forEach(entry => {
        const { boughtTicketTime } = entry;
        if (boughtTicketTime) {
          const localDateTime = new Date(boughtTicketTime);
          const date = localDateTime.toLocaleDateString('en-CA');
          const hours = localDateTime.getHours();
          if (!dateSummary[date]) {
            dateSummary[date] = { totalEntries: 0, ticketsBefore12: 0, ticketsAfter12: 0 };
          }
          dateSummary[date].totalEntries++;
          if (hours < 12) {
            dateSummary[date].ticketsBefore12++;
          } else {
            dateSummary[date].ticketsAfter12++;
          }
        }
      });

      this.dateSummary = Object.entries(dateSummary)
        .sort((a, b) => b[0].localeCompare(a[0]))
        .map(([date, details]) => ({ date, ...details }));
    },
    formatDate(date) {
      const d = new Date(date);
      const day = d.getDate().toString().padStart(2, '0');
      const month = (d.getMonth() + 1).toString().padStart(2, '0');
      const year = d.getFullYear();
      return `${day}.${month}.${year}.`;
    }
  }
}
</script>
