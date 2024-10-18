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
          <tr style="overflow:auto;" v-for="tag in tags" :key="tag.id">
            <td>{{ tag.name }}</td>
            <td>{{ tag.count }}</td>
            <td>{{ tag.bought }}</td>
            <td>{{ tag.entered }}</td>
            <td><button class="button-icon" @click="deleteTag(tag)"> <img src="@/assets/icons/trash-icon.svg"></button>
            </td>
          </tr>
        </tbody>
      </table>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TagsTable',
  data() {
    return {
      tags: [],
      tagStatistics: {
        numc: 0,
        numb: 0,
        nume: 0,
      },
    };
  },
  watch: {
    'tagsUpdateKey': {
      deep: true,
      handler() {
        this.fetchTags();
      }
    }
  },
  created() {
    this.fetchTags();
  },
  methods: {
    async fetchTags() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_BASE_URL}/tags/`);
        this.processTags(response.data);
      } catch (error) {
        console.error('Failed to fetch tags:', error);
      }
    },
    async processTags(tags) {
      console.log(tags)
      try {
        for (const tag of tags) {
          const response = await axios.get(`${process.env.VUE_APP_BASE_URL}/guests/?search=${tag.name}&search_fields=tag`);
          let { numc, numb, nume } = { numc: 0, numb: 0, nume: 0 };

          response.data.forEach(guest => {
            numc++;
            if (guest.bought == 1) numb++;
            if (guest.entered == 1) nume++;
          });

          if (`${numc}` != `${tag.count}` || numb != tag.bought || nume != tag.entered) {
            await axios.put(`${process.env.VUE_APP_BASE_URL}/tags/${tag.id}/`, 
              { count: numc, bought: numb, entered: nume },
              { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
            );

            Object.assign(tag, { count: numc, bought: numb, entered: nume });
          }
        }
        this.tags = [...tags];
      } catch (error) {
        console.error('Failed to process tags:', error);
      }
    },
    async deleteTag(tag) {
      try {
        await axios.delete(`${process.env.VUE_APP_BASE_URL}/tags/${tag.id}/`, 
          { auth: { username: process.env.VUE_APP_DJANGO_USER, password: process.env.VUE_APP_DJANGO_PASS } }
        );
        this.fetchTags();
      } catch (error) {
        console.error('Failed to delete tag:', error);
      }
    }
  }
};
</script>

<style>
.button-icon {
  border: 0px;
  background-color: white;
  padding: 0px;
}

tbody {
  display: block;
  height: 100%;
  overflow: auto;
}

thead,
tbody tr {
  display: table;
  width: 100%;
  table-layout: fixed;
}
</style>


