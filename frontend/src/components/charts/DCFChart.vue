<script setup lang="ts">
// Components
import DataNotAvailable from '@/components/charts/DataNotAvailable.vue'
import BarGradient from '@/components/lineair_gradient/BarGradient.vue'
import FailPattern from '@/components/patterns/FailPattern.vue'
import FetchingData from '@/components/charts/FetchingData.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref, watch } from 'vue'

// Types
import type { Chart, Options, Point, SeriesOptionsType } from 'highcharts'
import { SVGElement } from 'highcharts'

type ValuationStatus = 'undervalued' | 'overvalued' | 'aboutRight'

interface PlotBox {
  x: number
  y: number
  height: number
  width: number
}

interface ValuationDiff {
  type: string
  class: string
  color: string
}

const store = useCompanyDetailStore()
const company = computed(() => store.company)
const { t, locale } = useI18n()
const chartRef = ref<{ chart: Chart }>()
const available = ref(true)
const currentDiff = ref<ValuationStatus>('aboutRight')
const diffPercentage = ref(0)
const chartElements = ref<SVGElement[]>([])

const valuationModes = computed<Record<ValuationStatus, ValuationDiff>>(() => ({
  undervalued: {
    type: t('companyDetail.valuation.shareFairValue.undervalued'),
    class: 'dcf-chart__data-label-diff--undervalued',
    color: '#2dc97e',
  },
  overvalued: {
    type: t('companyDetail.valuation.shareFairValue.overvalued'),
    class: 'dcf-chart__data-label-diff--overvalued',
    color: '#e64141',
  },
  aboutRight: {
    type: t('companyDetail.valuation.shareFairValue.aboutRight'),
    class: 'dcf-chart__data-label-diff--about-right',
    color: '#eeb219',
  },
}))

const chartOptions = computed<Options>(
  () =>
    ({
      chart: {
        type: 'bar',
        height: 358,
        styledMode: true,
        borderWidth: 0,
        spacingTop: 69,
        spacingBottom: 100,
        className: 'dcf-chart__container',
        events: {
          load: drawChartElements,
          redraw: drawChartElements,
        },
      },
      title: {
        text: undefined,
      },
      xAxis: {
        visible: false,
      },
      yAxis: getYAxisOptions(),
      legend: {
        enabled: false,
      },
      plotOptions: {
        bar: {
          groupPadding: 0.1,
          borderWidth: 0,
          borderRadius: 0,
          pointWidth: 72, // Высота бары
        },
      },
      series: chartSeries.value,
    }) satisfies Options
)

function getCurrentValuationStatus(diff: number): ValuationStatus {
  if (diff >= 20) return 'undervalued'
  if (diff <= -20) return 'overvalued'
  return 'aboutRight'
}

function getYAxisOptions() {
  const currentValue = company.value.price_data.last_price || 1
  const fairValue = Number((currentValue * 1.2).toFixed(2))
  const highestValue = Math.max(currentValue, fairValue)

  return {
    visible: false,
    max: highestValue * 1.5,
  }
}

const chartSeries = computed<SeriesOptionsType[]>(() => {
  if (!company.value) return []

  const currencySymbol = company.value.formatting.primaryCurrencySymbol
  const currentValue = company.value.price_data.last_price || 1
  const fairValue = Number((currentValue * 1.2).toFixed(2))

  diffPercentage.value = +(
    ((fairValue - currentValue) / currentValue) *
    100
  ).toFixed(2)
  currentDiff.value = getCurrentValuationStatus(diffPercentage.value)

  return [
    {
      name: 'Current Price',
      type: 'bar',
      data: [currentValue],
      enableMouseTracking: false,
      dataLabels: {
        align: 'right',
        enabled: true,
        useHTML: true,
        formatter: function (this: Point) {
          return `
            <div class="d-flex flex-column" style="width: 200px">
              <div class='dcf-chart__data-label-name'>${t('companyDetail.valuation.shareFairValue.currentPrice')}</div>
              <div class='dcf-chart__data-label-value'>${this.y}${currencySymbol}</div>
            </div>
          `
        },
      },
    },
    {
      name: 'Fair Price',
      type: 'bar',
      data: [fairValue],
      enableMouseTracking: false,
      dataLabels: {
        align: 'right',
        enabled: true,
        useHTML: true,
        formatter: function (this: Point) {
          return `
            <div class="d-flex flex-column" style="width: 200px">
              <div class='dcf-chart__data-label-name'>${t('companyDetail.valuation.shareFairValue.fairPrice')}</div>
              <div class='dcf-chart__data-label-value'>${this.y}${currencySymbol}</div>
            </div>
          `
        },
      },
    },
  ]
})

