<template>
    <button @click="$router.push(this.link)">
      {{name}}
      </button>
</template>

<script>
export default {
  name: 'GridRouterLinkElement',
  props: [
    'name',
    'link',
  ]
}
</script>
