<template>
  <div id="users-search">
    <h>Search:  </h>
      <input @input="searchUser" type="form" id="searchgumb" v-model="search">
      <div class=row>
            <table id="users">
              <thead>
              <th>Name</th>
              <th>Email</th>
              <th>privilege</th>
              <th>Options</th>
              </thead>
              <tbody>
                <tr  v-for="user in users" :key="user.id">
                  <td v-if="user.email!=''">{{user.name}}</td>
                  <td v-if="user.email!=''">{{user.email}}</td>
                  <td v-if="user.email!=''">{{user.privilege}}</td>
                  <td v-if="user.email!=''">
                    <button @click="changeprivilege(user,'1')" class="btn btn-primary" id="gumbar"> 1</button>
                    <button @click="changeprivilege(user,'2')" class="btn btn-primary" id="gumbar"> 2</button>
                    <button @click="changeprivilege(user,'3')" class="btn btn-primary" id="gumbar"> 3</button>
                    <button @click="changeprivilege(user,'4')" class="btn btn-primary" id="gumbar"> 4</button>
                    <button @click="deleteUser(user)" class="btn btn-primary" id="gumbard">  <font-awesome-icon icon="fa-solid fa-trash-can" /></button>
                  </td>
                </tr>
              </tbody>
            </table>
        
      
  </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UsersTable',
  props: {
    msg: String
  },
  data(){
    return{
      users: [],
      id:'',
      name:'',
      email:'',
      privilege:'',
    }
    
  },
  mounted(){
    this.created();
  },
  
  methods:{
    created() {
    axios.get('http://127.0.0.1:8000/users/',)
    .then(response => {
      this.users =response.data;
      console.log(this.users);

    })},
    changeprivilege(user,changenum){
      axios.put('http://127.0.0.1:8000/users/'+user.id+'/',
      {privilege:changenum},
      {auth:{username:process.env.VUE_APP_AUTH_USER,password:VUE_APP_AUTH_PASS}}
      )
      .then(()=>{
        this.created();
      })
    },
    deleteUser(user){
      axios.delete('http://127.0.0.1:8000/users/'+user.id+'/',
      {auth:{username:process.env.VUE_APP_AUTH_USER,password:VUE_APP_AUTH_PASS}}
      )
      .then(()=>{
        this.created();
      })
    },
    searchUser(){
      axios.get('http://127.0.0.1:8000/users/?search='+this.search,)
    .then(response => {
      this.users =response.data;
    })
    }
  }
   
}


</script>

<style>
#users {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
  text-align: center;
}

#users td, #users th {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

#users tr:nth-child(even){background-color: #f2f2f2;}

#users tr:hover {background-color: #ddd;}

#users th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #9e9e9e;
  color: white;
  text-align: center;
}
#gumbard{
  padding: 0px;
  background-color: #FFAE42;
  border-color: #FFAE42;
  margin: 2px;
  width: 40px;
  height: 40px;
}

#gumbar{
  padding: 0px;
  background-color: #111;
  border-color: #111;
  margin: 2px;
  width: 40px;
  height: 40px;
}
</style>


