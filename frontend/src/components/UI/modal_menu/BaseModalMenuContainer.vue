<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "BaseModalMenuContainer",
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    close() {
      this.isOpen=false
    },
  },
})
</script>

<template>
<div>

  <div @click="isOpen=true">
    <slot name="button"/>
  </div>

  <teleport v-if="isOpen" to="body">
    <div>
      <slot :close="close" name="menu"/>
    </div>
  </teleport>

</div>
</template>
