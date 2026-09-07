<template>
  <ComingSoon v-if="COMINGSOON_VISIBILITY === true" />
  <Naslovnica v-else />
</template>

<script>
import ComingSoon from '@/views/BruciWebViews/ComingSoonView.vue'
import Naslovnica from '@/views/BruciWebViews/NaslovnicaView.vue'
import visibilityStore from '@/store/visibilityStore.js'

export default {
  name: 'Home',
  components: { ComingSoon, Naslovnica },

  computed: {
    COMINGSOON_VISIBILITY() {
      return visibilityStore.state.COMINGSOON_VISIBILITY;
    },
  },
}
</script>