function drawChartElements(this: Chart) {
  chartElements.value.forEach((el) => el?.destroy())
  chartElements.value = []

  if (!this.series?.[0].points?.[0]) return
  const currentMode = valuationModes.value[currentDiff.value]
  const box: PlotBox = {
    x: this.plotLeft,
    y: this.plotTop,
    height: this.plotHeight,
    width: this.plotWidth,
  }

  drawBackground(this, box)
  drawPriceLines(this, box, currentMode)
  drawDifferenceLabel(this, box, currentMode)
  drawThresholdLabels(this, box)
}

function drawBackground(chart: Chart, plotBox: PlotBox) {
  const { x, y, height } = plotBox
  const barWidth = chart.series[1].data[0].shapeArgs?.height || 0

  chartElements.value.push(
    chart.renderer
      .rect(x, y, barWidth * 1.2, height)
      .attr({
        fill: '#eeb219',
      })
      .add()
  )

  chartElements.value.push(
    chart.renderer
      .rect(x, y, barWidth * 0.8, height)
      .attr({
        fill: '#2dc97e',
      })
      .add()
  )
}

function drawPriceLines(chart: Chart, plotBox: PlotBox, mode: ValuationDiff) {
  const OUTLINE_OFFSET = 24
  const { x, y, height } = plotBox

  const fairPriceX = (chart.series[1].data[0].shapeArgs?.height || 0) + x
  const currentPriceX = (chart.series[0].data[0].shapeArgs?.height || 0) + x

  // Fair price line
  chartElements.value.push(
    chart.renderer
      .rect(
        fairPriceX,
        y + 0.5 - OUTLINE_OFFSET,
        0.5,
        height - 1 + OUTLINE_OFFSET
      )
      .attr({
        fill: 'rgb(var(--v-theme-on-surface-light))',
        opacity: 0.7,
        zIndex: 10,
      })
      .add()
  )
  // Current price line
  chartElements.value.push(
    chart.renderer
      .rect(
        currentPriceX,
        y + 0.5 - OUTLINE_OFFSET,
        0.5,
        height - 1 + OUTLINE_OFFSET
      )
      .attr({
        fill: 'rgb(var(--v-theme-on-surface-light))',
        opacity: 0.7,
      })
      .add()
  )
  // Connecting line
  const lineX = Math.min(currentPriceX, fairPriceX) + 0.5
  const lineY = y + 0.5 - OUTLINE_OFFSET
  const lineWidth = Math.abs(currentPriceX - fairPriceX) - 0.5

  chartElements.value.push(
    chart.renderer
      .rect(lineX, lineY, lineWidth, 2)
      .attr({ fill: mode.color })
      .add()
  )
}

function drawDifferenceLabel(
  chart: Chart,
  plotBox: PlotBox,
  mode: ValuationDiff
) {
  const OUTLINE_OFFSET = 24
  const { x, y } = plotBox

  const fairPriceX = (chart.series[1].data[0].shapeArgs?.height || 0) + x
  const currentPriceX = (chart.series[0].data[0].shapeArgs?.height || 0) + x
  const lineX = Math.min(currentPriceX, fairPriceX) + 0.5

  const labelText = `
    <tspan class="dcf-chart__data-label-diff-value">${diffPercentage.value}%</tspan>
    <br>
    <tspan class="dcf-chart__data-label-diff-type">${mode.type}</tspan>
  `

  chartElements.value.push(
    chart.renderer
      .text(labelText, lineX, y - 22 + 0.5 - OUTLINE_OFFSET)
      .attr({ class: mode.class })
      .add()
  )
}

