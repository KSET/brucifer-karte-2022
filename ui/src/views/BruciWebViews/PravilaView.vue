<template>
  <div class="bw-page-container">
    <div class="contents">
      <section>
        <h1 id="opća-pravila-brucošijade-fer-a">OPĆA PRAVILA BRUCOŠIJADE FER-A
        </h1>

        <p>
          <br>
          Kupovinom ulaznice posjetitelj bezuvjetno prihvaća pravila ponašanja mjesta događaja i organizatora.
          <br>

          <br>
          Za sve eventualne ozljede, oštećenja sluha i druge povrede organizator ne snosi odgovornost.
          <br>

          <br>
          Organizator ne odgovara za izgubljene ili ukradene stvari.
          <br>

          <br>
          Zabranjeno je točenje alkohola maloljetnicima i osobama u vidno alkoholiziranom stanju.
          <br>

          <br>
          Zbog osobne sigurnosti publike organizator zadržava pravo zabrane ulaska osobama za koje smatra da mogu
          prouzročiti probleme ili ugroziti sigurnost ostalih posjetitelja.
          <br>

          <br>
          Kupnjom ulaznice pristajete da kao dio publike budete zvučno i/ili slikovno snimljeni te da snimke mogu biti
          korištene u svakom trenutku u svrhu promocije Brucošijade FER-a.
          <br>

          <br>
          Osobe mlađe od 18 godina uz kupljenu ulaznicu i pratnju punoljetne osobe mogu prisustvovati događaju.
          <br>

          <br>
          Kupljena ulaznica omogućava jedan ulazak u prostor održavanja događaja.
          <br>

          <br>
          Ponovni ulazak nakon izlaska iz prostora radi sigurnosnih razloga nije moguć.
          <br>

          <br>
          Jednom kupljena ulaznica ne može se zamijeniti niti vratiti, osim u slučaju otkazivanja cijelog festivala od
          strane organizatora.
          <br>

          <br>
          Važeće su ulaznice kupljene samo na ovlaštenim prodajnim mjestima.
          <br>

          <br>
          Organizator zadržava pravo izmjene programa događaja.
          <br>

          <br>
          Organizator sugerira da u duhu nenasilja, tolerancije i jednakosti pripazite jedni na druge.
          <br>

        </p>
        <br>
        <h1 id="zabranjeno-je">ZABRANJENO JE:
        </h1>

        <p>
          <br>
          Unošenje hrane i pića u prostor događaja.
          <br>

          <br>
          Unošenje narkotika.
          <br>

          <br>
          Unošenje lako zapaljivih goriva, pirotehničkih i eksplozivnih sredstava.
          <br>

          <br>
          Dovođenje kućnih ljubimaca.
          <br>

          <br>
          Unošenje oružja, velikih kišobrana, boca i drugih oštrih predmeta koji mogu ugroziti sigurnost posjetitelja.
          <br>

          <br>
          Unošenje kamera i profesionalnih fotoaparata te tehničke opreme i instrumenata bez dozvole organizatora.
          <br>

        </p>
        <br>
        <h1 id="dozvoljeno-je">DOZVOLJENO JE:
        </h1>

        <p>
          <br>
          Unošenje malih rasklopnih kišobrana.
          <br>

          <br>
          Unošenje manjih ručnih torbi ili ruksaka uz obavezan pregled sadržaja torbi prilikom ulaska.
          <br>

          <br>
          Unošenje mobilnih telefona.
          <br>

          <br>
          Unošenje cigareta i upaljača.
        </p>

      </section>

    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'

export default {
  name: 'PravilaView',
  components: { Footer },
  mounted(){
    document.getElementById("nav-naslovnica").style.textDecoration = "none";
    document.getElementById("nav-lineup").style.textDecoration = "none";
    document.getElementById("nav-ulaznice").style.textDecoration = "none";
    document.getElementById("nav-sponsors").style.textDecoration = "none";
    document.getElementById("nav-kontakt").style.textDecoration = "none";

    document.getElementById("nav-naslovnica").style.fontWeight = "400";
    document.getElementById("nav-lineup").style.fontWeight = "400";
    document.getElementById("nav-ulaznice").style.fontWeight = "400";
    document.getElementById("nav-sponsors").style.fontWeight = "400";
    document.getElementById("nav-kontakt").style.fontWeight = "400";
  }

}
</script>

<style>
@import url(../../bruciweb.css);
</style>