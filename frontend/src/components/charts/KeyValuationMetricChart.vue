<script setup lang="ts">
// Components
import DataNotAvailable from '@/components/charts/DataNotAvailable.vue'
import FetchingData from '@/components/charts/FetchingData.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, onBeforeMount, ref, shallowRef, watch } from 'vue'
import { chartOpts as _chartOpts } from '@/components/charts/keyValuationMetricChart'

// Types
import type { PropType } from 'vue'
import type { FairValueTab } from '@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue'
import type { Chart } from 'highcharts-vue'

interface ChartData {
  name: string
  value: number
  unit: string
  currency_iso: string
  mult?: number
}

const props = defineProps({
  tabs: {
    type: Object as PropType<FairValueTab[]>,
    required: true,
  },
  selected: {
    type: Object as PropType<FairValueTab>,
    required: true,
  },
})

const store = useCompanyDetailStore()
const company = computed(() => store.company)

const chartOpts = ref(_chartOpts)
const chartData = ref<Record<string, ChartData>>({})

const available = shallowRef(true)

const name = computed(() => props.selected.name)
const value = computed(() => {
  if (!chartData.value.length) return

  if (props.selected?.id === 'pe') return chartData.value.earnings.mult
  if (props.selected?.id === 'pb') return chartData.value.book.mult
  if (props.selected?.id === 'ps') return chartData.value.sales.mult
})

const chartRef = ref<typeof Chart>()

function getData(): Record<string, ChartData> {
  if (
    !company.value.reports.length &&
    !company.value.price_data?.capitalisation
  ) {
    available.value = false
    return {}
  } else {
    available.value = true
  }

  const report = company.value.reports[0]
  const earnings = report.income_net || 0
  const equity = report.equity || 0
  const revenue = report.sales || 0
  const reportUnit = report.scale
  const marketCap =
    humanize(company.value.price_data.capitalisation, reportUnit) || 0
  const currency_symbol = company.value.formatting.primaryCurrencySymbol || ''

  return {
    sales: {
      name: 'Sales',
      value: revenue,
      unit: reportUnit,
      currency_iso: currency_symbol,
      mult: Number((revenue / marketCap).toFixed(1)),
    },
    book: {
      name: 'Book',
      value: equity,
      unit: reportUnit,
      currency_iso: currency_symbol,
      mult: Number((equity / marketCap).toFixed(1)),
    },
    earnings: {
      name: 'Earnings',
      value: earnings,
      unit: reportUnit,
      currency_iso: currency_symbol,
      mult: Number((earnings / marketCap).toFixed(1)),
    },
    marketCap: {
      name: 'Market Cap',
      value: marketCap,
      unit: reportUnit,
      currency_iso: currency_symbol,
    },
  }
}

function humanize(value: number = 0, unitFormat: string = '') {
  for (const unit of ['', 't', 'M', 'B', 'T']) {
    if (Math.abs(value) < 1000 || unit === unitFormat)
      return Number(value.toFixed(2))
    value /= 1000
  }
  return Number(value.toFixed(2))
}

function getSeries() {
  const data = chartData.value
  if (!data.length) return []

  return [
    {
      name: 'Market Cap',
      data: [
        {
          name: 'Market Cap',
          y: data.marketCap.value,
          color: 'rgb(62, 72, 85)',
          radius: '65%',
          innerRadius: '100%',
          label: `${data.marketCap.currency_iso}${data.marketCap.value}${data.marketCap.unit}`,
          dataLabels: {
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format:
              '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
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
      name: 'Earnings',
      visible: true,
      data: [
        {
          name: 'Earnings',
          y: data.earnings.value,
          color: 'rgb(35, 148, 223)',
          radius: '65%',
          innerRadius: '100%',
          label: `${data.earnings.currency_iso}${data.earnings.value}${data.earnings.unit}`,
          dataLabels: {
            allowOverlap: true,
            // crop: true,
            overflow: 'allow',
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format:
              '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 0, // 153.5
            y: -184 / 2 - 64,
          },
        },
      ],
    },
    {
      name: 'Book',
      visible: false,
      data: [
        {
          name: 'Book',
          y: data.book.value,
          color: 'rgb(35, 148, 223)',
          radius: '65%',
          innerRadius: '100%',
          label: `${data.book.currency_iso}${data.book.value}${data.book.unit}`,
          dataLabels: {
            allowOverlap: true,
            // crop: true,
            overflow: 'allow',
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format:
              '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 0, // 153.5
            y: -184 / 2 - 64,
          },
        },
      ],
    },
    {
      name: 'Sales',
      visible: false,
      data: [
        {
          name: 'Sales',
          y: data.sales.value,
          color: 'rgb(35, 148, 223)',
          radius: '65%',
          innerRadius: '100%',
          label: `${data.sales.currency_iso}${data.sales.value}${data.sales.unit}`,
          dataLabels: {
            allowOverlap: true,
            // crop: true,
            overflow: 'allow',
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format:
              '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 0, // 153.5
            y: -184 / 2 - 64,
          },
        },
      ],
    },
  ]
}

function getAxisY() {
  const data = chartData.value
  if (!data.length) return

  return {
    min: 0,
    max: data.marketCap.value,
    lineWidth: 0,
    tickPositions: [],
  }
}

function draw(event: Event) {
  const chart = event.target as typeof Chart | null

  if (chart == null || !chart.series.length) return

  const plotOffsetX = chart.plotBox.x
  const plotOffsetY = chart.plotBox.y
  const lineH = 64
  const lineX = plotOffsetX + chart.series[0].data[0].graphic.pathArray[0][1]
  const lineY =
    plotOffsetY + chart.series[0].data[0].graphic.pathArray[0][2] - lineH
  const lineW = 0.5

  chart.renderer
    .rect(lineX, lineY, lineW, lineH)
    .attr({
      fill: '#2394df',
      zIndex: 10,
    })
    .add()

  chart.renderer
    .circle()
    .attr({
      cx: lineX,
      cy: lineY,
      fill: '#2394df',
      r: 2.5,
      zIndex: 10,
    })
    .add()
}

onBeforeMount(() => {
  chartData.value = getData()
  chartOpts.value.series = getSeries() as []
  chartOpts.value.yAxis = getAxisY() as {}
  chartOpts.value.chart.events = { load: draw }
})

watch(
  () => props.tabs,
  () => {
    const chart = chartRef.value?.chart

    if (!chart || !chart.series.length) return

    chart.series[1].visible = false
    chart.series[2].visible = false
    chart.series[3].visible = false
    chart.series[props.selected.value].visible = true

    chart.renderSeries()
  },
  { deep: true }
)
</script>

<template>
  <div class="detail-key-valuation-metric__chart-wrapper">
    <FetchingData v-if="store.fetchingCompany" />

    <div v-else-if="available" class="detail-key-valuation-metric__chart">
      <charts :options="chartOpts" constructorType="chart" ref="chartRef" />

      <div class="detail-key-valuation-metric__chart-metric">
        <h4 class="detail-key-valuation-metric__chart-metric-value">
          {{ value }}x
        </h4>
        <span class="detail-key-valuation-metric__chart-metric-text"
          >{{ name }} Ratio</span
        >
      </div>
    </div>

    <DataNotAvailable v-else chart-name="Key Valuation Metric  Chart" />
  </div>
</template>

<style lang="scss">
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
  font-size: 2.25rem;
  font-weight: normal;
}
.detail-key-valuation-metric__chart-metric-text {
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5;
  color: rgba(var(--v-theme-on-surface-light), 0.7);
}
</style>
