<template>
  <div class="bw-page-container">
    <div class="satnica">
      <div class="image">
        <BwResponsiveImage :desktop-src="satnicaDesktop" :tablet-src="satnicaTablet" :mobile-src="satnicaMobile"
          alt="Brucifer Satnica" />
      </div>

    </div>
    <Footer></Footer>

  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwResponsiveImage from '@/components/BruciWeb/BwResponsiveImage.vue'
import satnicaDesktop from '@/assets/satnica/satnica-desktop.svg'
import satnicaTablet from '@/assets/satnica/satnica-tablet.svg'
import satnicaMobile from '@/assets/satnica/satnica-mobile.svg'

export default {
  name: 'SatnicaView',
  components: { Footer, BwResponsiveImage },
  props: {
    msg: String
  },
  data() {
    return { satnicaDesktop, satnicaTablet, satnicaMobile }
  },
}
</script>

<style scoped>
.satnica {
  width: 100%;
  min-height: 93vh;
}

.image {
  width: 100%;
  height: 100%;
}

@media screen and (max-width: 550px) {
  .image :deep(.bw-responsive-image) {
    margin-top: 10px;
  }
}
</style>
  