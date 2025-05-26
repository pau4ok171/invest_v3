<script setup lang="ts">
// Composables
import { useFinancialFormatter } from '@/composables/formatter'
import { useDisplay } from 'vuetify'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, nextTick, ref, watch } from 'vue'
import { DateTime } from 'ts-luxon'
import { data as finData } from './bigFinData'

// Types
import type {
  Options,
  Point,
  SVGPathArray,
  SVGElement,
  Series,
  Chart,
} from 'highcharts'
import type { FinUnit } from '@/composables/formatter'

// Constants
const CHART_HEIGHT = 356
const TOOLTIP_WIDTH = 340

// Interfaces
interface FinancialData {
  revenue: [number, number]
  earnings: [number, number]
  fcf: [number, number]
  cfo: [number, number]
  opex: [number, number]
}
interface FinancialObject {
  revenue: [number, number][]
  earnings: [number, number][]
  fcf: [number, number][]
  cfo: [number, number][]
  opex: [number, number][]
}
interface ChartData {
  currency: string
  financialData: FinancialData[]
  financialUnit: FinUnit
}
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
const { fin } = useFinancialFormatter()
const chartRef = ref<{ chart: Chart } | null>(null)
const { t, locale } = useI18n()
const currentDate = DateTime.now()
const currentPoint = ref<Point | null>(null)
const chartElements = {
  tooltipConnector: null as SVGElement | null,
  markers: null as SVGElement[] | null,
  oneYearZone: null as SVGElement | null,
}
const activeLegends = ref<string[]>(['revenue', 'earnings', 'fcf'])
const legendOptions = computed(() => [
  {
    text: t('companyDetail.past.earningsRevenueHistory.chart.legends.revenue'),
    value: 'revenue',
    color: 'rgb(var(--v-theme-hc-series1-color))',
    fillColor: 'url(#Chart_01_Gradient_02)',
  },
  {
    text: t('companyDetail.past.earningsRevenueHistory.chart.legends.earnings'),
    value: 'earnings',
    color: 'rgb(var(--v-theme-hc-series2-color))',
    fillColor: 'url(#Chart_02_Gradient_02)',
  },
  {
    text: t('companyDetail.past.earningsRevenueHistory.chart.legends.fcf'),
    value: 'fcf',
    color: 'rgb(var(--v-theme-hc-series3-color))',
    fillColor: 'url(#Chart_03_Gradient_02)',
  },
  {
    text: t('companyDetail.past.earningsRevenueHistory.chart.legends.cfo'),
    value: 'cfo',
    color: 'rgb(var(--v-theme-hc-series4-color))',
    fillColor: 'url(#Chart_04_Gradient_02)',
  },
  {
    text: t('companyDetail.past.earningsRevenueHistory.chart.legends.opex'),
    value: 'opex',
    color: 'rgb(var(--v-theme-hc-series5-color))',
    fillColor: 'url(#Chart_05_Gradient_02)',
  },
])

const tooltipData = computed(() => {
  if (!currentPoint.value) return null

  const point = currentPoint.value
  const dataKey = point.category
  const dataInstance = data.financialData.find((f) => f.revenue[0] === dataKey)

  if (!dataInstance) return null

  const tooltipPos = smAndDown.value
    ? 0
    : (point.plotX || 0) + point.series.chart.plotLeft - TOOLTIP_WIDTH <= 0
      ? (point.plotX || 0) + point.series.chart.plotLeft
      : (point.plotX || 0) + point.series.chart.plotLeft - TOOLTIP_WIDTH

  return {
    date: DateTime.fromMillis(point.category as number).toFormat('DD', {
      locale: locale.value,
    }),
    revenue: fin({
      currency: data.currency,
      value: dataInstance.revenue[1],
      finUnit: data.financialUnit,
    }),
    profiteMargin:
      dataInstance.revenue[1] !== 0
        ? ((dataInstance.earnings[1] / dataInstance.revenue[1]) * 100).toFixed(
            2
          ) + '%'
        : undefined,
    earnings: fin({
      currency: data.currency,
      value: dataInstance.earnings[1],
      finUnit: data.financialUnit,
    }),
    fcf: fin({
      currency: data.currency,
      value: dataInstance.fcf[1],
      finUnit: data.financialUnit,
    }),
    cfo: fin({
      currency: data.currency,
      value: dataInstance.cfo[1],
      finUnit: data.financialUnit,
    }),
    opex: fin({
      currency: data.currency,
      value: dataInstance.opex[1],
      finUnit: data.financialUnit,
    }),
    tooltipStyle: {
      transform: `translateX(${tooltipPos}px)`,
    },
  }
})

// Data
const data: ChartData = {
  currency: 'US$',
  financialUnit: 'M',
  financialData: Object.entries(finData).map(([dateStr, v]) => {
    const date = Number(dateStr)
    return {
      revenue: [date, v.total_rev.value],
      earnings: [date, v.ni.value],
      fcf: [date, v.levered_fcf.value],
      cfo: [date, v.cash_oper.value],
      opex: [date, v.r_d_expense?.value + v.g_a_expense.value],
    }
  }),
}

