<template>
  <div class="import">
    <br>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Import</div>
          <div class="card-body">
            <section>
              <input class="btn btn-primary" type="file" @change="importGuests" />
            </section>
            <section>
              <br>
              <h1>Prvi redak mora sadržavati imena polja koja moraju biti lowercase te u istom formatu kao u sljedećem
                redu</h1>
              <h1>Imena polja mogu biti: name surname jmbag email tag bought entered</h1>
              <h1>Tablica ne mora sadržavati sva imena polja, redoslijed stupaca nije bitan</h1>
              <h1>Ukoliko se polje tag kod nekog gosta ostavi prazno, tag će automatski biti Brucoši</h1>
              <h1>Ukoliko se polja bought i entered kod nekog gosta ostave prazna, bit će postavljena na 0</h1>
              <br>
              <button type="submit" onclick="window.open('../assets/import_example.xlsx')">Download!</button>

              <a class="btn btn-primary" href="../assets/import_example.xlsx" download="import_example.xlsx">Download
                example</a>
            </section>
            <section>
              <input class="btn btn-primary" type="file" @change="importUsers" />
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

import { XlsxRead, XlsxJson } from "../../node_modules/vue3-xlsx/dist/vue3-xlsx.cjs.prod.js";
import readXlsxFile from 'read-excel-file';
import axios from 'axios';

export default {
  components: {
    XlsxRead,
    XlsxJson
  },
  data() {
    return {
      file: null,
      collection: null,
      guests: [],
      users: [],
      idsguests: [],
      idsusers: [],
    };
  },
  mounted() {
    axios.get('http://127.0.0.1:8000/guests/',)
      .then(response => {
        this.guests = response.data;
        this.len = this.guests.length;

        this.guests.forEach(element => {
          this.idsguests.push(element.id);
        });
        axios.get('http://127.0.0.1:8000/users/',)
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
    importGuests(event) {
      this.file = event.target.files ? event.target.files[0] : null;
      readXlsxFile(this.file).then((rows) => {

        const gosti = [];

        for (let index = 1; index < rows.length; index++) {
          const element = rows[index];

          const obj = {};
          obj["name"] = "";
          obj["id"] = "";
          obj["surname"] = "";
          obj["jmbag"] = "";
          obj["email"] = "";
          obj["tag"] = "";
          obj["bought"] = "";
          obj["entered"] = "";

          for (let indexy = 0; indexy < rows[0].length; indexy++) {
            obj[rows[0][indexy]] = element[indexy];
            if (obj[rows[0][indexy]] == null) {
              obj[rows[0][indexy]] = "";
            }
          }

          var nextId;

          for (let index = 0; index < this.idsguests.length; index++) {
            if (this.idsguests.includes(String(index)) == false) {
              nextId = index;
              break;
            }
          }
          if (nextId == '') {
            nextId = idsguests.length;
          }

          obj["id"] = nextId;
          if (obj["tag"] == "") {
            obj["tag"] = "Brucoši";
          }
          if (obj["bought"] == "") {
            obj["bought"] = "0";
          }
          if (obj["entered"] == "") {
            obj["entered"] = "0";
          }

          this.idsguests.push(String(nextId));
          axios.post('http://127.0.0.1:8000/guests/',
            { id: obj.id, name: obj.name, surname: obj.surname, jmbag: obj.jmbag, tag: obj.tag, bought: obj.bought, entered: obj.entered },
            { auth: { username: process.env.VUE_APP_AUTH_USER, password: process.env.VUE_APP_AUTH_PASS } }
          )

          gosti.push(obj);
        }




      })


    },
    importUsers(event) {
      this.file = event.target.files ? event.target.files[0] : null;
      readXlsxFile(this.file).then((rows) => {


        const users = [];

        for (let index = 1; index < rows.length; index++) {
          const element = rows[index];


          const obj = {};
          obj["id"] = "";
          obj["name"] = "";
          obj["email"] = "";
          obj["privilege"] = "";

          for (let indexy = 0; indexy < rows[0].length; indexy++) {
            obj[rows[0][indexy]] = element[indexy];
            if (obj[rows[0][indexy]] == null) {
              obj[rows[0][indexy]] = "";
            }
          }

          var nextId;

          for (let index = 0; index < this.idsusers.length; index++) {
            if (this.idsusers.includes(String(index)) == false) {
              nextId = index;
              break;
            }
          }
          if (nextId == '') {
            nextId = this.idsusers.length;
          }



          obj["id"] = nextId;


          this.idsusers.push(String(nextId));
          axios.post('http://127.0.0.1:8000/users/',
            { id: obj.id, name: obj.name, email: obj.email, privilege: obj.privilege },
            { auth: { username: process.env.VUE_APP_AUTH_USER, password: process.env.VUE_APP_AUTH_PASS } }
          )

          users.push(obj);
        }




      })


    }
  }
}
</script>

<style scoped>
</style>