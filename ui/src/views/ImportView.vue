<template>
<div class="import">
    <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
          <div class="card-header">Import</div>
          <div class="card-body">
    <section>
      <input type="file" @change="onChange" />
      <xlsx-read :file="file">
        <xlsx-json :sheet="selectedSheet">
          <template #default="{collection}">
            <div>
              {{ collection }}
            </div>
          </template>
        </xlsx-json>
      </xlsx-read>
    </section>
          </div></div></div></div></div>
</template>
<script>

import { XlsxRead, XlsxJson } from "../../node_modules/vue3-xlsx/dist/vue3-xlsx.cjs.prod.js";


export default {
  components: {
    XlsxRead,
    XlsxJson
  },
  data() {
    return {
      file: null,
    };
  },
  methods: {
    onChange(event) {
      this.file = event.target.files ? event.target.files[0] : null;
      console.log(XlsxJson)
    },
  }
}
</script>

<style scoped>
</style>