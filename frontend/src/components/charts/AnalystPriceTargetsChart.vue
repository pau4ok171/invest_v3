<script setup lang="ts">
// Composables
import { useI18n } from 'vue-i18n'
import { useDisplay } from "vuetify";

// Utilities
import { computed, ref } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type { Options, Point, SVGElement, SVGPathArray } from 'highcharts'

// Constants
const CHART_HEIGHT = 356
const TOOLTIP_WIDTH = 340

// Interfaces
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

// Reactive states
const { smAndDown } = useDisplay()
const { t } = useI18n()
const currentDate = DateTime.now()
const currentPoint = ref<Point | null>(null)
const chartElements = {
  tooltipConnector: null as SVGElement | null,
  sharePriceMarker: null as SVGElement | null,
  analystMarker: null as SVGElement | null,
  markerConnector: null as SVGElement | null,
  markerPolygon: null as SVGElement | null,
  oneYearZone: null as SVGElement | null,
}

// Chart data
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

// Computed data series
const [sharePrices, averages, averagesRange] = [
  data.items.map((p) => p.sharePrice).reverse(),
  data.items.map((p) => p.average1YPrice).reverse(),
  data.items
    .map((p) => [
      p.average1YPrice * (1 - p.dispersion),
      p.average1YPrice * (1 + p.dispersion),
    ])
    .reverse(),
]

// Helper functions
const destroyChartElements = () => {
  Object.values(chartElements).forEach((el) => el?.destroy())
  Object.keys(chartElements).forEach((key) => {
    chartElements[key as keyof typeof chartElements] = null
  })
}

const drawConnector = (point: Point) => {
  const chart = point.series.chart
  const fromX = (point.plotX || 0) + chart.plotLeft
  const fromY = chart.plotTop + chart.plotHeight
  const toX = fromX
  const toY = -20

  return chart.renderer
    .path(['M', fromX, fromY, 'L', toX, toY] as unknown as SVGPathArray)
    .attr({
      'stroke-width': 1,
      stroke: 'rgb(var(--v-theme-hc-average-series-color))',
      zIndex: 4,
    })
    .add()
}

const getAgreementStatus = (dispersion: number) => {
  const isAgr = dispersion < 0.15
  return {
    isAgr,
    color: isAgr ? 'text-success' : 'text-error',
    status: isAgr ? 'Good' : 'Low',
    text: isAgr
      ? 'Analysts agreement range is spread less than 15% from the average'
      : 'Analysts agreement range is spread more than 15% from the average',
  }
}

// Computed properties
const tooltipData = computed(() => {
  if (!currentPoint.value) return null

  const point = currentPoint.value
  const dataIndex = currentPoint.value.index
  const dataInstance = data.items[dataIndex]

  const date = DateTime.fromMillis(point.category as number).toFormat(
    'LLL dd yyyy'
  )
  const analysts = t('analyst', { n: dataInstance.analysts })
  const diff =
    (dataInstance.average1YPrice - dataInstance.sharePrice) /
    dataInstance.sharePrice
  const isPos = diff >= 0
  const agreement = getAgreementStatus(dataInstance.dispersion)
  const tooltipPos = smAndDown.value
    ? 0
    : (point.plotX || 0) + point.series.chart.plotLeft - TOOLTIP_WIDTH <= 0
      ? (point.plotX || 0) + point.series.chart.plotLeft
      : (point.plotX || 0) + point.series.chart.plotLeft - TOOLTIP_WIDTH

  return {
    date,
    analysts,
    sharePrice: `${data.currency}${dataInstance.sharePrice}`,
    analyticsPrice: `${data.currency}${dataInstance.average1YPrice}`,
    margeColorClass:
      diff >= 0.15 ? 'text-success' : diff < 0 ? 'text-error' : 'text-disabled',
    marge: `${isPos ? '+' : ''}${(diff * 100).toFixed(2)}%`,
    agrColorClass: agreement.color,
    agrStatus: agreement.status,
    agrText: agreement.text,
    tooltipStyle: {
      transform: `translateX(${tooltipPos}px)`,
    },
  }
})

