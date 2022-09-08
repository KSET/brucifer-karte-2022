<template>
  <div id="sponsors-add">
    <br>
    <h1 v-if="(this.slug == '0')" id="page-title1">Dodavanje sponzora</h1>
    <h1 v-else id="page-title1">Uređivanje sponzora</h1>

    <form @submit="postGuest">

      <h1 class="textfield1">Ime </h1>
      <input class="inputfield1" type="text" v-model="name" placeholder="Name">

      <h1 class="textfield2">Link </h1>
      <input class="inputfield2" type="text" v-model="url" placeholder="Url">


      <h1 class="textfield3">Slika </h1>
      <input class="inputfield3" type="file" accept="image/*" ref="file" @change="selectImage">

      <img class="image-preview"  :src="previewImage" alt="" />
      <button v-if="(this.slug == '0')" class="submit-button">Dodaj</button>
      <button v-else class="submit-button">Spremi promjene</button>
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
      slug: 0,
      sponsor: '',
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
      axios.get('http://127.0.0.1:8000/sponsors/?search=' + this.slug,)
        .then(response => {
          this.sponsors = response.data;
          this.sponsor = this.sponsors[0];
          this.name = this.sponsor.name;
          this.url = this.sponsor.url;
          this.previewImage = this.sponsor.image;

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

      axios.post('http://127.0.0.1:8000/sponsors/',
        { id: this.nextId, name: this.name, url: this.url, image: this.currentImage },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS }, },
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



