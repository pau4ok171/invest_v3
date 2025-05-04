<script setup lang="ts">
// Composables
import { useFinancialFormatter } from '@/composables/formatter'

// Utilities
import { computed } from 'vue'

// Types
import type { PropType } from 'vue'
import type { FinUnit } from '@/composables/formatter'
import type { Options, Point } from 'highcharts'

// Interfaces
interface ChartData {
  currency: string
  finUnit: FinUnit
  finData: FinData[]
}
interface FinData {
  name: string
  value: number
}

const props = defineProps({
  data: {
    type: Object as PropType<ChartData>,
    required: true,
  },
  title: String,
})

const { fin } = useFinancialFormatter()

const options = computed<Options>(
  () =>
    ({
      chart: {
        backgroundColor: 'transparent',
        spacing: [0, 0, 10, 0],
      },
      title: {
        text: props.title || '',
        align: 'left',
        style: {
          color: 'rgb(var(--v-theme-on-surface))',
          fontWeight: 'light',
          fontSize: '1rem',
        },
      },
      series: [
        {
          type: 'treemap',
          layoutAlgorithm: 'squarified',
          clip: false,
          color: 'rgb(41, 201, 126)',
          data: props.data?.finData,
          borderColor: 'rgb(var(--v-theme-surface-bright))',
          borderWidth: 2,
          dataLabels: {
            align: 'left',
            verticalAlign: 'top',
            padding: 4,
            useHTML: true,
            formatter: function () {
              const point = this as Point & { value: number }
              if (point.shapeArgs?.width && point.shapeArgs.width < 80)
                return ''
              return `
          <div class="d-flex flex-column text-caption">
            <div class="font-weight-medium">${point.name}</div>
            <div>
              ${fin({
                currency: props.data?.currency,
                value: point.value,
                finUnit: props.data?.finUnit,
              })}
            </div>
          </div>
        `
            },
          },
        },
      ],
      plotOptions: {
        series: {
          states: {
            hover: {
              enabled: false,
            },
          },
        },
      },
      tooltip: {
        outside: true,
        useHTML: true,
        formatter: function () {
          const point = this as Point & { value: number }
          const value = fin({
            currency: props.data?.currency,
            value: point.value,
            finUnit: props.data?.finUnit,
          })
          return `<div class="treemap-chart__tooltip">${point.name}: ${value}</div>`
        },
        positioner: function (labelWidth, labelHeight, point) {
          return {
            x: point.plotX + this.chart.plotLeft - labelWidth / 2,
            y: point.plotY + this.chart.plotTop - labelHeight / 2,
          }
        },
      },
    }) satisfies Options
)
</script>

<template>
  <div class="treemap-chart">
    <charts
      class="treemap-chart__chart"
      constructorType="chart"
      :options="options"
    />
  </div>
</template>

<style lang="scss">
.treemap-chart {
  &__tooltip {
    background-color: rgb(var(--v-theme-surface));
    padding: 8px;
    color: rgb(var(--v-theme-on-surface));
    font-size: 0.75rem;
    font-weight: 400;
    border-radius: 8px;
  }
}
</style>
