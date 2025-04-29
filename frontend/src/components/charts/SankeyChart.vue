<script setup lang="ts">
// Components
import YearSlider from '@/components/charts/YearSlider.vue'

// Composables
import { useFinancialFormatter } from '@/composables/formatter'

// Utilities
import { computed, ref, watch } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type {
  Chart,
  Options,
  SankeyNodeObject,
  Point,
  SeriesSankeyOptions,
} from 'highcharts'
import type { FinUnit } from '@/composables/formatter'

// Constants
const CHART_HEIGHT = 500

// Interfaces
interface ChartData {
  currency: string
  financialUnit: FinUnit
  financialData: FinancialData
}
interface FinancialData {
  [year: number]: Record<string, number>
}
interface SankeyPoint extends Point {
  formatPrefix: string
  name: string
  sum: number
  weight: number
  toNode: SankeyNode
  fromNode: SankeyNode
}
interface SankeyNode extends SankeyNodeObject {
  formatPrefix: string
  name: string
  sum: number
}

const isSankeyNode = (point: SankeyPoint | SankeyNode): point is SankeyNode => {
  return point.formatPrefix === 'node'
}

const { fin } = useFinancialFormatter()

const chartRef = ref<{ chart: Chart } | null>(null)
const currentDate = DateTime.now()
const selectedYear = ref<number>(currentDate.year)

const data: ChartData = {
  currency: 'US$',
  financialUnit: 'M',
  financialData: {
    2014: {
      Revenue: 4575,
      'Cost of Sales': 2056,
      'Gross Profit': 2519,
      Expenses: 1935,
      'General & Administrative': 477,
      'Non-Operating Expense': 111,
      'Research & Development': 1348,
      'Sales & Marketing': 0,
      Earnings: 584,
    },
    2015: {
      Revenue: 4860,
      'Cost of Sales': 2141,
      'Gross Profit': 2719,
      Expenses: 2119,
      'General & Administrative': 545,
      'Non-Operating Expense': 223,
      'Research & Development': 1336,
      'Sales & Marketing': 15,
      Earnings: 600,
    },
    2016: {
      Revenue: 6138,
      'Cost of Sales': 2587,
      'Gross Profit': 3551,
      Expenses: 2331,
      'General & Administrative': 548,
      'Non-Operating Expense': 340,
      'Research & Development': 1413,
      'Sales & Marketing': 30,
      Earnings: 1220,
    },
    2017: {
      Revenue: 8976,
      'Cost of Sales': 3652,
      'Gross Profit': 5324,
      Expenses: 2742,
      'General & Administrative': 770,
      'Non-Operating Expense': 288,
      'Research & Development': 1684,
      'Sales & Marketing': 0,
      Earnings: 2582,
    },
    2018: {
      Revenue: 12422,
      'Cost of Sales': 4657,
      'Gross Profit': 7765,
      Expenses: 3071,
      'General & Administrative': 946,
      'Non-Operating Expense': -111,
      'Research & Development': 2236,
      'Sales & Marketing': 0,
      Earnings: 4694,
    },
    2019: {
      Revenue: 10018,
      'Cost of Sales': 4058,
      'Gross Profit': 5960,
      Expenses: 3549,
      'General & Administrative': 1072,
      'Non-Operating Expense': -261,
      'Research & Development': 2738,
      'Sales & Marketing': 0,
      Earnings: 2411,
    },
    2020: {
      Revenue: 14777,
      'Cost of Sales': 5361,
      'Gross Profit': 9416,
      Expenses: 5590,
      'General & Administrative': 1724,
      'Non-Operating Expense': 350,
      'Research & Development': 3516,
      'Sales & Marketing': 0,
      Earnings: 3826,
    },
    2021: {
      Revenue: 24274,
      'Cost of Sales': 8642,
      'Gross Profit': 15632,
      Expenses: 7426,
      'General & Administrative': 2078,
      'Non-Operating Expense': 400,
      'Research & Development': 4948,
      'Sales & Marketing': 0,
      Earnings: 8206,
    },
    2022: {
      Revenue: 28566,
      'Cost of Sales': 12044,
      'Gross Profit': 16522,
      Expenses: 10565,
      'General & Administrative': 2378,
      'Non-Operating Expense': 1334,
      'Research & Development': 6853,
      'Sales & Marketing': 0,
      Earnings: 5957,
    },
    2023: {
      Revenue: 44870,
      'Cost of Sales': 13527,
      'Gross Profit': 31343,
      Expenses: 12454,
      'General & Administrative': 2567,
      'Non-Operating Expense': 1725,
      'Research & Development': 8162,
      'Sales & Marketing': 0,
      Earnings: 18889,
    },
    2024: {
      Revenue: 113269,
      'Cost of Sales': 27343,
      'Gross Profit': 85926,
      Expenses: 22852,
      'General & Administrative': 3228,
      'Non-Operating Expense': 7959,
      'Research & Development': 11665,
      'Sales & Marketing': 0,
      Earnings: 63074,
    },
    2025: {
      Revenue: 130497,
      'Cost of Sales': 32639,
      'Gross Profit': 97858,
      Expenses: 24978,
      'General & Administrative': 3491,
      'Non-Operating Expense': 8573,
      'Research & Development': 12914,
      'Sales & Marketing': 0,
      Earnings: 72880,
    },
  },
}

