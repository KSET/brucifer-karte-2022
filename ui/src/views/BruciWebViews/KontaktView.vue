<template>
  <div id="kontakt">
    <br>
    <p>slay</p>
    <footer></footer>
  </div>
</template>

<script>
import Footer from '../../components/Footer.vue';

export default {
name: 'KontaktView',
Footer
}
</script>

<style>

footery {
    position: relative;
    display: flex;
    align-items: center;
    height: 110px;
    padding: 0 calc(var(--padding-percent) * 1vw);
    color: var(--bruc-white);
    background-color: var(--bruc-pink);
}
h6{
        color:white;
    }
</style>