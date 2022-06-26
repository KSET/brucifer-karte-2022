<template>
  <div id="tags-table">
      <div class=row>
        
            <table class="table" id="guests">
              <thead>
              <th>IMG</th>
              <th>Id</th>
              <th>Name</th>
              <th>Url</th>
              <th>Options</th>
              </thead>
              <tbody>
                <tr v-for="sponsor in sponsors" :key="sponsor.id">
                  <td><img v-bind:src="sponsor.image"></td>
                  <td>{{sponsor.id}}</td>
                  <td>{{sponsor.name}}</td>
                  <td><a v-bind:href="sponsor.url">{{sponsor.url}}</a></td>
                  <td><button @click="deleteTag(sponsor)" class="btn btn-primary" id="gumbard">  <font-awesome-icon icon="fa-solid fa-trash-can" /></button>
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
  name: 'SponsorsTable',
  props: {
    msg: String
  },
  data(){
    return{
      sponsors: [],
    }
    
  },
  mounted(){
    this.created();
  },
  methods:{
    created() {
    axios.get('http://127.0.0.1:8000/sponsors/',)
    .then(response => {
      this.sponsors =response.data;  
      });
  },
    deleteTag(tag){
      axios.delete('http://127.0.0.1:8000/sponsors/'+tag.id+'/',
      {auth:{username:'paxx',password:'KSETpenisica43'}}
      )
      .then(()=>{
        this.created();
      })
    },
    getAp(elementName){
    
    
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


