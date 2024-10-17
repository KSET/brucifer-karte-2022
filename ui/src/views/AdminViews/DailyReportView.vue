<template>
  <div class="tagss">
    <Sidebar />
    <div class="admin-page-container">
      <div class="page-header">
        <h1 class="page-title">Dnevni Izveještaj</h1>
      </div>
      <div class="tags-table">
        <div class="row">
          <table id="guests">
            <thead>
              <th>Datum</th>
              <th>Prodane ukupno u danu</th>
              <th>Prodane smjena prije 13.00</th>
              <th>Prodane smjena poslije 13.00</th>
            </thead>
            <tbody>
              <tr v-for="date in dateSummary" :key="date.date">
                <td>{{ formatDate(date.date) }}</td>
                <td>{{ date.totalEntries }}</td>
                <td>{{ date.ticketsBefore13 }}</td>
                <td>{{ date.ticketsAfter13 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import axios from 'axios';

export default {
  name: 'DailyReportView',
  components: { Sidebar },
  data() {
    return {
      dateSummary: [],
      name: ''
    };
  },
  created() {
    this.fetchGuests();
  },
  methods: {
    async fetchGuests() {
      const response = await axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=1&search_fields=bought');
      this.guests = response.data;
      this.processDailyReport();
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
            dateSummary[date] = { totalEntries: 0, ticketsBefore13: 0, ticketsAfter13: 0 };
          }
          dateSummary[date].totalEntries++;
          if (hours < 13) {
            dateSummary[date].ticketsBefore13++;
          } else {
            dateSummary[date].ticketsAfter13++;
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



<style>
#title0 {
  display: inline-block;
}

.tags-table {
  height: 100%;
}

.inputtag {
  height: 40px;
  text-align: left;
  width: 80%;
  vertical-align: top;
  font-family: 'Montserrat';

  height: 39px;
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;

  font-size: 16px;

  border: 1px solid black;
}

.add-icon {
  padding-top: 2px;
  padding-left: 5px;
  height: 40px;
  vertical-align: top;
}
</style>