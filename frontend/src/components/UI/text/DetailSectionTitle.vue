<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "DetailSectionTitle"
})
</script>

<template>
  <h2 class="detail-section__title"><slot/></h2>
</template>

<style scoped>
  .detail-section__title {
    font-size: 2rem;
    line-height: 1.5;
    font-weight: 500;
    margin-bottom: 8px;
  }
</style>