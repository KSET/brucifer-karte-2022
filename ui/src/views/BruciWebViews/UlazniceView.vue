<template>
  <div class="bw-page-container">
    <div>
      <div class="contents">

        <!-- Pretix Widget -->
        <pretix-widget event="https://karte.kset.org/kset/brucosijada/" data-domain="karte.kset.org"
          data-embed="true"></pretix-widget>
        <noscript>
          <div class="pretix-widget">
            <div class="pretix-widget-info-message">
              JavaScript is disabled in your browser. To access our ticket shop without JavaScript, please
              <a target="_blank" rel="noopener" href="https://karte.kset.org/kset/brucosijada/">click here</a>.
            </div>
          </div>
        </noscript>

        <div v-if="translationsLength != 0">
          <section v-for="i in translationsLength" :key="i">
            <h1>{{ translations.ulaznice["title" + i] }}</h1>
            <div class="text">
              <p class="pText" v-for="text in translations.ulaznice['text' + i].split('\n\n')" :key="text">{{ text }}
              </p>
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
import translationsStore from '@/store/translationsStore'

export default {
  name: 'UlazniceView',
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
      return this.translations.ulaznice ? Object.keys(this.translations.ulaznice).length / 2 : 0;
    }
  },
  mounted() {
    // Dynamically load the Pretix widget JavaScript after Vue has mounted
    const script = document.createElement('script');
    script.src = 'https://karte.kset.org/widget/v1.en.js';
    script.async = true;
    script.crossOrigin = 'anonymous';
    document.body.appendChild(script);
  }
}
</script>


<style>
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

.pretix-widget {
  background-color: white;
}

@import url(../../bruciweb.css);
</style>