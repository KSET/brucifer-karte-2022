<template>
    <div id="lineup-add">
        <Sidebar />
        <div class="admin-page-container" style="overflow: auto; display: flex; flex-direction: column">
            <div class="header">
                <h1 v-if="(this.slug == '0')" class="page-title">Dodavanje izvođača</h1>
                <h1 v-else class="page-title">Uređivanje izvođača</h1>
            </div>
            <img class="image-preview hideTablet showMobile" style="display: block; margin-bottom: 5%; margin-left: 5%;"
                :src="previewImage" alt="" />

            <img class="image-preview hideMobile" :src="previewImage" alt="" />

            <form onsubmit="return false" class="lineup-form">
                <div class="grid-container">

                    <h1 class="textfield">Ime </h1>
                    <input required class="inputfield" type="text" v-model="name">

                    <h1 class="textfield">Slika </h1>
                    <label for="file-upload" class="button white" style="margin-top: 0px;">
                        Odaberi PNG
                    </label>
                    <input required id="file-upload" type="file" accept="image/*" ref="file" @change="selectImage" />

                    <h1 class="textfield">Vidljvo </h1>

                    <label class="switch">
                        <input id="switchLineup" type="checkbox">
                        <span class="slider round"></span>
                    </label>
                </div>
                <button v-if="(this.slug == '0')" class="button submit" @click="postLineup">Dodaj</button>
                <button v-else class="button submit" @click="postLineup">Spremi promjene</button>

                <button v-if="(this.slug != '0')" class="button submit del" style="background-color: white; margin-left: 10px"
                    @click="deleteLineup">
                    <img class="va" src="../../assets/icons/trash-icon.svg">
                </button>
            </form>

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
            nextOrder: '',
            order: '',
            visible: '',
            formData: '',
        };
    },
    created() {
        this.slug = this.$route.params.slug;

        if (this.slug != '0') {
            axios.get(process.env.VUE_APP_BASE_URL + '/lineup/?search=' + this.slug + "&search_fields=slug")
                .then(response => {
                    this.lineup = response.data;
                    if (this.lineup.length == 0) {
                        this.$router.push({ path: '/admin/lineup-add/0' });
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
            axios.get(process.env.VUE_APP_BASE_URL + '/lineup/?ordering=order',)
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
        async deleteLineup() {
            const resp = await axios.delete(process.env.VUE_APP_BASE_URL + "/lineup/" + this.id + "/",
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                },
            )
            this.$router.push({ path: '/admin/lineup-list/' });
        },
        async postLineup() {
            if (this.currentImage == undefined) {
                window.alert("Uploadajte fotografiju")
            } else {
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

                    const resp = await axios.put(process.env.VUE_APP_BASE_URL + "/lineup/" + this.id + "/", formData,
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                        {
                            headers: {
                                "Content-Type": "multipart/form-data"

                            }
                        })
                } else {
                    if (this.lineups.length > 0) {
                        var lastOrder = this.lineups[this.lineups.length - 1].order;

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
                        this.nextOrder = "00";
                    }
                    let r = (Math.random() + 1).toString(36).substring(7);

                    formData.append("order", this.nextOrder);
                    formData.append("image", this.currentImage);
                    formData.append("slug", r);



                    const resp = await axios.post(process.env.VUE_APP_BASE_URL + "/lineup/", formData,
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                        {
                            headers: {
                                "Content-Type": "multipart/form-data"
                            }
                        },
                    )


                }

                this.$router.push({ path: '/admin/lineup-list/' });


            }
        }
    },

};
</script>
  
<style scoped>
.lineup-form {
    display: inline-block;
    width: 60%;
}

.button.submit.del {
    margin-left: 0px;
}

.image-preview{
    margin: 20px 0px;
}

@media screen and (max-width: 900px) {
    .lineup-form {
        margin-left: 5%;
    }

    .button.submit {
        font-size: 14px;
    }

    .button.submit.del {
        margin-left: 50px;
    }
}

@media screen and (max-width: 550px) {
    .button.submit.del {
        margin-left: 50px;
    }

    .lineup-form {
        width: 100%;
    }

    .button.submit {
        width: 130px;
        height: 40px;
    }
}
</style>