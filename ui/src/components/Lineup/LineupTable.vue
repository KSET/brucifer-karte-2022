<template>
  <div class="grid">
    <article v-for="sponsor in sponsors" :key="sponsor.id">
    <img v-bind:src="sponsor.image">
    <div>
      <h3> {{sponsor.name}}</h3>
      <button @click="deleteTag(sponsor)" class="button10" >  <font-awesome-icon icon="fa-solid fa-trash-can" /></button>
      <button @click="deleteTag(sponsor)" class="button11" >  <font-awesome-icon icon="fa-solid fa-trash-can" /></button>
      <button @click="deleteTag(sponsor)" class="button12" >  <font-awesome-icon icon="fa-solid fa-trash-can" /></button>
    </div>
    </article>

  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'LineupTable',
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
    axios.get('http://127.0.0.1:8000/lineup/',)
    .then(response => {
      this.sponsors =response.data;  
      });
  },
    deleteTag(tag){
      axios.delete('http://127.0.0.1:8000/lineup/'+tag.id+'/',
      {auth:{username:process.env.VUE_APP_AUTH_USER,password:process.env.VUE_APP_AUTH_PASS}}
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
.grid { 
  position: absolute;
  left: 2.83%;
  top: 26.3%;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-gap: 20px;
  align-items: stretch;
  }
.grid > article {
  border: 1px solid #ccc;
}
.grid > article img {
  max-width: 100%;
}

.button10{
left: 4.1%;
top: 60.29%;

}

.button11{

  bottom:0%;
  left: 0%;
}

.button12{

  bottom:90%;
  left: 90%;
}
</style>