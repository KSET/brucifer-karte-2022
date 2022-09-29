<template>
  <div class="bw-page-container">
    <div>
      <div class="contents">
        <section>
          <h1 id="ulaznice">ULAZNICE</h1>

          <p>Ulaznice po redovnoj cijeni od 80 kuna u prodaji su od 14. rujna do 12. studenog ili do isteka zaliha.
            Ulaznice se mogu kupiti u KSET-u te u Dirty Old Shopu.</p>

          <p>Ulaznice za brucoše FER-a po cijeni od 50 kuna kreću u prodaju od 30. rujna, a moguće ih je kupiti
            isključivo u KSET-u uz predočenje e-indeksa. Više informacija možete pronaći i na službenoj Facebook
            stranici Brucošijade FER-a.</p>

          <br>
          <h1 id="pravila-ponašanja">PRAVILA PONAŠANJA</h1>

          <p>Kupljena ulaznica omogućava jedan ulazak u prostor održavanja događaja. Ponovni ulazak nakon izlaska iz
            prostora radi sigurnosnih razloga nije moguć.</p>

          <p>Za sve eventualne ozljede, oštećenja sluha i druge povrede organizator ne snosi odgovornost.</p>

          <p>Organizator ne odgovara za izgubljene ili ukradene stvari.</p>

          <p>Zbog osobne sigurnosti publike, organizator zadržava pravo zabrane ulaska osobama za koje smatra da mogu
            prouzročiti probleme ili ugroziti sigurnost ostalih posjetitelja.</p>

          <p>Kupnjom ulaznice pristajete da kao dio publike budete zvučno i/ili slikovno snimljeni te da snimke mogu
            biti korištene u svakom trenutku u svrhu promocije Brucošijade FER-a.</p>

          <p>S obzirom na epidemiološku situaciju, događaj će se održati prema uputama Civilnog stožera koje će biti
            važeće u trenutku održavanja.</p>

          <p>Ova ulaznica obvezuje posjetitelje na poštivanje kućnog reda u prostoru održavanja događaja.</p>

          <p>Ugodan provod žele vam KSET i SS FER!</p>


        </section>

      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'

export default {
  name: 'UlazniceView',
  components: { Footer },
  mounted() {
    document.getElementById("nav-naslovnica").style.textDecoration = "none";
    document.getElementById("nav-lineup").style.textDecoration = "none";
    document.getElementById("nav-ulaznice").style.textDecoration = "underline";
    document.getElementById("nav-sponsors").style.textDecoration = "none";
    document.getElementById("nav-kontakt").style.textDecoration = "none";

    document.getElementById("nav-naslovnica").style.fontWeight = "400";
    document.getElementById("nav-lineup").style.fontWeight = "400";
    document.getElementById("nav-lineup").style.fontWeight = "400";
    document.getElementById("nav-ulaznice").style.fontWeight = "700";
    document.getElementById("nav-sponsors").style.fontWeight = "400";
    document.getElementById("nav-kontakt").style.fontWeight = "400";
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
  padding-top: 4.5%;
  padding-left: 2.73%;
  padding-right: 4.5%;


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