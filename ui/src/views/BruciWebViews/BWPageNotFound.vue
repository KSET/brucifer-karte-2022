<template>
  <div class="bw-page-container">
    <div class="contents">
      <section>
        <h1 class="bwh1 opa">...OPA!
        </h1>

        <p class="p404">
          Izgleda da tražena stranica ne postoji!
        </p>
        <br>

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
  components: { Footer, RouterElement },
  mounted() {
    
  }
}
</script>
  
<style scoped>
.opa {
  display: block;
  font-size: 128px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 5rem;
  margin-top: 5rem;
}

.p404 {
  font-size: 24px;
  font-weight: 400;
  text-align: center;
  margin-top: 5rem;
}
</style>