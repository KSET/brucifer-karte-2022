<template>

  <div id="guests-table">
    <div id="guests-search">
      <h1>Search: </h1>
      <input @input="searchGuest" type="form" id="searchgumb" v-model="search">
    </div>

    <table class="table" id="guests">
      <thead>
        <th>Name</th>
        <th>Surname</th>
        <th>JMBAG</th>
        <th>Karta</th>
      </thead>
      <tbody>
        <tr v-for="guest in guests" :key="guest.id">
          <td>
            <div contenteditable id="contentedit" @keypress.enter="loggg">{{ guest.name }}</div>
          </td>
          <td>{{ guest.surname }}</td>
          <td>{{ guest.jmbag }}</td>
          <td>
            <button @click="changeBought(guest, '1')" v-if="guest.bought == '0'" class="btn btn-xs btn-danger"
              id="gumbarn">
              <font-awesome-icon icon="fa-solid fa-xmark" />
            </button>
            <button v-else class="btn btn-xs btn-success" id="gumbary" @click="changeBought(guest, '0')">
              <font-awesome-icon icon="fa-solid fa-check" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>



  </div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'GuestsTable',
  props: {
    msg: String
  },
  data() {
    return {
      guests: [],
      id: '',
      name: '',
      surname: '',
      jmbag: '',
      phone: '',
      tag: '',
      bought: '',
      entered: '',
      deleted: '',

      guestsAdded: '',
      guetsEntered: '',
    }
  },
  mounted() {
    this.created();
  },
  methods: {
    loggg() {
    },
    created() {
      axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=Brucoši&search_fields=tag',)
        .then(response => {
          this.guests = response.data;

        })
    },
    changeBought(guest, changenum) {
      axios.put(process.env.VUE_APP_BASE_URL + '/guests/' + guest.id + '/',
        { bought: changenum },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created();
        })

    },
    searchGuest() {
      axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=Brucoši ' + this.search + "&search_fields=tag&search_fields=name&search_fields=surname",)
        .then(response => {
          this.guests = response.data;
        })
    }
  }

}
</script>
<style>
#guests {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
  text-align: center;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;

}

#guests td,
#guests th {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

#guests tr:nth-child(even) {
  background-color: #f2f2f2;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

#guests tr:hover {
  background-color: #ddd;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

#guests th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: rgba(0, 119, 255, 0.979);
  color: white;
  text-align: center;
}

#gumbary {

  padding: 0px;
  margin: 2px;
  width: 40px;
  height: 40px;
  background-color: green;
  border-color: green;
}

#gumbarn {
  padding: 0px;
  margin: 2px;
  width: 40px;
  height: 40px;
  background-color: red;
  border-color: red;
}
</style>


