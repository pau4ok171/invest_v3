<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/keyValuationMetricChart";

export default defineComponent({
  name: "KeyValuationMetricChart",
  data() {
    return {
      chartOpts: chartOpts
    }
  },
})
</script>

<template>
<div class="detail-key-valuation-metric__chart-wrapper">
  <div class="detail-key-valuation-metric__chart">

    <charts
      :options="chartOpts"
      :constructorType="'chart'"
    />

    <div class="detail-key-valuation-metric__chart-metric">
      <h4 class="detail-key-valuation-metric__chart-metric-value">2.6x</h4>
      <span class="detail-key-valuation-metric__chart-metric-text">PE Ratio</span>
    </div>

  </div>
</div>
</template>

<style>
.detail-key-valuation-metric__chart-wrapper {
    display: grid;
    height: 280px;
}
.detail-key-valuation-metric__chart {
    display: grid;
    grid-template-columns: auto 200px;
    grid-template-rows: auto;
}
.detail-key-valuation-metric__chart svg {
  width: auto;
  height: auto;
}
.detail-key-valuation-metric__chart-metric {
    display: grid;
    place-content: center start;
}
.detail-key-valuation-metric__chart-metric-value {
    line-height: 1.25;
    font-size: 3.6rem;
    font-weight: normal;
}
.detail-key-valuation-metric__chart-metric-text {
    font-size: 1.6rem;
    font-weight: 500;
    line-height: 1.5;
    color: rgba(255, 255, 255, .7);
}
</style>