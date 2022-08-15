<template>
    <div id="adminPanel">
      <GridRouterLink></GridRouterLink>

      </div>
</template>

<script>
import GridRouterLink from '@/components/AdminPanel/GridRouterLink.vue';
export default {
    components:{GridRouterLink}
}
</script>

<style>
.wrapper {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  grid-auto-rows: minmax(100px, auto);
}
</style>