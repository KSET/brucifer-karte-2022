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
    if ((this.$route.params.pathMatch[0]) == "admin") {
      this.$router.push({ name: 'PageNotFound' });

    }

  }
}
</script>
  
<style>
@import url(../../bruciweb.css);

.opa {
  font-size: 128px !important;
  font-weight: 700 !important;
  text-align: center;
  margin-bottom: 5rem !important;
  margin-top: 5rem !important;

}

.p404 {
  font-size: 24px !important;
  font-weight: 400;
  text-align: center;
  margin-top: 5rem !important;
}
</style>