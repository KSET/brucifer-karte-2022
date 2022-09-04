<template>
<div class="page-container">
<img src="../../assets/bg/home/bg-desktop.svg">
<Footer></Footer>
</div>
</template>

<script>
  import Footer from '../../components/NavbarAndFooter/Footer.vue'

export default {
name: 'Naslovnica',
conponenets:  {Footer},
  props: {
    msg: String
  },
  data(){
    return{
      w:'',
    }
    
  },
  mounted(){
    this.w=window.innerWidth;
    console.log(this.w>1280);
  },
}
</script>

<style>
:root{
  /* BACKGROUND IMAGES
  --background-image -> homepage images
  var(--background-default); -> default images on other pages
  */

  --background-image : url("../../assets/bg/home/bg-desktop.svg");
  --background-default : url("../../assets/bg/default/bg-desktop.svg");

  /* COLORS */

  --header-color: white;
  --footer-color: white;
  --background--color: white;
  --artist-name-color: #FAFAFB;

}
@media screen and (max-width: 1280px) {
:root{  
  --background-home-image : url("../../assets/bg/home/bg-tablet.svg");
}}
.page-containter{  
  position: relative;
    background-image: --background-image;
    background-repeat: no-repeat;
    background-size: cover;
    background-color: #F6BB96;
}

img{padding-bottom: 2.5rem;}

</style>