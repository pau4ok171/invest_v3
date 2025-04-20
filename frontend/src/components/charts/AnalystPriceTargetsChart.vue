<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref } from 'vue'

// Types
import type { Options, Point, SVGElement } from 'highcharts'
import { DateTime } from 'ts-luxon'

interface AnalystChartData {
  currency: string
  items: ChartData[]
}

interface ChartData {
  datetime: number | 'current'
  sharePrice: number
  average1YPrice: number
  dispersion: number
  analysts: number
}

const { t } = useI18n()

const currentDate = DateTime.now()

function drawToolbarConnector(point: Point) {
  const chart = point.series.chart
  // Координаты линии
  const fromX = (point.plotX || 0) + chart.plotLeft
  const fromY = chart.plotTop + chart.plotHeight
  const toX = (point.plotX || 0) + chart.plotLeft
  const toY = -20

  // Рисуем новую линию
  return chart.renderer
    .path(['M', fromX, fromY, 'L', toX, toY])
    .attr({
      'stroke-width': 1,
      stroke: '#A54CEC',
      zIndex: 4,
    })
    .add()
}

let toolbarConnector = null as SVGElement | null
let sharePriceMarker = null as SVGElement | null
let analystMarker = null as SVGElement | null
let markerConnector = null as SVGElement | null
let markerPolygon = null as SVGElement | null
let oneYearZone = null as SVGElement | null

const currentPoint = ref<Point | null>(null)
const tooltipData = computed(() => {
  if (!currentPoint.value) return null
  const chart = currentPoint.value.series.chart

  const posX = (currentPoint.value.plotX || 0) + chart.plotLeft
  const dataIndex = currentPoint.value.index
  const dataInstance = data.items[dataIndex]
  const date = DateTime.fromMillis(
    currentPoint.value.category as number
  ).toFormat('LLL dd yyyy')
  const analysts = t('analyst', { n: dataInstance.analysts })
  const sharePrice = `${data.currency}${dataInstance.sharePrice}`
  const analyticsPrice = `${data.currency}${dataInstance.average1YPrice}`
  const diff =
    (dataInstance.average1YPrice - dataInstance.sharePrice) /
    dataInstance.sharePrice
  const isPos = diff >= 0
  const marge = `${isPos ? '+' : ''}${(diff * 100).toFixed(2)}%`
  const margeColorClass =
    diff >= 0.15 ? 'text-success' : diff < 0 ? 'text-error' : 'text-disabled'
  const isAgr = dataInstance.dispersion < 0.15
  const agrStatus = isAgr ? 'Good' : 'Low'
  const agrText = isAgr
    ? 'Analysts agreement range is spread less than 15% from the average'
    : 'Analysts agreement range is spread more than 15% from the average'
  const agrColorClass = isAgr ? 'text-success' : 'text-error'
  const tooltipStyle = { transform: `translateX(${posX - 340}px)` }

  return {
    date,
    analysts,
    sharePrice,
    analyticsPrice,
    margeColorClass,
    marge,
    agrColorClass,
    agrStatus,
    agrText,
    tooltipStyle,
  }
})

function updateTooltip(point: Point) {
  updatePointElements(point)
  currentPoint.value = point
}

