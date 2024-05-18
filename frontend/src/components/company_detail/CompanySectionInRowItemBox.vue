<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "CompanySectionInRowItemBox"
})
</script>

<template>
<div class="detail-section__in-row-item-box">
  <slot/>
</div>
</template>

<style>
.detail-section__in-row-item-box {
  display: flex;
  flex-flow: wrap;
  justify-content: left;
}
.detail-section__in-row-item {
  padding-bottom: 24px;
  margin-top: 32px;
  max-width: 100%;
  flex: 0 0 50%;
}
.detail-section__in-row-item:first-child {
  padding-right: 16px;
}
.detail-section__in-row-item:last-child {
  padding-left: 16px;
}
</style>