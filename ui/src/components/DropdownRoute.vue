<template>
  <div class="menu-item" @click="isOpen = !isOpen">
    <a v-if="type == '1'" href="#">
      {{ title }}
    </a>
    <a v-else href="#">
      {{ name }}
    </a>
    <div class="sub-menu" v-if="isOpen">
      <div class="menu-item" v-for="(item, i) in items" :key="i" >
        <router-link v-if="type == '1'" :to="'/guest_tag/' + item">{{ item }}</router-link>
        <router-link v-else :to="item">{{ item }}</router-link>
      </div>
    </div>

  </div>
</template>

<script>
import store from '@/store/index.js';
export default {
  el: '#app',
  computed: {
    name() {
      return store.state.name;
    }
  },
  name: 'dropdown',
  props: ['title', 'items', 'type'],
  data() {
    return {
      isOpen: false
    }
  }
}
</script>

<style>
nav .menu-item svg {
  width: 10px;
  margin-left: 10px;
}

nav .menu-item .sub-menu {
  position: absolute;
  background-color: #222;
  top: calc(100% + 18px);
  left: 50%;
  width: 50px;
  border-radius: 0px 0px 16px 16px;
}
</style>