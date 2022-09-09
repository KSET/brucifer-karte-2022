<template>
  <div>
    <Sidebar />
    <div class="admin-page-container">
      <SponsorsAdd />
    </div>
  </div>
</template>

<script>
import SponsorsAdd from '@/components/Sponsors/SponsorsAdd.vue';
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue';

export default {
  name: 'SponsorsAddView',
  components: { SponsorsAdd, SponsorsAdd,Sidebar },
}
</script>

<style lang="scss" scope>
@import '../../assets/scss/Admin-scss/SponsorsAddView.scss';
</style>