<template>
<div class="lineup"> 
    <div v-for="user in users" :key="user.id">
            <div class="artist" title="{{ user.name }}">
                <div class="image-container">
                    <div class="image-sizer"></div>
                    <img class="image-frame" v-bind:src="user.image">
                </div>
                <h3>{{ user.name }}</h3>
            </div>
    </div>
    <footer></footer>
    </div>
</template>

<script>
import axios from 'axios'
import Footer from '../../components/Footer.vue';
export default {
  name: 'UsersTable',
    Footer,
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
    axios.get('http://127.0.0.1:8000/lineup/',)
    .then(response => {
      this.users =response.data;


    })},
    changeprivilege(user,changenum){
      axios.put('http://127.0.0.1:8000/users/'+user.id+'/',
      {privilege:changenum},
      {auth:{username:'paxx',password:'KSETpenisica43'}}
      )
      .then(()=>{
        this.created();
      })
    },
    deleteUser(user){
      axios.delete('http://127.0.0.1:8000/users/'+user.id+'/',
      {auth:{username:'paxx',password:'KSETpenisica43'}}
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
@import url('https://fonts.googleapis.com/css2?family=Raleway&family=Righteous&display=swap');
h3,
h4 {
    font-family: 'Righteous', cursive;
}
        
        .contents {
            padding-top: 3.14159em;
        }

        .lineup {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            grid-row-gap: 3.45rem;
            grid-column-gap: 5.25rem;
            will-change: grid-row-gap, grid-column-gap;
            transition-duration: .2s;
            transition-timing-function: ease;
            transition-property: grid-row-gap, grid-column-gap;

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

        .artist {
            background: rgba(0, 0, 0, .3);
            border-radius: 18px;
            padding: 15px 30px;
        }

        .artist h3 {
            text-align: center;
            font-style: normal;
            font-weight: normal;
            font-size: 2.25rem;
            color: var(--bruc-white);
            text-transform: uppercase;
            margin-top: .3em;
            will-change: font-size;
            transition-duration: .2s;
            transition-timing-function: ease;
            transition-property: font-size;
        }

        @media screen and (max-width: 1400px) {
            .lineup {
                grid-template-columns: repeat(3, minmax(0, 1fr));
                grid-column-gap: 3rem;
            }

            .artist {
                padding: 15px 30px;
            }

            .artist h3 {
                font-size: 1.85rem;
            }
        }

        @media screen and (max-width: 980px) {
            .lineup {
                grid-template-columns: repeat(3, minmax(0, 1fr));
                grid-column-gap: 2.85rem;
            }

            .artist {
                padding: 10px 20px;
            }

            .artist h3 {
                font-size: 1.4rem;
            }
        }

        @media screen and (max-width: 635px) {
            .lineup {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                grid-column-gap: 2rem;
            }

            .artist h3 {
                font-size: 1.1rem;
            }
        }

        @media screen and (max-width: 350px) {
            .lineup {
                grid-template-columns: repeat(1, minmax(0, 1fr));
                grid-row-gap: 1.2rem;
            }


            .artist {
                padding: 8px 12px;
            }
        }
        
        .contents {
            padding-top: 3.14159em;
        }

        .lineup {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            grid-row-gap: 3.45rem;
            grid-column-gap: 5.25rem;
            will-change: grid-row-gap, grid-column-gap;
            transition-duration: .2s;
            transition-timing-function: ease;
            transition-property: grid-row-gap, grid-column-gap;
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

        .artist {
            background: rgba(0, 0, 0, .3);
            border-radius: 18px;
            padding: 15px 30px;
        }

        .artist h3 {
            text-align: center;
            font-style: normal;
            font-weight: normal;
            font-size: 2.25rem;
            color: var(--bruc-white);
            text-transform: uppercase;
            margin-top: .3em;
            will-change: font-size;
            transition-duration: .2s;
            transition-timing-function: ease;
            transition-property: font-size;
        }

        @media screen and (max-width: 1400px) {
            .lineup {
                grid-template-columns: repeat(3, minmax(0, 1fr));
                grid-column-gap: 3rem;
            }

            .artist {
                padding: 15px 30px;
            }

            .artist h3 {
                font-size: 1.85rem;
            }
        }

        @media screen and (max-width: 980px) {
            .lineup {
                grid-template-columns: repeat(3, minmax(0, 1fr));
                grid-column-gap: 2.85rem;
            }

            .artist {
                padding: 10px 20px;
            }

            .artist h3 {
                font-size: 1.4rem;
            }
        }

        @media screen and (max-width: 635px) {
            .lineup {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                grid-column-gap: 2rem;
            }

            .artist h3 {
                font-size: 1.1rem;
            }
        }

        @media screen and (max-width: 350px) {
            .lineup {
                grid-template-columns: repeat(1, minmax(0, 1fr));
                grid-row-gap: 1.2rem;
            }


            .artist {
                padding: 8px 12px;
            }
        }

      footer::before {
    position: absolute;
    top: -81px;
    right: 0;
    left: 0;
    height: 82px;
    content: "";
    background-image: url(../../assets/images/footer/bg.svg);
    background-repeat: repeat-x;
}


    </style>

       
