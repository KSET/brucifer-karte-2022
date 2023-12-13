<template>
  <div class="page-container">
    <NavbarBweb></NavbarBweb>
    <div class="tlocrt">
      <div class="image">
        <img class="tlocrt-desktop" src="../../assets/tlocrt/tlocrt-desktop.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-tablet" src="../../assets/tlocrt/tlocrt-tablet.svg" alt="Brucifer Tlocrt" />
        <img class="tlocrt-mobile" src="../../assets/tlocrt/tlocrt-mobile.svg" alt="Brucifer Tlocrt" />
      </div>

    </div>
    <Footer></Footer>

  </div>
</template>
  
<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import NavbarBweb from '@/components/NavbarAndFooter/NavbarBweb.vue'

export default {
  name: 'Naslovnica',
  components: { Footer, NavbarBweb },
  props: {
    msg: String
  },
}
</script>
  
<style scoped>
.tlocrt {
  width: 100%;
  min-height: 93vh;
  padding-top: 3rem;
}

.tlocrt-desktop {
  width: 100%;
  height: 100%;
  display: block;
}

.tlocrt-tablet {
  display: none !important;
}

.tlocrt-mobile {
  display: none !important;
}

.image {
  width: 100%;
  height: 100%;
}

.navbar.bw {
  background: #c15476;
}

.navbar.bw::after {
  background: linear-gradient(#c15476, transparent);
}

@media screen and (max-width: 980px) {
  .tlocrt-desktop {
    display: none !important;
  }

  .tlocrt-tablet {
    height: 100%;
    display: block !important;
  }

  .tlocrt-mobile {
    display: none !important;
  }
}

@media screen and (max-width: 550px) {
  .tlocrt-desktop {
    display: none !important;
  }

  .tlocrt-tablet {
    display: none !important;
  }

  .tlocrt-mobile {
    height: 100%;
    display: block !important;
  }

}

@import url(../../bruciweb.css);
</style>
  