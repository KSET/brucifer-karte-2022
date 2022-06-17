<template>
  <div id="guests-add">
    <form @submit="postGuest">
      <h>Dodaj na popis: </h>
      <input type="text" id="inputname" v-model="name" placeholder="Name">
      <input type="text" id="inputsurname" v-model="surname" placeholder="Surname">
      <select v-model="selectedTag" name={{selectedTag}} id={{selectedTag}}>
        <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
      </select>
      <button class="btn btn-primary" id="gumb2">Add</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

import Dropdown from '../DropdownRoute.vue';
export default {
  name: 'GuestsAdd',
  components: {
    Dropdown
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
    axios.get('http://127.0.0.1:8000/guests/',)
      .then(response => {
        this.guests = response.data;
        this.len = this.guests.length;
      })
  },
  methods: {
    postGuest() {
      var ids = [];

      this.guests.forEach(element => {
        ids.push(element.id);
      });
      for (let index = 0; index < ids.length; index++) {
        if (ids.includes(String(index)) == false) {
          this.nextId = index;
          break;
        }
      }
      if (this.nextId == '') {
        this.nextId = ids.length;
      }
      axios.post('http://127.0.0.1:8000/guests/',
        { id: this.nextId, name: this.name, surname: this.surname, jmbag: this.jmbag, tag: this.selectedTag, bought: '0', entered: '0' },
        { auth: { username: 'paxx', password: 'KSETpenisica43' } }
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
  margin: 2px;
  width: 220px;
  height: 30px;
  text-align: center;
}
</style>


