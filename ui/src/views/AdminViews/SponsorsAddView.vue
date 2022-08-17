<template>
  <div>
    <SponsorsAdd />
  </div>
</template>

<script>
import SponsorsAdd from '@/components/Sponsors/SponsorsAdd.vue';
export default {
    name: 'SponsorsAddView',
    components: { SponsorsAdd, SponsorsAdd },
}
</script>

<style lang="scss" scope>
@import '../../assets/scss/Admin-scss/SponsorsAddView.scss';
</style>