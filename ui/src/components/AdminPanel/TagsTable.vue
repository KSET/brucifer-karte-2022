<template>
  <div class="tags-table">
    <div class=row>
      <table id="guests">
        <thead>
          <th>Ime</th>
          <th>Broj</th>
          <th>Karta</th>
          <th>Ulaz</th>
          <th>Opcije</th>
        </thead>
        <tbody>
          <tr style="overflow:auto; height=200px;" v-for="tag in tags" :key="tag.id">
            <td>{{tag.name}}</td>
            <td>{{tag.count}}</td>
            <td>{{tag.bought}}</td>
            <td>{{tag.entered}}</td>
            <td><button class="button-icon" @click="deleteTag(tag)"> <img src="@/assets/icons/trash-icon.svg"></button>
            </td>
          </tr>
        </tbody>
      </table>

    </div>
  </div>


</template>

<script>
import axios from 'axios'
export default {
  name: 'TagsTable',
  props: {
    msg: String
  },
  data() {
    return {
      tags: [],
      id: '',
      name: '',
      surname: '',
      jmbag: '',
      phone: '',
      tag: '',
      bought: '',
      entered: '',
      deleted: '',
      numc: '',
      numb: '',
      nume: '',
    }

  },
  mounted() {
    this.created();
  },
  methods: {
    created() {
      axios.get(process.env.VUE_APP_BASE_URL + ':8000/tags/',)
        .then(response => {
          this.tags = response.data;
          this.tags.forEach(element => {
            axios.get(process.env.VUE_APP_BASE_URL + ':8000/guests/?search=' + element.name + '&search_fields=tag',)
              .then(response => {
                this.numc = 0;
                this.numb = 0;
                this.nume = 0;
                response.data.forEach(element => {
                  this.numc++;
                  if (element.bought == 1) {
                    this.numb++;
                  }
                  if (element.entered == 1) {
                    this.nume++;
                  }


                });
                if (String(this.numc) != String(element.count) || this.numb != element.bought || this.nume != element.entered) {

                  axios.put(process.env.VUE_APP_BASE_URL + ':8000/tags/' + element.id + '/',
                    { count: this.numc, bought: this.numb, entered: this.nume },
                    { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }

                  )

                  this.created();

                }
              })


          });
        })

    },
    deleteTag(tag) {
      axios.delete(process.env.VUE_APP_BASE_URL + ':8000/tags/' + tag.id + '/',
        { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
      )
        .then(() => {
          this.created();
        })
    }
  }

}
</script>
<style>
.button-icon {
  border: 0px;
  background-color: white;
  padding: 0px;
}

tbody {
  display: block;
  height: 500px;
  overflow: auto;
}

thead,
tbody tr {
  display: table;
  width: 100%;
  table-layout: fixed;
  /* even columns width , fix width of table too*/
}
</style>


