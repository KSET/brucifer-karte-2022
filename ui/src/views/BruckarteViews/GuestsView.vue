<template>
  <div class="guestss">
    <CircularLoading :dialog="selling"></CircularLoading>

    <div class="header guests">
      <input class="nosubmit search" @input="prepSearchGuest" type="form" v-model="search" placeholder="Unesi JMBAG">

      <v-progress-circular v-if="loading == true" size="90px" indeterminate color="black"></v-progress-circular>
      <h1 class="textfield" :class="{ 'error-text': isFormMissing || isError }"> {{ this.nomatch }}</h1>
      <button class="button change" @click="getTodayStats">Dohvati broj prodanih karata</button>
    </div>
    <p style="color: black; text-align: center;">
      Napomenite brucošima da karta dolazi na mail!
    </p>

    <div class="grid-container guests">
      <h1 class="textfield">Ime </h1>
      <input class="inputfield" :disabled="this.name == ''" type="text" @input="changeValue" v-model="name">

      <h1 class="textfield">Prezime </h1>
      <input class="inputfield" :disabled="this.surname == ''" type="text" @input="changeValue" v-model="surname">

      <h1 class="textfield">JMBAG </h1>
      <input class="inputfield" readonly type="text" v-model="jmbag">

      <h1 class="textfield">Karta </h1>

      <button class="button change" :disabled="this.id == ''" v-if="guest.bought == true" @click="onSoldClick">
        <img src="../../assets/icons/yes-icon.svg">
      </button>
      <button class="button change" :disabled="this.id == '' || selling" v-else @click="sell"
        style="background-color: white;">
        <img class="image1" src="../../assets/icons/no-icon.svg">
      </button>

      <h1 class="textfield">Potvrda </h1>
      <h1 class="textfield">{{ this.confCode }} </h1>

      <h1 class="textfield">Vrijeme kupnje karte </h1>
      <h1 class="textfield">{{ formatDate(this.boughtTicketTime) }} </h1>
    </div>

    <div class="mail-warning" v-if="mailFailureReason">
      <p><strong>Karta prodana, ali mail nije poslan:</strong> {{ mailFailureReason }}. Javite blagajniku ili web adminu.</p>
      <p>Email: {{ ticketEmail }}</p>
      <p>Potvrda: {{ confCode }}</p>
      <v-btn v-if="isAdmin" color="primary" :loading="resending" @click="resendMail">Pošalji ponovno</v-btn>
    </div>


    <v-dialog v-model="dialog">
      <v-card>
        <v-card-text style="height:150%">
          <div class="grid-container guests">
            <h1 class="textfield">Ime </h1>
            <input class="inputfield" readonly type="text" v-model="name">

            <h1 class="textfield">Prezime </h1>
            <input class="inputfield" readonly type="text" v-model="surname">

            <h1 class="textfield">JMBAG </h1>
            <input class="inputfield" readonly type="text" v-model="jmbag">

            <h1 class="textfield" style="grid-column: span 2;"> Brucoš je uspješno kupio kartu, te mu je poslan
              konfirmacijski mail na: {{ this.email }}
            </h1>
          </div>

        </v-card-text>


        <v-card-actions>
          <v-btn color="primary" block @click="dialog = false">Zatvori</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="unsellInfoOpen" max-width="500px">
      <v-card>
        <v-card-text>
          <p>Pokušavate maknuti kupljenu kartu, javite se blagajniku ili web adminu</p>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" block @click="unsellInfoOpen = false">Zatvori</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="confirmUnsellOpen" max-width="500px" :persistent="unselling">
      <v-card>
        <v-card-title>
          Poništiti prodaju za {{ name }} {{ surname }}?
        </v-card-title>
        <v-card-actions>
          <v-btn text :disabled="unselling" @click="confirmUnsellOpen = false">Odustani</v-btn>
          <v-btn color="error" :loading="unselling" @click="unsell">Poništi prodaju</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="submissionPickerOpen" max-width="500px">
      <v-card>
        <v-card-title>
          Odaberi prijavu
        </v-card-title>

        <v-card-text>
          <v-list>
            <v-list-item v-for="submission in submissionCandidates" :key="submission.id"
              @click="selectSubmission(submission)" class="submission-item">
              <v-list-item-content>
                <v-list-item-title>{{ submission.name }} {{ submission.surname }}</v-list-item-title>
                <v-list-item-subtitle>{{ submissionEmail(submission) }}</v-list-item-subtitle>
                <v-list-item-subtitle>{{ formatDate(submission.submitted_at) }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions>
          <v-btn text @click="submissionPickerOpen = false">Zatvori</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="todayStatsDialog" max-width="500px">
      <v-card>
        <v-card-title>
          Statistika za danas
        </v-card-title>

        <v-card-text v-if="todayStats">
          <p><strong>Datum:</strong> {{ formatStatDate(todayStats.date) }}</p>
          <p><strong>Ukupno prodano:</strong> {{ todayStats.totalEntries }}</p>
          <p><strong>Prije 12h:</strong> {{ todayStats.ticketsBefore12 }}</p>
          <p><strong>Poslije 12h:</strong> {{ todayStats.ticketsAfter12 }}</p>
        </v-card-text>

        <v-card-actions>
          <v-btn color="primary" block @click="todayStatsDialog = false">Zatvori</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>




<script>
import GuestsAdd from '@/components/Bruckarte/GuestsAdd.vue'
import GuestsTable from '@/components/Bruckarte/GuestsTable.vue'
import CircularLoading from '@/components/Default/CircularLoading.vue';
import debounce from 'lodash/debounce';
import { api } from "@/plugins/api";
import store from "@/store/index.js";
import { ADMIN } from "@/plugins/roles";
import { deriveFerEmail } from '@/utils/ferEmail';

const FAILED_MAIL_STATUSES = ['failed', 'bounced'];

export default {
  name: 'GuestsView',
  components: {
    GuestsTable,
    GuestsAdd,
    CircularLoading
  },
  data() {
    return {
      search: '',
      guest: '',
      id: '',
      name: '',
      surname: '',
      jmbag: '',
      email: '',
      nomatch: '',
      confCode: '',
      boughtTicketTime: '',
      isFormMissing: false,
      isError: false,
      dialog: false,

      loading: false,
      searchSeq: 0,

      selling: false,
      resending: false,
      unselling: false,
      mailWarning: '',
      unsellInfoOpen: false,
      confirmUnsellOpen: false,

      todayStatsDialog: false,
      todayStats: null,

      submissionPickerOpen: false,
      submissionCandidates: [],
    }
  },
  computed: {
    isAdmin() {
      return store.getters.hasAnyRole(ADMIN);
    },
    ticketEmail() {
      return this.email || deriveFerEmail(this.name, this.surname, this.jmbag);
    },
    mailFailureReason() {
      if (this.mailWarning) return this.mailWarning;
      if (this.guest && this.guest.bought && FAILED_MAIL_STATUSES.includes(this.guest.mailStatus)) {
        return this.guest.mailError || 'nepoznata greška';
      }
      return '';
    }
  },
  created() {
    this.searchGuest = debounce(this.searchGuest, 400);
    this.changeValue = debounce(this.changeValue, 1000);
  },
  methods: {
    submissionEmail(submission) {
      return deriveFerEmail(submission.name, submission.surname, submission.jmbag);
    },
    async getTodayStats() {
      try {
        this.loading = true;
        const response = await api.get("/guests/today-stats/");
        this.todayStats = response.data;
        this.todayStatsDialog = true;
      } catch (error) {
        console.error("Error fetching today stats:", error);
        this.todayStats = {
          date: new Date().toISOString().slice(0, 10),
          totalEntries: "-",
          ticketsBefore12: "-",
          ticketsAfter12: "-",
        };
        this.todayStatsDialog = true;
      } finally {
        this.loading = false;
      }
    },
    loadGuest(guest) {
      this.guest = guest;
      this.id = guest.id;
      this.name = guest.name || "";
      this.surname = guest.surname || "";
      this.jmbag = guest.jmbag || "";
      this.email = guest.email || "";
      this.confCode = guest.confCode || "";
      this.boughtTicketTime = guest.boughtTicketTime || "";
      this.mailWarning = "";
    },
    resetGuest() {
      this.changeValue.cancel();
      this.guest = "";
      this.id = "";
      this.name = "";
      this.surname = "";
      this.jmbag = "";
      this.email = "";
      this.confCode = "";
      this.boughtTicketTime = "";
      this.mailWarning = "";
      this.isFormMissing = false;
    },
    showError(message) {
      this.nomatch = message;
      this.isError = true;
    },
    async changeValue() {
      const guest = this.guest;
      if (!guest) return;
      const name = this.name.trim();
      const surname = this.surname.trim();
      if (name === (guest.name || "") && surname === (guest.surname || "")) return;
      try {
        await api.patch(`/guests/${guest.id}/`, { name, surname });
        guest.name = name;
        guest.surname = surname;
      } catch (err) {
        if (this.guest === guest) this.showError("Spremanje imena nije uspjelo.");
      }
    },
    async sell() {
      if (!this.guest || this.selling) return;
      if (!this.name.trim() || !this.surname.trim()) {
        window.alert("Ispunite polja ime i prezime!");
        return;
      }
      if (!deriveFerEmail(this.name, this.surname, this.jmbag)) {
        this.showError("Nedostaje ime, prezime ili JMBAG - email nije poslan.");
        return;
      }
      const guestId = this.id;
      this.selling = true;
      try {
        await this.changeValue.flush();
        const { data } = await api.post(`/guests/${guestId}/sell/`,
          { name: this.name.trim(), surname: this.surname.trim() });
        if (this.id !== guestId) return;
        this.loadGuest(data.guest);
        if (data.mail_sent) {
          this.dialog = true;
        } else {
          this.mailWarning = data.mail_error || 'nepoznata greška';
        }
      } catch (err) {
        if (err?.response?.status === 409) {
          this.showError("Karta je već prodana.");
          this.refreshGuest(guestId);
        } else {
          this.showError(err?.response?.data?.detail || "Greška prilikom prodaje, pokušajte ponovno.");
        }
      } finally {
        this.selling = false;
      }
    },
    async refreshGuest(guestId) {
      try {
        const { data } = await api.get(`/guests/${guestId}/`);
        if (this.id === guestId) this.loadGuest(data);
      } catch (err) {
        // the error message from the failed action is already shown
      }
    },
    async resendMail() {
      const guestId = this.id;
      this.resending = true;
      try {
        const { data } = await api.post(`/guests/${guestId}/resend-mail/`,
          { name: this.name.trim(), surname: this.surname.trim() });
        if (this.id !== guestId) return;
        this.loadGuest(data.guest);
        if (data.mail_sent) {
          this.dialog = true;
        } else {
          this.mailWarning = data.mail_error || 'nepoznata greška';
        }
      } catch (err) {
        this.mailWarning = err?.response?.data?.detail || 'ponovno slanje nije uspjelo';
      } finally {
        this.resending = false;
      }
    },
    onSoldClick() {
      if (this.isAdmin) {
        this.confirmUnsellOpen = true;
      } else {
        this.unsellInfoOpen = true;
      }
    },
    async unsell() {
      const guestId = this.id;
      this.unselling = true;
      try {
        const { data } = await api.post(`/guests/${guestId}/unsell/`);
        if (this.id === guestId) this.loadGuest(data.guest);
      } catch (err) {
        this.showError(err?.response?.data?.detail || "Poništavanje prodaje nije uspjelo.");
      } finally {
        this.unselling = false;
        this.confirmUnsellOpen = false;
      }
    },
    prepSearchGuest() {
      this.changeValue.flush();
      this.nomatch = "";
      this.isError = false;

      if (!this.search.trim()) {
        this.searchGuest.cancel();
        this.searchSeq++;
        this.loading = false;
        this.resetGuest();
        return;
      }
      this.loading = true;
      this.searchGuest()
    },
    async searchGuest() {
      const seq = ++this.searchSeq;
      try {
        const response = await api.get(`/guests/search-brucosi/?jmbag=${encodeURIComponent(this.search.trim())}`);
        if (seq !== this.searchSeq) return;
        this.isFormMissing = false;

        const { count = 0, guests = [], submissions = [] } = response.data;

        if (count !== 1) {
          this.resetGuest();
          if (count === 0) {
            this.nomatch = "JMBAG nije pronađen!";
          } else if (count < 10) {
            this.nomatch = `Pronađeno ${count} podudaranja, nastavite upisivati`;
          }
          return;
        }

        this.nomatch = "";
        this.loadGuest(guests[0]);

        const needsName = !this.name;
        const needsSurname = !this.surname;

        if (submissions.length == 0) {
          this.nomatch = `JMBAG pronađen, ali korisnik nije ispunio formu.`;
          this.isFormMissing = true;
          return
        }

        if (needsName || needsSurname) {
          const fillCandidates = submissions.filter(s =>
            s &&
            s.jmbag === this.jmbag && (
              (needsName && s.name) ||
              (needsSurname && s.surname)
            )
          );

          if (fillCandidates.length === 1) {
            const s = fillCandidates[0];
            if (needsName && s.name) this.name = s.name;
            if (needsSurname && s.surname) this.surname = s.surname;
          } else if (fillCandidates.length > 1) {
            this.openSubmissionPicker(fillCandidates);
            this.nomatch = `Pronađeno ${fillCandidates.length} podudaranja iz prijava – odaberite ispravno ime/prezime.`;
          }
        }
      } catch (err) {
        if (seq !== this.searchSeq) return;
        this.resetGuest();
        this.showError("Greška prilikom pretraživanja.");
      } finally {
        if (seq === this.searchSeq) this.loading = false;
      }
    },
    openSubmissionPicker(candidates) {
      this.submissionCandidates = candidates;
      this.submissionPickerOpen = true;
    },
    selectSubmission(submission) {
      if (!this.name && submission.name) this.name = submission.name;
      if (!this.surname && submission.surname) this.surname = submission.surname;

      this.submissionPickerOpen = false;
    },
    formatDate(date) {
      if (date == '' || date == null) {
        return ''
      }
      const d = new Date(date);
      const day = d.getDate().toString().padStart(2, '0');
      const month = (d.getMonth() + 1).toString().padStart(2, '0');
      const year = d.getFullYear();
      const hours = d.getHours().toString().padStart(2, '0');
      const minutes = d.getMinutes().toString().padStart(2, '0');
      const seconds = d.getSeconds().toString().padStart(2, '0');
      return `${day}.${month}.${year}. ${hours}:${minutes}:${seconds}`;
    },
    formatStatDate(date) {
      const d = new Date(date);
      const day = d.getDate().toString().padStart(2, '0');
      const month = (d.getMonth() + 1).toString().padStart(2, '0');
      const year = d.getFullYear();
      return `${day}.${month}.${year}.`;
    }
  }

}
</script>

<style lang="scss" scoped>
@import url('https://fonts.cdnfonts.com/css/montserrat');
@import '../../assets/scss/Admin-scss/gird-view.scss';

.header.guests {
  height: 7.188rem;
  width: 100%;
  border-bottom: 1px solid black;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 1rem;
  justify-content: space-between;
  padding-right: 3%;

}

.submission-item {
  cursor: pointer;
  border-bottom: 1px solid black;
}

.submission-item:hover {
  background-color: lightgray;
}

.nosubmit.search {
  margin-top: 0rem;
  width: 20%;
  left: 0% !important;
}

.grid-container.guests {
  margin-top: 3.5%;
  margin-left: 6%;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}

p {
  color: black;
}



@media screen and (max-width: 980px) {
  .nosubmit.search {
    width: 40% !important;
    font-size: 12px;
  }

  .inputfield {
    width: 80% !important;
  }
}

@media screen and (max-width: 550px) {
  .nosubmit.search {
    width: 55% !important;
  }
}

.error-text {
  color: red;
}

.mail-warning {
  margin: 1.5rem 6%;
  padding: 1rem;
  border: 2px solid red;
  color: red;
}

.mail-warning p {
  color: red;
}
</style>
