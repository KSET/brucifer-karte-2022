<template>
  <div id="tags-add">
      <h1>Dodaj: </h1>
      <input type="text" id="inputtagname" v-model="name" placeholder="Tag Name">
      <button @click="postTag" class="btn btn-primary"
                      id="gumb2" >Dodaj</button>
  </div>
</template>


<script>
import axios from 'axios'
export default {
  name: 'TagsAdd',
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
      nextId:'',
    }
  },
  created() {
    console.log(process.env.VUE_APP_AUTH_USER);
    axios.get('http://127.0.0.1:8000/tags/',)
    .then(response => {
      this.tags =response.data;
    })
  },
  methods:{
    postTag(){
      var ids =[];
      
      this.tags.forEach(element => {
        ids.push(element.id);
      });
      for (let index = 0; index < ids.length; index++) {
        if(ids.includes(String(index))==false){
          this.nextId=index;
          break;
        }
      }
      if(this.nextId==''){
        this.nextId=ids.length;
      }


      console.log(process.env.VUE_APP_AUTH_USER);
      axios.post('http://127.0.0.1:8000/tags/',
      {id:this.nextId,name:this.name},
      {auth:{username:process.env.VUE_APP_AUTH_USER,password:process.env.VUE_APP_AUTH_PASS}}
      )
      .then(()=>{
        location.reload();
      })
    }
  }
}
</script>


<style>
#inputname{
    width: 220px;
    margin: 2px;
}
#inputsurname{
    width: 220px;
    margin: 2px;
}


#gumb2{
  margin: 2px;
  width: 220px;
  height: 30px;
  text-align: center;
}
</style>

