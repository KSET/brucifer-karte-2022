<template>
  <div class="page-container">
    <br>
    <main>
      <div class="contents">


        <h15>ULAZNICE</h15>

          <p>Ulaznice po redovnoj cijeni od 70 kuna u prodaji su od 29. rujna do 12. studenog ili do isteka zaliha.
            Ulaznice se mogu kupiti u KSET-u, glazbenoj knjižari Rockmark te u Dirty Old Shopu.</p>
          <p>Prvog listopada u prodaju kreću ulaznice za brucoše FER-a po cijeni od 40 kuna, a moguće ih je kupiti
            isključivo u KSET-u uz predočenje e-indeksa. Više informacija možete pronaći i na službenoj Facebook
            stranici.</p>
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


      </div>
    </main>

  </div>
</template>

<script>
export default {
  name: 'UlazniceView',
}
</script>

<style>
.page-container {
  background-image: var(--background-default);;
  background-repeat: no-repeat;
  background-size: cover;
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