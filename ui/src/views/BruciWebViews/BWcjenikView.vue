<template>
  <div class="bw-page-container">
    <div class="contents">
      <section>
        <h1 class="bwh1">CJENIK PIĆA
        </h1>
        <div class="cjenik-table">
          <div class="cjenik-title" v-for="tag in tags" :key="tag.id">
            <h1>{{ tag }}</h1>
            <h1>KOLIČINA</h1>
            <h1>CIJENA</h1>

            <div class="cjenik-items" v-for="artikl in artikli[tag]" :key="artikl.id">
              <h1>{{ artikl.name }}</h1>
              <h1>{{ artikl.volume }} L</h1>
              <h1>{{ artikl.priceHRK }} kn</h1>
              <h1>{{ artikl.priceEUR }} €</h1>
            </div>
          </div>

        </div>
        <p class="disclamer-text">Prodaju pića vrši ElektroStudent d.o.o. (OIB: 18333034190) sa
          sjedištem u Unskoj 3, 10 000 Zagreb čiji je vlasnik udruga SS FER. Zabranjeno usluživanje i konzumiranje
          alkoholnih pića mlađima od 18 godina!
          Porez je uračunat u cijenu.</p>

      </section>
    </div>
    <Footer></Footer>
  </div>
</template>
  
<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import axios from 'axios';

export default {
  name: 'KontaktView',
  components: { Footer },
  mounted() {
    this.created();
  },
  data() {
    return {
      showContactForm: true,
      showHid: false,
      tbodyHigh: false,

      tags: ["SOK", "PIVO", "DOLJEVI", "ALKOHOL", "OSTALO"],
      artikli: [],

    }
  },
  methods: {
    async created() {
      this.artikli = [];
      this.tags.forEach(async element => {
        console.log(element)
        const resp = await axios.get(process.env.VUE_APP_BASE_URL + '/cjenik/?ordering=order&search=' + element + '&search_fields=tag',)
        if (resp.data.length != 0) {
          this.artikli[element] = resp.data
        }
      });
      console.log(this.artikli)

    },
  }
}
</script>
  
<style>
.cjenik-table {
  width: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  height: 100%;
  overflow: auto;
  padding: 10px;
  padding-top: 0px;
  padding-right: 0px;


}

.cjenik-title {
  display: grid;
  grid-template-columns: 40% 28% 32%;
}

.cjenik-title h1 {
  color: white;
  font-size: 24px;
  font-weight: 700;
  padding: 20px;
  padding-left: 10px;
  padding-top: 50px;
  padding-bottom: 20px;


}

.cjenik-items h1 {
  font-weight: 400;
  padding: 10px;

}

.cjenik-items {
  display: grid;
  grid-template-columns: 40% 28% 15% auto;
  grid-column: span 3;

}

.disclamer-text {
  font-size: 20px;
  font-weight: 400;
}

@media screen and (max-width: 980px) {
  .cjenik-title h1 {
    font-size: 24px;
  }
}

@media screen and (max-width: 980px) {
  .cjenik-title h1 {
    font-size: 14px;
  }

  .disclamer-text {
    font-size: 14px;

  }
}

@import url(../../bruciweb.css);
</style>