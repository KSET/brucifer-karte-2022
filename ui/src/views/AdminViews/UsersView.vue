<template>
  <div class="users">
    <Sidebar />
    <div class="admin-page-container">
      <img class="search-icon" src="@/assets/icons/search-icon.svg">
      <div class="page-header user-page">
        <h1 class="page-title user-title">Korisnici</h1>
        <button class="button-icon"> <img class="add-icon user-icon" src="@/assets/icons/add-icon.svg"></button>
        <input @input="searchUser" type="text" class="user-search" placeholder="Unesi ime ili prezime ili e-mail"
          v-model="search" style="display: inline-block; ">
      </div>
      <div class=row>
        <table id="guests">
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td v-bind:style= "[(user.privilege=='0') ? {color:'red'}: { color:'black'}]">{{user.name}} <br> {{user.email}}</td>
              <td></td>
              <td><button class="button-priv" v-bind:style= "[(user.privilege=='1') ? {backgroundColor: 'black', color:'white'}: {backgroundColor: 'white', color:'black'}]"  @click="changeprivilege(user,'1')" >Admin</button></td>
              <td><button class="button-priv" v-bind:style= "[(user.privilege=='2') ? {backgroundColor: 'black', color:'white'}: {backgroundColor: 'white', color:'black'}]" @click="changeprivilege(user,'2')" >Ulaz</button></td>
              <td> <button class="button-priv" v-bind:style= "[(user.privilege=='3') ? {backgroundColor: 'black', color:'white'}: {backgroundColor: 'white', color:'black'}]" @click="changeprivilege(user,'3')" >Karte</button></td>
              <td><button class="button-priv" v-bind:style= "[(user.privilege=='4') ? {backgroundColor: 'black', color:'white'}: {backgroundColor: 'white', color:'black'}]" @click="changeprivilege(user,'4')" >Ulaz <br>+Karte</button></td>
              <td><button class="button-priv" @click="deleteUser(user)" >
                <img src="@/assets/icons/trash-icon.svg">
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

.page-header.user-page{
  border-bottom: 0.5px solid black;
}

.page-title.user-title {
  padding-right: 1%;
  vertical-align: middle;
}

.user-search {
  padding-left: 40px;
  margin-left: 7%;
  width: 35%;
  height: 40px;
  vertical-align: middle;
  height: 40px;
  font-family: 'Montserrat';
  font-size: 16px;
  
}

.add-icon.user-icon {
  vertical-align: middle;
}

.search-icon {
  position: absolute;
  top: 8.4%;
  left: 24.7%;
}


.button-priv{
  position: relative;
  border: 0.5px solid black;
  background-color: white;
  height: 70px;
  width: 70px;

}
</style>