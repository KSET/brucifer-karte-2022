<template>
  <div id="privileges">
    <Sidebar />
    <div class="admin-page-container">
      <h1 class="page-title">Privilegije</h1>
      <h1 class="text1">UKUPNO {{this.countNista+this.countAdmin+this.countUlaz+this.countKarte+this.countUlplK}}</h1>
      <table class="table" id="guests">
        <thead>
          <th>Oznaka</th>
          <th>Ime</th>
          <th>Broj</th>
        </thead>
        <tbody>
          <tr>
            <td>0</td>
            <td>Ništa</td>
            <td>{{this.countNista}}</td>
          </tr>
          <tr>
            <td>1</td>
            <td>Admin</td>
            <td>{{this.countAdmin}}</td>
          </tr>
          <tr>
            <td>2</td>
            <td>Ulaz</td>
            <td>{{this.countUlaz}}</td>
          </tr>
          <tr>
            <td>3</td>
            <td>Karte</td>
            <td>{{this.countKarte}}</td>
          </tr>
          <tr>
            <td>4</td>
            <td>Ulaz+Karte</td>
            <td>{{this.countUlplK}}</td>
          </tr>
          

        </tbody>
      </table>



    </div>
  </div>

</template>

<script>
import axios from 'axios'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

export default {
  name: 'GuestsTable',
  props: {
    msg: String
  },
  components: {
    Sidebar
  },
  data() {
    return {
      countNista: 0,
      countAdmin: 0,
      countUlaz: 0,
      countKarte: 0,
      countUlplK: 0,
    }
  },
  mounted() {
    this.created();
  },
  methods: {
    created() {
      axios.get('http://127.0.0.1:8000/users/',)
        .then(response => {
          this.users = response.data;
          this.users.forEach(element => {
            if (element.privilege == 0) {
              this.countNista++
            } else if (element.privilege == 1) {
              this.countAdmin++
            } else if (element.privilege == 2) {
              this.countUlaz++
            } else if (element.privilege == 3) {
              this.countKarte++
            } else if (element.privilege == 4) {
              this.countUlplK++
            }
          });
        })
    }
  }

}
</script>
<style>
.page-title{
  vertical-align: middle;
  display: inline-block;
  padding-top: 3%;
  padding-bottom: 3%;
  padding-right: 5%;

  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-size: 32px;
  line-height: 36px;
  /* identical to box height, or 112% */

  letter-spacing: -0.015em;

  color: #000000;
}

.text1{
  padding-bottom: 3%;
  font-family: 'Montserrat';
font-style: normal;
font-weight: 700;
font-size: 16px;
line-height: 36px;
/* identical to box height, or 225% */

display: flex;
align-items: left;
letter-spacing: -0.015em;

color: #000000;
}

#guests {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
  text-align: left;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;

}

#guests td,
#guests th {
  border: 0px;
  border-bottom: 0.5px solid black;
  padding: 8px;
  text-align: left;
  vertical-align:middle;
  font-family: 'Montserrat';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  font-size: 16px;
}
#guests tr {overflow:auto;}



#guests tr:nth-child(even) {
  background-color: white;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
}

#guests tr:hover {
  background-color: white;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
}

#guests th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color:white;
  color: black;
}



</style>


