<template>
  <div class="bw-page-container">
    <div>
      <div class="contents">
        <div v-if="translationsLength != 0">
          <section v-for="i in translationsLength" :key="i">

            <h1>{{ translations.pravilaponasanja["title" + i] }}</h1>
            <div class="text">
              <p class="pText" v-for="text in translations.pravilaponasanja['text' + i].split('\n\n')" :key="text">{{ text
              }}</p>
            </div>
          </section>
        </div>

        <div v-else>
          <h1>pravilaponasanja.title1</h1>
          <h1>pravilaponasanja.text1</h1>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import translationsStore from '@/store/translationsStore';

export default {
  name: 'PravilaPonasanjaView',
  components: { Footer },
  data() {
    return {
    }
  },
  computed: {
    translations() {
      return translationsStore.state.translations;
    },
    translationsLength() {
      return this.translations.pravilaponasanja ? Object.keys(this.translations.pravilaponasanja).length / 2 : 0;
    }
  }
}
</script>

