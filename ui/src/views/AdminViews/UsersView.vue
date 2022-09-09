<template>
  <div class="users">
    <Sidebar />
    <div class="admin-page-container">
      <h1 class="page-title">Korisnici</h1>
        <h1 >Search: </h1>
        <input @input="searchUser" type="form" id="searchgumb" v-model="search">
        <div class=row>
          <table id="guests">
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td >{{user.name}} <br> {{user.email}}</td>
                <td >{{user.privilege}}</td>
                <td >
                  <button @click="changeprivilege(user,'1')" class="btn btn-primary" id="gumbar"> 1</button>
                  <button @click="changeprivilege(user,'2')" class="btn btn-primary" id="gumbar"> 2</button>
                  <button @click="changeprivilege(user,'3')" class="btn btn-primary" id="gumbar"> 3</button>
                  <button @click="changeprivilege(user,'4')" class="btn btn-primary" id="gumbar"> 4</button>
                  <button @click="deleteUser(user)" class="btn btn-primary" id="gumbard">
                    <font-awesome-icon icon="fa-solid fa-trash-can" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>


        </div>
      </div>
    </div>

</template>


<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import axios from 'axios'
export default {
  name: 'UsersView',
  components: {
    Sidebar
  },
  data() {
    return {
      users: [],
      id: '',
      name: '',
      email: '',
      privilege: '',
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

        })
    },
    changeprivilege(user, changenum) {
      axios.put('http://127.0.0.1:8000/users/' + user.id + '/',
        { privilege: changenum },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created();
        })
    },
    deleteUser(user) {
      axios.delete('http://127.0.0.1:8000/users/' + user.id + '/',
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created();
        })
    },
    searchUser() {
      axios.get('http://127.0.0.1:8000/users/?search=' + this.search,)
        .then(response => {
          this.users = response.data;
        })
    }
  }

}


</script>


<style >
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
</style>