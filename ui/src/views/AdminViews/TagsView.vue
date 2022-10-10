<template>
  <div class="tagss">
    <Sidebar />
    <div class="admin-page-container">
      <div class="page-header">
        <h1 class="page-title">Tagovi</h1>
        <form onsubmit="return false" style="display: inline-block;  vertical-align: middle;" >
          <input required type="text" class="inputtag" v-model="name" placeholder="Unesi ime taga">
          <button class="button-icon" @click="postTag"> <img class="add-icon" src="@/assets/icons/add-icon.svg"></button>
        </form>
      </div>
      <tags-table></tags-table>
    </div>
  </div>

</template>

<script>
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
import TagsTable from '@/components/AdminPanel/TagsTable.vue'
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
  mounted(){
    this.created();
  },
  methods: {
    created() {
    axios.get(process.env.VUE_APP_BASE_URL + '/tags/',)
      .then(response => {
        this.tags = response.data;
      })
  },
    postTag() {
      if(this.name!=""){
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
      if (this.nextId === '') {
        this.nextId = ids.length;
      }


      axios.post(process.env.VUE_APP_BASE_URL + '/tags/',
        { id: this.nextId, name: this.name },
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.name="";
          location.reload();
        })
    }}
  }
}
</script>


<style >
#title0 {
  display: inline-block;
}



.inputtag {
  height: 40px;
  text-align: left;
  width: 80%;
  vertical-align: top;
  font-family: 'Montserrat';

  height: 39px;
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;

  font-size: 16px;
}

.add-icon {
  padding-top: 2px;
  padding-left: 5px;
  height: 40px;
  vertical-align: top;
}
</style>