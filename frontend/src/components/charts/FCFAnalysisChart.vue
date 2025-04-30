<script setup lang="ts">
// Composables
import { useFinancialFormatter } from '@/composables/formatter'

// Utilities
import { computed } from 'vue'

// Types
import type { Options } from 'highcharts'

const { fin } = useFinancialFormatter()

const data = {
  currency: 'US$',
  finUnit: 'M',
  finData: [
    { value: 72880.0, name: 'Earnings' },
    { value: 1864.0, name: 'Depreciation & Amortisation' },
    { value: 4737.0, name: 'Stock Based Compensation' },
    { value: -9949.0, name: 'Net Working Capital' },
    { value: -8679.0, name: 'Others' },
    { value: 60853.0, name: 'Free Cash Flow' },
  ],
}

// Helpers
const getSeriesColor = (item) => {
  if (item.name === 'Earnings') return 'rgb(var(--v-theme-hc-series2-color))'
  if (item.name === 'Free Cash Flow')
    return 'rgb(var(--v-theme-hc-series3-color))'
  if (item.value >= 0) return 'rgb(var(--v-theme-success))'
  return 'rgb(var(--v-theme-error))'
}

const options = computed<Options>(
  () =>
    ({
      chart: {
        type: 'waterfall',
        backgroundColor: 'transparent',
      },
      title: {
        text: undefined,
      },
      legend: {
        enabled: false,
      },
      yAxis: {
        title: undefined,
        enabled: false,
        gridLineWidth: 0,
        labels: {
          enabled: false,
        },
      },
      xAxis: {
        type: 'category',
        lineColor: 'rgb(var(--v-theme-on-surface))',
        labels: {
          style: {
            color: 'rgb(var(--v-theme-on-surface))',
          },
        },
      },
      tooltip: {
        format: '{point.name}',
        backgroundColor: 'rgb(var(--v-theme-surface-bright))',
        style: {
          color: 'rgb(var(--v-theme-on-surface-bright))',
        },
      },
      series: [
        {
          type: 'waterfall',
          data: data.finData.map((item) => ({
            isSum: item.name === 'Free Cash Flow' ? true : undefined,
            color: getSeriesColor(item),
            name: item.name,
            y: item.value,
          })),
          groupPadding: 0.01,
          pointPadding: 0.01,
          borderRadius: 0,
          borderWidth: 0,
          dataLabels: {
            enabled: true,
            verticalAlign: 'top',
            align: 'left',
            y: -20,
            style: {
              color: 'rgb(var(--v-theme-on-surface))',
              fontSize: '0.75rem',
              fontWeight: '500',
              textOutline: 'none',
              stroke: 'none',
            },
            formatter: function () {
              return fin({
                currency: data.currency,
                finUnit: data.finUnit,
                value: this.y,
              })
            },
          },
        },
      ],
    }) satisfies Options
)
</script>

<template>
  <div>
    <charts
      ref="chartRef"
      class="fcf-analysis-chart__chart"
      constructorType="chart"
      :options="options"
    />
  </div>
</template>
