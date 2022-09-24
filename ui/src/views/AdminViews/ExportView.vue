<template>
  <div class="export">
    <Sidebar />
    <div class="admin-page-container">
      <br>
      <download-csv id="gumb2" class="btn btn-primary" :data=this.users separator-excel=true, encoding='UTF-8'
        name="export.csv">

        Download CSV

      </download-csv>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
import JsonCSV from 'vue-json-csv'
import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'

export default {
  name: 'GuestsExport',
  components: { JsonCSV, Sidebar },
  props: {
    msg: String
  },
  data() {
    return {
      users: [],
      id: '',
      name: '',
      email: '',
      privilege: '',
    }

  },
  created() {
    axios.get(process.env.VUE_APP_BASE_URL+':8000/guests/',)
      .then(response => {
        this.users = response.data;
      })
  }
}
</script>


<style>
#gumb2 {
  padding: 0px;
  margin: 2px;
  width: 220px;
  height: 100px;
  text-align: center;
}
</style>