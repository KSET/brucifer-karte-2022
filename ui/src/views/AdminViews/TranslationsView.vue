<template>
    <div id="translations">
        <Sidebar />
        <div class="admin-page-container">
            <h1 class="page-title">Translations</h1>

            <div class="input-grid">
                <input class="inputfield" type="text" placeholder="Unesite ključ" v-model="key">
                <textarea style="font-size: 12px;" class="inputfield" type="text" placeholder="Unesite vrijednost"
                    v-model="value"></textarea>
                <button class="button submit" @click="postTranslation">Dodaj</button>
            </div>

            <div class="clumnname-grid">
                <h1 class="textfield">Key</h1>
                <h1 class="textfield">Value</h1>
                <h1 class="textfield">Options</h1>
            </div>

            <div class="translations-grid">
                <div class="translations-item" v-for="( translation ) in  translationsTable " :key="translation.key">
                    <div class="textfield" @input="changeTranslationKey(translation)"
                    contenteditable="true" v-html="translation.key"></div>
                    <div style="padding: 7px" class="textfield" @input="changeTranslationValue(translation)"
                        contenteditable="true" v-html="translation.value"></div>
                    <button class="button-icon" @click="deleteTranslation(translation)"> <img
                            src="@/assets/icons/trash-icon.svg"></button>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import translationsStore from "@/store/translationsStore.js";

export default {
    name: 'TranslationsView',
    components: {
        Sidebar,
    },
    data() {
        return {
            key: '',
            value: '',
        }
    },
    computed: {
        translationsTable() {
            return translationsStore.state.translationsTable
        }
    },
    methods: {
        async postTranslation() {
            await axios.post(process.env.VUE_APP_BASE_URL + '/translations/',
                { key: this.key, value: this.value },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )

            this.key = "";
            this.value = "";
            await translationsStore.dispatch("fetchTranslations")

        },
        async deleteTranslation(translation) {
            console.log(translation)
            await axios.delete(process.env.VUE_APP_BASE_URL + '/translations/' + translation.id + '/',
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
            await translationsStore.dispatch("fetchTranslations")
        },
        async changeTranslationValue(translation) {
            let changeVal = event.target.innerHTML.replace(/<(?!br\s*\/?)[^>]+>/gi, '').replace('<br>', '\n\n')
            await axios.put(process.env.VUE_APP_BASE_URL + '/translations/' + translation.id + '/',
                { value: changeVal },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
        },
        async changeTranslationKey(translation) {
            let changeKey = event.target.innerHTML.replace(/<(?!br\s*\/?)[^>]+>/gi, '').replace('<br>', '\n\n')
            await axios.put(process.env.VUE_APP_BASE_URL + '/translations/' + translation.id + '/',
                { key: changeKey },
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            )
        },
        changeValue() {
            this.value = event.target.innerHTML.replace(/<(?!br\s*\/?)[^>]+>/gi, '').replace('<br>', '\n\n')
        }
    }
}
</script>


<style scoped lang="scss">
.inputfield {
    width: 90%;
}

.button.submit {
    margin-top: 0px;
}

.input-grid,
.clumnname-grid,
.translations-item {
    display: grid;
    grid-template-columns: 30% 50% 20%;
    align-items: center;
}

.translations-item {
    border-bottom: 1px solid lightgray;
    padding: 10px 0;
}

.translations-grid {
    overflow-y: scroll;
    height: 70%;
}

.clumnname-grid {
    margin: 0.5em 0 0.5em 0;
    padding: 0.5em 0 0.5em 0;
    border-top: 1px solid black;
    border-bottom: 1px solid black;
}

p {
    font-family: "Montserrat" !important;
    color: red;
}

.textfield {
    white-space: pre-wrap;
}
</style>

  
  
  