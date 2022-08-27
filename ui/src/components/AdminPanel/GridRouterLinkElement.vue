<template>
  <div class="grid-element">
    <router-link :to=link>
      {{name}}
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'GridRouterLinkElement',
  props: [
    'name',
    'link',
  ]
}
</script>

<style scoped>
.grid-element {
  display: block;
  color: white;

  text-align: center;
        background: rgba(0, 0, 0, .3);
        border-radius: 18px;
        padding: 30px;
    }
</style>
