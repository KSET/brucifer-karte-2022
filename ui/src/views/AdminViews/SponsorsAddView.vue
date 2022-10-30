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

            <form class="sponsors-form" onsubmit="return false">
                <div class="grid-container" style="row-gap:10%;">

                    <h1 class="textfield">Ime </h1>
                    <input required class="inputfield" type="text" v-model="name">

                    <h1 class="textfield">Link </h1>
                    <input required class="inputfield" type="text" v-model="url">


                    <h1 class="textfield">Slika </h1>
                    <label for="file-upload" class="button white" style="margin-top: 0px;">
                        Odaberi PNG
                    </label>

                    <h1 class="textfield">Vidljvo </h1>

                    <label class="switch">
                        <input id="switchSponsors" type="checkbox">
                        <span class="slider round"></span>
                    </label>

                    <input id="file-upload" type="file" accept="image/*" ref="file" @change="selectImage" />

                    <h1 class="textfield" style="width: 150%;">E-mail </h1>
                    <input required class="inputfield" type="text" v-model="email">

                    <h1 class="textfield" style="width: 150%;">Broj uzvanika </h1>
                    <input required class="inputfield" type="text" v-model="guestCap">

                    <button v-if="(this.slug == '0')" class="button submit" style=" margin-top: 0px "
                        @click="postSponsors">Dodaj</button>
                    <button v-else class="button submit" style=" margin-top: 0px" @click="postSponsors">Spremi
                        promjene</button>

                    <button v-if="(this.slug != '0')" class="button submit del"
                        style="background-color: white; margin-top: 0px; " @click="deleteSponsors">
                        <img class="va" src="../../assets/icons/trash-icon.svg">
                    </button>

                    <button v-if="(this.slug != '0')" class="button submit" style=" margin-top: 0px "
                        @click="sendMail">Pozovi</button>

                    <button v-if="(this.slug != '0')" class="button submit" style=" margin-top: 0px "
                        @click="reroutePopis">Popis</button>

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
    created() {
        this.slug = this.$route.params.slug;

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
        reroutePopis(){
            this.$router.push({ path: '/sponzori/'+this.slug });
        },
        async deleteSponsors() {
            const resp = await axios.delete(process.env.VUE_APP_BASE_URL + "/sponsors/" + this.id + "/",
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                },
            )
            this.$router.push({ path: '/admin/sponsors-list/' });
        },
        async sendMail() {
            if (window.confirm("Klikom na OK šaljete mail sponzoru!!!")) {
                const resp = await axios.get(process.env.VUE_APP_BASE_URL + "/mailer/")
                let mailsent = 0;

                resp.data.forEach(element => {
                    if (element.message.includes(this.email)) {
                        mailsent = 1;
                    }
                });

                if (mailsent == 1) {
                    if (window.confirm("Sponzoru je već poslan mail, klikom na 'OK' sponzoru će se ponovno poslati mail!!!")) {
                        mailsent = 0;
                    }
                }
                if (mailsent == 0) {
                    let msg = this.name + " " + this.email + " " + this.slug

                    let email = this.email

                    await axios.post(process.env.VUE_APP_BASE_URL + '/mailer/0/send_mail/',
                        {
                            subject: "[KSET] Link za uređivanje popisa za 40. Brucošijadu FER-a",
                            template: "sponsors_email",
                            message: msg,
                            name: this.name,
                            link: "https://brucosijada.kset.org/sponzori/" + this.slug,
                            to_mail: email
                        },
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                    )
                    await axios.post(process.env.VUE_APP_BASE_URL + '/mailer/',
                        {
                            subject: "[KSET] Link za uređivanje popisa za 40. Brucošijadu FER-a",
                            template: "sponsors_email",
                            message: msg,
                            name: this.name,
                            link: "https://brucosijada.kset.org/sponzori/" + this.slug,
                            to_mail: email
                        },
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                    )
                }
            }
        },
        async postSponsors() {
            if (this.currentImage == undefined) {
                window.alert("Uploadajte fotografiju")
            } else {

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

                    const resp = await axios.put(process.env.VUE_APP_BASE_URL + "/sponsors/" + this.id + "/", formData,
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                        {
                            headers: {
                                "Content-Type": "multipart/form-data"

                            }
                        })
                } else {
                    if (this.sponsorss.length != 1) {
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
                        if (this.nextId === '') {
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



                    const resp = await axios.post(process.env.VUE_APP_BASE_URL + "/sponsors/", formData,
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                        {
                            headers: {
                                "Content-Type": "multipart/form-data"
                            }
                        },
                    )
                }
                this.$router.push({ path: '/admin/sponsors-list/' });


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
        margin-left: 70px !important;
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