function updatePointElements(point: Point) {
  const chart = point.series.chart

  console.log(point)

  // Удаляем предыдущие значения
  if (toolbarConnector) toolbarConnector.destroy()
  if (sharePriceMarker) sharePriceMarker.destroy()
  if (analystMarker) analystMarker.destroy()
  if (markerConnector) markerConnector.destroy()
  if (markerPolygon) markerPolygon.destroy()
  if (oneYearZone) oneYearZone.destroy()

  // Если это наша целевая серия
  if (point) {
    toolbarConnector = drawToolbarConnector(point)

    const index = point.index

    const dataInstance = data.items[index]
    const isAgr = dataInstance.dispersion < 0.15
    const agrColor = isAgr
      ? 'rgb(var(--v-theme-success))'
      : 'rgb(var(--v-theme-error))'
    const agrGradient = isAgr
      ? 'url(#Chart_POS_Gradient_02)'
      : 'url(#Chart_NEG_Gradient_02)'

    // Координаты текущей точки
    const currentX = (point.plotX || 0) + chart.plotLeft
    const currentY = (point.plotY || 0) + chart.plotTop

    const sharePriceSeries = chart.series.find((f) => f.name === 'Share Price')
    const targetRangeSeries = chart.series.find(
      (f) => f.name === 'Price Target Range'
    )

    const sharePricePoint = sharePriceSeries
      ? sharePriceSeries.points[index]
      : undefined

    const targetRangePoint = targetRangeSeries
      ? (targetRangeSeries.points[index] as Point & {
          plotHigh?: number
          plotLow?: number
        })
      : undefined

    if (!sharePricePoint || !targetRangePoint) return

    // Координаты точки 12 месяцев назад
    const yearAgoX = (sharePricePoint.plotX || 0) + chart.plotLeft
    const yearAgoY = (sharePricePoint.plotY || 0) + chart.plotTop

    const targetUpX = (targetRangePoint.plotX || 0) + chart.plotLeft
    const targetUpY = (targetRangePoint.plotHigh || 0) + chart.plotTop
    const targetDownX = (targetRangePoint.plotX || 0) + chart.plotLeft
    const targetDownY = (targetRangePoint.plotLow || 0) + chart.plotTop

    // Рисуем соединительную линию
    markerConnector = chart.renderer
      .path(['M', currentX, currentY, 'L', yearAgoX, yearAgoY])
      .attr({
        'stroke-width': 2,
        stroke: agrColor,
        dashstyle: 'Dash',
        zIndex: 5,
      })
      .add()

    const points = [
      // Точка Share Price (год назад) [x, y]
      [yearAgoX, yearAgoY],
      // Верхняя граница диапазона  [x, y]
      [targetUpX, targetUpY],
      // Нижняя граница диапазона  [x, y]
      [targetDownX, targetDownY],
    ]

    // 4. Рисуем полигон
    markerPolygon = chart.renderer
      .path([
        'M',
        points[0][0],
        points[0][1],
        'L',
        points[1][0],
        points[1][1],
        'L',
        points[2][0],
        points[2][1],
        'Z', // Замыкаем путь
      ])
      .attr({
        fill: agrGradient,
        zIndex: 4,
      })
      .add()

    // Маркер для точки 12 месяцев назад
    sharePriceMarker = chart.renderer
      .circle(yearAgoX, yearAgoY, 5)
      .attr({
        fill: 'rgb(var(--v-theme-info))',
        stroke: 'white',
        'stroke-width': 2,
        zIndex: 5,
      })
      .add()

    analystMarker = chart.renderer
      .circle(currentX, currentY, 5)
      .attr({
        fill: '#A54CEC',
        stroke: 'white',
        'stroke-width': 2,
        zIndex: 5,
      })
      .add()

    // One year zone
    oneYearZone = chart.renderer
      .rect(yearAgoX, chart.plotTop, currentX - yearAgoX, chart.plotHeight)
      .attr({
        fill: 'url(#YearMarkerGradient)',
        stroke: 'rgba(35, 148, 223, 0.1)',
        'stroke-width': 1,
        zIndex: -1,
      })
      .add()
  }
}

