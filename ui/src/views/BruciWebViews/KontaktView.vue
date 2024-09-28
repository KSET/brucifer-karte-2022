<template>
  <div class="bw-page-container">
    <div>
      <div class="contents">
        <div v-if="translationsLength != 0">
          <section v-for="i in translationsLength" :key="i">

            <h1>{{ translations.kontakt["title" + i] }}</h1>
            <div class="text">
              <p class="pText" v-for="text in translations.kontakt['text' + i].split('\n\n')" :key="text">{{ text }}</p>
            </div>
          </section>
        </div>

        <div v-else>
          <h1>kontakt.title1</h1>
          <h1>kontakt.text1</h1>
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
  name: 'KontaktView',
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
      return this.translations.kontakt ? Object.keys(this.translations.kontakt).length / 2 : 0;
    }
  }
}
</script>

<style>
@import url('https://fonts.cdnfonts.com/css/myriad-pro');

h1 {
  font-weight: 700;
  font-size: 36px;
  line-height: 47px;
}

p {
  padding-bottom: 10px;
  padding-top: 10px;
}

.text {
  background: #00000026;
}

@import url(../../bruciweb.css);
</style>