<template>
  <div class="bw-page-container ulaznice-page bw-overlay-footer bw-textured">
    <div class="bw-ulaznice-content">

      <BwBackButton />

      <div class="bw-ulaznice-head">
        <h2 class="bw-section-title">Ulaznice</h2>
        <h4 class="bw-section-subtitle">Brucifer 2026.</h4>
      </div>

      <div class="bw-panel">
        <!-- Pretix Widget -->
        <pretix-widget event="https://karte.kset.org/kset/43-brucifer/"></pretix-widget>
        <noscript>
          <div class="pretix-widget">
            <div class="pretix-widget-info-message">
              JavaScript is disabled in your browser. To access our ticket shop without JavaScript, please
              <a target="_blank" rel="noopener" href="https://karte.kset.org/kset/43-brucifer/">click here</a>.
            </div>
          </div>
        </noscript>

        <template v-if="translationsLength != 0">
          <section v-for="i in translationsLength" :key="i" class="bw-panel-section">
            <h3 class="bw-panel-section-title">{{ translations.ulaznice["title" + i] }}</h3>
            <p class="bw-panel-text" v-for="text in translations.ulaznice['text' + i].split('\n\n')" :key="text">
              {{ text }}
            </p>
          </section>
        </template>

        <section v-else class="bw-panel-section">
          <h3 class="bw-panel-section-title">ulaznice.title1</h3>
          <p class="bw-panel-text">ulaznice.text1</p>
        </section>
      </div>

    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwBackButton from '@/components/BruciWeb/BwBackButton.vue'
import translationsStore from '@/store/translationsStore'

export default {
  name: 'UlazniceView',
  components: { Footer, BwBackButton },
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
    script.src = 'https://karte.kset.org/widget/v2.en.js';
    script.async = true;
    script.crossOrigin = 'anonymous';
    document.body.appendChild(script);
  }
}
</script>

<style>
.pretix-widget {
  background-color: white;
}
</style>

<style scoped>
.ulaznice-page {
  overflow: visible;
  justify-content: flex-start;
  background-image: none;
  background-color: var(--bw-teal-ink);
  min-height: 100vh;
  min-height: 100dvh;
}

.bw-ulaznice-content {
  position: relative;
  z-index: 1;
  padding: 0 4vw calc(4vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
}

.bw-ulaznice-head {
  text-align: center;
  padding-top: clamp(88px, 11vw, 132px);
}

.bw-panel :deep(.bw-panel-section:last-child .bw-panel-text:last-child) {
  text-align: center;
  font-weight: 600;
  padding-top: clamp(28px, 3vw, 40px);
}

@media screen and (max-width: 980px) {
  .bw-ulaznice-content {
    padding: 0 6vw calc(6vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }
}

@media screen and (max-width: 550px) {
  .bw-ulaznice-content {
    padding: 0 6vw calc(8vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }
}
</style>