const data: AnalystChartData = {
  currency: 'US$',
  items: [
    {
      datetime: 1774990800,
      sharePrice: 110.15,
      average1YPrice: 171.89,
      dispersion: 0.122,
      analysts: 56,
    },
    {
      datetime: 1772312400,
      sharePrice: 124.92,
      average1YPrice: 173.62,
      dispersion: 0.109,
      analysts: 55,
    },
    {
      datetime: 1769893200,
      sharePrice: 120.07,
      average1YPrice: 174.25,
      dispersion: 0.108,
      analysts: 54,
    },
    {
      datetime: 1767214800,
      sharePrice: 134.29,
      average1YPrice: 172.95,
      dispersion: 0.102,
      analysts: 53,
    },
    {
      datetime: 1764536400,
      sharePrice: 138.25,
      average1YPrice: 171.19,
      dispersion: 0.104,
      analysts: 53,
    },
    {
      datetime: 1761944400,
      sharePrice: 135.4,
      average1YPrice: 150.43,
      dispersion: 0.131,
      analysts: 52,
    },
    {
      datetime: 1759266000,
      sharePrice: 117.0,
      average1YPrice: 149.8,
      dispersion: 0.127,
      analysts: 53,
    },
    {
      datetime: 1756674000,
      sharePrice: 119.37,
      average1YPrice: 148.68,
      dispersion: 0.138,
      analysts: 51,
    },
    {
      datetime: 1753995600,
      sharePrice: 109.21,
      average1YPrice: 139.23,
      dispersion: 0.173,
      analysts: 51,
    },
    {
      datetime: 1751317200,
      sharePrice: 124.3,
      average1YPrice: 132.34,
      dispersion: 0.166,
      analysts: 50,
    },
    {
      datetime: 1748725200,
      sharePrice: 109.63,
      average1YPrice: 119.29,
      dispersion: 0.118,
      analysts: 50,
    },
    {
      datetime: 1746046800,
      sharePrice: 83.04,
      average1YPrice: 99.9,
      dispersion: 0.142,
      analysts: 51,
    },
    {
      datetime: 1743454800,
      sharePrice: 90.36,
      average1YPrice: 96.39,
      dispersion: 0.157,
      analysts: 51,
    },
    {
      datetime: 1740776400,
      sharePrice: 82.28,
      average1YPrice: 88.04,
      dispersion: 0.18,
      analysts: 51,
    },
    {
      datetime: 1738357200,
      sharePrice: 63.03,
      average1YPrice: 66.63,
      dispersion: 0.199,
      analysts: 49,
    },
    {
      datetime: 1735678800,
      sharePrice: 49.52,
      average1YPrice: 65.63,
      dispersion: 0.19,
      analysts: 49,
    },
    {
      datetime: 1733000400,
      sharePrice: 46.77,
      average1YPrice: 65.29,
      dispersion: 0.194,
      analysts: 50,
    },
    {
      datetime: 1730408400,
      sharePrice: 42.33,
      average1YPrice: 63.91,
      dispersion: 0.197,
      analysts: 49,
    },
    {
      datetime: 1727730000,
      sharePrice: 43.5,
      average1YPrice: 63.87,
      dispersion: 0.2,
      analysts: 49,
    },
    {
      datetime: 1725138000,
      sharePrice: 48.51,
      average1YPrice: 62.97,
      dispersion: 0.214,
      analysts: 49,
    },
    {
      datetime: 1722459600,
      sharePrice: 46.51,
      average1YPrice: 49.26,
      dispersion: 0.17,
      analysts: 47,
    },
    {
      datetime: 1719781200,
      sharePrice: 42.3,
      average1YPrice: 46.0,
      dispersion: 0.169,
      analysts: 45,
    },
    {
      datetime: 1717189200,
      sharePrice: 39.77,
      average1YPrice: 43.02,
      dispersion: 0.211,
      analysts: 45,
    },
    {
      datetime: 1714510800,
      sharePrice: 28.91,
      average1YPrice: 28.15,
      dispersion: 0.147,
      analysts: 44,
    },
    {
      datetime: 1711918800,
      sharePrice: 27.78,
      average1YPrice: 27.51,
      dispersion: 0.15,
      analysts: 44,
    },
  ],
}

const sharePrices = data.items.map((p) => p.sharePrice).reverse()
const averages = data.items.map((p) => p.average1YPrice).reverse()
const averagesRange = data.items
  .map((p) => [
    p.average1YPrice * (1 - p.dispersion),
    p.average1YPrice * (1 + p.dispersion),
  ])
  .reverse()

