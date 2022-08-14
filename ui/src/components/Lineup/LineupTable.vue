<template>
  <div class="grid">
    <article v-for="sponsor in sponsors" :key="sponsor.id">
    <img v-bind:src="sponsor.image">
    <div class="text">
      <h3>{{sponsor.id}} ; {{sponsor.name}}</h3>
      <button @click="deleteTag(sponsor)" class="btn btn-primary" id="gumbard">  <font-awesome-icon icon="fa-solid fa-trash-can" /></button>
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
      {auth:{username:process.env.VUE_APP_AUTH_USER,password:VUE_APP_AUTH_PASS}}
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
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-gap: 20px;
  align-items: stretch;
  }
.grid > article {
  border: 1px solid #ccc;
  box-shadow: 2px 2px 6px 0px  rgba(0,0,0,0.3);
}
.grid > article img {
  max-width: 100%;
}
.text {
  padding: 0 20px 20px;
}
.text > button {
  background: gray;
  border: 0;
  color: white;
  padding: 10px;
  width: 100%;
  }
</style>