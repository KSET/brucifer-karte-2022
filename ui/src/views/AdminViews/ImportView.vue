<template>
  <div class="import">
    <Sidebar />
    <div class="admin-page-container">
      <h1 class="page-title">Uvoz Gostiju</h1>
      <br>
      <label for="file-upload" class="button-upload ">
        Odaberi CSV
      </label>
      <input id="file-upload" type="file" @change="importGuests" />
      <button class="button-upload white" @click="exportExample(1)">Preuzmi CSV template</button>

      <h1 class="textfield" style="display: inline-block">{{ this.importstatusGuests }}</h1>

      <div>
        <ul class="list">
          <li>Prvi redak mora sadržavati imena polja koja moraju biti lowercase te u istom formatu kao u sljedećemredu
          </li>
          <li>Imena polja mogu biti: name, surname, jmbag, email, tag, bought, entered</li>
          <li>Tablica ne mora sadržavati sva imena polja, redoslijed stupaca nije bitan</li>
          <li>Ukoliko se polje tag kod nekog gosta ostavi prazno, tag će automatski biti Brucoši</li>
          <li>Ukoliko se polja bought i entered kod nekog gosta ostave prazna, bit će postavljena na 0</li>
        </ul>
      </div>
      <h1 class="page-title">Uvoz Korisnika</h1>
      <br>
      <label for="file-uploadd" class="button-upload ">
        Odaberi CSV
      </label>
      <input id="file-uploadd" type="file" @change="importUsers" />
      <button class="button-upload white" @click="exportExample(2)">Preuzmi CSV template</button>

      <h1 class="textfield" style="display: inline-block">{{ this.importstatusUsers }}</h1>

      <div>
        <ul class="list">
          <li>Prvi redak mora sadržavati imena polja koja moraju biti lowercase te u istom formatu kao u sljedećem redu.
          </li>
          <li>Imena polja mogu biti: name, email, privilege.</li>
          <li>Mogće vrijednosti privilege su cijeli brojevi izmešu 0 i 4 s uključivim granicama.</li>
          <li>Polje name može se ostaviti prazno, taj podatadak će se sam updeatati kada se korisnik prijavi</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import * as XLSX from 'xlsx'
import { XlsxRead, XlsxJson } from "../../../node_modules/vue3-xlsx/dist/vue3-xlsx.cjs.prod.js";
import readXlsxFile from 'read-excel-file';
import axios from 'axios';

