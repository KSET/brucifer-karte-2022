<template>
  <div class="grid">
    <div class="card" style="height: 40%;" ref="" v-for="sponsor in sponsors" :key="sponsor.id">

      <img class="ccard-img" v-bind:src="sponsor.image">
      <div class="ccard-body">
        <h3 class="name"> {{sponsor.name}} </h3>
        <a class="name" :href="sponsor.url" target="_blank">{{sponsor.url}}</a>

        <div class="ccard-buttons">
          <button @click="changesponsororder(sponsor, 'b')" class="ccard-button">
            <img src="../../assets/icons/arrow-left-icon.svg">
          </button>
          <button @click="editsponsor(sponsor)" class="ccard-button" style="padding-bottom: 5px;">
            <img src="../../assets/icons/edit-icon.svg">
          </button>
          <button @click="changesponsororder(sponsor, 'f')" class="ccard-button">
            <img src="../../assets/icons/arrow-right-icon.svg">
          </button>
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
      sponsors: [],
      sponsor: '',
      sponsor: '',
    }

  },
  mounted() {
    this.created();
  },
  methods: {
    created() {
      axios.get(process.env.VUE_APP_BASE_URL + '/sponsors/?ordering=order',)
        .then(response => {
          this.sponsors = response.data;
          this.sponsors.splice(this.sponsors.length - 1, 1);

        });
    },
    editsponsor(sponsor) {
      this.$router.push({ path: '/admin/sponsors-add/' + sponsor.slug });
    },
    changesponsororder(sponsor, direction) {
      var nextsponsorobj = (this.sponsors.indexOf(sponsor));

      if (direction == "f") {
        if (sponsor.id != this.sponsors[this.sponsors.length - 1].id) {
          var nextsponsor = this.sponsors[nextsponsorobj + 1];
        }
      } else {
        if (sponsor.order != "00") {
          var nextsponsor = this.sponsors[nextsponsorobj - 1];
        }
      }

      axios.put(process.env.VUE_APP_BASE_URL + '/sponsors/' + nextsponsor.id + '/',
        { order: "1000000" },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          axios.put(process.env.VUE_APP_BASE_URL + '/sponsors/' + sponsor.id + '/',
            { order: nextsponsor.order },
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
          )
            .then(() => {
            })
          axios.put(process.env.VUE_APP_BASE_URL + '/sponsors/' + nextsponsor.id + '/',
            { order: sponsor.order },
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
          )
            .then(() => {
              this.created();
            })

        })

    }
  }

}
</script>

<style>
.grid {
  height: 100%;
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