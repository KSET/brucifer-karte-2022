<template>
  <div class="tagss">
    <Sidebar />
    <div class="admin-page-container">
      <div class="page-header">
        <h1 class="page-title">Tagovi</h1>
        <form onsubmit="return false" style="display: inline-block;  vertical-align: middle;">
          <input required type="text" class="inputtag" v-model="name" placeholder="Unesi ime taga">
          <button class="button-icon" @click="postTag"> <img class="add-icon"
              src="@/assets/icons/add-icon.svg"></button>
        </form>
      </div>
      <TagsTable :tags="tags" @refreshTags="fetchTags" />
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
    }
  },
  created() {
    this.fetchTags();
  },
  methods: {
    async fetchTags() {
      const response = await axios.get(process.env.VUE_APP_BASE_URL + '/tags/');
      this.tags = response.data;
    },
    postTag() {
      if (this.name != "") {
        axios.post(process.env.VUE_APP_BASE_URL + '/tags/',
          { name: this.name },
          { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
        )
          .then(() => {
            this.name = "";
            this.fetchTags();
          })
      }
    }
  }
}
</script>


<style>
#title0 {
  display: inline-block;
}

.tags-table {
  height: 100%;
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

  border: 1px solid black;
}

.add-icon {
  padding-top: 2px;
  padding-left: 5px;
  height: 40px;
  vertical-align: top;
}
</style>