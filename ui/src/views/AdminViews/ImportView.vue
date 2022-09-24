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
      <button class="button-upload white">Preuzmi  CSV template</button>
     
      <div class="list">
        <ul>
          <li>Prvi redak mora sadržavati imena polja koja moraju biti lowercase te u istom formatu kao u sljedećemredu
          </li>
          <li>Imena polja mogu biti: name surname jmbag email tag bought entered</li>
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

      <button class="button-upload white">Preuzmi  CSV template</button>
     
      <div class="list">
      <ul>
        <li>Prvi redak mora sadržavati imena polja koja moraju biti lowercase te u istom formatu kao u sljedećem redu.
        </li>
        <li>Imena polja mogu biti: name, email, privilege.</li>
        <li>Mogće vrijednosti privilege su cijeli brojevi izmešu 0 i 4 s uključivim granicama.</li>
      </ul></div>
    </div>
  </div>

</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

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
            nextId = this.idsguests.length;
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
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
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
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
          )

          users.push(obj);
        }




      })


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
.button-upload.white{
  line-height: 0%;
  width: 200px;
  color: black;
  background: white;
}


input[type="file"] {
  display: none;

}
.list{
  margin-top: 2.5%;
  margin-bottom: 2.5%;
}

ul {
 
}

li {
    font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
}
</style>