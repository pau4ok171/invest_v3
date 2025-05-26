<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type {
  Chart,
  Options,
  SVGElement,
  TooltipOptions,
  SeriesBarOptions,
} from 'highcharts'

// Constants
const BAR_WIDTH = 40
const LINE_WIDTH = 2
const LINE_HEIGHT = 56
const TEXT_STYLE = {
  color: 'rgb(var(--v-theme-on-surface))',
  fontSize: '0.875rem',
  fontWeight: '500',
}

// Data
const data = {
  exDividendDate: 1749168000,
  dividendPayDate: 1750982400,
}

// Refs
const chartElements = ref<SVGElement[]>([])
const today = DateTime.now()
const { t, locale } = useI18n()

// Computed properties
const daysToDividend = computed(
  () =>
    Math.round(
      DateTime.fromSeconds(data.exDividendDate).diff(today, 'days').days
    ) + 1
)

const daysToPayment = computed(
  () =>
    Math.round(
      DateTime.fromSeconds(data.dividendPayDate).diff(
        DateTime.fromSeconds(data.exDividendDate),
        'days'
      ).days
    ) + 1
)

const chartOptions = computed<Options>(() => {
  const todaySeconds = today.toSeconds()
  const totalDuration = data.dividendPayDate - todaySeconds
  const exDividendPosition =
    (data.exDividendDate - todaySeconds) / totalDuration

  return {
    chart: {
      type: 'bar',
      height: 227,
      backgroundColor: 'transparent',
      spacingRight: 0,
      events: {
        load: drawChartElements,
        redraw: drawChartElements,
      },
    },
    title: { text: undefined },
    legend: { enabled: false },
    xAxis: { visible: false },
    yAxis: { visible: false, min: 0, max: 1 },
    tooltip: getTooltipConfig(),
    plotOptions: {
      bar: getBarPlotOptions(),
    },
    series: getChartSeries(exDividendPosition),
  } satisfies Options
})

// Methods
function getTooltipConfig(): TooltipOptions {
  return {
    format: t('companyDetail.dividend.upcomingPayment.chart.tooltip', {
      n: daysToDividend.value,
    }),
    backgroundColor: 'rgb(var(--v-theme-surface))',
    style: {
      color: 'rgb(var(--v-theme-on-surface))',
    },
    positioner: function (labelWidth: number, labelHeight: number) {
      const chart = this.chart
      return {
        x: chart.plotLeft + chart.plotWidth / 2 - labelWidth / 2,
        y: chart.plotTop + chart.plotHeight / 2 - labelHeight / 2,
      }
    },
  }
}

function getBarPlotOptions() {
  return {
    borderRadius: 0,
    grouping: false,
    pointWidth: BAR_WIDTH,
    borderWidth: 0,
    states: {
      inactive: { enabled: false },
      hover: { enabled: false },
    },
  }
}

function getChartSeries(exDividendPosition: number): SeriesBarOptions[] {
  return [
    {
      type: 'bar',
      dataLabels: getDataLabelConfig(`${daysToPayment.value} days`, 'left'),
      data: [
        {
          x: 0,
          y: 1,
          color: 'rgb(var(--v-theme-hc-series3-color))',
        },
      ],
    },
    {
      type: 'bar',
      dataLabels: getDataLabelConfig(`${daysToDividend.value} days`, 'right'),
      data: [
        {
          x: 0,
          y: exDividendPosition,
          color: 'rgb(var(--v-theme-hc-series1-color))',
        },
      ],
    },
  ]
}

function getDataLabelConfig(text: string, align: 'left' | 'right') {
  return {
    enabled: true,
    format: text,
    align,
    verticalAlign: 'center',
    style: {
      ...TEXT_STYLE,
      textOutline: 'none',
      stroke: 'none',
    },
  }
}

function drawChartElements(this: Chart) {
  clearChartElements()

  const [mainSeries, exDividendSeries] = this.series
  const fromX = this.plotLeft
  const fromY =
    this.plotTop + (mainSeries.points[0].shapeArgs?.x || 0) + BAR_WIDTH
  const exDivFromX = fromX + (exDividendSeries.points[0].shapeArgs?.height || 0)
  const divPayFromX =
    fromX + (mainSeries.points[0].shapeArgs?.height || 0) - LINE_WIDTH

  // Today elements
  createLine(this, fromX, fromY, LINE_WIDTH, LINE_HEIGHT, 'hc-series1-color')
  createText(
    this,
    `${t('companyDetail.dividend.upcomingPayment.chart.today')}<br/>${today.toFormat('DD', { locale: locale.value })}`,
    fromX,
    fromY + LINE_HEIGHT + 20
  )

  // Ex Dividend elements
  createLine(
    this,
    exDivFromX,
    fromY - LINE_HEIGHT - BAR_WIDTH + 20,
    LINE_WIDTH,
    LINE_HEIGHT - 20,
    'hc-series3-color'
  )
  createText(
    this,
    `${t('companyDetail.dividend.upcomingPayment.chart.exDividendDate')}<br/>${DateTime.fromSeconds(data.exDividendDate).toFormat('DD', { locale: locale.value })}`,
    exDivFromX,
    fromY - LINE_HEIGHT - 50
  )

  // Dividend Pay elements
  createLine(
    this,
    divPayFromX,
    fromY,
    LINE_WIDTH,
    LINE_HEIGHT,
    'hc-series3-color'
  )
  createText(
    this,
    `<div class="text-hc-series3-color">${t('companyDetail.dividend.upcomingPayment.chart.dividendPayDate')}</div><div>${DateTime.fromSeconds(data.dividendPayDate).toFormat('DD', { locale: locale.value })}</div>`,
    divPayFromX,
    fromY + LINE_HEIGHT + 20,
    true,
    'right'
  )
}

function getTextWidth(
  text: string,
  fontSize = '0.875rem',
  fontFamily = 'inherit'
) {
  // Создаем временный элемент для измерения
  const span = document.createElement('span')
  span.style.visibility = 'hidden'
  span.style.position = 'absolute'
  span.style.whiteSpace = 'nowrap'
  span.style.fontSize = fontSize
  span.style.fontFamily = fontFamily
  span.style.fontWeight = '500'
  span.innerHTML = text

  document.body.appendChild(span)
  const width = span.offsetWidth
  document.body.removeChild(span)

  return width
}

function createLine(
  chart: Chart,
  x: number,
  y: number,
  width: number,
  height: number,
  colorVar: string
) {
  const line = chart.renderer
    .rect(x, y, width, height)
    .attr({
      fill: `rgb(var(--v-theme-${colorVar}))`,
      zIndex: 4,
    })
    .add()
  chartElements.value.push(line)
}

function createText(
  chart: Chart,
  text: string,
  x: number,
  y: number,
  useHTML = false,
  align: 'left' | 'right' = 'left'
) {
  if (align === 'right') {
    const textWidth = getTextWidth(text)
    x = x - textWidth
  }

  const textElement = chart.renderer
    .text(text, x, y, useHTML)
    .css(TEXT_STYLE)
    .add()
  chartElements.value.push(textElement)
}

function clearChartElements() {
  chartElements.value.forEach((el) => el.destroy())
  chartElements.value = []
}
</script>

<template>
  <div class="upcoming-dividend-payment-chart">
    <charts
      class="upcoming-dividend-payment-chart__chart"
      constructor-type="chart"
      :options="chartOptions"
    />
  </div>
</template>

<style scoped lang="scss">
.upcoming-dividend-payment-chart {
  &__chart {
    width: 100%;
    height: 100%;
  }
}
</style>
