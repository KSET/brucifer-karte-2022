<template>
  <GridRouterLink></GridRouterLink>
</template>

<script>
import GridRouterLink from '@/components/AdminPanel/GridRouterLink.vue';
    export default {
        components:{ GridRouterLink, GridRouterLink }
    }
    </script>

<style>

.admin-page-container {
    position:relative;
  margin-left: 26%; /* Same as the width of the sidenav */
  margin-right: 1%;
  font-size: 28px; /* Increased text to enable scrolling */
  padding: 10px 10px;

}
</style>