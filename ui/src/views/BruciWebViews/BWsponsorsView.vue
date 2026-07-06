<template>
  <div class="bw-page-container">
    <BwCardGrid :items="sponsors" variant="sponsors">
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

  data() {
    return {
      sponsors: [],
    }
  },

  async mounted() {
    const data = await sponsorsStore.dispatch('fetchVisible')
    this.sponsors = data
  },

  computed: {
    loading() {
      return sponsorsStore.state.loading
    },
    error() {
      return sponsorsStore.state.error
    }
  },
}
</script>



