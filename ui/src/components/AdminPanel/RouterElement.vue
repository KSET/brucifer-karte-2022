<template>
  <button @click="$router.push(this.link)">
    {{ name }}
  </button>
</template>

<script>
export default {
  name: 'RouterElement',
  props: [
    'name',
    'link',
  ]
}
</script>
