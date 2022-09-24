<template>
  <div id="guests-add">
    <form @submit="postGuest">
      <h1>Dodaj na popis: </h1>
      <input type="text" id="inputname" v-model="name">
      <input type="text" id="inputsurname" v-model="surname" >
      <select v-model="selectedTag" name={{selectedTag}} id={{selectedTag}}>
        <option v-for="(item, i) in items" :key="i" class="menu-item">{{ item }}</option>
      </select>
      <button class="btn btn-primary" id="gumb2">Dodaj</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

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
    axios.get(process.env.VUE_APP_BASE_URL+':8000/guests/',)
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
      
      axios.post(process.env.VUE_APP_BASE_URL+':8000/guests/',
        { id: this.nextId, name: this.name, surname: this.surname, jmbag: this.jmbag, tag: this.selectedTag, bought: '0', entered: '0' },
        { auth: { username: process.env.AUTH_USER, password: process.env.VUE_APP_DJANGO_PASS } }
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


