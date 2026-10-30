<template>
  <div class="tagss">
    <Sidebar />
    <div class="admin-page-container admin-table-page">
      <div class="admin-table-header">
        <h1 class="page-title">Dnevni Izveještaj</h1>
      </div>
      <div v-if="failedMails.length" class="failed-mails">
        <h2 class="failed-mails-title">Neuspjeli mailovi ({{ failedMails.length }})</h2>
        <AdminTable :rows="failedMails" :loading="failedLoading" minWidth="50rem">
          <Column header="Gost">
            <template #body="{ data }">{{ data.name }} {{ data.surname }}</template>
          </Column>
          <Column field="jmbag" header="JMBAG" />
          <Column header="Email">
            <template #body="{ data }">{{ ticketEmail(data) }}</template>
          </Column>
          <Column header="Greška">
            <template #body="{ data }">{{ failureReason(data) }}</template>
          </Column>
          <template #actions="{ data }">
            <Button icon="pi pi-send" text rounded size="small" title="Pošalji ponovno"
              :loading="resendingId === data.id" :disabled="resendingId !== null" @click="resendMail(data)" />
          </template>
        </AdminTable>
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
import Button from 'primevue/button'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import AdminTable from '@/components/AdminPanel/AdminTable.vue'
import { api } from "@/plugins/api";
import { deriveFerEmail } from '@/utils/ferEmail';

export default {
  name: 'DailyReportView',
  components: { Sidebar, AdminTable, Column, Button },
  data() {
    return {
      dateSummary: [],
      loading: false,
      failedMails: [],
      failedLoading: false,
      resendingId: null,
    };
  },
  created() {
    this.fetchGuests();
    this.fetchFailedMails();
  },
  methods: {
    async fetchFailedMails() {
      this.failedLoading = true;
      try {
        const response = await api.get('/guests/failed-mails/');
        this.failedMails = response.data;
      } finally {
        this.failedLoading = false;
      }
    },
    ticketEmail(guest) {
      return deriveFerEmail(guest.name, guest.surname, guest.jmbag) || guest.email || '-';
    },
    failureReason(guest) {
      if (guest.mailError) return guest.mailError;
      return guest.mailStatus === 'pending' ? 'slanje nije dovršeno' : 'nepoznata greška';
    },
    async resendMail(guest) {
      this.resendingId = guest.id;
      try {
        const { data } = await api.post(`/guests/${guest.id}/resend-mail/`, {});
        if (data.mail_sent) {
          this.failedMails = this.failedMails.filter(g => g.id !== guest.id);
        } else {
          this.replaceFailed(guest.id, data.guest);
        }
      } catch (err) {
        this.replaceFailed(guest.id, {
          ...guest, mailError: err?.response?.data?.detail || 'ponovno slanje nije uspjelo' });
      } finally {
        this.resendingId = null;
      }
    },
    replaceFailed(id, updated) {
      this.failedMails = this.failedMails.map(g => (g.id === id ? updated : g));
    },
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

<style scoped>
.failed-mails {
  display: flex;
  flex-direction: column;
  max-height: 40vh;
  margin-bottom: 2rem;
  flex-shrink: 0;
}

.failed-mails-title {
  margin: 0 0 0.75rem;
  font-size: 1.1rem;
  color: #c62828;
}
</style>
