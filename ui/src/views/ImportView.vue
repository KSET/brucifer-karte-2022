<template>
  <div class="import">
    <br>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Import</div>
          <div class="card-body">
            <section>
              <input class = "btn btn-primary" type="file" @change="onChange" />
            </section>
            <section>
              <br>
              <h1>Prvi redak mora sadržavati imena polja koja moraju biti lowercase te u istom formatu kao u sljedećem redu</h1>
              <h1>Imena polja mogu biti: name surname jmbag email tag bought enetered</h1>
              <h1>Tablica ne mora sadržavati sva imena polja, redoslijed stupaca nije bitan</h1>
              <h1>Ukoliko se polje tag kod nekog gosta ostavi prazno, tag će automatski biti Brucoši</h1>
              <h1>Ukoliko se polja bought i enetered kod nekog gosta ostave prazna, bit će postavljena na 0</h1>
              <br>
              <button type="submit" onclick="window.open('../assets/import_example.xlsx')">Download!</button>

              <a class = "btn btn-primary" href="../assets/import_example.xlsx" download="import_example.xlsx">Download example</a>
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
      ids: [],
    };
  },
  mounted() {
    axios.get('http://127.0.0.1:8000/guests/',)
      .then(response => {
        this.guests = response.data;
        this.len = this.guests.length;
        
        this.guests.forEach(element => {
          this.ids.push(element.id);
        });
        console.log(this.ids);
      })
  },
  methods: {
    onChange(event) {
      this.file = event.target.files ? event.target.files[0] : null;
      readXlsxFile(this.file).then((rows) => {
        console.log("rows:", rows)

        const gosti = [];

        for (let index = 1; index < rows.length; index++) {
            const element = rows[index];

            console.log(element);
            const obj={};
            obj["name"]="";
            obj["id"]="";
            obj["surname"]="";
            obj["jmbag"]="";
            obj["email"]="";
            obj["tag"]="";
            obj["bought"]="";
            obj["entered"]="";

            for(let indexy = 0; indexy < rows[0].length; indexy++) {
              obj[rows[0][indexy]] = element[indexy];
              if(obj[rows[0][indexy]]==null){
                obj[rows[0][indexy]] = "";
              }
            }

            var nextId;

            for (let index = 0; index < this.ids.length; index++) {
              if (this.ids.includes(String(index)) == false) {
                nextId = index;
                break;
              }
            }
            if (nextId == '') {
              nextId = ids.length;
            }



            obj["id"]=nextId;
            if(obj["tag"]==""){
              obj["tag"]="Brucoši";
            }
            if(obj["bought"]==""){
              obj["bought"]="0";
            }
            if(obj["entered"]==""){
              obj["entered"]="0";
            }

            this.ids.push(String(nextId));
            axios.post('http://127.0.0.1:8000/guests/',
              { id: obj.id, name: obj.name, surname: obj.surname, jmbag: obj.jmbag, tag: obj.tag, bought: obj.bought, entered: obj.entered },
              { auth: { username: 'paxx', password: 'KSETpenisica43' } }
            )

            gosti.push(obj);
        }

        console.log(gosti);
        
        

      })


    },
  }
}
</script>

<style scoped>
</style>