<template>
  <div id="lineup-add">
    <br>
    <h1 v-if="(this.slug == '0')" id="page-title">Dodavanje izvođača</h1>
    <h1 v-else id="page-title">Uređivanje izvođača</h1>

    <form @submit="postGuest">

      <h1 id="textfield1">Ime </h1>
      <input id="inputfield1" type="text" v-model="name" placeholder="Name">


      <h1 id="textfield3">Slika </h1>
      <input id="inputfield3" type="file" accept="image/*" ref="file" @change="selectImage">


      <img id="image-preview" class="preview my-3" :src="previewImage" alt="" />
      <button v-if="(this.slug == '0')" id="submit-button" class="btn btn-primary">Dodaj</button>
      <button v-else id="submit-button" class="btn btn-primary">Spremi promjene</button>
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
      lineup: [],
      slug: 0,
      lineupp: '',
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

    }
  },

  mounted() {
    console.log(this.$route.params.slug)
    this.slug = this.$route.params.slug;
    if (this.slug != '0') {
      axios.get('http://127.0.0.1:8000/lineup/?search=' + this.slug,)
        .then(response => {
          this.lineup = response.data;
          this.lineupp = this.lineup[0];
          this.name = this.lineupp.name;
          this.url = this.lineupp.url;
          this.previewImage = this.lineupp.image;

        })

    }

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

      this.lineup.forEach(element => {
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
      return axios.post("http://127.0.0.1:8000/lineup/", fd, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      
    });*/

      axios.post('http://127.0.0.1:8000/lineup/',
        { id: this.nextId, name: this.name, url: this.url, image: this.currentImage },
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

</style>


