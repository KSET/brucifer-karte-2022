<template>

  <div id="guests-table">
    <br>
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Ulaz</div>
          <div class="card-body">
            <div id="guests-search">
              <h>Search: </h>
              <input @input="searchGuest" type="form" id="searchgumb" v-model="search" placeholder="Name">
              <button @click="searchGuest" class="btn btn-primary" id="gumb2">search</button>
            </div>

            <table class="table" id="guests">
              <thead>
                <th>Name</th>
                <th>Surname</th>
                <th>Tag</th>
                <th>Bought</th>
                <th>Ulaz</th>
              </thead>
              <tbody>
                <tr v-for="guest in guests" :key="guest.id">
                  <td><a href="" class="update" data-name="name" data-type="text" data-pk="{{ guest.id }}"
                      data-title="Enter name">{{ guest.name }}</a></td>
                  <td>{{ guest.surname }}</td>
                  <td>{{ guest.tag }}</td>
                  <td>{{ guest.bought }}</td>
                  <td>
                    <button @click="changebought(guest, '1')" v-if="guest.entered == '0'" class="btn btn-primary"
                      id="gumbarn">
                      <font-awesome-icon icon="fa-solid fa-xmark" />
                    </button>
                    <button v-else class="btn btn-primary" id="gumbary" @click="changebought(guest, '0')">
                      <font-awesome-icon icon="fa-solid fa-check" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>



          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {

  name: 'GuestTag',

  props: {
    msg: String
  },
  data() {
    return {
      guests: [],
      slug: '',
      path: '',
      id: '',
      name: '',
      surname: '',
      jmbag: '',
      phone: '',
      tag: '',
      bought: '',
      entered: '',
      deleted: '',
    }
  },



  mounted() {
    this.slug = this.$route.params.slug


    var changeSlugs = ["guests", "tags", "home", "", "privileges", "users", "import", "export", "logout"]
    if (changeSlugs.includes(String(this.slug))) {
      this.$router.push({ name: String(this.slug) })
    }
    this.created();
  },
  methods: {
    created() {
      axios.get('http://127.0.0.1:8000/guests/?search=' + this.slug + '&search_fields=tag',)

        .then(response => {
          this.guests = response.data;
        })
    },
    changebought(guest, changenum) {
      axios.put('http://127.0.0.1:8000/guests/' + guest.id + '/',
        { entered: changenum },
        { auth: { username: process.env.VUE_APP_AUTH_USER, password: process.env.VUE_APP_AUTH_PASS } }
      )
        .then(() => {
          this.created();
        })

    },
    searchGuest() {
      axios.get('http://127.0.0.1:8000/guests/?search=' + this.slug + ' ' + this.search + "&search_fields=tag&search_fields=name&search_fields=surname",)
        .then(response => {
          this.guests = response.data;
        })
    }
  }
}
</script>

<style scoped>
</style>