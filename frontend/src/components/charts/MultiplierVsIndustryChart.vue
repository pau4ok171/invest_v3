<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/multiplierVsIndustryChart";

export default defineComponent({
  name: "MultiplierVsIndustryChart",
  data() {
    return {
      chartOpts: chartOpts
    }
  },
})
</script>

<template>
<div class="detail-multiple-vs-industry-chart">
  <charts
    :options="chartOpts"
    :constructorType="'chart'"
  />
</div>
</template>

<style>
.detail-multiple-vs-industry-chart {
    height: 364px;
}
.detail-multiple-vs-industry-chart svg {
  height: auto;
  width: auto;
}
</style>