<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "DetailAnalysisTitle"
})
</script>

<template>
<h2 class="detail-analysis__title">
  <slot/>
</h2>
</template>

<style>
.detail-analysis__title {
  font-size: 2.4rem;
  margin: 16px 0 24px;
  line-height: 1.25;
  font-weight: 500;
}
.detail-analysis__title span {
  color: rgba(255, 255, 255, .2);
  line-height: .75;
  padding-right: 16px;
}
</style>