const options = computed<Options>(
  () =>
    ({
      chart: {
        type: 'sankey',
        height: CHART_HEIGHT,
        backgroundColor: 'transparent',
        marginTop: 80,
        marginLeft: 40,
        marginRight: 40,
      },
      title: {
        text: undefined,
      },
      series: [
        {
          type: 'sankey',
          keys: ['from', 'to', 'weight'],
          data: getSankeyData(selectedYear.value),
          nodes: getSankeyNodes(),
          nodePadding: 60,
          nodeWidth: 20,
          name: 'Financial Flow',
          linkOpacity: 0.25,
          linkColorMode: 'to',
          states: {
            hover: {
              linkOpacity: 0.25,
            },
          },
          dataLabels: {
            enabled: true,
            backgroundColor: 'transparent',
            color: 'rgb(var(--v-theme-on-surface))',
            borderWidth: 0,
            padding: 0,
            verticalAlign: 'top',
            overflow: 'allow',
            y: -40,
            useHTML: true,
            nodeFormatter: function () {
              const point = (
                'point' in this ? (this as any).point : null
              ) as SankeyPoint | null
              if (!point) return ''

              return `
                <div class="text-truncate">${point.name}</div>
                <div class="text-medium-emphasis">
                  ${fin({
                    currency: data.currency,
                    value: point.sum,
                    finUnit: data.financialUnit,
                  })}
                </div>
              `
            },
            style: {
              color: '#333',
              fontSize: '0.875rem',
              fontWeight: '500',
            },
          },
        },
      ],
      tooltip: {
        followPointer: false,
        outside: true,
        padding: 0,
        useHTML: true,
        formatter: function () {
          const point = (
            'point' in this ? (this as any).point : null
          ) as SankeyPoint | null
          if (!point) return ''

          if (isSankeyNode(point)) {
            return getNodeTooltip(point)
          }

          return getPointTooltip(point)
        },
        positioner: function (labelWidth, labelHeight, point) {
          return {
            x: point.plotX + this.chart.plotLeft - labelWidth / 2,
            y: point.plotY + this.chart.plotTop - labelHeight,
          }
        },
      },
    }) satisfies Options
)

// Helper functions
function updateChart() {
  if (!chartRef.value) return
  chartRef.value.chart.series[0].update({
    data: getSankeyData(selectedYear.value),
  } as SeriesSankeyOptions)
}
function getSankeyData(year: number) {
  const _data = data.financialData[year]
  return [
    ['Revenue', 'Gross Profit', _data['Gross Profit']],
    ['Revenue', 'Cost of Sales', _data['Cost of Sales']],
    ['Gross Profit', 'Earnings', _data['Earnings']],
    ['Gross Profit', 'Expenses', _data['Expenses']],
    ['Expenses', 'General & Administrative', _data['General & Administrative']],
    ['Expenses', 'Research & Development', _data['Research & Development']],
    [
      'Expenses',
      'Non-Operating Expense',
      Math.abs(_data['Non-Operating Expense']),
    ],
    ['Expenses', 'Sales & Marketing', _data['Sales & Marketing']],
  ]
}
function getSankeyNodes() {
  return [
    {
      id: 'Revenue',
      color: 'rgb(35, 148, 223)',
    },
    {
      id: 'Cost of Sales',
      color: 'rgb(229, 176, 97)',
    },
    {
      id: 'Gross Profit',
      color: 'rgb(113, 231, 214)',
    },
    {
      id: 'Expenses',
      color: 'rgb(229, 176, 97)',
    },
    {
      id: 'General & Administrative',
      color: 'rgb(229, 176, 97)',
    },
    {
      id: 'Non-Operating Expense',
      color: 'rgb(229, 176, 97)',
    },
    {
      id: 'Research & Development',
      color: 'rgb(229, 176, 97)',
    },
    {
      id: 'Sales & Marketing',
      color: 'rgb(229, 176, 97)',
    },
    {
      id: 'Earnings',
      color: 'rgb(113, 231, 214)',
    },
  ]
}

const getNodeTooltip = (point: SankeyNode): string => {
  const name = point.name
  const sum = fin({
    currency: data.currency,
    value: point.sum,
    finUnit: data.financialUnit,
  })
  return `
    <div class="sankey-chart__tooltip text-subtitle-2">
      <div class="d-flex justify-space-between"><div>${name}</div><div>${sum}</div></div>
    </div>
  `
}

const getPointTooltip = (point: SankeyPoint): string => {
  const name = point.toNode.name
  const sum = fin({
    currency: data.currency,
    value: point.weight,
    finUnit: data.financialUnit,
  })
  const from = point.fromNode.name
  const weight = ((point.weight / point.fromNode.sum) * 100).toFixed(2) + '%'

  return `
    <div class="sankey-chart__tooltip text-subtitle-2">
      <div class="d-flex justify-space-between"><div>${name}</div><div>${sum}</div></div>
      <div class="sankey-chart__divider"></div>
      <div class="d-flex justify-space-between text-disabled"><div>${from}</div><div>${weight}</div></div>
    </div>
  `
}

watch(selectedYear, updateChart)
</script>

<template>
  <div class="sankey-chart">
    <year-slider
      :model-value="selectedYear"
      @update:model-value="(val: number) => (selectedYear = val)"
      :min-year="2014"
      :max-year="2025"
    />

    <charts
      ref="chartRef"
      class="sankey-chart__chart"
      constructor-type="chart"
      :options="options"
    />
  </div>
</template>

<style lang="scss">
.sankey-chart {
  &__tooltip {
    width: 340px;
    padding: 12px 8px;
    border-radius: 8px;
    color: rgb(var(--v-theme-on-surface));
    background-color: rgb(var(--v-theme-surface));
    pointer-events: none;
  }
  &__divider {
    width: 100%;
    height: 1px;
    margin: 4px 0;
    background-color: rgba(var(--v-theme-on-surface), 0.2);
  }
}
</style>
