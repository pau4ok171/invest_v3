<script setup lang="ts">
// Composables
import { useDisplay } from 'vuetify'

// Utilities
import { computed, nextTick, ref, watch } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type {
  Options,
  Point,
  SVGPathArray,
  SVGElement,
  Series,
  Chart,
} from 'highcharts'

// Constants
const CHART_HEIGHT = 356
const TOOLTIP_WIDTH = 340

// Interfaces
interface FinancialData {
  date: number
  eps: number
  epsHigh: number
  epsLow: number
  analysts: number | null
  lastUpdated: number
}
interface ChartData {
  currency: string
  financialData: FinancialData[]
}
// Базовый тип точки с расширением для areasplinerange
interface RangePoint extends Point {
  high?: number
  low?: number
  plotHigh: number
  plotLow: number
}
const isRangePoint = (point: Point): point is RangePoint => {
  return 'high' in point && 'low' in point
}

// Reactive states
const { smAndDown } = useDisplay()
const chartRef = ref<{ chart: Chart } | null>(null)
const currentDate = DateTime.now()
const currentPoint = ref<Point | null>(null)
const chartElements = {
  tooltipConnector: null as SVGElement | null,
  markers: null as SVGElement[] | null,
  oneYearZone: null as SVGElement | null,
}
const activeLegends = ref<string[]>(['eps', 'epsRange'])
const legendOptions = [
  {
    text: 'EPS',
    value: 'eps',
  },
  {
    text: "Analysts' EPS Range",
    value: 'epsRange',
  },
]

const tooltipData = computed(() => {
  if (!currentPoint.value) return null

  const point = currentPoint.value
  const dataKey = point.category
  const dataInstance = data.financialData.find((f) => f.date === dataKey)

  if (!dataInstance) return null

  const tooltipPos = smAndDown.value
    ? 0
    : (point.plotX || 0) + point.series.chart.plotLeft - TOOLTIP_WIDTH <= 0
      ? (point.plotX || 0) + point.series.chart.plotLeft
      : (point.plotX || 0) + point.series.chart.plotLeft - TOOLTIP_WIDTH

  return {
    date: DateTime.fromMillis(point.category as number).toFormat('LLL dd yyyy'),
    eps: `${data.currency}${dataInstance.eps}`,
    epsRange: `${data.currency}${dataInstance.epsLow} - ${data.currency}${dataInstance.epsHigh}`,
    analysts: dataInstance.analysts,
    lastUpdated: DateTime.fromMillis(dataInstance.lastUpdated).toFormat(
      'LLL dd yyyy'
    ),
    tooltipStyle: {
      transform: `translateX(${tooltipPos}px)`,
    },
  }
})

// Data
const data: ChartData = {
  currency: 'US$',
  financialData: [
    {
      date: 1674950400000,
      eps: 0.18,
      epsHigh: 0.18,
      epsLow: 0.18,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1682812800000,
      eps: 0.19,
      epsHigh: 0.19,
      epsLow: 0.19,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1690675200000,
      eps: 0.42,
      epsHigh: 0.42,
      epsLow: 0.42,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1698537600000,
      eps: 0.77,
      epsHigh: 0.77,
      epsLow: 0.77,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1706400000000,
      eps: 1.21,
      epsHigh: 1.21,
      epsLow: 1.21,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1714262400000,
      eps: 1.73,
      epsHigh: 1.73,
      epsLow: 1.73,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1722124800000,
      eps: 2.15,
      epsHigh: 2.15,
      epsLow: 2.15,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1729987200000,
      eps: 2.56,
      epsHigh: 2.56,
      epsLow: 2.56,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1737763200000,
      eps: 2.97,
      epsHigh: 2.97,
      epsLow: 2.97,
      analysts: null,
      lastUpdated: 1745280000000,
    },
    {
      date: 1769817600000,
      eps: 4.26,
      epsHigh: 5.33,
      epsLow: 3.56,
      analysts: 29,
      lastUpdated: 1745280000000,
    },
    {
      date: 1801353600000,
      eps: 5.44,
      epsHigh: 7.55,
      epsLow: 4.61,
      analysts: 26,
      lastUpdated: 1745280000000,
    },
    {
      date: 1832889600000,
      eps: 6.39,
      epsHigh: 9.73,
      epsLow: 5.33,
      analysts: 13,
      lastUpdated: 1745280000000,
    },
  ],
}

