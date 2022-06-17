<template>
  <div class="menu-item" @click="isOpen = !isOpen">
    <a v-if="type=='1'" href="#">
      {{ title }}
    </a>
    <a v-else href="#">
      "bararaarar"
    </a>

      <div class="sub-menu" v-if="isOpen">
        <div v-for="(item, i) in this.items" :key="i" class="menu-item">
          <option value={{item}}>{{item}}</option>
        </div>
      </div>
   
  </div>
</template>

<script>
export default {
  name: 'dropdown',
  props: ['title', 'items','type'],
  data () {
    return {
    items: ['Brucoši','KSET','VIP'],
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