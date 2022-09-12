<template>
  <div class="grid">
    <div class="card" ref="" v-for="sponsor in sponsors" :key="sponsor.id">

      <img class="ccard-img" v-bind:src="sponsor.image">
      <div class="ccard-body">
        <h3 class="name"> {{sponsor.name}}</h3>

        <div class="ccard-buttons">
          <button @click="deleteTag(sponsor)" class="ccard-button" >
            <img src="../../assets/icons/arrow-left-icon.svg">
          </button>
          <button @click="deleteTag(sponsor)" class="ccard-button" style="padding-bottom: 5px;">
            <img src="../../assets/icons/edit-icon.svg">
          </button>
          <button @click="deleteTag(sponsor)" class="ccard-button">
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
  name: 'SponsorsTable',
  props: {
    msg: String
  },
  data() {
    return {
      sponsors: [],
    }

  },
  mounted() {
    this.created();
  },
  methods: {
    created() {
      axios.get('http://127.0.0.1:8000/sponsors/',)
        .then(response => {
          this.sponsors = response.data;
        });
    },
    deleteTag(tag) {
      axios.delete('http://127.0.0.1:8000/sponsors/' + tag.id + '/',
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

