<script setup lang="ts">
// Components
import BackgroundGradient from '@/components/lineair_gradient/BackgroundGradient.vue'
import ChartGradient from '@/components/lineair_gradient/ChartGradient.vue'

// Utilities
import { ref } from 'vue'
import { chartOpts as _chartOpts } from '@/components/charts/historicalMultiplierChart'

const chartOpts = ref(_chartOpts)
</script>

<template>
  <div class="detail-historical-metrics-chart">
    <charts constructorType="stockChart" :options="chartOpts" />
    <background-gradient />
    <chart-gradient />
  </div>
</template>

<style lang="scss">
.detail-historical-metrics-chart svg {
  height: auto;
  width: auto;
}
.historical-metrics-chart__tooltip {
  background: rgb(0, 0, 0);
  padding: 8px;
  margin: 0;
  width: 340px;
  max-width: 340px;
}
.historical-metrics-chart__tooltip-table {
  width: 100%;
  table-layout: auto;
  margin: 0 auto;
  border-spacing: 0;
  color: rgb(255, 255, 255);
  background-color: rgb(0, 0, 0);
  user-select: none;
}
.historical-metrics-chart__tooltip-table thead tr th {
  line-height: 1.5;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  text-transform: capitalize;
  font-size: .75rem;
}
.historical-metrics-chart__tooltip-title {
  line-height: 1.5;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  vertical-align: top;
  font-size: .75rem;
  color: rgba(255, 255, 255, 0.5);
}
.historical-metrics-chart__tooltip-value {
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.5;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  vertical-align: top;
  font-size: .75rem;
  width: 100%;
  padding-left: 16px;
  font-weight: 500;
  color: rgb(35, 148, 223);
}
</style>
