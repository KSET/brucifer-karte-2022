<template>
    <div class="bw-page-container">
      <div class="contents">
        <section>
          <h1 class="bwh1">CJENIK PIĆA
          </h1>
          <div class="cjenik-table">
            <h1>adas</h1>
          </div>
          <p style="font-size: 20px; font-weight: 400;">Prodaju pića vrši ElektroStudent d.o.o. (OIB: 18333034190) sa sjedištem u Unskoj 3, 10 000 Zagreb čiji je vlasnik udruga SS FER.  Zabranjeno usluživanje i konzumiranje
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
    mounted(){
        this.created();
    },
    data() {
    return {
      showContactForm: true,
      showHid: false,
      tbodyHigh: false,

      tags: ["Bezalkoholna pića", "Pivo", "Vino", "Žestoka pića", "Ostalo"],
      artikli: [],

    }
  },
    methods: {
      async created() {
      this.artikli=[];
      this.tags.forEach(async element => {
        console.log(element)
        const resp = await axios.get(process.env.VUE_APP_BASE_URL + '/cjenik/?search=' + element + '&search_fields=tag',)
        if(resp.data.length!=0){
          resp.data.forEach(elementy => {
            console.log(this.artikli)
            this.artikli[element]=elementy
          });
        }
      });
      console.log(this.artikli)

    },
    }
  }
  </script>
  
  <style>
  .cjenik-table{
    width:100%;
    background-color: rgba(0, 0, 0, 0.3);
    height: 30rem;
    overflow: auto;
    padding: 20px;
  }
  @import url(../../bruciweb.css);
  </style>