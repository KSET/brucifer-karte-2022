<template>
    <div id="cjenik">
      <Sidebar />
      <div class="admin-page-container">
        <h1 class="page-title">Cjenik</h1>

      </div>
    </div>
  
  </template>
  
  <script>
  import axios from 'axios'
  import Sidebar from '@/components/NavbarAndFooter/Sidebar.vue'
  
  export default {
    name: 'GuestsTable',
    props: {
      msg: String
    },
    components: {
      Sidebar
    },
    data() {
      return {
        
      }
    },
    mounted() {
      this.created();
    },
    methods: {
      created() {
        
      }
    }
  
  }
  </script>

  
  
  