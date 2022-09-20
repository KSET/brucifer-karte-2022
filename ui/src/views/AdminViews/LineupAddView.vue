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
                    <input required class="inputfield" type="text" v-model="name">

                    <h1 class="textfield">Slika </h1>
                    <label for="file-upload" class="button white" style="margin-top: 0px;">
                        Odaberi PNG
                    </label>
                    <input id="file-upload" type="file" accept="image/*" ref="file" @change="selectImage" />

                    <h1 class="textfield">Prikaz na brucwebu </h1>

                    <label class="switch">
                        <input id="switchLineup" type="checkbox">
                        <span class="slider round"></span>
                    </label>

                    <button v-if="(this.slug == '0')" class="button submit">Dodaj</button>
                    <button v-else class="button submit">Spremi promjene</button>

                    <button v-if="(this.slug != '0')" class="button submit" style="background-color: white;"
                        @click="deleteLineup">
                        <img class="va" src="../../assets/icons/trash-icon.svg">
                    </button>
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
            name: '',
            id: '',
            len: '',
            nextId: '',
            nextOrder: '',
            order: '',
            visible: '',
            formData: '',
        };
    },

    mounted() {
        this.slug = this.$route.params.slug;

        if (this.slug != '0') {
            axios.get('http://127.0.0.1:8000/lineup/?search=' + this.slug,)
                .then(response => {
                    this.lineup = response.data;
                    if (this.lineup.length == 0) {
                        this.$router.push({ path: '/bruckarte/lineup-add/0' });
                    }
                    this.lineupp = this.lineup[0];
                    this.name = this.lineupp.name;
                    this.previewImage = this.lineupp.image;
                    this.id = this.lineupp.id;
                    this.order = this.lineupp.order;
                    this.currentImage = this.lineupp.image;

                    this.visible = this.lineupp.visible;
                    if (this.visible == '1') {
                        document.getElementById("switchLineup").checked = true;
                    } else {
                        document.getElementById("switchLineup").checked = false;
                    }

                })

        } else {
            axios.get('http://127.0.0.1:8000/lineup/?ordering=order',)
                .then(response => {
                    this.lineups = response.data;

                })
        }

    },
    methods: {
        selectImage() {
            this.currentImage = this.$refs.file.files.item(0);
            this.previewImage = URL.createObjectURL(this.currentImage);
            this.progress = 0;
            this.message = "";
        },
        deleteLineup() {
            axios.delete("http://127.0.0.1:8000/lineup/" + this.id + "/",
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                {
                    headers: {
                        "Content-Type": "multipart/form-data"

                    }
                },

            )
        },
        postLineup() {

            let formData = new FormData();
            formData.append("name", this.name);
            if (document.getElementById("switchLineup").checked == true) {
                formData.append("visible", "1");
            } else {
                formData.append("visible", "0");
            }

            if (this.slug != "0") {

                formData.append("id", this.id);
                formData.append("order", this.order);
                formData.append("slug", this.slug);


                if (this.currentImage instanceof File) {
                    formData.append("image", this.currentImage);
                }

                axios.put("http://127.0.0.1:8000/lineup/" + this.id + "/", formData,
                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                    {
                        headers: {
                            "Content-Type": "multipart/form-data"

                        }
                    })
            } else {
                console.log(this.lineups.length);
                if (this.lineups.length != 1) {
                    var ids = [];

                    this.lineups.forEach(element => {
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

                    var lastOrder = this.lineups[this.lineups.length - 2].order;

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


                } else {
                    this.nextId = 0;
                    this.nextOrder = "00";
                }
                let r = (Math.random() + 1).toString(36).substring(7);


                formData.append("id", this.nextId);
                formData.append("order", this.nextOrder);
                formData.append("image", this.currentImage);
                formData.append("slug", r);



                axios.post("http://127.0.0.1:8000/lineup/", formData,
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
.lineup-form {
    display: inline-block;
    width: 70%;
}
</style>