// Chart options
const options = computed<Options>(
  () =>
    ({
      chart: {
        type: 'spline',
        height: CHART_HEIGHT,
        width: null,
        backgroundColor: 'transparent',
        events: {
          load() {
            const points = this.series[2].points
            updateTooltip(points[points.length - 1])
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
                fontWeight: '400',
                fontSize: '0.75rem',
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
              text: '12m Forecast',
              align: 'left',
              style: {
                color: '#606060',
                opacity: 1,
                fontWeight: '400',
                fontSize: '0.75rem',
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
              mouseOver() {
                updateTooltip(this)
              },
            },
          },
          pointStart: '2023-04-01',
          pointIntervalUnit: 'month',
          events: {
            legendItemClick() {
              return false // Highcharts ожидает boolean
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
          color: 'rgb(var(--v-theme-hc-average-series-color))',
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

// Core functions
const updatePointElements = (point: Point) => {
  destroyChartElements()

  const chart = point.series.chart
  const dataInstance = data.items[point.index]
  const agreement = getAgreementStatus(dataInstance.dispersion)

  // Draw main elements
  chartElements.tooltipConnector = drawConnector(point)

  const currentX = (point.plotX || 0) + chart.plotLeft
  const currentY = (point.plotY || 0) + chart.plotTop

  const sharePriceSeries = chart.series.find((f) => f.name === 'Share Price')
  const targetRangeSeries = chart.series.find(
    (f) => f.name === 'Price Target Range'
  )

  if (!sharePriceSeries || !targetRangeSeries) return

  const sharePricePoint = sharePriceSeries.points[point.index]
  const targetRangePoint = targetRangeSeries.points[point.index] as Point & {
    plotHigh: number
    plotLow: number
  }

  // Draw connection elements
  const yearAgoX = (sharePricePoint.plotX || 0) + chart.plotLeft
  const yearAgoY = (sharePricePoint.plotY || 0) + chart.plotTop

  chartElements.markerConnector = chart.renderer
    .path([
      'M',
      currentX,
      currentY,
      'L',
      yearAgoX,
      yearAgoY,
    ] as unknown as SVGPathArray)
    .attr({
      'stroke-width': 2,
      stroke: agreement.isAgr
        ? 'rgb(var(--v-theme-success))'
        : 'rgb(var(--v-theme-error))',
      dashstyle: 'Dash',
      zIndex: 5,
    })
    .add()

  // Draw polygon
  const polygonPoints = [
    [yearAgoX, yearAgoY],
    [currentX, (targetRangePoint.plotHigh || 0) + chart.plotTop],
    [currentX, (targetRangePoint.plotLow || 0) + chart.plotTop],
  ]

  chartElements.markerPolygon = chart.renderer
    .path([
      'M',
      ...polygonPoints[0],
      'L',
      ...polygonPoints[1],
      'L',
      ...polygonPoints[2],
      'Z',
    ] as unknown as SVGPathArray)
    .attr({
      fill: agreement.isAgr
        ? 'url(#Chart_POS_Gradient_02)'
        : 'url(#Chart_NEG_Gradient_02)',
      zIndex: 4,
    })
    .add()

  // Draw markers
  chartElements.sharePriceMarker = chart.renderer
    .circle(yearAgoX, yearAgoY, 5)
    .attr({
      fill: 'rgb(var(--v-theme-info))',
      stroke: 'white',
      'stroke-width': 2,
      zIndex: 5,
    })
    .add()

  chartElements.analystMarker = chart.renderer
    .circle(currentX, currentY, 5)
    .attr({
      fill: 'rgb(var(--v-theme-hc-average-series-color))',
      stroke: 'white',
      'stroke-width': 2,
      zIndex: 5,
    })
    .add()

  // Draw year zone
  chartElements.oneYearZone = chart.renderer
    .rect(yearAgoX, chart.plotTop, currentX - yearAgoX, chart.plotHeight)
    .attr({
      fill: 'url(#YearMarkerGradient)',
      stroke: 'rgba(35, 148, 223, 0.1)',
      'stroke-width': 1,
      zIndex: -1,
    })
    .add()
}

const updateTooltip = (point: Point) => {
  updatePointElements(point)
  currentPoint.value = point
}
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
@use 'vuetify/settings' as vuetify;

.analyst-price-targets-chart {
  &__tooltip-box {
    height: 190px;
    position: relative;
    display: flex;
    align-items: end;

    @media #{map-get(vuetify.$display-breakpoints, 'sm-and-down')} {
      justify-content: center;
    }
  }
  &__chart {
    position: relative;
    display: grid;
    justify-content: center;
    align-items: center;

    .highcharts-legend {
      pointer-events: none;
    }
  }
}
</style>