function drawThresholdLabels(chart: Chart, plotBox: PlotBox) {
  const { y, height } = plotBox
  const barWidth = chart.series[1].data[0].shapeArgs?.height || 0
  const textY = y + height
  const textYOffset = 12
  const textXOffset = 12

  const labels = [
    {
      text: `20% ${t('companyDetail.valuation.shareFairValue.undervalued')}`,
      x: barWidth * 0.8,
      class: 'undervalued',
    },
    {
      text: t('companyDetail.valuation.shareFairValue.aboutRight'),
      x: barWidth,
      class: 'about_right',
    },
    {
      text: `20% ${t('companyDetail.valuation.shareFairValue.overvalued')}`,
      x: barWidth * 1.2,
      class: 'overvalued',
    },
  ]

  labels.forEach((label) => {
    chartElements.value.push(
      chart.renderer
        .text(
          `<tspan class='dcf-chart__label-level-name'>${label.text}</tspan>`,
          label.x + textXOffset,
          textY + textYOffset
        )
        .attr({
          rotation: -35,
          class: `dcf-chart__data-label-diff--${label.class}`,
        })
        .add()
    )
  })
}

watch(locale, () => {
  if (!chartRef.value?.chart) return

  chartRef.value.chart.series[0].update(chartSeries.value[0])
})
</script>

<template>
  <div class="dcf-chart">
    <fetching-data v-if="store.fetchingCompany" />
    <charts
      v-else-if="available"
      ref="chartRef"
      constructorType="chart"
      :options="chartOptions"
    />
    <data-not-available v-else chart-name="DCF Chart" />
    <fail-pattern />
    <bar-gradient />
  </div>
</template>

<style lang="scss">
.dcf-chart svg {
  height: auto;
  width: auto;
}
.dcf-chart .highcharts-visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  white-space: nowrap;
  clip: rect(1px, 1px, 1px, 1px);
  margin-top: -3px;
  opacity: 0.01;
}
.dcf-chart .highcharts-container {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 100%;
  text-align: left;
  line-height: normal;
  z-index: 0;
  font-size: 0.625rem;
  user-select: none;
  touch-action: manipulation;
  outline: none;
}
.dcf-chart .highcharts-plot-border,
.dcf-chart .highcharts-plot-background {
  fill: none;
}
.dcf-chart g.highcharts-series,
.dcf-chart .highcharts-point,
.dcf-chart .highcharts-markers,
.dcf-chart .highcharts-data-labels {
  transition: opacity 250ms;
}
.dcf-chart .highcharts-data-label-box {
  fill: none;
  stroke-width: 0;
}
.dcf-chart {
  height: 380px;
  width: 100%;
}
.dcf-chart__container {
  font-family: inherit;
}
.dcf-chart .highcharts-background {
  fill: rgb(var(--v-theme-surface-light));
}
.dcf-chart .highcharts-plot-background {
  fill: url(#Chart_Fail_Pattern);
}
.dcf-chart .highcharts-color-0 {
  outline: none;
  stroke-width: 0;
  fill: rgb(var(--v-theme-surface-light));
}
.dcf-chart .highcharts-color-1 {
  outline: none;
  stroke-width: 0;
  fill: url(#BarGradient);
}
.dcf-chart__data-label-value {
  fill: rgb(var(--v-theme-on-surface-light));
  font-size: 1.5rem;
  line-height: 1.25;
  font-weight: 500;
}
.dcf-chart__data-label-name {
  fill: rgb(var(--v-theme-on-surface-light));
  font-size: 1rem;
  line-height: 1.5;
  font-weight: 500;
}
.dcf-chart__data-label-diff--undervalued {
  fill: #2dc97e;
}
.dcf-chart__data-label-diff--about_right {
  fill: #eeb219;
}
.dcf-chart__data-label-diff--overvalued {
  fill: #e64141;
}
.dcf-chart__data-label-diff-value {
  line-height: 1.25;
  font-weight: 500;
  font-size: 1.5rem;
}
.dcf-chart__data-label-diff-type {
  line-height: 1.5;
  font-weight: 500;
  font-size: 0.875rem;
}
.dcf-chart__label-level-name {
  line-height: 1.5;
  font-weight: 500;
  font-size: 0.875rem;
  text-anchor: end;
}
</style>
