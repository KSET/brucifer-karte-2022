<template>
  <div class="bw-page-container">
    <div v-if="this.cjenikVisible == '1'" class="contents">
      <section>
        <h1 class="bwh1" style="display:inline-block; vertical-align: middle; margin-top: 2rem;">CJENIK PIĆA
        </h1>
        <div lass="aircash-block">
          <div class="aircash">
            <h1 class="bwh1 cj" style="color: white;display:inline-block; vertical-align: middle;">Plaćaj 20% jeftinije uz
              Aircash!
            </h1>

            <a href="https://aircash.page.link/fer-download" class="aircash-btn" rel="noreferrer noopener"
              target="_blank">Preuzmi aircash</a>

            <img src="@/assets/icons/aircash-logo.svg">
          </div>
        </div>
        <div class="cjenik-table">
          <div class="cjenik-title" v-for="tag in tags" :key="tag.id">
            <h1>{{ tag }}</h1>
            <h1>KOLIČINA</h1>
            <h1>CIJENA</h1>

            <div class="cjenik-items" v-for="artikl in artikli[tag]" :key="artikl.id">
              <h1>{{ artikl.name }}</h1>
              <h1 v-if="artikl.tag != 'OSTALO'">{{ artikl.volume }} L</h1>
              <h1 v-else>{{ artikl.volume }}</h1>

              <h1>{{ artikl.priceHRK }} kn</h1>
              <h1>{{ artikl.priceEUR }} €</h1>
            </div>
          </div>

        </div>
        <p class="disclamer-text">Prodaju pića vrši ElektroStudent d.o.o. (OIB: 18333034190) sa sjedištem u Unskoj 3, 10
          000 Zagreb čiji je vlasnik udruga SS FER. Zabranjeno usluživanje i konzumiranje
          alkoholnih pića mlađima od 18 godina!
          Porez je uračunat u cijenu. Cijene izražene u eurima informativnog su karaktera. Konverzija u eure odrađena je
          prema tečaju 1 EUR = 7,53450 HRK. Plaćanje je moguće samo u hrvatskim kunama gotovinom ili putem aplikacije
          Aircash.</p>

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

      cjenikVisible: 1,

    }
  },
  methods: {
    async created() {
      axios.get(process.env.VUE_APP_BASE_URL + '/cjenik/31/',)
        .then(response => {
          var cjenik = response.data.name;
          if (cjenik == 0) {
            this.cjenikVisible = 0;
          } else {
            this.cjenikVisible = 1;
          }
        })
      if (this.cjenikVisible == 1) {
        this.artikli = [];
        this.tags.forEach(async element => {
          const resp = await axios.get(process.env.VUE_APP_BASE_URL + '/cjenik/?ordering=order&search=' + element + '&search_fields=tag',)
          if (resp.data.length != 0) {
            this.artikli[element] = resp.data
          }
        });
      }
    },
  }
}
</script>
  
<style>
.aircash {
  position: absolute;
  display: grid;
  grid-template-columns: 50% 30% 20%;
  right: 0px;
  margin-right: 4.5%;
  left: 15%;
  top: 3.8%;
  vertical-align: middle;
  background-color: rgba(0, 0, 0, 0.3);
  align-items: center;
  justify-items: center;
}

.aircash-block {
  display: inline-block !important;
}

.cjenik-table {
  width: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  height: 100%;
  overflow: auto;
  padding: 10px;
  padding-top: 0px;
  padding-right: 0px;
}

.aircash-btn {
  width: 186px;
  height: 40px;

  padding: 11px;

  font-family: 'Antonio';
  font-style: normal;
  font-weight: 400;
  font-size: 15px;
  line-height: 15px;
  /* identical to box height, or 100% */

  color: black;
  vertical-align: middle;
  display: flex;
  align-items: center;
  text-align: center;

  display: inline-block;
  background: #FFFFFF;
  border-radius: 6px;
  border: 0px;
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

  .aircash {
    grid-template-columns: 60% 20% 20%;
  }

  .aircash {
    left: 3%;
    top: 6%;
  }

  .aircash-block {
    display: block;
  }

  .cjenik-table {
    margin-top: 100px;
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

@media screen and (max-width: 550px) {
  .aircash-btn {
    width: 155px;
    height: 33px;
  }

  .aircash {
    font-size: 14px;
    grid-template-columns: 45% 33% 20%;
    top: 5.5%;
  }
  .bwh1.cj{
    font-size: 15px;
    width: 70%;
  }
}

@import url(../../bruciweb.css);
</style>