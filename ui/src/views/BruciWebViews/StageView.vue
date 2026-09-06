<template>
  <div class="bw-page-container stage-page bw-overlay-footer"
    :class="{ 'stage-page--no-sponsors': SPONSORS_VISIBILITY !== true }">
    <BwStickyHeader />
    <BwHero />
    <BwBreakMarquee />
    <BwGallery />
    <template v-if="LINEUP_VISIBILITY === true">
      <BwBreakMarquee />
      <BwLineup />
    </template>
    <template v-if="SPONSORS_VISIBILITY === true">
      <BwBreakMarquee />
      <BwSponsors />
    </template>
    <Footer />
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwStickyHeader from '@/components/BruciWeb/BwStickyHeader.vue'
import BwHero from '@/components/BruciWeb/BwHero.vue'
import BwBreakMarquee from '@/components/BruciWeb/BwBreakMarquee.vue'
import BwGallery from '@/components/BruciWeb/BwGallery.vue'
import BwLineup from '@/components/BruciWeb/BwLineup.vue'
import BwSponsors from '@/components/BruciWeb/BwSponsors.vue'
import visibilityStore from '@/store/visibilityStore.js'

export default {
  name: 'Stage',
  components: { Footer, BwStickyHeader, BwHero, BwBreakMarquee, BwGallery, BwLineup, BwSponsors },

  computed: {
    LINEUP_VISIBILITY() {
      return visibilityStore.state.LINEUP_VISIBILITY;
    },
    SPONSORS_VISIBILITY() {
      return visibilityStore.state.SPONSORS_VISIBILITY;
    },
  },
}
</script>

<style scoped>
.stage-page {
  justify-content: flex-start;
  background-image: none;
  background-color: var(--bw-ink);

  min-height: 100vh;
  min-height: 100dvh;
}

.stage-page--no-sponsors {
  padding-bottom: var(--bw-footer-measured-h, var(--bw-footer-h));
}
</style>
