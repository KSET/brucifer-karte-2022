<template>
    <div class="page-container">
      <div class="satnica">
        <div class="image-container">
          <div class="image-sizer"></div>
          <div class="image-frame"></div>
        </div>
  
      </div>
      <Footer></Footer>
  
    </div>
  </template>
  
  <script>
  import Footer from '@/components/NavbarAndFooter/Footer.vue'
  
  export default {
    name: 'Naslovnica',
    components: { Footer },
    props: {
      msg: String
    },
    }
  </script>
  
  <style>
  .satnica {
    background-image: url("../../assets/satnica/satnica-desktop.svg");
    background-repeat: no-repeat;
    background-size: cover;
  }

  @media screen and (max-width: 980px) {
    .satnica {
    background-image: url("../../assets/satnica/satnica-tablet.svg");

  }
}
  

  @import url(../../bruciweb.css);
  </style>
  