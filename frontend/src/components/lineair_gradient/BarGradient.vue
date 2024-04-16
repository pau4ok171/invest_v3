<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "BarGradient"
})
</script>

<template>
  <svg height="0" width="0">
    <linearGradient id="BarGradient">
      <stop offset="0%" stop-color="rgb(21, 27, 36)" stop-opacity="0.5"></stop>
      <stop offset="100%" stop-color="rgb(21, 27, 36)" stop-opacity="0.8"></stop>
    </linearGradient>
  </svg>
</template>

<style scoped>

</style>