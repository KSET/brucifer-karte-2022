<template>
  <div id="guests-add">
    <form @submit="postGuest">
      <a>Dodaj na popis: </a>
      <input type="text" id="inputname" v-model="name" placeholder="Name">
      <input type="file" accept="image/*" ref="file" id="file-input" @change="selectImage">
      <button class="btn btn-primary" id="gumb2">Add</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

import Dropdown from '../DropdownRoute.vue';
export default {
  name: 'SponsorsAdd',
  components: {
    Dropdown
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
      img:'',
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

  created() {
    axios.get('http://127.0.0.1:8000/sponsors/',)
      .then(response => {
        this.sponsors = response.data;
      })
  },
  methods: {
    selectImage(e) {
      //this.currentImage = this.$refs.file.files.item(0);
      this.currentImage=e.target.files[0]
      console.log(this.currentImage)
      this.previewImage = URL.createObjectURL(this.currentImage);
      this.progress = 0;
      this.message = "";
      console.log(this.currentImage)
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
      axios.post('http://127.0.0.1:8000/sponsors/',
        { id: this.nextId, name: this.name, url: this.url},
        { auth: { username: 'paxx', password: 'KSETpenisica43' } }
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
  margin: 2px;
  width: 220px;
  height: 30px;
  text-align: center;
}
</style>


