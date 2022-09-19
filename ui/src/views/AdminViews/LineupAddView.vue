<template>


    <div id="sponsors-add">
        <Sidebar />
        <div class="admin-page-container">
            <div class="header">
                <h1 v-if="(this.slug == '0')" class="page-title">Dodavanje izvođača</h1>
                <h1 v-else class="page-title">Uređivanje izvođača</h1>
            </div>
            <form class="lineup-form" @submit="checkLineup">
                <div class="grid-container">

                    <h1 class="textfield">Ime </h1>
                    <input class="inputfield" type="text" v-model="name" placeholder="Name">

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

            lineups: [],
            name: '',
            id: '',
            len: '',
            nextId: '',
            nextOrder: '',
            order: '',
            formData: '',
        };
    },
    computed: {
        updateData() {
            return store.state.updateData;
        },
        setfformData(){
            return store.state.fformData;
        }
    },
    mounted() {
        this.slug = this.$route.params.slug;
        console.log(this.updateData[0]);
        console.log(this.fformData);

        if (this.updateData != []) {

            let formData = new FormData();

            formData.append("image", this.updateData[0]);


            formData.append("name", this.updateData[1]);
            formData.append("id", "555");
            formData.append("order", this.updateData[3]);
            formData.append("slug", this.updateData[4]);

            axios.post("http://127.0.0.1:8000/lineup/", formData,
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                {
                    headers: {
                        "Content-Type": "multipart/form-data"

                    }
                },)
        }
        if (this.slug != '0') {
            axios.get('http://127.0.0.1:8000/lineup/?search=' + this.slug,)
                .then(response => {
                    this.lineup = response.data;
                    /*
                                        this.lineup.forEach(element => {
                                            if (element.id == 1500) {
                                                this.lineup.forEach(elementy => {
                                                    console.log(elementy.id);
                                                    console.log(element.order);
                    
                                                    if (elementy.id == element.order) {
                                                        axios.delete("http://127.0.0.1:8000/lineup/" + elementy.id + "/",
                                                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                                                        {
                                                            headers: {
                                                                "Content-Type": "multipart/form-data"
                                                            }
                                                        },
                                                    )
                                                    }
                                                });
                                                axios.put("http://127.0.0.1:8000/lineup/" + 1515 + "/", { id: element.order },
                                                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                                                    {
                                                        headers: {
                                                            "Content-Type": "multipart/form-data"
                                                        }
                                                    },
                                                ).then(() => {
                                                    console.log("request pass3");
                                                    axios.delete("http://127.0.0.1:8000/lineup/" + 1500 + "/",
                                                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                                                        {
                                                            headers: {
                                                                "Content-Type": "multipart/form-data"
                                                            }
                                                        },
                                                    )
                                                })
                                            }
                                            if(element.id==1515){
                                                axios.delete("http://127.0.0.1:8000/lineup/" + 1515 + "/",
                                                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                                                        {
                                                            headers: {
                                                                "Content-Type": "multipart/form-data"
                                                            }
                                                        },
                                                    )
                                            }
                                        });*/

                    this.lineupp = this.lineup[0];
                    this.name = this.lineupp.name;
                    this.previewImage = this.lineupp.image;
                    this.id = this.lineupp.id;
                    this.order = this.lineupp.order;
                    this.currentImage = this.lineupp.image;

                })

        } else {
            axios.get('http://127.0.0.1:8000/lineup/',)
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
        postLineup(formdata) {
            axios.post("http://127.0.0.1:8000/lineup/", formdata,
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                },
            )
        }
        , checkLineup() {

            let formData = new FormData();
            let updateData=[];
            formData.append("image", this.currentImage);
            updateData.push(this.currentImage);




            formData.append("name", this.name);
            updateData.push(this.name);


            if (this.slug != "0") {

                formData.append("id", this.id);
                updateData.push(this.id);
                formData.append("order", this.order);
                updateData.push(this.order);
                formData.append("slug", this.slug);
                updateData.push(this.slug);

                store.commit('setupdateData', updateData);
                store.dispatch('storePost',formData);
                console.log("fja");

                console.log(formData.get("image"));

                axios.post("http://127.0.0.1:8000/lineup/", formData,
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                {
                    headers: {
                        "Content-Type": "multipart/form-data"

                    }
                },)

                axios.put("http://127.0.0.1:8000/lineup/" + this.id + "/", formData,
                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                    {
                        headers: {
                            "Content-Type": "multipart/form-data"

                        }
                    },

                )/*.then(() => {
                    console.log("request pass1");
                    axios.post("http://127.0.0.1:8000/lineup/", formData,
                        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                        {
                            headers: {
                                "Content-Type": "multipart/form-data"
                            }
                        },
                    ).then(() => {
                        console.log("request pass2");

                    })
                })
*/
            } else {
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

                console.log(this.lineups[this.lineups.length - 1].order)

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

                console.log(this.nextOrder)

                formData.append("id", this.nextId);
                formData.append("order", this.nextOrder);
                this.postLineup(formData);
            }
            console.log("adksad")



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