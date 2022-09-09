<template>
  <div class="tagss">
    <Sidebar />
    <div class="admin-page-container">
      <div class="page-header">
      <h1 class="page-title" >Tagovi</h1>
      <form style="display: inline-block; width: 40%; vertical-align: middle;" @submit="postTag">
        <input required type="text" class="inputtag"  v-model="name" placeholder="Unesi ime taga">
        <button class="button-icon"> <img class="add-icon" src="@/assets/icons/add-icon.svg"></button>
      </form>
    </div>
      <tags-table></tags-table>
    </div>
  </div>

</template>




<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import TagsTable from '@/components/Tags/TagsTable.vue'
import axios from 'axios';
export default {
  name: 'TagsView',
  props: {
    msg: String
  },
  components: { TagsTable, Sidebar },
  data() {
    return {
      tags: [],
      name: '',
      nextId: '',
    }
  },
  created() {
    axios.get('http://127.0.0.1:8000/tags/',)
      .then(response => {
        this.tags = response.data;
      })
  },
  methods: {
    postTag() {
      var ids = [];

      this.tags.forEach(element => {
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


      axios.post('http://127.0.0.1:8000/tags/',
        { id: this.nextId, name: this.name },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          location.reload();
        })
    }
  }
}
</script>


<style >
#title0 {
  display: inline-block;
}



.inputtag{
  height: 40px;
  text-align: left;
  width:80%;
  vertical-align: top;
  font-family: 'Montserrat';
  
  
font-size: 16px;
}

.add-icon{
  padding-top: 2px;
  padding-left: 5px;
  height: 40px;
  vertical-align: top;
}
</style>