<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/earningsRevenueChart";

export default defineComponent({
  name: "EarningsRevenueChart",
  data() {
    return {
      chartOpts: chartOpts
    }
  }
})
</script>

<template>
<div class="earnings-revenue-chart">
  <charts
    :constructorType="'chart'"
    :options="chartOpts"
  />
</div>
</template>

<style>
.earnings-revenue-chart {
  height: 248px;
}
.earnings-revenue-chart svg {
  height: auto;
  width: auto;
}
</style>