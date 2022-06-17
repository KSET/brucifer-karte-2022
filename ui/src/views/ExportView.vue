<template>
  <div class="export">
    <download-csv
	class   = "btn btn-default"
	:data   = this.users
  separator-excel = true,
  encoding = 'UTF-8'
	name    = "export.csv">
  

	Download CSV (This is a slot)

</download-csv>
  </div>
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
