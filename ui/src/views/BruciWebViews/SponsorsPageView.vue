<template>
    <div class="bw-page-container sponsors-page">
        <div class="popis">
            <div class="popis-element1">
                <h1 class="page-title">Popis uzvanika</h1>

                <h1 class="textfield">Ime i prezime </h1>
                <input class="inputfield " type="text" v-model="sponsorName">

                <button class="button submit" style="background-color: white; margin-top: 0px; display: block; "
                    @click="sponsorPost">
                    Dodaj
                </button>
            </div>

            <div class="infofield">
                <img class="image-preview" style="border: none;" :src="previewImage" alt="" />

                <div class="infofield-element">
                    <div class="grid-container">
                        <h1 class="textfield">Ograničenje</h1>
                        <h1 class="textfield" style="font-weight: 400">{{this.guestCap}}</h1>
                        <h1 class="textfield">Broj unesenih</h1>
                        <h1 class="textfield" style="font-weight: 400">{{this.guestsAdded}}</h1>
                    </div>
                </div>
            </div>

        </div>

        <div class="sponsorsPage-table">
            <div class=row>
                <table id="guests">

                    <tbody :class="{ [$style.tbodyHigh]: this.tbodyHigh }" style="overflow:auto;" class="tbody">
                        <tr v-for="guest in sponsorGuests" :key="guest.id">
                            <td style="padding-left: 20% !important;">{{guest.name}}</td>
                            <td style="padding-left: 10%% !important;"><button class="button-icon"
                                    @click=sponsorDelete(guest)
                                    style="margin-left: 0.9rem;     background: transparent;"> <img
                                        src="@/assets/icons/trash-icon-white.svg"></button>
                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>
        </div>


        <Footer></Footer>
    </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import axios from 'axios'

export default {
    components: { Footer },
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
            guestCap: '',
            guestsAdded: '',
            guestIDs: '',
            sponsorGuests: [],
            guests: [],
        };
    },
    mounted() {
        this.created();
    },

    methods: {
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
                        this.guestCap = this.sponsorsInstance.guestCap;

                        this.currentImage = this.sponsorsInstance.image;

                        this.guestIDs = this.sponsorsInstance.guests;

                        axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=' + this.slug + "&search_fields=tag")
                            .then(response => {
                                this.sponsorGuests = response.data;
                                this.guestsAdded = this.sponsorGuests.length;
                                axios.get(process.env.VUE_APP_BASE_URL + '/guests/')
                                    .then(response => {
                                        this.guests = response.data;
                                    })
                            })
                    })

            } else {
                axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?ordering=order',)
                    .then(response => {
                        this.sponsorss = response.data;

                    })
            }
        },
        sponsorDelete(guest) {
            axios.delete(process.env.VUE_APP_BASE_URL + '/guests/' + guest.id + '/',
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
                .then(() => {
                    this.created();
                })
        },
        sponsorPost() {
            if (this.guestCap == this.guestsAdded) {
                window.alert("Već ste unjeli maximum dozvoljenih gostiju")
            } else {
                var ids = [];
                this.guests.forEach(element => {
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

                let sponsorTag = "Sponzori" + this.slug

                axios.post(process.env.VUE_APP_BASE_URL + '/guests/',
                    { id: this.nextId, name: this.sponsorName, tag: sponsorTag, bought: '1', entered: '0' },
                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                )
                    .then(() => {
                        this.sponsorName = "";
                        this.created()
                    })
            }

        }

    }
}
</script>
<style module>
:global(#app) .tbodyHigh {
    height: 100%;
}
</style>

<style scoped>
.popis-element1 {
    border-bottom: white solid 2px !important;
    border-right: white solid 2px !important;
    padding-left: 6%;
    padding-top: 5%
}

.sponsorsPage-table {
    margin-top: 3rem;
}

.grid-container {
    grid-template-columns: 95% auto;
    row-gap: 100%;
}

.sponsors-page {

    position: relative;
    display: grid;
    grid-template-columns: 50% 50%;
    width: 100%;
    height: 93vh;

    background-color: #CCCCCCCC;
    background-blend-mode: multiply;
}

.popis {
    position: relative;
    margin-top: 2%;
    display: grid;
    grid-template-rows: 50% 50%;
    width: 100%;
    height: 100%;
    border-bottom: white solid 2px !important;
}

h1 {
    color: white;
}

.infofield-element {
    padding-left: 12%;
}

.inputfield {
    background: transparent;
    border: none;
    border: white solid 2px !important;
    color: white;

    margin-top: 2%;
    margin-bottom: 5%;
}

.button.submit {
    color: black;
    font-family: 'Montserrat';
    font-weight: 500;
    border: none;
}

.row {
    margin-left: 0px;
}

.infofield {
    display: flex;
    flex-direction: row;
    align-items: center;
    border-right: white solid 2px !important;
    padding-left: 6%;
}

#guests td {
    color: white;
    border-bottom: 2px solid white;
}

#guests tr:nth-child(even) {
    background-color: transparent;
}

#guests tr:hover {
    background-color: transparent;
    ;

}

@media screen and (max-width: 980px) {
    .sponsors-page {
        display: flex;
        flex-direction: column;
    }

    .popis {
        display: grid;
        grid-template-columns: 65% auto;
        width: 100%;
        margin-top: 2rem;
        padding-bottom: 2rem;

    }

    .infofield {
        display: flex;
        flex-direction: column;
        border: none !important;
        padding: 0px;
        margin: 0px;
        align-items: flex-start;
    }

    .popis-element1 {
        border: none !important;
        padding-top: 0px;
    }

    .grid-container {
        row-gap: 50%;
        padding-left: 0%;
    }

    .image-preview {
        height: 150px;
        width: 150px;
    }

    .infofield-element {
        padding-top: 6%;
        padding-left: 0%;
    }

    .inputfield {
        margin-top: 5%;
        margin-bottom: 7%;
    }

    .page-title {
        padding-bottom: 7%;
    }

    .sponsorsPage-table {
        margin-top: 0rem;
    }
}
</style>