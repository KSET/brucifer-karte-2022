<template>
  <div class="bw-page-container">
    <div>
      <div class="contents">
        <div v-if="length != 0">
          <section v-for="i in length" :key="i">

            <h1>{{ translations.ulaznice["title" + i] }}</h1>
            <p v-for="text in translations.ulaznice['text' + i].split('\n\n')" :key="text">{{ text }}</p>

          </section>
        </div>

        <div v-else>
          <h1>ulaznice.title1</h1>
          <h1>ulaznice.text1</h1>
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
  name: 'UlazniceView',
  components: { Footer },
  data() {
    return {
      translations: translationsStore.state.translations,
      length: '0',
    }
  },
  created() {
    if (this.translations.ulaznice) {
      this.length = Object.keys(this.translations.ulaznice).length / 2
    }
  }
}
</script>

<style>
@import url('https://fonts.cdnfonts.com/css/myriad-pro');

h1 {

  font-family: 'Antonio';
  font-style: normal;
  font-weight: 700;
  font-size: 36px;
  line-height: 47px;

  color: #000000;
}

p {
  font-family: 'Myriad Pro';
  font-style: normal;
  font-weight: 300;
  font-size: 20px;
  line-height: 18px;

  color: #000000;

  transition: margin-top .3s ease;
  will-change: margin-top;
}

.contents {
  padding-top: 3.5em;
  padding-left: 2.73%;
  padding-right: 4.5%;
  padding-bottom: 4.5%;



}

@media screen and (max-width: 1280px) {
  #page-container {
    background-image: url("../../assets/bg/default/bg-tablet.svg");
    background-repeat: no-repeat;
    background-size: cover;
  }
}

@import url(../../bruciweb.css);
</style>