<template>
  <div>
    <div class="grid">
      <div class="card" style="height: 40%; border: none;" v-for="lineup in lineups" :key="lineup.id">
        <img class="ccard-img" v-bind:src="lineup.image"
          v-bind:style="[(lineup.visible == '0') ? { opacity: '0.25' } : { opacity: '1' }]">
        <div class="ccard-body">
          <h3 class="name"> {{ lineup.name }}</h3>

          <div class="ccard-buttons">
            <button v-if="buttonEnabeled" @click="changelineuporder(lineup, 'b')" id="b4" class="ccard-button">
              <img src="../../assets/icons/arrow-left-icon.svg">
            </button>
            <button v-else disabeled id="b4" class="ccard-button">
              <img src="../../assets/icons/arrow-left-gray-icon.svg">
            </button>

            <button @click="editlineup(lineup)" class="ccard-button" style="padding-bottom: 5px;">
              <img src="../../assets/icons/edit-icon.svg">
            </button>

            <button v-if="buttonEnabeled" @click="changelineuporder(lineup, 'f')" id="next" class="ccard-button">
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
import axios from 'axios'
export default {
  name: 'LineupTable',
  props: {
    msg: String
  },
  data() {
    return {
      lineups: [],
      lineup: '',
      lineup: '',
      buttonEnabeled: true,

    }

  },
  mounted() {
    this.created();
  },
  methods: {
    created() {
      axios.get(process.env.VUE_APP_BASE_URL + '/lineup/?ordering=order',)
        .then(response => {
          this.lineups = response.data;
        });
    },
    editlineup(lineup) {
      this.$router.push({ path: '/admin/lineup-add/' + lineup.slug });
    },
    async changelineuporder(lineup, direction) {
      this.buttonEnabeled = false;

      var nextlineupobj = (this.lineups.indexOf(lineup));
      if (direction == "f") {
        if (lineup.id != this.lineups[this.lineups.length - 1].id) {
          var nextlineup = this.lineups[nextlineupobj + 1];
        }
      } else {
        if (lineup.order != "00") {
          var nextlineup = this.lineups[nextlineupobj - 1];
        }
      }

      await axios.put(process.env.VUE_APP_BASE_URL + '/lineup/' + lineup.id + '/',
        { order: nextlineup.order },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )

      await axios.put(process.env.VUE_APP_BASE_URL + '/lineup/' + nextlineup.id + '/',
        { order: lineup.order },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } })

      this.buttonEnabeled = true;
      this.created();
    }
  }

}
</script>

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