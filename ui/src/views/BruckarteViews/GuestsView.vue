<template>
  <div class="guestss">
    <CircularLoading :dialog="dialogProgress"></CircularLoading>

    <div class="header guests">
      <input class="nosubmit search" @input="prepSearchGuest" type="form" v-model="search" placeholder="Unesi JMBAG">

      <v-progress-circular v-if="loading == true" size="90px" indeterminate color="black"></v-progress-circular>
      <h1 class="textfield" :class="{ 'error-text': isFormMissing }"> {{ this.nomatch }}</h1>
    </div>
    <p style="color: black; text-align: center;">Napomenite brucošima da karta dolazi na mail i da dolazi u SPAM/JUNK!
    </p>

    <div class="grid-container guests">
      <h1 class="textfield">Ime </h1>
      <input class="inputfield" :disabled="this.name == ''" type="text" @input="changeValue" v-model="name">

      <h1 class="textfield">Prezime </h1>
      <input class="inputfield" :disabled="this.surname == ''" type="text" @input="changeValue" v-model="surname">

      <h1 class="textfield">JMBAG </h1>
      <input class="inputfield" readonly type="text" v-model="jmbag">

      <h1 class="textfield">Karta </h1>

      <button class="button change" :disabled="this.id == ''" v-if="guest.bought == '1'"
        @click="prepChangebought(guest, '0')">
        <img src="../../assets/icons/yes-icon.svg">
      </button>
      <button class="button change" :disabled="this.id == ''" v-else @click="prepChangebought(guest, '1')"
        style="background-color: white;">
        <img class="image1" src="../../assets/icons/no-icon.svg">
      </button>

      <h1 class="textfield">Potvrda </h1>
      <h1 class="textfield">{{ this.confCode }} </h1>

      <h1 class="textfield">Vrijeme kupnje karte </h1>
      <h1 class="textfield">{{ formatDate(this.boughtTicketTime) }} </h1>
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
                <v-list-item-subtitle>{{ submission.email }}</v-list-item-subtitle>
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
  </div>
</template>




<script>
import { uuid } from 'vue-uuid';
import GuestsAdd from '@/components/Bruckarte/GuestsAdd.vue'
import GuestsTable from '@/components/Bruckarte/GuestsTable.vue'
import CircularLoading from '@/components/Default/CircularLoading.vue';
import debounce from 'lodash/debounce';
import { api } from "@/plugins/api";

