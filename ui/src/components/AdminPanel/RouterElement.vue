<template>
  <button
    type="button"
    class="router-element"
    v-bind="$attrs"
    @click="$router.push(link)"
  >
    <slot>
      <span class="router-element__label">{{ name }}</span>
      <i v-if="icon" :class="['pi', icon, 'router-element__icon']"></i>
    </slot>
  </button>
</template>

<script>
export default {
  name: 'RouterElement',
  props: {
    name: { type: String, default: '' },
    link: { type: String, required: true },
    icon: { type: String, default: '' }
  }
}
</script>

<style scoped>
.router-element {
  align-items: center;  
  gap: 6px;
  background: transparent;
  border: 0;
  cursor: pointer;
  padding: 0;
  color: white;
}
.router-element__icon {
  margin-left: 0.5rem;
  font-size: 1rem;
  line-height: 1;
}
</style>
