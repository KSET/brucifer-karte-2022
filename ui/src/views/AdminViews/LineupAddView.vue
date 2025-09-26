<template>
    <div id="lineup-add">
        <Sidebar />
        <div class="admin-page-container" style="overflow:auto; display:flex; flex-direction:column">
            <div class="header">
                <h1 class="page-title">{{ isEdit ? 'Uređivanje izvođača' : 'Dodavanje izvođača' }}</h1>
            </div>

            <img v-if="previewImage" class="image-preview hideTablet showMobile"
                style="display:block; margin-bottom:5%; margin-left:5%" :src="previewImage" alt="Preview (mobile)" />
            <img v-if="previewImage" class="image-preview hideMobile" :src="previewImage" alt="Preview" />

            <form class="lineup-form" @submit.prevent="submit">
                <div class="grid-container">
                    <h1 class="textfield">Ime</h1>
                    <input required class="inputfield" type="text" v-model.trim="name" />

                    <h1 class="textfield">Slika</h1>
                    <label for="file-upload" class="button white" style="margin-top:0px;">Odaberi sliku</label>
                    <input id="file-upload" type="file" accept="image/*" ref="file" @change="selectImage"
                        :required="!isEdit && !currentImage" />

                    <h1 class="textfield">Vidljivo</h1>
                    <label class="switch">
                        <input type="checkbox" v-model="visibility" />
                        <span class="slider round"></span>
                    </label>

                    <h1 class="textfield">Biografija</h1>
                    <textarea class="inputfield" rows="6" v-model.trim="biography"
                        placeholder="Unesite biografiju izvođača..."></textarea>
                </div>

                <button class="button submit" type="submit">
                    {{ isEdit ? 'Spremi promjene' : 'Dodaj' }}
                </button>

                <button v-if="isEdit" type="button" class="button submit del"
                    style="background-color:white; margin-left:10px" @click="deleteLineup" title="Obriši">
                    <img class="va" src="../../assets/icons/trash-icon.svg" alt="Delete" />
                </button>
            </form>
        </div>
    </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import lineupStore from '@/store/lineupStore'

export default {
    name: 'LineupAdd',
    components: { Sidebar },

    data() {
        return {
            slug: '0',
            id: null,

            name: '',
            visibility: true,
            biography: '',         // ← NEW

            currentImage: null,
            previewImage: null,

            loading: false,
        }
    },

    computed: {
        isEdit() {
            return this.slug !== '0'
        },
        lineup() {
            return lineupStore.state.item
        },
        storeLoading() {
            return lineupStore.state.loading
        },
        storeError() {
            return lineupStore.state.error
        },
    },

    async created() {
        this.slug = this.$route.params.slug
        if (this.isEdit) {
            await this.fetchLineup()
        }
    },

    methods: {
        async fetchLineup() {
            try {
                const item = await lineupStore.dispatch('fetchBySlug', this.slug)
                if (!item) {
                    this.$router.push({ path: '/admin/lineup-add/0' })
                    return
                }
                this.id = item.id
                this.name = item.name || ''
                this.visibility = Boolean(item.visible)
                this.biography = item.biography || ''   // ← NEW
                this.previewImage = item.image || null
                this.currentImage = null
            } catch (e) {
                console.error(e)
                alert('Greška pri dohvaćanju izvođača.')
            }
        },

        selectImage() {
            const file = this.$refs.file?.files?.[0]
            if (!file) return
            this.currentImage = file
            this.previewImage = URL.createObjectURL(file)
        },

        async deleteLineup() {
            if (!this.isEdit || !this.id) return
            if (!confirm('Sigurno želite obrisati izvođača?')) return

            try {
                await lineupStore.dispatch('remove', this.id)
                this.$router.push({ path: '/admin/lineup-list/' })
            } catch (e) {
                console.error(e)
                alert('Brisanje nije uspjelo.')
            }
        },

        buildFormData({ name, visible, image, biography }) {
            const fd = new FormData()
            if (name != null) fd.append('name', name)
            if (visible != null) fd.append('visible', visible) // boolean true/false
            if (biography != null) fd.append('biography', biography) // ← NEW
            if (image instanceof File) fd.append('image', image)
            return fd
        },

        async submit() {
            this.loading = true
            try {
                if (this.isEdit) {
                    const formData = this.buildFormData({
                        name: this.name,
                        visible: this.visibility,
                        biography: this.biography,      // ← NEW
                        image: this.currentImage,
                    })
                    await lineupStore.dispatch('update', { id: this.id, formData })
                } else {
                    if (!(this.currentImage instanceof File)) {
                        alert('Učitajte fotografiju.')
                        this.loading = false
                        return
                    }
                    const formData = this.buildFormData({
                        name: this.name,
                        visible: this.visibility,
                        biography: this.biography,      // ← NEW
                        image: this.currentImage,
                    })
                    await lineupStore.dispatch('create', formData)
                }

                this.$router.push({ path: '/admin/lineup-list/' })
            } catch (e) {
                console.error(e)
                alert('Spremanje nije uspjelo.')
            } finally {
                this.loading = false
            }
        },
    },
}
</script>

<style scoped>
.lineup-form {
    display: inline-block;
    width: 60%;
}

.button.submit.del {
    margin-left: 0px;
}

.image-preview {
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