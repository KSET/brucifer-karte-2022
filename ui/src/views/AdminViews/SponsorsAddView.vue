<template>
    <div id="sponsors-add">
        <Sidebar />
        <div class="admin-page-container" style=" overflow: auto;">
            <div class="header">
                <h1 v-if="(this.slug == '0')" class="page-title">Dodavanje sponzora</h1>
                <h1 v-else class="page-title">Uređivanje sponzora</h1>
            </div>
            <img class="image-preview hideDesktop" style="display: block; margin-bottom: 5%; margin-left: 5%;"
                :src="previewImage" alt="" />

            <form class="sponsors-form" @submit.prevent="postSponsors">
                <div class="grid-container" style="row-gap:3rem;">

                    <h1 class="textfield">Ime </h1>
                    <input required class="inputfield" type="text" v-model="name">

                    <h1 class="textfield">Link </h1>
                    <input required class="inputfield" type="url" v-model="url">


                    <h1 class="textfield">Slika </h1>
                    <label for="file-upload" class="button white" style="margin-top: 0px;">
                        Odaberi PNG
                    </label>

                    <input id="file-upload" type="file" accept="image/*" ref="file" @change="selectImage" />

                    <h1 class="textfield" style="width: 150%;">E-mail </h1>
                    <input required class="inputfield" type="text" v-model="email">

                    <h1 class="textfield" style="width: 150%;">Broj uzvanika </h1>
                    <input required class="inputfield" type="text" v-model="guestCap">

                    <h1 class="textfield">Vidljivo</h1>
                    <label class="switch">
                        <input id="switchSponsors" type="checkbox" v-model="visible">
                        <span class="slider round"></span>
                    </label>

                    <h1 class="textfield">Popis</h1>
                    <label class="switch">
                        <input id="switchPopis" type="checkbox" v-model="guestsEnabled">
                        <span class="slider round"></span>
                    </label>


                    <button type="submit" class="button submit" style="margin-top: 0px"
                        v-if="slug === '0'">Dodaj</button>
                    <button type="submit" class="button submit" style="margin-top: 0px" v-else>Spremi
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
            <img class="image-preview hideTablet" :src="previewImage" alt="" />

        </div>
    </div>
</template>

<script>
import { uuid } from 'vue-uuid'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import sponsorsStore from '@/store/sponsorsStore'
import ToggleSwitch from 'primevue/toggleswitch'

export default {
    name: "SponsorsAdd",
    components: { Sidebar, ToggleSwitch },

    data() {
        return {
            currentImage: undefined,
            previewImage: undefined,
            slug: '0',
            progress: 0,
            message: "",

            id: '',
            name: '',
            order: '',
            url: '',
            email: '',
            guestCap: '',
            visible: false,
            guestsEnabled: '0',

            uuid: uuid.v1(),
            buttonEnabled: true,
        }
    },

    async created() {
        this.slug = this.$route.params.slug

        if (this.slug !== '0') {
            // fetch single sponsor by slug
            const sponsor = await sponsorsStore.dispatch('fetchBySlug', this.slug)
            if (!sponsor) {
                this.$router.push({ path: '/admin/sponsors-add/0' })
                return
            }
            this.id = sponsor.id
            this.name = sponsor.name
            this.previewImage = sponsor.image
            this.order = sponsor.order
            this.url = sponsor.url
            this.email = sponsor.email
            this.guestCap = sponsor.guestCap
            this.guestsEnabled = sponsor.guestsEnabled
            this.visible = sponsor.visible
            this.currentImage = sponsor.image
        } else {
            // fetch all sponsors to compute next order
            await sponsorsStore.dispatch('fetchAll')
        }
    },

    computed: {
        sponsors() {
            return sponsorsStore.state.list
        },
        loading() {
            return sponsorsStore.state.loading
        },
        error() {
            return sponsorsStore.state.error
        },
    },

    methods: {
        selectImage() {
            this.currentImage = this.$refs.file.files.item(0)
            this.previewImage = URL.createObjectURL(this.currentImage)
            this.progress = 0
            this.message = ""
        },

        reroutePopis() {
            this.$router.push({ path: '/sponzori/' + this.slug })
        },

        async deleteSponsors() {
            if (!this.id) return
            await sponsorsStore.dispatch('remove', this.id)
            this.$router.push({ path: '/admin/sponsors-list/' })
        },

        async postSponsors() {
            if (!this.currentImage) {
                window.alert("Uploadajte fotografiju")
                return
            }

            const formData = new FormData()
            formData.append("name", this.name)
            formData.append("url", this.url)
            formData.append("email", this.email)
            formData.append("guestCap", this.guestCap)
            formData.append("visible", this.visible ? "1" : "0")

            // guestsEnabled logic
            if (this.guestsEnabled === '1') {
                const closeTime = 1668276000000
                formData.append("guestsEnabled", Date.now() > closeTime ? "2" : "1")
            } else {
                formData.append("guestsEnabled", "0")
            }

            if (this.slug !== "0") {
                // update
                formData.append("id", this.id)
                formData.append("order", this.order)
                formData.append("slug", this.slug)

                if (this.currentImage instanceof File) {
                    formData.append("image", this.currentImage)
                }

                await sponsorsStore.dispatch('update', { id: this.id, formData })
            } else {
                // create
                const last = this.sponsors[this.sponsors.length - 1]
                const nextOrder = last ? last.order + 1 : 0
                formData.append("order", nextOrder.toString())
                formData.append("slug", uuid.v1())
                formData.append("image", this.currentImage)

                await sponsorsStore.dispatch('create', formData)
            }

            this.$router.push({ path: '/admin/sponsors-list/' })
        },

        linkValidator(text) {
            if (!text) return false
            return text.startsWith("http://") || text.startsWith("https://")
        },
    },
}
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
        row-gap: 3rem;
    }

    .button.submit {
        width: 130px;
        height: 40px;
    }
}
</style>