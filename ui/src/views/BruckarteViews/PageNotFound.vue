<template>
  <section style="padding:20%">
    <h1>404 Page not found
    </h1>

    <p>
      Izgleda da si pronašao stranicu koja ne postoji
    </p>
    <br>
    <RouterElement class="overlay-element" :name="'Naslovnica'" :link="'/admin/'"></RouterElement>

  </section>

</template>
  
<script>
import RouterElement from '@/components/AdminPanel/RouterElement.vue'


export default {
  name: 'KontaktView',
  components: { RouterElement }

}
</script>