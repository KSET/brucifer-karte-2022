<template>
  <div class="bw-page-container pravila-page bw-overlay-footer bw-textured">
    <div class="bw-pravila-content">

      <BwBackButton />

      <div class="bw-pravila-head">
        <h2 class="bw-section-title">Pravila ponašanja</h2>
        <h4 class="bw-section-subtitle">Brucifer 2026.</h4>
      </div>

      <div class="bw-panel">
        <template v-if="translationsLength != 0">
          <section v-for="i in translationsLength" :key="i" class="bw-panel-section">
            <h3 class="bw-panel-section-title">{{ translations.pravilaponasanja["title" + i] }}</h3>
            <p class="bw-panel-text" v-for="text in translations.pravilaponasanja['text' + i].split('\n\n')"
              :key="text">
              {{ text }}
            </p>
          </section>
        </template>

        <section v-else class="bw-panel-section">
          <h3 class="bw-panel-section-title">pravilaponasanja.title1</h3>
          <p class="bw-panel-text">pravilaponasanja.text1</p>
        </section>
      </div>

    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwBackButton from '@/components/BruciWeb/BwBackButton.vue'
import translationsStore from '@/store/translationsStore';

export default {
  name: 'PravilaPonasanjaView',
  components: { Footer, BwBackButton },
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

<style scoped>
.pravila-page {
  overflow: visible;
  justify-content: flex-start;
  background-image: none;
  background-color: var(--bw-teal-ink);
  min-height: 100vh;
  min-height: 100dvh;
}

.bw-pravila-content {
  position: relative;
  z-index: 1;
  padding: 0 4vw calc(4vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
}

.bw-pravila-head {
  text-align: center;
  padding-top: clamp(88px, 11vw, 132px);
}

@media screen and (max-width: 980px) {
  .bw-pravila-content {
    padding: 0 6vw calc(6vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }
}

@media screen and (max-width: 550px) {
  .bw-pravila-content {
    padding: 0 6vw calc(8vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }

  .bw-pravila-head :deep(.bw-section-title) {
    font-size: 40px;
  }
}
</style>
