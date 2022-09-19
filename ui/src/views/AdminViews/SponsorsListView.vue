<template>

  <div id="sponsors-add">
      <Sidebar />
      <div class="admin-page-container">
          <div class="header">
              <h1 v-if="(this.slug == '0')" class="page-title">Dodavanje izvođača</h1>
              <h1 v-else class="page-title">Uređivanje izvođača</h1>
          </div>
          <form class="sponsors-form" @submit="checkLineup">
              <div class="grid-container">

                  <h1 class="textfield">Ime </h1>
                  <input required class="inputfield" type="text" v-model="name" placeholder="Name">

                  <h1 class="textfield">Slika </h1>
                  <label for="file-upload" class="button white">
                      Odaberi PNG
                  </label>
                  <input id="file-upload" type="file" accept="image/*" ref="file" @change="selectImage" />

                  <button v-if="(this.slug == '0')" class="button submit">Dodaj</button>
                  <button v-else class="button submit">Spremi promjene</button>
              </div>
          </form>
          <img class="image-preview" :src="previewImage" alt="" />

      </div>
  </div>


</template>

<script>
import axios from 'axios'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'


export default {
  name: "upload-image",
  components: { Sidebar },
  data() {
      return {
          currentImage: undefined,
          previewImage: undefined,
          slug: '0',
          progress: 0,
          message: "",

          sponsorss: [],
          name: '',
          id: '',
          len: '',
          nextId: '',
          nextOrder: '',
          order: '',
          formData: '',
      };
  },

  mounted() {
      this.slug = this.$route.params.slug;

      if (this.slug != '0') {
          axios.get('http://127.0.0.1:8000/sponsors/?search=' + this.slug,)
              .then(response => {
                  this.sponsors = response.data;


                  this.sponsorsp = this.sponsors[0];
                  this.name = this.sponsorsp.name;
                  this.previewImage = this.sponsorsp.image;
                  this.id = this.sponsorsp.id;
                  this.order = this.sponsorsp.order;
                  this.currentImage = this.sponsorsp.image;

              })

      } else {
          axios.get('http://127.0.0.1:8000/sponsors/?ordering=order',)
              .then(response => {
                  this.sponsorss = response.data;
              })
      }

  },
  methods: {
      selectImage() {
          this.currentImage = this.$refs.file.files.item(0);
          this.previewImage = URL.createObjectURL(this.currentImage);
          this.progress = 0;
          this.message = "";
      }
      , checkLineup() {

          let formData = new FormData();
          formData.append("name", this.name);
          if (this.slug != "0") {

              formData.append("id", this.id);
              formData.append("order", this.order);
              formData.append("slug", this.slug);

              if (this.currentImage instanceof File) {
                  formData.append("image", this.currentImage);

              }

              axios.put("http://127.0.0.1:8000/sponsors/" + this.id + "/", formData,
                  { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                  {
                      headers: {
                          "Content-Type": "multipart/form-data"

                      }
                  },

              )
          } else {
              console.log(this.sponsorss.length);
              if (this.sponsorss.length != 0) {
                  var ids = [];

                  this.sponsorss.forEach(element => {
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

                  var lastOrder = this.sponsorss[this.sponsorss.length - 2].order;

                  if (lastOrder[0] == "0") {
                      if (lastOrder == "09") {
                          this.nextOrder = "10"
                      }
                      else {
                          this.nextOrder = "0" + (parseInt(lastOrder[1]) + 1).toString();
                      }
                  } else {
                      this.nextOrder = (parseInt(lastOrder) + 1).toString();

                  }


              }else{
                  this.nextId=0;
                  this.nextOrder="00";
              }
              let r = (Math.random() + 1).toString(36).substring(7);


              formData.append("id", this.nextId);
              formData.append("order", this.nextOrder);
              formData.append("image", this.currentImage);
              formData.append("slug", r);

              formData.append("visible", "0");


              axios.post("http://127.0.0.1:8000/sponsors/", formData,
                  { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                  {
                      headers: {
                          "Content-Type": "multipart/form-data"
                      }
                  },
              )
          }



      },
  },

};
</script>

<style scoped>
.sponsors-form {
  display: inline-block;
  width: 70%;
}
</style>