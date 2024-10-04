<template>
  <div class="tagss">
    <Sidebar />
    <div class="admin-page-container">
      <div class="page-header">
        <input style=" display: block" type="file" @change="handleFileUpload" accept=".xlsx" />
        <button @click="executeTagChange">Execute Tag Change</button>
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
import * as XLSX from 'xlsx';

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
      file: null,
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
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async executeTagChange() {
      if (!this.file) {
        alert("Please upload an Excel file first.");
        return;
      }

      // Step 1: Process the file asynchronously
      const fileData = await this.processExcelFile();
      
      // Step 2: Loop through file data and retrieve users using the exact search format
      for (const row of fileData) {
        const jmbag = row[0]; // jmbag is in the first position
        const newTag = row[1]; // tag is in the second position
        if (!jmbag || !newTag) continue;

        try {
          // Get the user by jmbag using your provided method
          const response = await axios.get(process.env.VUE_APP_BASE_URL + '/guests/?search=Brucoši ' + jmbag + "&search_fields=tag&search_fields=jmbag");

          const user = response.data[0]; // assuming response is user data
          
          if (user && user.tag !== newTag) {
            // Step 3: Update the tag if it differs from the current one
            await this.updateUserTag(user.id, newTag);
          }

        } catch (error) {
          console.error(`Error fetching user with jmbag ${jmbag}:`, error);
        }
      }
    },
    // Function to update the user's tag
    async updateUserTag(userId, newTag) {
      try {
        const response = await axios.put(process.env.VUE_APP_BASE_URL + '/guests/' + userId + '/', {
          tag: newTag
        }, {
          auth: {
            username: process.env.VUE_APP_DJANGO_USER,
            password: process.env.VUE_APP_DJANGO_PASS
          }
        });
        console.log(`Tag updated for user ${userId}: ${newTag}`);
      } catch (error) {
        console.error(`Error updating tag for user ${userId}:`, error);
      }
    },
    processExcelFile() {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
          const fileData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });
          resolve(fileData);
        };
        reader.onerror = (error) => reject(error);
        reader.readAsArrayBuffer(this.file);
      });
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