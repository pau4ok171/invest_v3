<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CompanyDetailContentGroup",
  props: {
    useGrid: {
      type: Boolean,
      default: false
    },
    useGridRow: {
      type: Boolean,
      default: false
    },
  }
})
</script>

<template>
  <div :class="[{'detail-section__content-group--grid-row': useGridRow}, {'detail-section__content-group--grid': useGrid}]">
    <slot/>
  </div>
</template>

<style scoped>
  .detail-section__content-group--grid-row {
    display: grid;
    grid-row: span 2 / auto;
  }
  .detail-section__content-group--grid {
    display: grid;
    grid-column: span 1 / auto;
  }
</style>