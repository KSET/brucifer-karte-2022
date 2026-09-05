<template>
  <button
    type="button"
    class="router-element"
    v-bind="$attrs"
    @click="navigate"
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
    link: {
      type: String,
      default: undefined,
      required: false,
      validator: (v) => typeof v === 'string' && v.length > 0
    },
    label: { type: Boolean, default: false },
    icon: { type: String, default: '' }
  },
  created() {
    if (!this.label && !this.link) {
      console.warn(
        `[RouterElement] "${this.name}" has no link; pass :label="true" if it is meant to be a heading.`
      )
    }
  },
  methods: {
    navigate() {
      if (this.label) return
      if (this.link) this.$router.push(this.link)
    }
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