const options = computed<Options>(
  () =>
    ({
      chart: {
        type: 'spline',
        height: 356,
        width: null,
        backgroundColor: 'transparent',
        events: {
          load: function () {
            const points = this.series[2].points
            const lastPoint = points[points.length - 1]
            updateTooltip(lastPoint)
          },
        },
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
      xAxis: {
        type: 'datetime',
        plotBands: [
          {
            from: 0,
            to: currentDate.toMillis(),
            color: 'url(#Actual_Background_Gradient)',
            label: {
              text: 'Past',
              align: 'right',
              style: {
                color: 'rgb(var(--v-theme-on-surface))',
              },
              x: -10,
            },
            zIndex: -1,
          },
          {
            from: currentDate.toMillis(),
            to: currentDate.plus({ year: 1 }).toMillis(),
            color: 'transparent',
            label: {
              text: '12m forecast',
              align: 'left',
              style: {
                color: '#606060',
                opacity: 1,
              },
              x: 10,
            },
            zIndex: -1,
          },
        ],
        labels: {
          format: '{value:%Y}', // Показывать только год
          align: 'center',
          step: 1, // Показывать каждый год
          style: {
            color: 'rgb(var(--v-theme-on-surface))',
          },
        },
        tickInterval: 365 * 24 * 3600 * 1000, // Интервал в 1 год (в миллисекундах)
        tickColor: 'rgb(70, 82, 96)',
        gridLineWidth: 0,
        lineColor: 'rgb(70, 82, 96)',
      },
      yAxis: {
        title: { text: '' }, // Скрываем заголовок
        gridLineWidth: 1,
        gridLineColor: 'rgba(var(--v-theme-on-surface), 0.1)',
        lineWidth: 0,
        plotLines: [
          {
            color: 'rgb(70, 82, 96)',
            width: 1,
            value: 200, // ДОЛЖНА БЫТЬ РАВНА МАКС
            zIndex: 5,
          },
        ],
        labels: {
          formatter: function () {
            return this.isFirst
              ? `US$20`
              : this.isLast
                ? `US$${this.value}`
                : ''
          },
          style: {
            color: 'rgb(var(--v-theme-on-surface))',
          },
        },
        min: 20,
        max: 200,
      },
      plotOptions: {
        series: {
          marker: {
            enabled: false,
          },
          point: {
            events: {
              mouseOver: function () {
                updateTooltip(this)
              },
            },
          },
          pointStart: '2023-04-01',
          pointIntervalUnit: 'month',
          events: {
            legendItemClick: function () {
              return false
            },
          },
          states: {
            inactive: {
              opacity: 1, // Полная видимость даже при "неактивности"
            },
            hover: {
              enabled: false, // Отключаем hover эффекты
            },
          },
        },
      },
      series: [
        {
          name: 'Share Price',
          type: 'spline',
          data: sharePrices,
          color: 'rgb(var(--v-theme-info))',
          lineWidth: 3,
          pointStart: Date.parse('2023-04-01'),
          enableMouseTracking: false,
        },
        {
          name: 'Average 1Y Target',
          type: 'spline',
          data: averages,
          color: '#A54CEC',
          lineWidth: 3,
          pointStart: Date.parse('2024-04-01'),
          enableMouseTracking: true,
        },
        {
          name: 'Price Target Range',
          type: 'areasplinerange',
          data: averagesRange,
          color: 'url(#Chart_05_Gradient_02)',
          fillOpacity: 0.5,
          lineWidth: 0,
          linkedTo: ':previous',
          zIndex: 0,
          pointStart: Date.parse('2024-04-01'),
          enableMouseTracking: false,
        },
      ],
      tooltip: {
        enabled: false,
      },
      legend: {
        align: 'left',
        verticalAlign: 'bottom',
        symbolHeight: 12,
        symbolWidth: 12,
        symbolRadius: 6,
        itemStyle: {
          color: 'rgb(var(--v-theme-on-surface))',
          fontSize: '0,75rem',
        },
        margin: 15,
        padding: 5,
      },
    }) satisfies Options
)
</script>

<template>
  <div class="analyst-price-targets-chart">
    <div class="analyst-price-targets-chart__tooltip-box">
      <v-card
        v-if="tooltipData"
        width="340"
        :style="tooltipData.tooltipStyle"
        class="text-caption text-disabled"
      >
        <v-card-item>
          <v-row no-gutters>
            <v-col class="text-high-emphasis">{{ tooltipData.date }}</v-col>
            <v-col
              ><div class="text-capitalize d-flex justify-end">
                {{ tooltipData.analysts }}
              </div></v-col
            >
          </v-row>
          <v-divider />
          <v-row no-gutters>
            <v-col cols="4">Share Price</v-col>
            <v-col offset="1"
              ><div class="text-info">
                {{ tooltipData.sharePrice }}
              </div></v-col
            >
          </v-row>
          <v-divider />
          <v-row no-gutters>
            <v-col cols="4">Average 1Y Price Target</v-col>
            <v-col offset="1"
              ><div class="text-hc-average-series-color">
                {{ tooltipData.analyticsPrice }}
              </div></v-col
            >
            <v-col :class="tooltipData.margeColorClass">{{
              tooltipData.marge
            }}</v-col>
          </v-row>
          <v-divider />
          <v-row no-gutters>
            <v-col cols="4">Agreement</v-col>
            <v-col offset="1">
              <div :class="tooltipData.agrColorClass">
                {{ tooltipData.agrStatus }}
              </div>
              <div>
                {{ tooltipData.agrText }}
              </div>
            </v-col>
          </v-row>
        </v-card-item>
      </v-card>
    </div>
    <charts
      class="analyst-price-targets-chart__chart"
      constructorType="chart"
      :options="options"
    />
  </div>
</template>

<style lang="scss">
.analyst-price-targets-chart__tooltip-box {
  height: 190px;
  position: relative;
  display: flex;
  align-items: end;
}
.analyst-price-targets-chart__chart {
  position: relative;
  display: grid;
  justify-content: center;
  align-items: center;

  .highcharts-legend {
    pointer-events: none;
  }
}
.highcharts-tooltip-container {
  > svg {
    display: none;
  }
}
.analyst-price-targets-chart-tooltip {
  display: flex;
  background: rgb(var(--v-theme-surface));
  color: rgba(var(--v-theme-on-surface), 0.5);
  font-size: 0.75rem;
  padding: 12px 8px;
  border-radius: 4px;
  flex-direction: column;
  width: 340px;

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  &__divider {
    width: 100%;
    height: 1px;
    background-color: rgb(51, 51, 51);
    margin: 4px 0;
  }
  &__grid {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 16px;
    white-space: break-spaces;
    overflow-wrap: break-word;
  }
  &__share-price {
    color: rgb(var(--v-theme-info));
  }
  &__average {
    color: #a54cec;
  }
}
</style>
