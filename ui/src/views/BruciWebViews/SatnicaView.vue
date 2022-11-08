<template>
    <div class="page-container">
    <NavbarBweb></NavbarBweb>
      <div class="satnica">
          <div class="image">
            <img class="satnica-desktop" src="../../assets/satnica/satnica-desktop.svg" alt="Brucifer Tlocrt"/>
            <img class="satnica-tablet" src="../../assets/satnica/satnica-tablet.svg" alt="Brucifer Tlocrt" />
          </div>
  
      </div>
      <Footer></Footer>
  
    </div>
  </template>
  
  <script>
  import Footer from '@/components/NavbarAndFooter/Footer.vue'
  import NavbarBweb from '@/components/NavbarAndFooter/NavbarBweb.vue'

  export default {
    name: 'Naslovnica',
    components: { Footer, NavbarBweb },
    props: {
      msg: String
    },
    }
  </script>
  
  <style>
  .satnica {
    width: 100%;
    min-height: 91vh;
    padding-top: 3rem;
  }

  .satnica-desktop {
    width: 100%;
    height: 100%;
    display: block;
  }

  .satnica-tablet {
    display: none !important;
  }

  .image {
    width: 100%;
    height: 100%;
  }

  .navbar.bw {
    background: #c15476;
  }

  .navbar.bw::after {
    background: linear-gradient(#c15476, transparent);
  }

  @media screen and (max-width: 980px) {
    .satnica-desktop {
      display: none !important;
    }

    .satnica-tablet {
      height: 100%;
      display: block !important;
    }

}
  

  @import url(../../bruciweb.css);
  </style>
  