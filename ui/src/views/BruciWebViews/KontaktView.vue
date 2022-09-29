<template>
  <div class="bw-page-container">
    <div class="contents">
      <section>
        <h1 class="bwh1">PR &amp; MARKETING:
        </h1>

        <p>
          Antica Župić
          <br><br>
          <a href="mailto:antica.zupic@kset.org" rel="nofollow noopener" style="color: black">antica.zupic@kset.org</a>
        </p>
        <br>
        <h1 class="bwh1">PRESS:
        </h1>

        <p>
          <a href="mailto:press@kset.org" rel="nofollow noopener" style="color: black">press@kset.org</a>
        </p>

      </section>

    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'

export default {
  name: 'KontaktView',
  components: { Footer },
  mounted() {
    document.getElementById("nav-naslovnica").style.textDecoration = "none";
    document.getElementById("nav-lineup").style.textDecoration = "none";
    document.getElementById("nav-ulaznice").style.textDecoration = "none";
    document.getElementById("nav-sponsors").style.textDecoration = "none";
    document.getElementById("nav-kontakt").style.textDecoration = "underline";

    document.getElementById("nav-naslovnica").style.fontWeight = "400";
    document.getElementById("nav-lineup").style.fontWeight = "400";
    document.getElementById("nav-ulaznice").style.fontWeight = "400";
    document.getElementById("nav-sponsors").style.fontWeight = "400";
    document.getElementById("nav-kontakt").style.fontWeight = "700";
  }
}
</script>

<style>
@import url(../../bruciweb.css);
</style>