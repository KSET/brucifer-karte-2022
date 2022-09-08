<template>
<div class="sponsors"> 
  <br>
    <div v-for="user in users" :key="user.id">
            <div class="artist" title="{{ user.name }}">
                <div class="image-container">
                    <div class="image-sizer"></div>
                    <img class="image-frame" v-bind:src="user.image">
                </div>
            </div>
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
    axios.get('http://127.0.0.1:8000/sponsors/',)
    .then(response => {
      this.users =response.data;


    })},
    changeprivilege(user,changenum){
      axios.put('http://127.0.0.1:8000/users/'+user.id+'/',
      {privilege:changenum},
      {auth:{username:process.env.VUE_APP_DJANGO_USER,password:process.env.VUE_APP_DJANGO_PASS}}
      )
      .then(()=>{
        this.created();
      })
    },
    deleteUser(user){
      axios.delete('http://127.0.0.1:8000/users/'+user.id+'/',
      {auth:{username:process.env.VUE_APP_DJANGO_USER,password:process.env.VUE_APP_DJANGO_PASS}}
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
.sponsors{  
  position: absolute;
  height: 100%;
  width: 100%;
    background-image: var(--background-default);
    background-size: cover;
    background-color:  var(--background-color);
}


    .contents {
        padding-top: 3.14159em;
    }

    .sponsors {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        grid-gap: 3.14159em;
    }

    .image-container {
        position: relative;
    }

    .image-container .image-sizer {
        padding-bottom: calc(0.86 * 100%);
        transition: padding-bottom .3s ease;
        will-change: padding-bottom;
    }

    .image-container .image-frame {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-repeat: no-repeat;
        background-position: center center;
        background-size: contain;
    }

    .sponsor {
        background: rgba(0, 0, 0, .3);
        border-radius: 18px;
        padding: 30px;
    }

    @media screen and (max-width: 1400px) {
        .sponsors {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }
    }

    @media screen and (max-width: 980px) {
        .sponsors {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }
    }

    @media screen and (max-width: 635px) {
        .sponsors {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media screen and (max-width: 350px) {
        .sponsors {
            grid-template-columns: repeat(1, minmax(0, 1fr));
        }
    }
    h6{
        color:white;
    }

</style>