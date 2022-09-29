<template>
    <div id="sponsors-add">
        <Sidebar />
        <div class="admin-page-container" style=" overflow: auto;">
            <div class="header">
                <h1 v-if="(this.slug == '0')" class="page-title">Dodavanje sponzora</h1>
                <h1 v-else class="page-title">Uređivanje sponzora</h1>
            </div>
            <img class="image-preview hidedesktop" style="display: block; margin-bottom: 5%; margin-left: 5%;"
                :src="previewImage" alt="" />

            <form class="sponsors-form" @submit="postSponsors">
                <div class="grid-container" style="row-gap:10%;">

                    <h1 class="textfield">Ime </h1>
                    <input required class="inputfield" type="text" v-model="name">

                    <h1 class="textfield">Link </h1>
                    <input required class="inputfield" type="text" v-model="url">


                    <h1 class="textfield">Slika </h1>
                    <label for="file-upload" class="button white" style="margin-top: 0px;">
                        Odaberi PNG
                    </label>

                    <h1 class="textfield">Prikaz na brucwebu </h1>

                    <label class="switch">
                        <input id="switchSponsors" type="checkbox">
                        <span class="slider round"></span>
                    </label>

                    <input id="file-upload" type="file" accept="image/*" ref="file" @change="selectImage" />

                    <h1 class="textfield">E-mail </h1>
                    <input required class="inputfield" type="text" v-model="email">

                    <h1 class="textfield">Broj uzvanika </h1>
                    <input required class="inputfield" type="text" v-model="guestCap">

                    <button v-if="(this.slug == '0')" class="button submit" style=" margin-top: 0px">Dodaj</button>
                    <button v-else class="button submit" style=" margin-top: 0px">Spremi promjene</button>

                    <button v-if="(this.slug != '0')" class="button submit del"
                        style="background-color: white; margin-top: 0px; " @click="deleteSponsors">
                        <img class="va" src="../../assets/icons/trash-icon.svg">
                    </button>
                </div>
            </form>
            <img class="image-preview hidetablet" :src="previewImage" alt="" />

        </div>
    </div>


</template>
  
<script>
import { uuid } from 'vue-uuid';

import axios from 'axios'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import store from '@/store/index.js';

export default {
    name: "upload-image",
    components: { Sidebar },
    computed: {
        refresh() {
            return store.state.refresh;
        },

    },
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
            visible: '',
            url: '',
            order: '',
            email: '',
            guestCap: '',
            formData: '',

            uuid: uuid.v1(),

        };
    },
    computed: {
        reroutePage() {
            return store.state.reroutePage;
        }
    },

    mounted() {
        this.slug = this.$route.params.slug;
        if (this.reroutePage == "1") {
            store.commit('setreroutePage', "0");
            this.$router.push({ path: '/admin/sponsors-list/' });
        }

        if (this.slug != '0') {
            axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?search=' + this.slug + "&search_fields=slug")
                .then(response => {
                    this.sponsors = response.data;
                    if (this.sponsors.length == 0) {
                        this.$router.push({ path: '/admin/sponsors-add/0' });
                    }

                    this.sponsorsInstance = this.sponsors[0];
                    this.name = this.sponsorsInstance.name;
                    this.previewImage = this.sponsorsInstance.image;
                    this.id = this.sponsorsInstance.id;
                    this.order = this.sponsorsInstance.order;
                    this.url = this.sponsorsInstance.url;
                    this.email = this.sponsorsInstance.email;
                    this.guestCap = this.sponsorsInstance.guestCap;

                    this.currentImage = this.sponsorsInstance.image;

                    this.visible = this.sponsorsInstance.visible;
                    if (this.visible == '1') {
                        document.getElementById("switchSponsors").checked = true;
                    } else {
                        document.getElementById("switchSponsors").checked = false;
                    }
                })

        } else {
            axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?ordering=order',)
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
        },
        deleteSponsors() {
            axios.delete(process.env.VUE_APP_BASE_URL + "/sponsors/" + this.id + "/",
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                },

            )
        },
        postSponsors() {
            if (this.currentImage == undefined) {
                window.alert("Uploadajte fotografiju")
            } else {
                store.commit('setreroutePage', "1");

                let formData = new FormData();
                formData.append("name", this.name);
                formData.append("url", this.url);
                formData.append("email", this.email);
                formData.append("guestCap", this.guestCap);

                if (document.getElementById("switchSponsors").checked == true) {
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

                    axios.put(process.env.VUE_APP_BASE_URL + "/sponsors/" + this.id + "/", formData,
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                        {
                            headers: {
                                "Content-Type": "multipart/form-data"

                            }
                        })
                } else {
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


                    } else {
                        this.nextId = 0;
                        this.nextOrder = "00";
                    }


                    formData.append("id", this.nextId);
                    formData.append("order", this.nextOrder);
                    formData.append("image", this.currentImage);
                    formData.append("slug", this.$uuid.v1());



                    axios.post(process.env.VUE_APP_BASE_URL + "/sponsors/", formData,
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                        {
                            headers: {
                                "Content-Type": "multipart/form-data"
                            }
                        },
                    )
                }


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

.button.submit.del {
    margin-left: 0px;
}

@media screen and (max-width: 550px) {
    .button.submit.del {
        margin-left: 50px;
    }

    .grid-container {
        row-gap: 5%;
    }

    .button.submit {
        width: 130px;
        height: 40px;
    }
}
</style>