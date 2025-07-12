<template>
  <div class="page-container">
    <div v-if="comingSoonVisible" class="page-container" style="min-height: 100vh;">
      <vue-countdown v-if="timerVisible" class="countdown-timer" :time="countdownTime" :transform="transformSlotProps"
        v-slot="{ days, hours, minutes, seconds }">
        <h5 class="countdown-textfield">{{ days }}</h5> :
        <h5 class="countdown-textfield">{{ hours }}</h5> :
        <h5 class="countdown-textfield">{{ minutes }}</h5> :
        <h5 class="countdown-textfield">{{ seconds }}</h5>
      </vue-countdown>

      <SponsorsIcons />
      <div class="homepage">
        <div class="image-container">
          <div class="image-sizer"></div>
          <div class="image-frame"></div>
        </div>
      </div>

      <Footer />

    </div>

    <div v-else>
      <div class="comingSoon">
        <div class="image-container">
          <div class="image-sizer"></div>
          <div class="image-frame"></div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue';
import store from '@/store/visibilityStore';
import SponsorsIcons from '@/components/BruciWeb/SponsorsIcons.vue';

export default {
  name: 'Naslovnica',
  components: { Footer, SponsorsIcons },
  props: {
    msg: String,
  },
  computed: {
    comingSoonVisible() {
      return store.state.COMINGSOON_VISIBILITY == 0;
    },
    timerVisible() {
      return store.state.TIMER_VISIBILITY == 1;
    },
    countdownTime() {
      const timeMS = Date.parse(store.state.TIMER_TIME);
      const seconds = new Date().getTime();
      return timeMS - seconds;
    },
  },
  methods: {
    transformSlotProps(props) {
      const formattedProps = {};

      Object.entries(props).forEach(([key, value]) => {
        formattedProps[key] = value < 10 ? `0${value}` : String(value);
      });

      return formattedProps;
    },
  },
};
</script>


<style>
:root {
  /* BACKGROUND IMAGES
  --background-image -> homepage images
  var(--background-default); -> default images on other pages
  */

  --background-image: url("../../assets/bg/home/bg-desktop.png");
  --background-default: url("../../assets/bg/default/bg-desktop.svg");
  --background-image-aspect-ratio: calc(1080 / 1920);

  /* COLORS */

  --header-color: white;
  --footer-color: white;
  --background--color: white;
  --artist-name-color: #FAFAFB;

  /* COUNTDOWN */

  --countdown-right-offset: 4vw;
  --countdown-font-size: 70px;
  --countdown-top-offset: 32%;

}

.comingSoon {
  background-image: url("../../assets/bg/comingSoon/comingSoon-desktop.png");
  background-repeat: no-repeat;
  background-size: cover;
}

.page-container {
  position: relative;
  background-color: #001723;
  min-height: 93vh;
  flex: 1;
}

.countdown-timer {
  position: absolute;
  font-family: 'CooperBits';
  top: 0;
  width: 100%;
  right: 0;
  padding-right: var(--countdown-right-offset);
  text-align: right;
  font-size: var(--countdown-font-size);
  color: #E0C5FF;
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

.countdown-textfield{
  display: inline;
  margin: 0px -15px;
}

@media screen and (max-width: 980PX) {
  :root {
    --background-image-aspect-ratio: calc(962 / 601);
    --countdown-right-offset: 9vw;
    --countdown-font-size: 8vw;
    --countdown-top-offset: 86.5%;
    --background-image: url("../../assets/bg/home/bg-tablet.png");
  }

  .comingSoon {
    background-image: url("../../assets/bg/comingSoon/comingSoon-tablet.png");
  }

  .page-container {
    background-color: #001723;
  }

  .countdown-timer {
    padding-top: 35%;
  }

  .countdown-textfield{
    display: inline;
    margin: 0px -10px;
  }
}

@media screen and (max-width: 550PX) {
  :root {
    --background-image-aspect-ratio: calc(962 / 601);
    --countdown-right-offset: 9vw;
    --countdown-font-size: 8vw;
    --countdown-top-offset: 86.5%;
    --background-image: url("../../assets/bg/home/bg-mobile.png");
  }

  .comingSoon {
    background-image: url("../../assets/bg/comingSoon/comingSoon-mobitel.png");
  }

  .page-container {
    background-color: #001723;
  }

  .countdown-timer {
    padding-top: 48%;
  }

  .countdown-textfield{
    display: inline;
    margin: 0px -5px;
  }
}



.bw-page-container {
  margin-top: 0;
  flex: 1;

  position: relative;
  background-image: var(--background-default);
  background-repeat: repeat;
  background-size: cover;
  background-color: #0E315B;
  ;
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
