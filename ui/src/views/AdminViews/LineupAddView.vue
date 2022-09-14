<template>


    <div id="sponsors-add">
        <Sidebar />
        <div class="admin-page-container">
            <div class="header">
                <h1 v-if="(this.slug == '0')" class="page-title">Dodavanje izvođača</h1>
                <h1 v-else class="page-title">Uređivanje izvođača</h1>
            </div>
            <form class="lineup-form" @submit="postLineup">
                <div class="grid-container">

                    <h1 class="textfield">Ime </h1>
                    <input class="inputfield" type="text" v-model="name" placeholder="Name">

                    <h1 class="textfield">Slika </h1>
                    <label for="file-upload" class="button white">
                        Odaberi CSV
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

            lineups: [],
            name:'',
            id:'',
            len:'',
            nextId:'',
            nextOrder:'',
        };
    },
    created() {
        axios.get('http://127.0.0.1:8000/lineup/',)
            .then(response => {
                this.lineups = response.data;
                this.len = this.lineups.length;
            })
    },
    methods: {
        selectImage() {
            this.currentImage = this.$refs.file.files.item(0);
            this.previewImage = URL.createObjectURL(this.currentImage);
            this.progress = 0;
            this.message = "";
        },

        postLineup() {
            var ids = [];

            this.lineups.forEach(element => {
                ids.push(element.id);
                ids.push(element.order);

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

            console.log(this.lineups[this.lineups.length-1].order[0])

            let formData = new FormData();

            formData.append("id", this.nextId);
            formData.append("name", this.name);

            formData.append("image", this.currentImage);

            axios.post("http://127.0.0.1:8000/lineup/", formData,
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                },
            )
                .then((response) => {
                    this.message = response.data.message;
                })
                .then((images) => {
                    this.imageInfos = images.data;
                })
                .catch((err) => {
                    this.progress = 0;
                    this.message = "Could not upload the image! " + err;
                    this.currentImage = undefined;
                });
        },
    },

};
</script>
  
<style scoped>
.lineup-form {
    display: inline-block;
    width: 70%;
}
</style>