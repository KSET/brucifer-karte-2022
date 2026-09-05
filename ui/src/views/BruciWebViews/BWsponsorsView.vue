<template>
  <div class="bw-page-container">
    <p v-if="error" class="bw-fetch-error">
      Trenutno nije moguće dohvatiti sponzore.
      <button type="button" @click="loadSponsors">Pokušaj ponovno</button>
    </p>
    <BwCardGrid v-else :items="sponsors" variant="sponsors">
      <template #default="{ item }">
        <a :href="item.url" rel="noreferrer noopener" target="_blank">
          <div class="card-image-container">
            <div class="card-image-sizer"></div>
            <img class="card-image-frame" :src="item.image" :alt="item.name ? `${item.name} logo` : 'sponsor'"
              loading="lazy" decoding="async">
          </div>
        </a>
      </template>
    </BwCardGrid>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import BwCardGrid from '@/components/BruciWeb/BwCardGrid.vue'
import sponsorsStore from '@/store/sponsorsStore'

export default {
  name: 'BWSponsors',
  components: { Footer, BwCardGrid },

  mounted() {
    this.loadSponsors()
  },

  computed: {
    sponsors() {
      return sponsorsStore.state.list
    },
    error() {
      return sponsorsStore.state.error
    },
  },

  methods: {
    async loadSponsors() {
      try {
        await sponsorsStore.dispatch('fetchVisible', { force: !!this.error })
      } catch (e) {
      }
    },
  },
}
</script>



