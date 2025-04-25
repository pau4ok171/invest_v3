<script setup lang="ts">
// Composables
import { useFinancialFormatter } from '@/composables/formatter'

// Utilities
import { computed, ref } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type { Options } from 'highcharts'

// Constants
const CHART_HEIGHT = 500

const { fin } = useFinancialFormatter()

const currentDate = DateTime.now()
const selectedYear = ref<number>(currentDate.year)

const data = {
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
      accessibility: {
        point: {
          valueDescriptionFormat:
            '{index}. {point.from} to {point.to}: {point.weight}.',
        },
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
            y: -40, // Смещаем выше узла
            useHTML: true,
            nodeFormatter: function () {
              console.log(this)
              return `<div class="text-truncate">${this.point.name}</div><div class="text-medium-emphasis">${fin({ currency: data.currency, value: this.point.sum, finUnit: data.financialUnit })}</div>`
            },
            style: {
              color: '#333',
              fontSize: '0.875rem',
              fontWeight: '500',
            },
          },
        },
      ],
    }) satisfies Options
)

// Helper functions
function updateChart(year) {
  this.chart.series[0].update({
    data: this.getSankeyData(this.selectedYear),
  })
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
</script>

<template>
  <div class="sankey-chart">
    <charts
      class="sankey-chart__chart"
      constructor-type="chart"
      :options="options"
    />
  </div>
</template>

<style scoped lang="scss"></style>
