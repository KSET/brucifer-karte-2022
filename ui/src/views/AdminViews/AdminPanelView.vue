<template>
  <div id="adminPanel">
      <Sidebar></Sidebar>
  </div>
</template>

<script>
import GridRouterLink from '@/components/AdminPanel/GridRouterLink.vue';
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

export default {
  components: { Sidebar }
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