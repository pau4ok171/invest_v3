<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "DetailAnalysisDesc"
})
</script>

<template>
  <p class="detail-analysis__desc">
    <slot/>
  </p>
</template>

<style>
  .detail-analysis__desc {
    color: #fff;
    font-size: 1.4rem;
    line-height: 1.7;
    margin-bottom: 16px;
}
</style>