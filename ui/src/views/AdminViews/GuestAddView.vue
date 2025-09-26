<template>
    <div class="guests-add">
        <Sidebar />
        <div class="admin-page-container">

            <h1 class="page-title">Dodavanje Gosta</h1>

            <form onsubmit="return false">
                <div class="grid-container" style="row-gap: 2rem;">
                    <h1 class="textfield">Ime: </h1>
                    <input required class="inputfield" type="text" @input="changeValue" v-model="name">

                    <h1 class="textfield">Prezime: </h1>
                    <input required class="inputfield" type="text" @input="changeValue" v-model="surname">

                    <h1 class="textfield">Tag: </h1>

                    <select id="tagselect" class="inputfield" v-model="selectedTag" name={{selectedTag}}
                        @input="checkJMBAGdisplay">
                        <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
                    </select>

                    <h1 id="jmbagselect" class="textfield">JMBAG: </h1>
                    <input id="jmbagselectt" class="inputfield" type="text" v-model="jmbag">

                    <h1 class="textfield">Karta: </h1>

                    <button class="button change" v-if="karta == '1'" type="button" @click="changeKarta()">
                        <img src="../../assets/icons/yes-icon.svg">
                    </button>
                    <button class="button change" v-else @click="changeKarta()" style="background-color: white;"
                        type="button ">
                        <img src="../../assets/icons/no-icon.svg">
                    </button>

                    <h1 class="textfield">Ulaz: </h1>

                    <button v-if="ulaz == '1'" type="button" class="button change" @click="changeUlaz()">
                        <img src="../../assets/icons/yes-icon.svg">
                    </button>
                    <button v-else @click="changeUlaz()" type="button" style="background-color: white;"
                        class="button change">
                        <img src="../../assets/icons/no-icon.svg">
                    </button>
                    <button class="button submit" @click="postGuest">Dodaj</button>
                </div>
            </form>

        </div>

        <v-dialog v-model="dialog" max-width="500">
            <v-card>
                <v-card-text>
                    <div v-if="dialogType === 'success'">
                        <h1 class="textfield">Uspjeh</h1>
                        <p>{{ dialogMessage }}</p>
                    </div>
                    <div v-else-if="dialogType === 'error'">
                        <h1 class="textfield">Greška</h1>
                        <p>{{ dialogMessage }}</p>
                    </div>
                    <div class="grid-container guests" v-if="dialogType === 'success'">
                        <h1 class="textfield">Ime</h1>
                        <input class="inputfield" readonly type="text" v-model="name">

                        <h1 class="textfield">Prezime</h1>
                        <input class="inputfield" readonly type="text" v-model="surname">

                        <h1 v-if="jmbag" class="textfield">JMBAG</h1>
                        <input v-if="jmbag" class="inputfield" readonly type="text" v-model="jmbag">

                        <h1 class="textfield">Tag</h1>
                        <input class="inputfield" readonly type="text" v-model="selectedTag">
                    </div>
                </v-card-text>

                <v-card-actions>
                    <v-btn color="primary" block @click="dialogClose">Zatvori</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

import { api } from "@/plugins/api";

export default {
    name: 'GuestsAdd',
    components: {
        Sidebar
    },
    props: {
        msg: String
    },
    data() {
        return {
            items: [],
            guests: [],
            karta: '1',
            ulaz: '1',
            guest: '',
            id: '',
            name: '',
            surname: '',
            jmbag: '',
            phone: '',
            tag: '',
            bought: '',
            entered: '',
            deleted: '',
            len: '',
            services: ['Brucoši', 'KSET', 'VIP'],
            selectedTag: '',

            dialog: false,
            dialogProgress: false,
        }
    },

    mounted() {
        this.created()
    },
    methods: {
        created() {
            api.get('/guests/',)
                .then(response => {
                    document.getElementById("jmbagselect").style.display = "none";
                    document.getElementById("jmbagselectt").style.display = "none";
                    this.guests = response.data;
                    this.len = this.guests.length;
                    api.get('/tags/',)
                        .then(response => {
                            var itemss = response.data;
                            this.items = [];
                            itemss.forEach(element => {
                                this.items.push(element.name);
                            });

                        })
                })
        },
        checkJMBAGdisplay() {
            var e = document.getElementById("tagselect").value;
            if (e.includes("Brucoši")) {
                document.getElementById("jmbagselect").style.display = "inline-block";
                document.getElementById("jmbagselectt").style.display = "inline-block";

            } else {
                document.getElementById("jmbagselect").style.display = "none";
                document.getElementById("jmbagselectt").style.display = "none";

            }
        },
        changeKarta() {
            if (this.karta == '1') {
                this.karta = '0';
            } else {
                this.karta = '1';
            }
        },
        changeUlaz() {
            if (this.ulaz == '1') {
                this.ulaz = '0';
            } else {
                this.ulaz = '1';
            }
        },
        postGuest() {
            if (this.name == '' || this.surname == '' || this.selectedTag == '') {
                window.alert("Unesite sva polja")
            } else {
                var ids = [];
                var jmbags = [];

                this.guests.forEach(element => {
                    ids.push(element.id);
                    jmbags.push(element.jmbag);
                });

                let post = 1;

                if (this.selectedTag.includes("Brucoši")) {
                    if (jmbags.includes(String(this.jmbag))) {
                        window.alert("Gost s ovim JMBAG-om već postoji!!")
                        post = 0;
                    }
                }

                if (post == 1) {

                    api.post('/guests/',
                        { name: this.name, surname: this.surname, jmbag: this.jmbag, tag: this.selectedTag, bought: this.karta, entered: this.ulaz },
                    )
                        .then(() => {
                            this.dialogProgress = false;
                            this.dialog = true;
                            this.dialogMessage = 'Gost je uspješno dodan!';
                            this.dialogType = 'success';
                        })
                        .catch((error) => {
                            this.dialogProgress = false;
                            this.dialog = true;
                            this.dialogMessage = `Greška prilikom dodavanja gosta: ${error.response?.data?.detail || error.message}`;
                            this.dialogType = 'error';
                        });
                }
            }
        },
        dialogClose() {
            this.dialog = false;
            this.name = ''
            this.surname = ''
            this.selectedTag = ''
            this.jmbag = ''
            this.karta = '1';
            this.ulaz = '1';
            document.getElementById("jmbagselect").style.display = "none";
            document.getElementById("jmbagselectt").style.display = "none";
            this.created()
        }
    }
}
</script>

<style lang="scss" scope>
@import '../../assets/scss/Admin-scss/gird-view.scss';
</style>