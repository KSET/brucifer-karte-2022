<template>
  <div class="page-container">
    <div v-if="comingSoonVisible" class="page-container homepage-container" style="min-height: 100vh;">
      <vue-countdown v-if="timerVisible" class="countdown-timer" :time="countdownTime" :transform="transformSlotProps"
        v-slot="{ days, hours, minutes, seconds }">
        <h5 class="countdown-textfield">{{ days }}</h5> :
        <h5 class="countdown-textfield">{{ hours }}</h5> :
        <h5 class="countdown-textfield">{{ minutes }}</h5> :
        <h5 class="countdown-textfield">{{ seconds }}</h5>
      </vue-countdown>

      <!-- <SponsorsIcons /> -->
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
      return store.state.COMINGSOON_VISIBILITY === false;
    },
    timerVisible() {
      return store.state.TIMER_VISIBILITY === true;
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
  --background-image -> homepage images (view-local)
  --background-default (default images on other pages) lives in bruciweb.css TOKENS
  */

  --background-image: url("../../assets/bg/home/bg-desktop.png");
  --background-image-aspect-ratio: calc(1081 / 1930);

  /* COUNTDOWN */

  --countdown-right-offset: 10.5%;
  --countdown-font-size: 5vw;
  --countdown-top-offset: 32%;
}

@media screen and (max-width: 980px) {
  :root {
    --background-image-aspect-ratio: calc(1677 / 1048);
    --countdown-right-offset: 17vw;
    --countdown-font-size: 8vw;
    --countdown-top-offset: 25.5%;
    --background-image: url("../../assets/bg/home/bg-tablet.png");
  }
}

@media screen and (max-width: 550px) {
  :root {
    --background-image-aspect-ratio: calc(1563 / 880);
    --countdown-right-offset: 13vw;
    --countdown-font-size: 8vw;
    --countdown-top-offset: 17.5%;
    --background-image: url("../../assets/bg/home/bg-mobile.png");
  }
}
</style>

<style scoped>
.homepage-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.comingSoon {
  background-image: url("../../assets/bg/comingSoon/comingSoon-desktop.png");
  background-repeat: no-repeat;
  background-size: cover;
}

.page-container {
  position: relative;
  background-color: var(--bw-page-color);
  min-height: 93vh;
  flex: 1;
}

.countdown-timer {
  position: absolute;
  font-family: 'Cobya';
  top: 0;
  width: 100%;
  right: 0;
  padding-left: var(--countdown-right-offset);
  text-align: left;
  color: #c5ecff;
  pointer-events: none;
  user-select: none;
  overflow: hidden;
  font-size: var(--countdown-font-size);
}

.countdown-timer h5 {
  font-size: var(--countdown-font-size);
  font-family: 'Cobya';
}

.countdown-timer::before {
  content: "";
  display: block;
  padding-top: var(--countdown-top-offset);
}

.countdown-textfield {
  display: inline;
  margin: 0px -15px;
}

.homepage {
  background-image: var(--background-image);
  background-repeat: no-repeat;
  background-size: cover;
}

@media screen and (max-width: 980px) {
  .comingSoon {
    background-image: url("../../assets/bg/comingSoon/comingSoon-tablet.png");
  }

  .countdown-timer {
    padding-top: 35%;
  }

  .countdown-textfield {
    margin: 0px -10px;
  }
}

@media screen and (max-width: 550px) {
  .comingSoon {
    background-image: url("../../assets/bg/comingSoon/comingSoon-mobitel.png");
  }

  .countdown-timer {
    padding-top: 48%;
  }

  .countdown-textfield {
    margin: 0px -5px;
  }
}
</style>
