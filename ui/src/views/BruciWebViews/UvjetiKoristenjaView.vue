<template>
    <div class="bw-page-container">
      <div>
        <div class="contents">
          <div v-if="translationsLength != 0">
            <section v-for="i in translationsLength" :key="i">
  
              <h1>{{ translations.uvjetikoristenja["title" + i] }}</h1>
              <div class="text">
                <p class="pText" v-for="text in translations.uvjetikoristenja['text' + i].split('\n\n')" :key="text">{{ text
                }}</p>
              </div>
            </section>
          </div>
  
          <div v-else>
            <h1>uvjetikoristenja.title1</h1>
            <h1>uvjetikoristenja.text1</h1>
          </div>
        </div>
      </div>
      <Footer></Footer>
    </div>
  </template>
  
  <script>
  import Footer from '@/components/NavbarAndFooter/Footer.vue'
  import translationsStore from '@/store/translationsStore';
  import visibilityStore from '@/store/visibilityStore';

  export default {
    name: 'uvjetikoristenjaView',
    components: { Footer },
    data() {
      return {
      }
    },
    mounted() {
    },
    computed: {
      translations() {
        return translationsStore.state.translations;
      },
      translationsLength() {
        return this.translations.uvjetikoristenja ? Object.keys(this.translations.uvjetikoristenja).length / 2 : 0;
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
  
  @media screen and (max-width: 1280px) {
    #page-container {
      background-image: url("../../assets/bg/default/bg-tablet.png");
      background-repeat: no-repeat;
      background-size: cover;
    }
  }
  
  @import url(../../bruciweb.css);
  </style>