<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/fundamentalSummaryChart";

export default defineComponent({
  name: "FundamentalSummaryChart",
  data() {
    return {
      chartOpts: chartOpts
    }
  }
})
</script>

<template>
<div class="fundamental-summary-chart">
  <charts
    :constructorType="'chart'"
    :options="chartOpts"
  />
</div>
</template>

<style>
.fundamental-summary-chart svg {
  width: auto;
  height: auto;
}
.fundamental-summary-chart__middle-label {
  line-height: 1.7;
  fill: rgba(255, 255, 255, .7);
}
</style>