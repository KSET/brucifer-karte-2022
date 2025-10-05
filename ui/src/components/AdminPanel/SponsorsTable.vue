<template>
  <div class="grid sponsors-table">
    <div class="card" style="height: 36%;" ref="" v-for="sponsor in sponsors" :key="sponsor.id">
      <div>
        <img class="ccard-img" v-bind:src="sponsor.image"
          v-bind:style="[(sponsor.visible == '0') ? { opacity: '0.25' } : { opacity: '1' }]"
          style="background-color: #D9D9D9; height: 10rem;">
      </div>
      <div class="ccard-body">
        <h3 class="name"> {{ sponsor.name }} </h3>

        <div class="ccard-buttons">
          <button v-if="buttonEnabeled" @click="changesponsororder(sponsor, 'b')" class="ccard-button">
            <img src="../../assets/icons/arrow-left-icon.svg">
          </button>

          <button v-else disabeled class="ccard-button">
            <img src="../../assets/icons/arrow-left-gray-icon.svg">
          </button>

          <button @click="editsponsor(sponsor)" class="ccard-button" style="padding-bottom: 5px;">
            <img src="../../assets/icons/edit-icon.svg">
          </button>

          <button v-if="buttonEnabeled" @click="changesponsororder(sponsor, 'f')" class="ccard-button">
            <img src="../../assets/icons/arrow-right-icon.svg">
          </button>
          <button v-else disabeled class="ccard-button">
            <img src="../../assets/icons/arrow-right-gray-icon.svg">
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import sponsorsStore from '@/store/sponsorsStore'

export default {
  name: 'SponsorsTable',
  components: { Sidebar },

  data() {
    return {
      buttonEnabled: true,
    }
  },

  computed: {
    sponsors() {
      return sponsorsStore.state.list
    },
    loading() {
      return sponsorsStore.state.loading
    },
    error() {
      return sponsorsStore.state.error
    },
    isBusy() {
      return this.loading || !this.buttonEnabled
    },
  },

  async mounted() {
    await sponsorsStore.dispatch('fetchAll')
  },

  methods: {
    editsponsor(sponsor) {
      this.$router.push({ path: `/admin/sponsors-add/${sponsor.slug}` })
    },

    canMoveBack(sponsor) {
      const idx = this.sponsors.indexOf(sponsor)
      return idx > 0
    },

    canMoveForward(sponsor) {
      const idx = this.sponsors.indexOf(sponsor)
      return idx > -1 && idx < this.sponsors.length - 1
    },

    async changesponsororder(sponsor, direction) {
      if (this.isBusy) return
      this.buttonEnabled = false

      try {
        const idx = this.sponsors.indexOf(sponsor)
        if (idx === -1) return

        let neighbor = null
        if (direction === 'f' && this.canMoveForward(sponsor)) {
          neighbor = this.sponsors[idx + 1]
        } else if (direction !== 'f' && this.canMoveBack(sponsor)) {
          neighbor = this.sponsors[idx - 1]
        }
        if (!neighbor) return

        // swap orders via backend bulk reorder
        const payload = [
          { id: sponsor.id, order: neighbor.order },
          { id: neighbor.id, order: sponsor.order },
        ]

        await sponsorsStore.dispatch('reorder', payload)
        await sponsorsStore.dispatch('fetchAll') // refresh
      } catch (e) {
        console.error(e)
        alert('Promjena poretka sponzora nije uspjela.')
      } finally {
        this.buttonEnabled = true
      }
    },
  },
}
</script>


<style scoped>
.sponsors-table .ccard-img {
  max-width: 100%;
}
</style>

<style>
.grid {
  height: 85%;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-gap: 20px;
  overflow: auto;
}

.name {
  position: relative;
  width: 100%;
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  /* identical to box height, or 257% */

  text-align: center;
  align-items: center;
  letter-spacing: -0.015em;
  vertical-align: bottom;
}

.ccard-body {
  background-color: #D9D9D9;
}

.ccard-img {
  position: relative;
  width: 150%;
  object-fit: contain;
}

.ccard-buttons {
  display: grid;
  margin: 1%;
  column-gap: 20%;
  grid-template-columns: 19% 20% 19%;
}

.ccard-button {
  border: 0px;
  background-color: #D9D9D9;
}

.card {
  height: 40%;
}
</style>