<template>
  <div class="grid">
    <div class="card" ref="" v-for="lineup in lineups" :key="lineup.id">

      <img class="ccard-img" v-bind:src="lineup.image">
      <div class="ccard-body">
        <h3 class="name"> {{lineup.name}}</h3>

        <div class="ccard-buttons">
          <button @click="deleteTag(lineup)" class="ccard-button" >
            <img src="../../assets/icons/arrow-left-icon.svg">
          </button>
          <button @click="deleteTag(lineup)" class="ccard-button" style="padding-bottom: 5px;">
            <img src="../../assets/icons/edit-icon.svg">
          </button>
          <button @click="deleteTag(lineup)" class="ccard-button">
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
    getAp(elementName) {


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
  width:100%;
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

.ccard-img{
  position: relative;
  width:150%;
}

.ccard-buttons{
  display: grid;
  margin: 1%;
  column-gap: 20%;
  grid-template-columns: 19% 20% 19%;
}

.ccard-button{
  border: 0px;
  background-color: #D9D9D9;
}
</style>