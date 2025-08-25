<template>
  <div class="bw-page-container">
    <div>
      <div class="contents">
        <div v-if="translationsLength != 0">
          <section v-for="i in translationsLength" :key="i">

            <h1>{{ translations.pravilaponasanja["title" + i] }}</h1>
            <div class="text">
              <p class="pText" v-for="text in translations.pravilaponasanja['text' + i].split('\n\n')" :key="text">{{ text
              }}</p>
            </div>
          </section>
        </div>

        <div v-else>
          <h1>pravilaponasanja.title1</h1>
          <h1>pravilaponasanja.text1</h1>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import translationsStore from '@/store/translationsStore';

export default {
  name: 'PravilaPonasanjaView',
  components: { Footer },
  data() {
    return {
    }
  },
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

<style>
@import url('https://fonts.cdnfonts.com/css/myriad-pro');

h1 {

  font-family: 'Ubuntu';
  font-style: normal;
  font-weight: 700;
  font-size: 36px;
  line-height: 47px;

  color: #FFFFFF;
}

p {
  font-family: 'Ubuntu';
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 18px;



  color: #FFFFFF;

  transition: margin-top .3s ease;
  will-change: margin-top;
}

.text {
  background: #00000026;
}

.contents {
  padding-top: 3.5em;
  padding-left: 2.73%;
  padding-right: 4.5%;
  padding-bottom: 4.5%;
}

@media screen and (max-width: 1280px) {
  #page-container {
    background-image: url("../../assets/bg/default/bg-tablet.png");
    background-repeat: no-repeat;
    background-size: cover;
  }
}

@import url(../../bruciweb.css);
</style>