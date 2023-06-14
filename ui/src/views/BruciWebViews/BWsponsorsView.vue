<template>
  <div class="bw-page-container">
    <div class="sponsors" v-if="SPONSORS_VISIBILITY == 1">
      <div v-for="sponsor in sponsors" :key="sponsor.id" class="sponsor">
        <a v-bind:href="sponsor.url" rel="noreferrer noopener" target="_blank">
          <div class="image-container">
            <div class="image-sizer2"></div>
            <img class="image-frame2" v-bind:src="sponsor.image">
          </div>
        </a>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/NavbarAndFooter/Footer.vue'
import axios from 'axios'
import store from '@/store/visibilityStore'

export default {
  name: 'UsersTable',
  components: { Footer },
  props: {
    msg: String
  },
  data() {
    return {
      sponsors: [],
      SPONSORS_VISIBILITY: store.state.SPONSORS_VISIBILITY
    }
  },
  mounted() {
    this.created();
  },
  methods: {
    created() {
      axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?ordering=order&search=1&search_fields=visible',)
        .then(response => {
          this.sponsors = response.data;
        })
    }
  }
}
</script>


<style>
.sponsors {
  padding: 3.14159em;
  padding-top: 5.5em;

  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  grid-gap: 3.14159em;
}

.image-container {
  position: relative;
}

.image-container .image-sizer {
  padding-bottom: calc(0.86 * 100%);
  transition: padding-bottom .3s ease;
  will-change: padding-bottom;
}

.image-container .image-frame {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-position: center center;
  background-size: contain;
}

.sponsor {
  background: rgba(0, 0, 0, .3);
  border-radius: 18px;
  padding: 30px;
}

@media screen and (max-width: 1550px) {
  .sponsors {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media screen and (max-width: 980px) {
  .sponsors {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media screen and (max-width: 635px) {
  .sponsors {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media screen and (max-width: 21.875rem) {
  .sponsors {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}
</style>