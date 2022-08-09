<template>
<div id="privileges">
  <br>
<div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">Prileges</div>
          <div class="card-body">
  
    
            <table class="table" id="guests">
              <thead>
              <th>Privilege name</th>
              <th>Count</th>
              </thead>
              <tbody>
                <tr>
                    <td>Ništa</td>
                    <td>{{this.countNista}}</td>
                </tr>
                <tr>
                    <td>Admin</td>
                    <td>{{this.countAdmin}}</td>
                </tr>
                <tr>
                    <td>Ulaz</td>
                    <td>{{this.countUlaz}}</td>
                </tr>
                <tr>
                    <td>Karte</td>
                    <td>{{this.countKarte}}</td>
                </tr>
                <tr>
                    <td>Ulaz+Karte</td>
                    <td>{{this.countUlplK}}</td>
                </tr>
                <tr>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                    <td><strong>Sum</strong></td>
                    <td><strong>{{this.countNista+this.countAdmin+this.countUlaz+this.countKarte+this.countUlplK}}</strong></td>
                </tr>
                
              </tbody>
            </table>
        
  
      
  </div></div></div></div></div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'GuestsTable',
  props: {
    msg: String
  },
  data(){
    return{
      countNista: 0,
      countAdmin: 0,
      countUlaz: 0,
      countKarte: 0,
      countUlplK: 0,
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
      this.users.forEach(element => {
        if(element.privilege==0){
            this.countNista++
        }else if(element.privilege==1){
            this.countAdmin++
        }else if(element.privilege==2){
            this.countUlaz++
        }else if(element.privilege==3){
            this.countKarte++
        }else if(element.privilege==4){
            this.countUlplK++
        }
      });
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

#guests td, #guests th {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

#guests tr:nth-child(even){background-color: #f2f2f2;
font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;}

#guests tr:hover {background-color: #ddd;font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;}

#guests th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: rgba(0, 119, 255, 0.979);
  color: white;
  text-align: center;
}
#gumbary{
  margin: 2px;
  width: 40px;
  height: 40px;
  background-color: green;
  border-color: green;
}
#gumbarn{
  margin: 2px;
  width: 40px;
  height: 40px;
  background-color: red;
  border-color: red;
}


</style>


