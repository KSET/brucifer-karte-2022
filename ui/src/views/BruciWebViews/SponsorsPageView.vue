<template>
    <div class="bw-page-container sponsors-page">
        <div class="popis">

            <div v-if="this.guestsEnabled != 0" class="popis-element1">
                <h1 class="page-title">Popis uzvanika</h1>

                <h1 class="textfield">Ime i prezime </h1>
                <input class="inputfield " type="text" v-model="sponsorName">

                <button class="button submit" style="background-color: white; margin-top: 0px; display: block; "
                    @click="sponsorPost">
                    Dodaj
                </button>
            </div>

            <div>
                <h1 v-if="this.guestsEnabled == 0" class="page-title-dis" style="margin-left: 50px; margin-top: 70px;">
                    Popis
                    uzvanika</h1>

                <div v-if="this.guestsEnabled != 0" class="infofield">
                    <div class="artist">
                        <div class="image-container">
                            <img class="image-frame2" style="border: none;" :src="previewImage">
                        </div>
                    </div>

                    <div class="infofield-element">
                        <div class="grid-container">
                            <h1 class="textfield" style="margin-bottom: 1em">Ograničenje</h1>
                            <h1 class="textfield" style="font-weight: 400; margin-bottom: 1em">{{ this.guestCap }}</h1>
                            <h1 class="textfield">Broj unesenih</h1>
                            <h1 class="textfield" style="font-weight: 400">{{ this.guestsAdded }}</h1>
                        </div>
                    </div>
                </div>
                <div v-else class="infofield-tablet">
                    <div class="artist tabb">
                        <div class="image-container">
                            <img class="image-frame2" style="border: none;" :src="previewImage">
                        </div>
                    </div>

                    <div class="infofield-element">
                        <div class="grid-container">
                            <h1 class="textfield" style="margin-bottom: 1em">Ograničenje</h1>
                            <h1 class="textfield" style="font-weight: 400; margin-bottom: 1em">{{ this.guestCap }}</h1>
                            <h1 class="textfield">Broj unesenih</h1>
                            <h1 class="textfield" style="font-weight: 400">{{ this.guestsAdded }}</h1>
                        </div>
                    </div>
                </div>
                <h1 v-if="this.guestsEnabled == 0" class="textfield dis" style="text-align: center;">Vrijeme za promjenu
                    popisa je isteklo! <br>
                    Ovo je vaš konačni popis!</h1>

            </div>
        </div>

        <div class="sponsorsPage-table">
            <div class=row>
                <table id="guests">
                    <tbody :class="{ [$style.tbodyHigh]: this.tbodyHigh }"
                        style="overflow:auto;height: 35rem !important;" class="tbody">
                        <tr v-for="guest in sponsorGuests" style=" width: 100%;" :key="guest.id">
                            <td style="padding-left: 20% !important;">{{ guest.name }}</td>
                            <td v-if="this.guestsEnabled != 0" style="padding-left: 10% !important;"><button
                                    class="button-icon" @click=sponsorDelete(guest)
                                    style="margin-left: 0.9rem;     background: transparent;"> <img
                                        src="@/assets/icons/trash-icon-white.svg"></button>
                            </td>
                        </tr>
                    </tbody>
                </table>

            </div>
        </div>

    </div>
    <Footer></Footer>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import NavbarBweb from '@/components/NavbarAndFooter/NavbarBweb.vue'
import store from '@/store/visibilityStore'
import { publicApi } from "@/plugins/publicApi";
import { api } from '@/plugins/api';

