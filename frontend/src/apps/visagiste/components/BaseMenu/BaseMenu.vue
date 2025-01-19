<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "BaseMenu",
  data() {
    return {
      isActive: false,
    }
  },
  methods: {
    clickHandler(event: Event) {
      const target = event.target as HTMLDivElement
      if (target.parentNode?.parentNode !== this.$el) {
        this.isActive = false
        document.removeEventListener('click', this.clickHandler)
      }
    }
  },
  watch: {
    isActive(value) {
      if (value) {
        document.addEventListener('click', this.clickHandler)
      }
    }
  }
})
</script>

<template>
<div class="base-menu">
  <div @click="isActive=!isActive">
    <slot name="activator"/>
  </div>

  <div v-if="isActive">
    <slot name="list"/>
  </div>

</div>
</template>

<style scoped>
.base-menu{
  position: relative;
}
</style>