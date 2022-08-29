<template>
<div class="page-container">
<img src="../../assets/bg/home/bg-desktop.svg">
</div>
</template>

<script>
export default {
name: 'Naslovnica',
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
.page-containter{  
    background-image: url("../../assets/bg/home/bg-desktop.svg");
    background-repeat: no-repeat;
    background-size: cover;
    background-color: #F6BB96;;
}

@media screen and (max-width: 1280px) {
.page-containter{  
    background-image: url("../../assets/bg/home/bg-tablet.svg");
  background-repeat: no-repeat;
    background-size: cover;
}
}
</style>