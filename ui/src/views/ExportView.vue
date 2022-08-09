<template>
  <div class="export">
    <br>
<div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
          <div class="card-header">Export</div>
          <div class="card-body">
    <download-csv id="gumb2"
	class   = "btn btn-primary"
	:data   = this.users
  separator-excel = true,
  encoding = 'UTF-8'
	name    = "export.csv">

	Download CSV

</download-csv>
  </div></div></div></div></div>
</template>

<script>
import axios from 'axios'
import JsonCSV from 'vue-json-csv'

export default {
  name: 'GuestsExport',
  components: JsonCSV,
  props: {
    msg: String
  },
  data(){
    return{
      users: [],
      id:'',
      name:'',
      email:'',
      privilege:'',
    }
    
  },
  created() {
    axios.get('http://127.0.0.1:8000/guests/',)
    .then(response => {
      this.users =response.data;
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