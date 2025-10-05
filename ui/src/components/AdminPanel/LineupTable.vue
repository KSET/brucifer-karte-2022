<template>
  <div class="lineup-table">
    <div class="grid">
      <div class="card" style="height: 40%; border: none;" v-for="lineup in lineups" :key="lineup.id">
        <img class="ccard-img" v-bind:src="lineup.image"
          v-bind:style="[(lineup.visible == '0') ? { opacity: '0.25' } : { opacity: '1' }]">
        <div class="ccard-body">
          <h3 class="name"> {{ lineup.name }}</h3>

          <div class="ccard-buttons">
            <button v-if="buttonEnabled" @click="changelineuporder(lineup, 'b')" id="b4" class="ccard-button">
              <img src="../../assets/icons/arrow-left-icon.svg">
            </button>
            <button v-else disabeled id="b4" class="ccard-button">
              <img src="../../assets/icons/arrow-left-gray-icon.svg">
            </button>

            <button @click="editlineup(lineup)" class="ccard-button" style="padding-bottom: 5px;">
              <img src="../../assets/icons/edit-icon.svg">
            </button>

            <button v-if="buttonEnabled" @click="changelineuporder(lineup, 'f')" id="next" class="ccard-button">
              <img src="../../assets/icons/arrow-right-icon.svg">
            </button>
            <button v-else disabeled id="next" class="ccard-button">
              <img src="../../assets/icons/arrow-right-gray-icon.svg">
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import lineupStore from '@/store/lineupStore'

export default {
  name: 'LineupTable',
  components: { Sidebar },

  data() {
    return {
      buttonEnabled: true,
    }
  },

  computed: {
    lineups() {
      return lineupStore.state.list
    },
    loading() {
      return lineupStore.state.loading
    },
    error() {
      return lineupStore.state.error
    },
    isBusy() {
      return this.loading || !this.buttonEnabled
    }
  },

  async mounted() {
    await lineupStore.dispatch('fetchAll')
  },

  methods: {
    editlineup(lineup) {
      console.log(`Editing lineup with slug ${lineup.slug}`)
      this.$router.push({ path: `/admin/lineup-add/${lineup.slug}` })
    },

    canMoveBack(lineup) {
      const idx = this.lineups.indexOf(lineup)
      return idx > 0
    },
    canMoveForward(lineup) {
      const idx = this.lineups.indexOf(lineup)
      return idx > -1 && idx < this.lineups.length - 1
    },

    async changelineuporder(lineup, direction) {
      if (this.isBusy) return
      this.buttonEnabled = false

      try {
        const idx = this.lineups.indexOf(lineup)
        if (idx === -1) return

        let neighbor = null
        if (direction === 'f' && this.canMoveForward(lineup)) {
          neighbor = this.lineups[idx + 1]
        } else if (direction !== 'f' && this.canMoveBack(lineup)) {
          neighbor = this.lineups[idx - 1]
        }
        if (!neighbor) return

        const payload = [
          { id: lineup.id, order: neighbor.order },
          { id: neighbor.id, order: lineup.order },
        ]

        await lineupStore.dispatch('reorder', payload)
        await lineupStore.dispatch('fetchAll')
      } catch (e) {
        console.error(e)
        alert('Promjena poretka nije uspjela.')
      } finally {
        this.buttonEnabled = true
      }
    },
  },
}
</script>

<style scoped>
.lineup-table .ccard-img {
  max-width: 100%;
}
</style>

<style>
.grid {
  height: 74vh;
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
  line-height: 36px;
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
</style>