<script setup lang="ts">
// Components
import DataNotAvailable from '@/components/charts/DataNotAvailable.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, onBeforeMount, ref, shallowRef } from 'vue'
import { chartOpts } from '@/components/charts/fundamentalSummaryChart'

const store = useCompanyDetailStore()
const company = computed(() => store.company)

const chartOptions = ref(chartOpts)
const available = shallowRef(false)

function getChartData() {
  if (!company.value.reports) {
    available.value = false
    return null
  }
  const report = company.value.reports[0]
  if (!report) {
    available.value = false
    return null
  }
  const currency_symbol = company.value.formatting.primaryCurrencySymbol
  const scale = report.scale
  const market_cap = (company.value.price_data.capitalisation || 0) / 1000000000
  const revenue = report.sales
  const earnings = report.income_net
  return {
    market_cap: {
      value: market_cap.toFixed(0),
      unit: scale,
      currency_iso: currency_symbol,
      ratio: (market_cap / market_cap) * 100,
    },
    revenue: {
      value: revenue.toFixed(0),
      unit: scale,
      currency_iso: currency_symbol,
      ratio: (revenue / market_cap) * 100,
    },
    earnings: {
      value: earnings.toFixed(0),
      unit: scale,
      currency_iso: currency_symbol,
      ratio: (earnings / market_cap) * 100,
    },
  }
}

function getChartSeries() {
  const chartData = getChartData()
  if (!chartData) return []
  return [
    {
      name: 'Market Cap',
      enableMouseTracking: false,
      data: [
        {
          color: 'rgb(62, 72, 85)',
          radius: '65%',
          innerRadius: '100%',
          y: chartData.market_cap.ratio,
          label: `${chartData.earnings.currency_iso}${chartData.market_cap.value}${chartData.earnings.unit}`,
          dataLabels: {
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format:
              '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 36,
          },
        },
      ],
    },
    {
      name: 'Revenue',
      enableMouseTracking: false,
      data: [
        {
          color: 'rgb(35, 148, 223)',
          radius: '85%',
          innerRadius: '100%',
          y: chartData.revenue.ratio,
          label: `${chartData.earnings.currency_iso}${chartData.revenue.value}${chartData.earnings.unit}`,
          dataLabels: {
            allowOverlap: true,
            crop: false,
            overflow: 'allow',
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format:
              '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 130,
            y: -110,
          },
        },
      ],
    },
    {
      name: 'Earnings',
      enableMouseTracking: false,
      data: [
        {
          color: 'rgb(113, 231, 214)',
          radius: '65%',
          innerRadius: '85%',
          y: chartData.earnings.ratio,
          label: `${chartData.earnings.currency_iso}${chartData.earnings.value}${chartData.earnings.unit}`,
          dataLabels: {
            allowOverlap: true,
            crop: false,
            overflow: 'allow',
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format:
              '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 30,
            y: -160,
          },
        },
      ],
    },
  ]
}

function drawLabels(event: Event) {
  if (!available.value) return null
  const chart = event.target as any
  const rDiffX = 10
  const rDiffY = 17
  const rOffsetY = -67
  const rData = chart.series[1].data

  const rStartX = rData[0].plotX + rDiffX
  const rStartY = rData[0].plotY + rDiffY
  const rFinishX = rStartX
  const rFinishY = rStartY + rOffsetY

  chart.renderer
    .path(['M', rStartX, rStartY, 'L', rFinishX, rFinishY])
    .attr({
      'stroke-width': 1,
      stroke: '#71E7D6',
      fill: 'transparent',
      zIndex: 6,
    })
    .add()
  chart.renderer
    .circle()
    .attr({ cx: rFinishX, cy: rFinishY, fill: '#71E7D6', r: 2.5 })
    .add()

  const eData = chart.series[2].data
  const eStartX = eData[0].plotX + 15
  const eStartY = eData[0].plotY - 15
  const eMiddleX = eStartX + 18
  const eMiddleY = eStartY - 18

  const eFinishX = eMiddleX + 27
  const eFinishY = eMiddleY

  chart.renderer
    .path([
      'M',
      eStartX,
      eStartY,
      'L',
      eMiddleX,
      eMiddleY,
      'L',
      eFinishX,
      eFinishY,
    ])
    .attr({
      'stroke-width': 1,
      stroke: '#2394DF',
      fill: 'transparent',
      zIndex: 6,
    })
    .add()
  chart.renderer
    .circle()
    .attr({ cx: eFinishX, cy: eFinishY, fill: '#2394DF', r: 2.5 })
    .add()
}

onBeforeMount(() => {
  chartOptions.value.series = getChartSeries() as []
  chartOptions.value.chart.events = { load: drawLabels }
})
</script>

<template>
  <div class="fundamental-summary-chart">
    <DataNotAvailable
      v-if="!available"
      chart-name="Fundamental Summary Chart"
    />
    <charts
      v-else
      ref="fundamentalSummaryChart"
      :constructorType="'chart'"
      :options="chartOptions"
    />
  </div>
</template>

<style>
.fundamental-summary-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}
.fundamental-summary-chart svg {
  width: auto;
  height: auto;
}
.fundamental-summary-chart__middle-label {
  line-height: 1.7;
  fill: rgba(255, 255, 255, 0.7);
}
</style>
