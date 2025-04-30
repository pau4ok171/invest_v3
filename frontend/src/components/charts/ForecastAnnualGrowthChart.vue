<script setup lang="ts">
// Utilities
import { computed } from 'vue'

// Types
import type { PropType } from 'vue'
import type { Options } from 'highcharts'

// Constants
const CHART_HEIGHT = 250

// Interfaces
interface SeriesOption {
  name: string
  value: number
  prefix?: string
  suffix?: string
}

const props = defineProps({
  data: {
    type: Object as PropType<SeriesOption[]>,
    required: true,
  },
  title: String,
})

const options = computed<Options>(
  () =>
    ({
      chart: {
        type: 'column',
        height: CHART_HEIGHT,
        backgroundColor: 'transparent',
        spacing: [10, 8, 10, 8],
      },
      accessibility: {
        enabled: false,
      },
      title: {
        text: undefined,
      },
      credits: {
        enabled: false,
      },
      legend: {
        enabled: false,
      },
      tooltip: {
        enabled: false,
      },
      xAxis: {
        labels: {
          enabled: false,
        },
        tickWidth: 0,
        lineColor: 'rgb(var(--v-theme-on-surface))',
      },
      yAxis: {
        visible: false,
      },
      series: props.data.map((o, i) => ({
        type: 'column',
        name: o.name,
        data: [o.value],
        color: `rgb(var(--v-theme-hc-series${i + 1}-color))`,
        dataLabels: [
          {
            enabled: true,
            verticalAlign: 'bottom',
            formatter: () => {
              return `${o.prefix || ''}${o.value.toFixed(1)}${o.suffix || ''}`
            },
            color: 'rgb(var(--v-theme-on-surface))',
            style: {
              fontSize: '1.25rem',
              fontWeight: '500',
              textOutline: 'none',
              stroke: 'none',
              color: 'rgb(var(--v-theme-on-surface))',
            },
          },
          {
            enabled: true,
            inside: true,
            verticalAlign: 'top',
            align: 'left',
            style: {
              color: `rgb(var(--v-theme-on-hc-series${i + 1}-color))`,
              fontSize: '0.875rem',
              textOutline: 'none',
              stroke: 'none',
              color: 'rgb(var(--v-theme-on-surface))',
            },
            formatter: function () {
              return this.series.name
            },
            y: 4,
          },
        ],
      })),
      plotOptions: {
        column: {
          borderWidth: 0,
          pointPadding: 0,
          groupPadding: 0.02,
          states: {
            inactive: {
              opacity: 1,
            },
          },
        },
      },
    }) satisfies Options
)
</script>

<template>
  <div class="forecast-annual-earnings-growth-chart">
    <charts
      class="forecast-annual-earnings-growth-chart__chart"
      constructorType="chart"
      :options="options"
    />
    <div class="text-h6 mb-4 ml-2">{{ title || '' }}</div>
  </div>
</template>
