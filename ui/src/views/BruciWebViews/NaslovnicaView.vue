<template>
  <div class="page-container">
    <vue-countdown class="countdown-timer" :time=this.time :transform="transformSlotProps"
      v-slot="{ days, hours, minutes, seconds }">
      {{ days }}:{{ hours }}:{{ minutes }}:{{ seconds }}
    </vue-countdown>
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
      time: '',
    }

  },
  mounted() {
    var seconds = new Date().getTime() / 1000;
    this.time = (1668283200 - (seconds)) * 1000;
  },
  methods: {
    transformSlotProps(props) {
      const formattedProps = {};

      Object.entries(props).forEach(([key, value]) => {
        formattedProps[key] = value < 10 ? `0${value}` : String(value);
      });

      return formattedProps;
    }
  }
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

  /* COUNTDOWN */

  --countdown-right-offset: 7vw;
  --countdown-font-size: 8.5vw;
  --countdown-top-offset: 16%;

}

@media screen and (max-width: 980PX) {
  :root {
    --background-image-aspect-ratio: calc(962 / 601);
    --countdown-right-offset: 9vw;
    --countdown-font-size: 8vw;
    --countdown-top-offset: 86.5%;
    --background-image: url("../../assets/bg/home/bg-tablet.svg");
  }
}

.page-container {
  position: relative;
  background-color: #F6BB96;
  min-height: 93vh;
  flex: 1;
}

.bw-page-container {
  margin-top: 0;
  flex: 1;

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

.countdown-timer {
  position: absolute;
  font-family: 'Antonio';
  top: 0;
  width: 100%;
  right: 0;
  padding-right: var(--countdown-right-offset);
  text-align: right;
  font-size: var(--countdown-font-size);
  color: white;
  text-shadow: .062em 0 black;
  pointer-events: none;
  user-select: none;
  padding-bottom: min(calc(var(--background-image-aspect-ratio) * 100%),
      calc(100vh - var(--topbar-height) - var(--footer-height) - var(--countdown-font-size) - var(--countdown-top-offset)));
  overflow: hidden;
}

.countdown-timer::before {
  content: "";
  display: block;
  padding-top: var(--countdown-top-offset);
}

@import url(../../bruciweb.css);
</style>
