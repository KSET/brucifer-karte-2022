<template>
  <div id="sponsors-add">
    <br><br>
    <h1>Dodavanje izvođača</h1>
    <br>
    <form @submit="postGuest">
      <br>
      <h>Ime </h>
      <input type="text" id="inputname" v-model="name" placeholder="Name">

      <br><br>
     
      <h>Slika </h>
      <input type="file" accept="image/*" ref="file" id="file-input" @change="selectImage">
      <br>
      <br>
      <img class="preview my-3" :src="previewImage" alt="" />
      <button class="btn btn-primary" id="gumb2">Add</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'


export default {
  name: 'SponsorsAdd',
  components: {
  },
  props: {
    msg: String
  },
  data() {
    return {
      items: ['Brucoši', 'KSET', 'VIP'],
      sponsors: [],
      id: '',
      name: '',
      surname: '',
      jmbag: '',
      phone: '',
      tag: '',
      bought: '',
      entered: '',
      url: '',
      img: '',
      nextId: '',
      services: ['Brucoši', 'KSET', 'VIP'],
      selectedTag: '',
      currentImage: undefined,
      previewImage: undefined,
      progress: 0,
      message: "",
      imageInfos: [],
      slug:'',

    }
  },

  mounted() {
    console.log(this.$route.params.slug)
    this.slug=this.$route.params.slug;
    axios.get('http://127.0.0.1:8000/sponsors',)
      .then(response => {
        this.sponsors = response.data;
      })
  },
  methods: {
    selectImage(e) {
      //this.currentImage = this.$refs.file.files.item(0);
      this.currentImage = this.$refs.file.files.item(0);
      this.previewImage = URL.createObjectURL(this.currentImage);
      this.progress = 0;
      this.message = "";
      //console.log(this.currentImage)
    },
    postGuest() {


      var ids = [];

      this.sponsors.forEach(element => {
        ids.push(element.id);
      });
      for (let index = 0; index < ids.length; index++) {
        if (ids.includes(String(index)) == false) {
          this.nextId = index;
          break;
        }
      }
      if (this.nextId == '') {
        this.nextId = ids.length;
      }
      const formData = new FormData();
      console.log(this.name)
      console.log(this.url)
      console.log(formData)
      formData.append('name', this.name);
      formData.append('url', this.url);

      console.log(this.currentImage)

      console.log(this.nextId)

      let fd = new FormData();
      fd.appent("int", this.nextId);
      fd.append("file", this.currentImage);/* 
      return axios.post("http://127.0.0.1:8000/sponsors/", fd, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      
    });*/

      axios.post('http://127.0.0.1:8000/lineup/',
        { id: this.nextId, name: this.name, image: this.currentImage },
        { auth: { username: process.env.VUE_APP_AUTH_USER, password: process.env.VUE_APP_AUTH_PASS }, },
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
        .then(() => {
          location.reload();
        })
    }
  }
}
</script>


<style>
#inputname {
  width: 220px;
  margin: 2px;
}

#inputsurname {
  width: 220px;
  margin: 2px;
}


#gumb2 {
  padding: 0px;
  margin: 2px;
  width: 220px;
  height: 30px;
  text-align: center;
}
</style>