export default {
  components: {
    XlsxRead,
    XlsxJson,
    Sidebar
  },
  data() {
    return {
      file: null,
      collection: null,
      guests: [],
      users: [],
      idsguests: [],
      idsusers: [],
      importstatusGuests: '',
      importstatusUsers: '',
    };
  },
  mounted() {
    axios.get(process.env.VUE_APP_BASE_URL + '/guests/',)
      .then(response => {
        this.guests = response.data;
        this.len = this.guests.length;
        this.guests.forEach(element => {
          this.idsguests.push(element.id);
        });
        axios.get(process.env.VUE_APP_BASE_URL + '/users/',)
          .then(response => {
            this.users = response.data;
            this.len = this.guests.length;

            this.users.forEach(element => {
              this.idsusers.push(element.id);
            });

          })
      })
  },
  methods: {
    exportExample(version) {
      if (version == 1) {
        var filename = 'import_example_guests.xlsx';
        var data = [{
          "name": "",
          "surname": "",
          "tag": "",
          "jmbag": 23945624
        },
        {
          "name": "",
          "surname": "",
          "tag": "",
          "jmbag": 23495862
        },
        {
          "name": "",
          "surname": "",
          "tag": "",
          "jmbag": 13659968
        },
        {
          "name": "",
          "surname": "",
          "tag": "",
          "jmbag": 36594856
        },
        {
          "name": "Ivan",
          "surname": "Svetić",
          "tag": "VIP",
          "jmbag": ""
        },
        {
          "name": "Maja",
          "surname": "Kovačević",
          "tag": "VIP",
          "jmbag": ""
        },
        {
          "name": "Petar",
          "surname": "Penić",
          "tag": "KSET",
          "jmbag": ""
        },
        {
          "name": "Tena",
          "surname": "Botas",
          "tag": "KSET",
          "jmbag": ""
        }];
      } else {
        var filename = 'import_example_users.xlsx';
        var data = [
          {
            "name": "",
            "email": "toni.batos@kset.org",
            "privilege": 3
          },
          {
            "name": "Zrika Petrović",
            "email": "zrinka.petrovic@kset.org",
            "privilege": 1
          },
          {
            "name": "",
            "email": "alen.ivic@kset.org",
            "privilege": 2
          },
          {
            "name": "Korina Ban",
            "email": "korina.ban@kset.org",
            "privilege": 2
          },
          {
            "name": "",
            "email": "tin.tinović@gmail.com",
            "privilege": 2
          },
          {
            "name": "Marija Erić",
            "email": "marija.eric@kset.org",
            "privilege": 1
          }
        ]
      }
      var ws = XLSX.utils.json_to_sheet(data);
      var wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "People");
      XLSX.writeFile(wb, filename);
    },
    async importGuests(event) {
      this.file = event.target.files ? event.target.files[0] : null;

      try {
        const rows = await readXlsxFile(this.file);
        const headerRow = rows[0];
        const guestsData = rows.slice(1).map(row => {
          const guest = {};
          headerRow.forEach((columnName, columnIndex) => {
            guest[columnName.toLowerCase()] = row[columnIndex] || "";
          });

          // Set default values for tag, bought, and entered fields if they are empty or 0
          guest.tag = guest.tag || "Brucoši";
          guest.bought = guest.bought || "0";
          guest.entered = guest.entered || "0";

          return guest;
        });

        console.log(guestsData);

        const response = await axios.post(`${process.env.VUE_APP_BASE_URL}/guests/bulk-import/`,
          guestsData,
          {
            auth: {
              username: process.env.VUE_APP_DJANGO_USER,
              password: process.env.VUE_APP_DJANGO_PASS
            }
          }
        );

        this.importstatusGuests = `Import successful! Imported ${guestsData.length} guests.`;
      } catch (error) {
        console.error("Import unsuccessful!", error);
        this.importstatusGuests = "Import unsuccessful!";
      }
    }
    ,
    async importUsers(event) {
      this.file = event.target.files ? event.target.files[0] : null;

      try {
        const rows = await readXlsxFile(this.file);
        const headerRow = rows[0];
        const usersData = rows.slice(1).map(row => {
          const user = {};
          headerRow.forEach((columnName, columnIndex) => {
            user[columnName.toLowerCase()] = row[columnIndex] || "";
          });
          return user;
        });

        console.log(usersData);

        const response = await axios.post(`${process.env.VUE_APP_BASE_URL}/users/bulk-import/`,
          usersData,
          {
            auth: {
              username: process.env.VUE_APP_DJANGO_USER,
              password: process.env.VUE_APP_DJANGO_PASS
            }
          }
        );

        this.importstatusUsers = `Import successful! Imported ${usersData.length} users.`;
      } catch (error) {
        console.error("Bulk import unsuccessful for some users", error);
        this.importstatusUsers = "Import unsuccessful!";
      }
    }


  }
}
</script>

<style >
.button-upload {
  display: inline-block;
  margin-right: 33px;
  color: white;
  height: 40px;
  width: 130px;
  background: #000000;
  border-radius: 6px;
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 230%;
  text-align: center;
  vertical-align: top;
}

.button-upload.white {
  line-height: 100%;
  width: 250px;
  color: black;
  background: white;
}


input[type="file"] {
  display: none;

}

ul.list {
  margin-top: 2.5%;
  margin-bottom: 2.5%;
  list-style-type: auto;
}


li {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
}
</style>