<template>
  <div class="grid">
    <div class="card" ref="" v-for="lineup in lineups" :key="lineup.id">

      <img class="ccard-img" v-bind:src="lineup.image">
      <div class="ccard-body">
        <h3 class="name"> {{lineup.name}}</h3>

        <div class="ccard-buttons">
          <button @click="changelineuporder(lineup, 'b')" class="ccard-button">
            <img src="../../assets/icons/arrow-left-icon.svg">
          </button>
          <button @click="editlineup(lineup)" class="ccard-button" style="padding-bottom: 5px;">
            <img src="../../assets/icons/edit-icon.svg">
          </button>
          <button @click="changelineuporder(lineup, 'f')" class="ccard-button">
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
      lineups: [],
      lineup: '',
      lineup: '',
    }

  },
  mounted() {
    this.created();
  },
  methods: {
    created() {
      axios.get('http://127.0.0.1:8000/lineup/',)
        .then(response => {
          this.lineups = response.data;
        });
    },
    deleteTag(tag) {
      axios.delete('http://127.0.0.1:8000/lineup/' + tag.id + '/',
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created();
        })
    },
    editlineup(lineup) {
      this.$router.push({ path: '/bruckarte/lineup-add/' + lineup.slug });
    },
    changelineuporder(lineup, direction) {
      if (direction == "f") {
        console.log(this.lineups);
        console.log(this.lineups.length);

        var nextlineupobj = (this.lineups.indexOf(lineup));

        console.log((lineup.id != this.lineups[this.lineups.length - 1].id));
        if (lineup.id != this.lineups[this.lineups.length - 1].id) {
          var nextlineup = this.lineups[nextlineupobj + 1].id;
        }
      } else {
        if (lineup.id != 0) {
          var nextlineup = this.lineups[nextlineupobj - 1].id;
        }
      }
      axios.put('http://127.0.0.1:8000/lineup/' + nextlineup + '/',
        { id: "1000000" },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
        axios.delete('http://127.0.0.1:8000/lineup/' + nextlineup + '/',
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
              )
                .then(() => {
          console.log("req1-pass");

          axios.put('http://127.0.0.1:8000/lineup/' + lineup.id + '/',
            { id: nextlineup },
            { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
          )
            .then(() => {
            })
              console.log("req2-pass");
              axios.delete('http://127.0.0.1:8000/lineup/' + lineup.id + '/',
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
              )
                .then(() => {
                  console.log("req3-pass");

                  axios.put('http://127.0.0.1:8000/lineup/' + 1000000 + '/',
                    { id: lineup.id },
                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
                  )
                    .then(() => {
                      axios.delete('http://127.0.0.1:8000/lineup/' + 1000000 + '/',
                { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
              )
                .then(() => {
                      console.log("req4-pass");

                      this.created();
                    })
                })
            })
        })
      })

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