const { revenue, earnings, fcf, cfo, opex } = data.financialData.reduce(
  (acc, curr) => {
    Object.keys(curr).forEach((key) => {
      if (!acc[key as keyof FinancialObject]) {
        acc[key as keyof FinancialObject] = []
      }
      acc[key as keyof FinancialObject].push(curr[key as keyof FinancialObject])
    })
    return acc
  },
  {} as FinancialObject
)

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

      const baseColor = legendOptions.value.find(
        (l) => l.value === seriesName
      )?.color

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

const getSeriesData = (seriesName: string) => {
  switch (seriesName) {
    case 'revenue':
      return revenue
    case 'earnings':
      return earnings
    case 'fcf':
      return fcf
    case 'cfo':
      return cfo
    case 'opex':
      return opex
    default:
      return []
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
          text: t('companyDetail.past.earningsRevenueHistory.chart.actual'),
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
        return this.isFirst ? `US$0` : this.isLast ? `US$140b` : ''
      },
      style: {
        color: 'rgb(var(--v-theme-on-surface))',
      },
    },
    min: 0,
    max: 140000,
  },
  series: legendOptions.value.map((series) => ({
    type: 'areaspline',
    name: series.value,
    data: getSeriesData(series.value),
    color: series.color,
    fillColor: series.fillColor,
    lineWidth: 3,
    visible: activeLegends.value.includes(series.value),
  })),
  plotOptions: {
    series: {
      marker: {
        enabled: false,
      },
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
  <div class="earnings-revenue-history-chart">
    <div class="earnings-revenue-history-chart__tooltip-box">
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

          <template v-if="activeLegends.includes('revenue')">
            <v-divider />

            <v-row no-gutters>
              <v-col>
                {{
                  t(
                    'companyDetail.past.earningsRevenueHistory.chart.tooltip.revenue'
                  )
                }}
              </v-col>
              <v-col>
                <div class="text-hc-series1-color">
                  {{ tooltipData.revenue }}
                  <span class="text-disabled">
                    /{{
                      t(
                        'companyDetail.past.earningsRevenueHistory.chart.tooltip.year'
                      )
                    }}</span
                  >
                </div>
              </v-col>
            </v-row>
          </template>
          <template v-if="activeLegends.includes('earnings')">
            <v-divider />

            <v-row no-gutters>
              <v-col>{{
                t(
                  'companyDetail.past.earningsRevenueHistory.chart.tooltip.earnings'
                )
              }}</v-col>
              <v-col>
                <div class="text-hc-series2-color">
                  {{ tooltipData.earnings }}
                  <span class="text-disabled">
                    /{{
                      t(
                        'companyDetail.past.earningsRevenueHistory.chart.tooltip.year'
                      )
                    }}</span
                  >
                </div>
                <div
                  v-if="tooltipData.profiteMargin"
                  class="text-high-emphasis"
                >
                  {{ tooltipData.profiteMargin }}
                  <span class="text-disabled">
                    {{
                      t(
                        'companyDetail.past.earningsRevenueHistory.chart.tooltip.profitMargin'
                      )
                    }}
                  </span>
                </div>
              </v-col>
            </v-row>
          </template>
          <template v-if="activeLegends.includes('fcf')">
            <v-divider />

            <v-row no-gutters>
              <v-col>
                {{
                  t(
                    'companyDetail.past.earningsRevenueHistory.chart.tooltip.fcf'
                  )
                }}
              </v-col>
              <v-col>
                <div class="text-hc-series3-color">
                  {{ tooltipData.fcf }}
                </div>
              </v-col>
            </v-row>
          </template>
          <template v-if="activeLegends.includes('cfo')">
            <v-divider />

            <v-row no-gutters>
              <v-col>
                {{
                  t(
                    'companyDetail.past.earningsRevenueHistory.chart.tooltip.cfo'
                  )
                }}
              </v-col>
              <v-col>
                <div class="text-hc-series4-color">
                  {{ tooltipData.cfo }}
                </div>
              </v-col>
            </v-row>
          </template>
          <template v-if="activeLegends.includes('opex')">
            <v-divider />

            <v-row no-gutters>
              <v-col>
                {{
                  t(
                    'companyDetail.past.earningsRevenueHistory.chart.tooltip.opex'
                  )
                }}
              </v-col>
              <v-col>
                <div class="text-hc-series5-color">
                  {{ tooltipData.opex }}
                </div>
              </v-col>
            </v-row>
          </template>
        </v-card-item>
      </v-card>
    </div>

    <charts
      ref="chartRef"
      class="earnings-revenue-history-chart__chart"
      constructorType="chart"
      :options="options"
    />

    <v-btn-toggle
      class="d-flex flex-wrap"
      :style="{ height: smAndDown ? '96px' : '48px' }"
      multiple
      mandatory
      variant="outlined"
      v-model="activeLegends"
    >
      <v-btn
        v-for="item in legendOptions"
        :key="`legend-${item.value}`"
        class="earnings-revenue-history-chart__legend-button"
        :value="item.value"
        size="small"
        :text="item.text"
        variant="elevated"
      >
        <template #prepend>
          <span
            class="earnings-revenue-history-chart__circle-indicator"
            :style="{
              backgroundColor: activeLegends.includes(item.value)
                ? item.color
                : 'transparent',
              borderColor: item.color,
            }"
          />
        </template>
      </v-btn>
    </v-btn-toggle>
  </div>
</template>

<style scoped lang="scss">
@use 'vuetify/settings' as vuetify;

.earnings-revenue-history-chart {
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
