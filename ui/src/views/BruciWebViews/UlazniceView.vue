<template>
  <div class="bw-page-container">
    <div>
      <div class="contents">
        <div v-if="length != 0">
          <section v-for="i in length" :key="i">

            <h1>{{ translations.ulaznice["title" + i] }}</h1>
            <div class="text">
              <p class="pText" v-for="text in translations.ulaznice['text' + i].split('\n\n')" :key="text">{{ text }}</p>
            </div>
          </section>
        </div>

        <div v-else>
          <h1>ulaznice.title1</h1>
          <h1>ulaznice.text1</h1>
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
  name: 'UlazniceView',
  components: { Footer },
  data() {
    return {
      length: '0',
    }
  },
  computed: {
    translations() {
      return translationsStore.state.translations;
    }
  },
  created() {
    if (this.translations.ulaznice) {
      this.length = Object.keys(this.translations.ulaznice).length / 2
    }
  }
}
</script>

<style >
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