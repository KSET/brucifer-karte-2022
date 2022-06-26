<template>
  <div id="tags-table">
     <div class=row>
            <table id="guests">
              <thead>
              <th>Name</th>
              <th>Count</th>
              <th>Bought</th>
              <th>Entered</th>
              <th>Options</th>
              </thead>
              <tbody>
                <tr v-for="tag in tags" :key="tag.id">
                  <td>{{tag.name}}</td>
                  <td>{{tag.count}}</td>
                  <td>{{tag.bought}}</td>
                  <td>{{tag.entered}}</td>
                  <td><button @click="deleteTag(tag)" class="btn btn-primary" id="gumbard"> <font-awesome-icon icon="fa-solid fa-trash-can" /></button>
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
  name: 'TagsTable',
  props: {
    msg: String
  },
  data(){
    return{
      tags: [],
      id:'',
      name:'',
      surname:'',
      jmbag:'',
      phone:'',
      tag:'',
      bought:'',
      entered:'',
      deleted:'',
      numc:'',
      numb:'',
      nume:'',
    }
    
  },
  mounted(){
    this.created();
  },
  methods:{
    created() {
    axios.get('http://127.0.0.1:8000/tags/',)
    .then(response => {
      this.tags =response.data;
      this.tags.forEach(element => {
        axios.get('http://127.0.0.1:8000/guests/?search='+element.name+'&search_fields=tag',)
    .then(response => {
      this.numc=0;
      this.numb=0;
      this.nume=0;
      response.data.forEach(element => {
        this.numc++;
        if(element.bought==1){
          this.numb++;
        }
        if(element.entered==1){
          this.nume++;
        }
       
        
      });
       if(String(this.numc)!=String(element.count) || this.numb!=element.bought || this.nume!=element.entered){
          
          axios.put('http://127.0.0.1:8000/tags/'+element.id+'/',
              {count:this.numc,bought:this.numb,entered:this.nume},
              {auth:{username:'paxx',password:'KSETpenisica43'}}
          
      )
            
          this.created();  

        }
    })

        
      });
    })

  },
    deleteTag(tag){
      axios.delete('http://127.0.0.1:8000/tags/'+tag.id+'/',
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