const [eps, epsRange] = [
  data.financialData.map((p) => [p.date, p.eps]),
  data.financialData
    .filter((p) => p.epsHigh != null && p.epsLow != null)
    .map((p) => [p.date, p.epsLow, p.epsHigh]),
]

// Helper functions
const destroyChartElements = () => {
  if (chartElements.markers) {
    chartElements.markers.forEach((m) => m?.destroy())
    chartElements.markers = null
  }
  chartElements.tooltipConnector?.destroy()
  chartElements.oneYearZone?.destroy()
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

const updateMarkers = (point: Point) => {
  const chart = point.series.chart
  const markers = [] as SVGElement[]

  // Создаем новые маркеры для всех активных серий
  chartElements.markers = activeLegends.value
    .map((seriesName) => {
      const series = chart.series.find((s) => s.name === seriesName)
      if (!series || !series.visible) return null

      const seriesPoint = series.points[point.index] as Point | RangePoint
      if (!seriesPoint) return null

      const isActualData = seriesPoint.x <= currentDate.toMillis()
      const baseColor = isActualData
        ? 'rgb(var(--v-theme-hc-series1-color))'
        : 'rgb(var(--v-theme-hc-series2-color))'

      const baseMarkerStyle = {
        stroke: 'white',
        'stroke-width': 2,
        zIndex: 5,
      }

      // Для обычных серий (spline, line и т.д.)
      if (series.type !== 'areasplinerange') {
        return chart.renderer
          .circle(
            (seriesPoint.plotX || 0) + chart.plotLeft,
            (seriesPoint.plotY || 0) + chart.plotTop,
            5
          )
          .attr({
            ...baseMarkerStyle,
            fill: baseColor,
          })
          .add()
      }
      // Для areasplinerange (рисуем два маркера)
      else if (isRangePoint(seriesPoint)) {
        const centerX = (seriesPoint.plotX || 0) + chart.plotLeft

        // Маркер для верхнего значения (high)
        if (seriesPoint.plotHigh !== undefined) {
          markers.push(
            chart.renderer
              .circle(centerX, (seriesPoint.plotHigh || 0) + chart.plotTop, 5)
              .attr({
                ...baseMarkerStyle,
                fill: baseColor,
              })
              .add()
          )
        }

        // Маркер для нижнего значения (low)
        if (seriesPoint.plotLow !== undefined) {
          markers.push(
            chart.renderer
              .circle(centerX, (seriesPoint.plotLow || 0) + chart.plotTop, 5)
              .attr({
                ...baseMarkerStyle,
                fill: baseColor,
              })
              .add()
          )
        }

        return markers
      }
    })
    .filter(Boolean)
    .flat() as SVGElement[] // Используем flat() для раскрытия массивов маркеров
}

function findPointOneYearAgo(
  series: Series,
  datetimeInMills: number
): Point | null {
  // Ищем ближайшую точку
  let closestPoint = null
  let minDiff = Infinity
  const yearAgo = DateTime.fromMillis(datetimeInMills)
    .minus({ year: 1 })
    .toMillis()

  series.points.forEach((point) => {
    const diff = Math.abs(point.x - yearAgo)
    if (diff < minDiff) {
      minDiff = diff
      closestPoint = point
    }
  })

  return closestPoint
}

const updatePointElements = (point: Point) => {
  destroyChartElements()

  const chart = point.series?.chart
  if (!chart) return

  // Draw main elements
  chartElements.tooltipConnector = drawConnector(point)

  // Update markers for all visible series
  updateMarkers(point)

  // Draw one year zone
  const activeSeries = chart.series.find(
    (s) => s.visible && activeLegends.value.includes(s.name)
  )
  if (activeSeries) {
    const pointOneYAgo = findPointOneYearAgo(activeSeries, point.x as number)

    if (pointOneYAgo) {
      const fromX = (pointOneYAgo.plotX || 0) + chart.plotLeft
      const toX = (point.plotX || 0) + chart.plotLeft

      chartElements.oneYearZone = chart.renderer
        .rect(fromX, chart.plotTop, toX - fromX, chart.plotHeight)
        .attr({
          fill: 'url(#YearMarkerGradient)',
          stroke: 'rgba(35, 148, 223, 0.1)',
          'stroke-width': 1,
          zIndex: -1,
        })
        .add()
    }
  }
}

const options = computed<Options>(() => ({
  chart: {
    type: 'spline',
    height: CHART_HEIGHT,
    backgroundColor: 'transparent',
    events: {
      load() {
        const points = this.series[0].points
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
  legend: {
    enabled: false,
  },
  tooltip: {
    enabled: false,
  },
  xAxis: {
    type: 'datetime',
    tickInterval: 365.25 * 24 * 3600 * 1000,
    tickColor: 'rgb(70, 82, 96)',
    lineColor: 'rgb(70, 82, 96)',
    gridLineWidth: 0,
    ordinal: false,
    labels: {
      format: '{value:%Y}',
      align: 'center',
      step: 1,
      style: {
        color: 'rgb(var(--v-theme-on-surface))',
      },
    },
    plotBands: [
      {
        from: 0,
        to: currentDate.toMillis(),
        color: 'url(#Actual_Background_Gradient)',
        label: {
          text: 'Actual',
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
        to: currentDate.plus({ year: 3 }).toMillis(),
        color: 'transparent',
        label: {
          text: 'Analysts Forecasts',
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
  },
  yAxis: {
    title: { text: '' },
    gridLineWidth: 1,
    gridLineColor: 'rgba(var(--v-theme-on-surface), 0.1)',
    lineWidth: 0,
    labels: {
      formatter: function () {
        return this.isFirst ? `US$0` : this.isLast ? `US$10` : ''
      },
      style: {
        color: 'rgb(var(--v-theme-on-surface))',
      },
    },
    min: 0,
    max: 10,
  },
  series: [
    {
      type: 'spline',
      name: 'eps',
      data: eps,
      lineWidth: 3,
      visible: activeLegends.value.includes('eps'),
      zoneAxis: 'x',
      zones: [
        {
          value: currentDate.toMillis(),
          color: 'rgb(var(--v-theme-hc-series1-color))',
        },
        {
          color: 'rgb(var(--v-theme-hc-series2-color))',
        },
      ],
    },
    {
      type: 'areasplinerange',
      name: 'epsRange',
      data: epsRange,
      lineWidth: 3,
      visible: activeLegends.value.includes('epsRange'),
      zoneAxis: 'x',
      marker: {
        enabled: false,
      },
      zones: [
        {
          value: currentDate.toMillis(),
          color: 'url(#Chart_01_Gradient_02)',
        },
        {
          color: 'url(#Chart_02_Gradient_02)',
        },
      ],
    },
  ],
  plotOptions: {
    series: {
      states: {
        inactive: {
          opacity: 1,
        },
        hover: {
          enabled: false,
        },
      },
      point: {
        events: {
          mouseOver() {
            updateTooltip(this)
          },
        },
      },
    },
  },
}))

// Core functions
const updateTooltip = (point: Point, force: boolean = false) => {
  if (currentPoint.value && point.index === currentPoint.value.index && !force)
    return

  updatePointElements(point)
  currentPoint.value = point
}

watch(
  activeLegends,
  () => {
    nextTick(() => {
      if (currentPoint.value) {
        const chart = chartRef.value?.chart
        if (!chart) return

        const mainSeries = chart.series.find((s) => s.visible)
        if (!mainSeries) return

        const updatedPoint = mainSeries.points[currentPoint.value.index]
        if (updatedPoint) {
          updateTooltip(currentPoint.value, true)
        }
      }
    })
  },
  { deep: true }
)
</script>

<template>
  <div class="eps-growth-forecast-chart">
    <div class="eps-growth-forecast-chart__tooltip-box">
      <v-card
        v-if="tooltipData"
        :width="TOOLTIP_WIDTH"
        :style="tooltipData.tooltipStyle"
        class="text-disabled"
      >
        <v-card-item>
          <v-row no-gutters>
            <v-col class="text-high-emphasis">{{ tooltipData.date }}</v-col>
          </v-row>

          <template v-if="activeLegends.includes('eps')">
            <v-divider />

            <v-row no-gutters>
              <v-col>EPS</v-col>
              <v-col>
                <div
                  :class="
                    (currentPoint?.x || 0) <= currentDate.toMillis()
                      ? 'text-hc-series1-color'
                      : 'text-hc-series2-color'
                  "
                >
                  {{ tooltipData.eps }}
                </div>
              </v-col>
            </v-row>
          </template>

          <template v-if="activeLegends.includes('epsRange')">
            <v-divider />

            <v-row no-gutters>
              <v-col>Analysts' EPS</v-col>
              <v-col>
                <div
                  :class="
                    (currentPoint?.x || 0) <= currentDate.toMillis()
                      ? 'text-hc-series1-color'
                      : 'text-hc-series2-color'
                  "
                >
                  {{ tooltipData.epsRange }}
                </div>
              </v-col>
            </v-row>
          </template>

          <v-divider />

          <v-row no-gutters>
            <v-col>Analysts' No</v-col>
            <v-col class="text-high-emphasis">
              {{ tooltipData.analysts || 'n/a' }}
            </v-col>
          </v-row>

          <v-divider />

          <v-row no-gutters>
            <v-col>Last Updated</v-col>
            <v-col class="text-high-emphasis">
              {{ tooltipData.lastUpdated }}
            </v-col>
          </v-row>
        </v-card-item>
      </v-card>
    </div>

    <charts
      ref="chartRef"
      class="eps-growth-forecast-chart__chart"
      constructorType="chart"
      :options="options"
    />

    <v-btn-toggle multiple mandatory variant="outlined" v-model="activeLegends">
      <v-btn
        v-for="item in legendOptions"
        :key="`legend-${item.value}`"
        class="eps-growth-forecast-chart__legend-button"
        :value="item.value"
        size="small"
        :text="item.text"
      >
        <template #prepend>
          <span
            class="eps-growth-forecast-chart__circle-indicator"
            :style="{
              backgroundColor: activeLegends.includes(item.value)
                ? 'rgb(var(--v-theme-hc-series1-color))'
                : 'transparent',
              borderColor: 'rgb(var(--v-theme-hc-series1-color))',
            }"
          />
          <span
            class="eps-growth-forecast-chart__circle-indicator mr-2"
            :style="{
              backgroundColor: activeLegends.includes(item.value)
                ? 'rgb(var(--v-theme-hc-series2-color))'
                : 'transparent',
              borderColor: 'rgb(var(--v-theme-hc-series2-color))',
            }"
          />
        </template>
      </v-btn>
    </v-btn-toggle>
  </div>
</template>

<style scoped lang="scss">
@use 'vuetify/settings' as vuetify;

.eps-growth-forecast-chart {
  &__tooltip-box {
    height: 190px;
    position: relative;
    display: flex;
    align-items: end;
    font-weight: 400;
    font-size: 0.75rem;
    line-height: 1.125rem;

    @media #{map-get(vuetify.$display-breakpoints, 'sm-and-down')} {
      justify-content: center;
    }
  }
  &__chart {
    position: relative;
    display: grid;
    justify-content: center;
  }
  &__legend-button {
    text-transform: none;
  }
  &__circle-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: 1px solid;
    transition: background-color 0.3s;
  }
}
</style>