export default {
  name: 'GuestsView',
  components: {
    GuestsTable,
    GuestsAdd,
    CircularLoading
  },
  data() {
    return {
      guest: '',
      guests: [],
      mails: [],
      id: '',
      name: '',
      surname: '',
      jmbag: '',
      phone: '',
      tag: '',
      bought: '',
      entered: '',
      deleted: '',
      nomatch: '',
      confCode: '',
      boughtTicketTime: '',
      isFormMissing: false,
      dialog: false,
      dialogProgress: false,

      loading: false,

      submissionPickerOpen: false,
      submissionCandidates: [],

      uuid: uuid.v1(),

    }
  },
  mounted() {
    this.searchGuest = debounce(this.searchGuest, 1000);
    this.changeValue = debounce(this.changeValue, 1000);
    this.changeBought = debounce(this.changeBought, 1000);

  },
  methods: {
    changeValue() {
      if (this.guest != '') {
        api.put('/guests/' + this.guest.id + '/',
          { name: this.name, surname: this.surname },
        )
      }
    },
    prepChangebought(guest, changenum) {
      if (changenum == 1) {
        this.dialogProgress = true;
      }

      this.changeBought(guest, changenum)
    },
    changeBought(guest, changenum) {
      if (this.name === "" || this.surname === "") {
        window.alert("Ispunite polja ime i prezime!");
      } else {
        let confCode, boughtTicketTime;

        if (changenum == 1) {
          confCode = this.$uuid.v1();
          boughtTicketTime = new Date().toISOString();
        } else {
          confCode = "";
          boughtTicketTime = null;
        }

        api.put(`/guests/${guest.id}/`, {
          name: this.name,
          surname: this.surname,
          bought: changenum,
          confCode: confCode,
          boughtTicketTime: boughtTicketTime
        })
          .then(() => {
            guest.bought = changenum;
            guest.confCode = confCode;
            guest.boughtTicketTime = boughtTicketTime;
            guest.name = this.name;
            guest.surname = this.surname;

            this.boughtTicketTime = boughtTicketTime;
            this.confCode = confCode;

            if (changenum == 1) {
              this.sendMail(guest);
            }
          });
      }
    },
    prepSearchGuest() {
      this.nomatch = ""
      this.loading = true;

      this.searchGuest()
    },
    searchGuest() {
      api.get(`/guests/search-brucosi/?jmbag=${encodeURIComponent(this.search)}`)
        .then(response => {
          this.loading = false;
          this.isFormMissing = false;

          const { guests = [], submissions = [] } = response.data;
          this.guests = guests;

          console.log(submissions)

          if (this.guests.length === 1) {
            this.nomatch = "";
            this.guest = this.guests[0];
            this.id = this.guest.id;
            this.name = this.guest.name || "";
            this.surname = this.guest.surname || "";
            this.jmbag = this.guest.jmbag || "";
            this.confCode = this.guest.confCode || "";
            this.boughtTicketTime = this.guest.boughtTicketTime || "";

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
                this.openSubmissionPicker?.(fillCandidates);
                this.nomatch = `Pronađeno ${fillCandidates.length} podudaranja iz prijava – odaberite ispravno ime/prezime.`;
              }
            }

          } else if (this.guests.length === 0) {
            this.nomatch = "JMBAG nije pronađen!";
            this.id = "";
            this.name = "";
            this.surname = "";
            this.jmbag = "";
            this.confCode = "";
            this.boughtTicketTime = "";

          } else if (this.guests.length > 1 && this.guests.length < 20) {
            this.nomatch = `Pronađeno ${this.guests.length} podudaranja, nastavite upisivati`;

          } else {
            this.nomatch = "";
            this.id = "";
            this.name = "";
            this.surname = "";
            this.jmbag = "";
            this.confCode = "";
            this.boughtTicketTime = "";
            this.bought = "0";
          }
        })
        .catch(err => {
          this.loading = false;
          console.error("Search error:", err?.response?.data || err.message);
          this.nomatch = "Greška prilikom pretraživanja.";
        });
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
    async sendMail(guest) {

      console.log("send mail attempt")

      var jmbagslice = guest.jmbag;
      if (jmbagslice.slice(0, 3) == "003") {
        jmbagslice = jmbagslice.slice(4, 9);
      } else if (jmbagslice.slice(0, 1) == "0") {
        jmbagslice = jmbagslice.slice(0, 9);
      } else {
        jmbagslice = jmbagslice.slice(2, 7);
      }

      var e_name = this.name[0].toLowerCase()
      if (e_name == "č") {
        e_name = "c";
      } else if (e_name == "š") {
        e_name = "s";
      } else if (e_name == "ž") {
        e_name = "z";
      } else if (e_name == "đ") {
        e_name = "d";
      } else if (e_name == "ć") {
        e_name = "c";
      }

      var e_surname = this.surname[0].toLowerCase()
      if (e_surname == "č") {
        e_surname = "c";
      } else if (e_surname == "š") {
        e_surname = "s";
      } else if (e_surname == "ž") {
        e_surname = "z";
      } else if (e_surname == "đ") {
        e_surname = "d";
      } else if (e_surname == "ć") {
        e_surname = "c";
      }


      var email = e_name + e_surname + jmbagslice + "@fer.hr";

      this.email = email
      // za testiranje, maknuti u produkciji
      // email = "pavleergovic@gmail.com"

      var msg = this.name + " " + this.surname + " " + guest.confCode

      await api.post('/mailer/send_mail/',
        {
          emails: [
            {
              subject: "[#BRUCIFER25] Potvrda za kupljenu kartu",
              template: "guest_email",
              message: msg,
              name: this.name,
              confCode: guest.confCode,
              to_mail: email
            }]
        },
      )
      await api.post('/mailer/',
        {
          subject: "[#BRUCIFER25] Potvrda za kupljenu kartu",
          template: "guest_email",
          message: msg,
          name: this.name,
          confCode: guest.confCode,
          to_mail: email
        },
      )
      this.dialogProgress = false;
      this.dialog = true;
    },
    formatDate(date) {
      if (date == '' || date == null) {
        return ''
      }
      const d = new Date(date);
      const day = d.getDate().toString().padStart(2, '0');
      const month = (d.getMonth() + 1).toString().padStart(2, '0'); // Month is 0-based, thus add 1
      const year = d.getFullYear();
      const hours = d.getHours().toString().padStart(2, '0');
      const minutes = d.getMinutes().toString().padStart(2, '0');
      const seconds = d.getSeconds().toString().padStart(2, '0');
      return `${day}.${month}.${year}. ${hours}:${minutes}:${seconds}`;
    },
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
</style>
