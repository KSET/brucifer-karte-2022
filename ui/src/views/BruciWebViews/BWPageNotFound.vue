<template>
  <div class="bw-page-container notfound-page bw-overlay-footer bw-textured">
    <div class="bw-notfound-content">

      <BwBackButton />

      <div class="bw-notfound-inner">
        <img class="bw-notfound-mark" :src="notFoundIcon" alt="" aria-hidden="true" />
        <h1 class="bw-notfound-title bw-section-title">Ne možemo pronaći<br />to što tražiš.</h1>
      </div>

    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwBackButton from '@/components/BruciWeb/BwBackButton.vue'
import notFoundIcon from '@/assets/design-elements/404.svg'

export default {
  name: 'BWPageNotFound',
  components: { Footer, BwBackButton },
  data() {
    return { notFoundIcon }
  },
}
</script>

<style scoped>
.notfound-page {
  overflow: visible;
  justify-content: flex-start;
  background-image: none;
  background-color: var(--bw-wine-ink);
  min-height: 100vh;
  min-height: 100dvh;
}

.bw-notfound-content {
  position: relative;
  z-index: 1;
  flex: 1;
  display: flex;
  padding: 0 4vw calc(4vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
}

/* centers the badge + title in the space left above the overlay footer */
.bw-notfound-inner {
  margin: auto;
  text-align: center;
}

.bw-notfound-mark {
  display: block;
  width: clamp(140px, 22vw, 276px);
  height: auto;
  margin: 0 auto clamp(24px, 3vw, 40px);
}

.bw-notfound-title.bw-notfound-title {
  font-size: clamp(32px, 5vw, 64px);
  text-transform: none;
  margin: 0;
}

@media screen and (max-width: 980px) {
  .bw-notfound-content {
    padding: 0 6vw calc(6vw + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }
}

@media screen and (max-width: 550px) {
  .bw-notfound-content {
    padding: 96px 6vw calc(64px + var(--bw-footer-measured-h, var(--bw-footer-total-h)));
  }

  .bw-notfound-title.bw-notfound-title {
    font-size: 28px;
  }
}
</style>
