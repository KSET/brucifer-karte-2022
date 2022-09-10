<template>
    <div>
        <Sidebar />
        <div class="admin-page-container">
            <div class="lineup-add">
                
                <h1 v-if="(this.slug == '0')" class="page-title lineup-title">Dodavanje izvođača</h1>


                <h1 v-else class="page-title lineup-title">Uređivanje izvođača</h1>

                <form @submit="postGuest">
                    <div class="grid-container">
                    <h1 class="textfield">Ime </h1>
                    <input required class="inputfield" type="text" v-model="name">


                    <h1 class="textfield">Slika </h1>
                    <input class="inputfield" type="file" accept="image/*" ref="file" @change="selectImage">
                
                    
                    
                    <button v-if="(this.slug == '0')" class="button submit" >Dodaj</button>
                    <button v-else class="button submit">Spremi promjene</button>
                    
                    <button v-if="(this.slug == '0')" class="button deletey" >Delete</button>
                </div>
                </form>
                <img class="image-preview" :src="previewImage" alt="" />
            </div>
        </div>
    </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import axios from 'axios';

import LineupAdd from '@/components/Lineup/LineupAdd.vue';
export default {
    components: { LineupAdd, Sidebar }
    ,
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
        this.slug = this.$route.params.slug;
        if (this.slug != '0') {
            axios.get('http://127.0.0.1:8000/lineup/?search=' + this.slug,)
                .then(response => {
                    this.lineup = response.data;
                    this.lineupp = this.lineup[0];
                    this.name = this.lineupp.name;
                    this.previewImage = this.lineupp.image;

                })

        } else {
            axios.get('http://127.0.0.1:8000/lineup/',)
                .then(response => {
                    this.lineup = response.data;
                })
        }

    },
    methods: {
        selectImage(e) {
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

            var formData = new FormData();

            console.log(this.nextId);

            formData.append("id", this.nextId);
            formData.append("name", this.name);
            formData.append("slug", "asdasd");
            //formData.append("image", this.currentImage);

            console.log(formData.get("id"));

            axios.post('http://127.0.0.1:8000/lineup/',
                { formData },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS }, }, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            }
            )
                .then(() => {
                })
        }
    }
}
</script>


<style>
@import '../../assets/scss/Admin-scss/gird-view.scss';
</style>