export default {
    components: { Footer, NavbarBweb },
    data() {
        return {
            currentImage: undefined,
            previewImage: undefined,
            slug: '0',
            progress: 0,
            message: "",

            name: '',
            id: '',
            len: '',
            guestCap: '',
            guestsAdded: '',
            guestIDs: '',
            sponsorGuests: [],
            guests: [],
            guestsEnabled: '',
        };
    },
    mounted() {
        this.slug = this.$route.params.slug;
        if (this.slug != '0') {
            publicApi.get("/sponsors/public/", { params: { slug: this.slug } })
                .then(async response => {
                    this.sponsors = response.data;
                    if (this.sponsors.length == 0) {
                        this.$router.push({ path: '/admin/sponsors-add/0' });
                    }

                    this.sponsorsInstance = this.sponsors;
                    this.name = this.sponsorsInstance.name;
                    this.previewImage = this.sponsorsInstance.image;
                    this.id = this.sponsorsInstance.id;
                    this.guestCap = this.sponsorsInstance.guestCap;

                    this.currentImage = this.sponsorsInstance.image;
                    this.guestIDs = this.sponsorsInstance.guests;

                    this.guestsEnabled = this.sponsorsInstance.guestsEnabled;

                    if (this.guestsEnabled != 2) {
                        let closeTime = Date.parse(store.state.SPONSORS_INPUT_TIME); // pravi closetime 12.11.2022 u 19.00
                        console.log(closeTime)
                        if (Date.now() > closeTime) {
                            console.log("zatvaraaaaj")
                            console.log(this.sponsorsInstance)

                            let formData = new FormData();

                            formData.append("guestsEnabled", 0);
                            this.guestsEnabled = 0;


                            const resp = await axios.put(process.env.VUE_APP_BASE_URL + "/sponsors/" + this.sponsorsInstance.id + "/", formData,
                                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } },
                                {
                                    headers: {
                                        "Content-Type": "multipart/form-data"

                                    }
                                })

                            console.log("posted")
                        }
                    }
                    console.log(Date.now())

                })
        }


        this.created();
    },

    methods: {
        created() {
            if (this.slug !== '0') {
                api
                    .get(`${process.env.VUE_APP_BASE_URL}/sponsors/public/guests/`, {
                        params: { slug: this.slug }
                    })
                    .then(response => {
                        this.sponsorGuests = response.data;
                        this.guestsAdded = this.sponsorGuests.length;
                    })
                    .catch(err => {
                        const msg = err?.response?.data?.detail || "Greška pri dohvaćanju gostiju";
                        window.alert(msg);
                    });
            }
        },
        sponsorDelete(guest) {
            api.delete(
                `${process.env.VUE_APP_BASE_URL}/sponsors/public/guests/`,
                { params: { slug: this.slug, id: guest.id } }
            ).then(() => {
                this.created();
            }).catch(err => {
                const msg = err?.response?.data?.detail || "Greška pri brisanju gosta";
                window.alert(msg);
            });
        },
        sponsorPost() {
            // Check if sponsor reached guest limit
            if (this.guestCap === this.guestsAdded) {
                window.alert("Već ste unijeli maksimalan broj dozvoljenih gostiju");
                return;
            }

            const guestName = (this.sponsorName || "").trim();
            if (!guestName) {
                return;
            }

            const payload = {
                slug: this.slug,
                name: guestName,
            };

            api.post(`${process.env.VUE_APP_BASE_URL}/sponsors/public/guests/`, payload)
                .then(() => {
                    this.sponsorName = "";
                    this.created();
                })
                .catch(err => {
                    const msg = err?.response?.data?.detail || "Greška pri unosu gosta";
                    window.alert(msg);
                });
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
.page-title-dis {
    vertical-align: middle;
    display: inline-block;
    padding-top: 3%;
    padding-bottom: 3%;
    padding-right: 5%;

    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 700;
    font-size: 32px;
    line-height: 36px;
    /* identical to box height, or 112% */

    letter-spacing: -0.015em;

    color: white;
}

.image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

.artist {
    width: 15rem;
    height: 15rem;
    background: rgba(0, 0, 0, .3);
    border-radius: 18px;
    padding: 15px 30px;
}

.popis-element1 {
    border-bottom: white solid 2px !important;
    padding-left: 6%;
    padding-top: 5.5rem;
    padding-bottom: 5rem;
}

.sponsorsPage-table {
    margin-top: 6.75rem;
}

.grid-container {
    grid-template-columns: 95% auto;
    row-gap: 0%;
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
    display: grid;
    grid-template-rows: 55% 45%;
    width: 100%;
    height: 100%;
    border-bottom: white solid 2px !important;
    border-right: white solid 2px !important;

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
    padding-left: 6%;
    height: 100%;

}

.infofield-tablet {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding-left: 6%;
    height: 100%;
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

.footery {
    background: var(--bw-footer-color);
    ;
}

.footery::after {
    background: linear-gradient(to top, var(--bw-footer-color), transparent);
}

.navbar.bw {
    background: var(--bw-footer-color);
}

.navbar.bw::after {
    background: linear-gradient(var(--bw-footer-color), transparent);
}

@media screen and (max-width: 980px) {
    .popis-element1 {
        margin-top: 0rem;
        padding-bottom: 0rem;
    }

    .sponsors-page {
        display: flex;
        flex-direction: column;
    }

    .popis {
        display: grid;
        grid-template-columns: 65% auto;
        width: 100%;
        padding-top: 5.75rem;
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
        row-gap: 0%;
        padding-left: 0%;
    }

    .artist {
        margin-top: 3%;
        width: 12rem;
        height: 12rem;
        padding: 20px;
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

    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 9rem;
    }

    .page-title-dis {
        margin-top: 0px !important;
        margin-bottom: 10px;
    }

    .infofield-tablet {
        width: 100%;
        margin-left: 10%;
    }

    .textfield.dis {
        margin-top: 30px;
        margin-left: 45%;

    }

    .artist.tabb {
        margin-right: 5%;
    }
}

@media screen and (max-width: 550px) {
    .artist {
        width: 8rem;
        height: 8rem;
        padding: 12px;
    }

    .image-container {
        width: 100%;
        height: 6rem;
    }

    .popis {
        grid-template-columns: 60% auto;
    }

    .page-title-dis {
        width: 150%;
    }

    .textfield.dis {
        margin-top: 30px;
        margin-left: 7%;
        width: 150%;

    }
}
</style>