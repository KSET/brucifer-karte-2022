<template>
  <div class="page-container">
    <div class="homepage">
      <div class="image-container">
        <div class="image-sizer"></div>
        <div class="image-frame"></div>
      </div>

    </div>
    <Footer></Footer>

  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'

export default {
  name: 'Naslovnica',
  components: { Footer },
  props: {
    msg: String
  },
  data() {
    return {
      w: '',
    }

  },
  mounted() {
  },
}
</script>

<style>
:root {
  /* BACKGROUND IMAGES
  --background-image -> homepage images
  var(--background-default); -> default images on other pages
  */

  --background-image: url("../../assets/bg/home/bg-desktop.svg");
  --background-default: url("../../assets/bg/default/bg-desktop.svg");
  --background-image-aspect-ratio: calc(1080 / 1920);

  /* COLORS */

  --header-color: white;
  --footer-color: white;
  --background--color: white;
  --artist-name-color: #FAFAFB;

}

@media screen and (max-width: 1280px) {
  :root {
    --background-image-aspect-ratio: calc(962 / 601);

    --background-image: url("../../assets/bg/home/bg-tablet.svg");
  }
}

.page-container {
  position: relative;
  background-color: #F6BB96;
  min-height: 93vh;
}

.bw-page-container {
  position: relative;
  background-image: var(--background-default);
  background-repeat: repeat;
  background-size: cover;
  background-color: #F6BB96;
  min-height: 93vh;
  padding-bottom: 60px;
}


.homepage {
  /* Footer height */
  background-image: var(--background-image);
  background-repeat: no-repeat;
  background-size: cover;

}

@import url(../../bruciweb.css);
</style>