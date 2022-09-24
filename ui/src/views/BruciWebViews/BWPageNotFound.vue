<template>
    <div class="bw-page-container">
      <div class="contents">
        <section>
          <h1 class="bwh1">404 Page not found
          </h1>
  
          <p>
           Izgleda da si pronašao stranicu koja ne postoji
          </p>
          <br>
          <RouterElement class="overlay-element" :name="'Naslovnica'" :link="'/'"></RouterElement>
  
        </section>
  
      </div>
      <Footer></Footer>
    </div>
  </template>
  
  <script>
import RouterElement from '@/components/AdminPanel/RouterElement.vue'

  import Footer from '@/components/NavbarAndFooter/Footer.vue'
import { onMounted } from 'vue';
  
  export default {
    name: 'KontaktView',
    components: { Footer,RouterElement },
    mounted(){
        if((this.$route.params.pathMatch[0])=="bruckarte"){
            this.$router.push({ name: 'PageNotFound' });

        }
  
  }}
  </script>
  
  <style>
  @import url(../../bruciweb.css);
  
  
  </style>