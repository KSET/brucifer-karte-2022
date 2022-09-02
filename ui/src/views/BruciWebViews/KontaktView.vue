<template>
  <div class="page-container">
    <br>
    <p>slay</p>
  </div>
</template>

<script>

export default {
name: 'KontaktView',

}
</script>

<style>
.page-container{ 
  position: absolute;
  height: 100%;
  width: 100%;
    background-image: var(--background-default);;
  background-repeat: no-repeat;
    background-size: cover;
    background-color: #F6BB96;;
}

@media screen and (max-width: 1280px) {
#page-container{  
    background-image: url("../../assets/bg/default/bg-tablet.svg");
  background-repeat: no-repeat;
    background-size: cover;
}
}
</style>