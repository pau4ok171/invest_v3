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
@use 'vuetify/settings' as vuetify;

.detail-historical-metrics-chart svg {
  height: auto;
  width: auto;
}
.historical-metrics-chart__tooltip {
  background: rgb(var(--v-theme-surface-bright));
  padding: 8px;
  margin: 0;
  width: 340px;
  max-width: 340px;

  @media #{map-get(vuetify.$display-breakpoints, 'md-and-down')} {
    width: 180px;
  }
}
.historical-metrics-chart__tooltip-table {
  width: 100%;
  table-layout: auto;
  margin: 0 auto;
  border-spacing: 0;
  color: rgb(var(--v-theme-on-surface-light));
  background-color: rgb(var(--v-theme-surface-bright));
  user-select: none;
}
.historical-metrics-chart__tooltip-table thead tr th {
  line-height: 1.5;
  text-align: left;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.2);
  text-transform: capitalize;
  font-size: 0.75rem;
}
.historical-metrics-chart__tooltip-title {
  line-height: 1.5;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.2);
  vertical-align: top;
  font-size: 0.75rem;
  color: rgba(var(--v-theme-on-surface-light), 0.5);
}
.historical-metrics-chart__tooltip-value {
  color: rgba(var(--v-theme-on-surface-light), 0.5);
  line-height: 1.5;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.2);
  vertical-align: top;
  font-size: 0.75rem;
  width: 100%;
  padding-left: 16px;
  font-weight: 500;
  color: rgb(35, 148, 223);
}
</style>
