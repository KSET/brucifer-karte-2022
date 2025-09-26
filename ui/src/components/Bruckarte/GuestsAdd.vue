<template>
  <div id="guests-add">
    <form @submit="postGuest">
      <h1>Dodaj na popis: </h1>
      <input type="text" id="inputname" v-model="name">
      <input type="text" id="inputsurname" v-model="surname">
      <select v-model="selectedTag" name={{selectedTag}} id={{selectedTag}}>
        <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
      </select>
      <button class="btn btn-primary" id="gumb2">Dodaj</button>
    </form>
  </div>
</template>

<script>
import { api } from "@/plugins/api";

export default {
  name: 'GuestsAdd',
  components: {

  },
  props: {
    msg: String
  },
  data() {
    return {
      items: ['Brucoši', 'KSET', 'VIP'],
      guests: [],
      id: '',
      name: '',
      surname: '',
      jmbag: '',
      phone: '',
      tag: '',
      bought: '',
      entered: '',
      deleted: '',
      len: '',
      services: ['Brucoši', 'KSET', 'VIP'],
      selectedTag: '',

    }
  },

  created() {
    api.get('/guests/',)
      .then(response => {
        this.guests = response.data;
        this.len = this.guests.length;
      })
  },
  methods: {
    postGuest() {
      api.post('/guests/',
        { name: this.name, surname: this.surname, jmbag: this.jmbag, tag: this.selectedTag, bought: '0', entered: '0' },
      )
        .then(() => {
          location.reload();
        })
    }
  }
}
</script>


<style>
#inputname {
  width: 220px;
  margin: 2px;
}

#inputsurname {
  width: 220px;
  margin: 2px;
}


#gumb2 {
  padding: 0px;
  margin: 2px;
  width: 220px;
  height: 30px;
  text-align: center;
}
</style>


