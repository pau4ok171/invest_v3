<script setup lang="ts">
// Composables
import { useFinancialFormatter } from '@/composables/formatter'
import { useDisplay } from 'vuetify'
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, nextTick, ref, watch } from 'vue'
import { DateTime } from 'ts-luxon'
import { data as finData, dividendsData } from './bigFinData'

// Types
import type {
  Options,
  Point,
  SVGPathArray,
  SVGElement,
  Series,
  Chart,
  SeriesOptionsType,
} from 'highcharts'
import type { FinUnit } from '@/composables/formatter'

// Constants
const CHART_HEIGHT = 356
const TOOLTIP_WIDTH = 340

// Interfaces
interface FinancialData {
  dividendYield: [number, number]
  dividendPayments: [number, number]
  annualAmount: [number, number]
  eps: [number, number]
}
interface FinancialObject {
  dividendYield: [number, number][]
  dividendPayments: [number, number][]
  annualAmount: [number, number][]
  eps: [number, number][]
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
const { t, locale } = useI18n()
const chartRef = ref<{ chart: Chart } | null>(null)
const currentDate = DateTime.now()
const currentPoint = ref<Point | null>(null)
const chartElements = {
  tooltipConnector: null as SVGElement | null,
  markers: null as SVGElement[] | null,
  oneYearZone: null as SVGElement | null,
}
const activeLegends = ref<string[]>([
  'dividendYield',
  'dividendPayments',
  'annualAmount',
])
const legendOptions = computed(() => [
  {
    text: t('companyDetail.dividend.stabilityAndGrowth.legends.dividendYield'),
    value: 'dividendYield',
    color: 'rgb(var(--v-theme-hc-series1-color))',
    fillColor: 'url(#Chart_01_Gradient_02)',
    type: 'areaspline',
    yAxis: 0,
  },
  {
    text: t(
      'companyDetail.dividend.stabilityAndGrowth.legends.dividendPayments'
    ),
    value: 'dividendPayments',
    color: 'rgb(var(--v-theme-hc-series2-color))',
    fillColor: 'url(#Chart_02_Gradient_02)',
    type: 'column',
    yAxis: 1,
  },
  {
    text: t('companyDetail.dividend.stabilityAndGrowth.legends.annualAmount'),
    value: 'annualAmount',
    color: 'rgb(var(--v-theme-hc-series5-color))',
    fillColor: 'url(#Chart_05_Gradient_02)',
    type: 'spline',
    yAxis: 1,
  },
  {
    text: t('companyDetail.dividend.stabilityAndGrowth.legends.eps'),
    value: 'eps',
    color: 'rgb(var(--v-theme-hc-series3-color))',
    fillColor: 'url(#Chart_03_Gradient_02)',
    type: 'spline',
    yAxis: 2,
  },
])

const tooltipData = computed(() => {
  if (!currentPoint.value) return null

  const point = currentPoint.value
  const dataKey = point.category
  const dataInstance = data.financialData.find(
    (f) => f.dividendYield[0] === dataKey
  )

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
    dividendPayments: fin({
      currency: data.currency,
      value: dataInstance.dividendPayments[1],
      finUnit: data.financialUnit,
    }),
    annualAmount: fin({
      currency: data.currency,
      value: dataInstance.annualAmount[1],
      finUnit: data.financialUnit,
    }),
    dividendYield: (dataInstance.dividendYield[1] * 100).toFixed(2) + '%',
    eps: fin({
      currency: data.currency,
      value: dataInstance.eps[1],
      finUnit: data.financialUnit,
    }),
    tooltipStyle: {
      transform: `translateX(${tooltipPos}px)`,
    },
  }
})

const preparedData = {
  dividendPayments: Object.entries(
    dividendsData.historical_dividend_payments
  ).map(([dateStr, v]) => [Number(dateStr), (v as number) / 4]),
  annualAmount: Object.entries({
    ...dividendsData.historical_dividend_payments,
    ...dividendsData.merged_future_dividends_per_share,
  }).map(([dateStr, v]) => [Number(dateStr), v as number]),
  dividendYield: Object.entries({
    ...dividendsData.historical_dividend_yield,
    ...dividendsData.merged_future_yield,
  }).map(([dateStr, v]) => [Number(dateStr), v as number]),
  eps: Object.entries(finData).map(([dateStr, v]) => [
    Number(dateStr),
    v.basic_eps.value as number,
  ]),
}

// Собираем все уникальные даты из всех массивов
const allDates = [
  ...new Set([
    ...preparedData.dividendYield.map(([date]) => date),
    ...preparedData.dividendPayments.map(([date]) => date),
    ...preparedData.annualAmount.map(([date]) => date),
    ...preparedData.eps.map(([date]) => date),
  ]),
].sort((a, b) => a - b)

// Создаем массив, объединяя данные по датам
const financialDataArray: FinancialData[] = allDates.map((date) => {
  const findData = (arr: number[][]) =>
    arr.find(([d]) => d === date) || [date, null]

  return {
    dividendYield: findData(preparedData.dividendYield),
    dividendPayments: findData(preparedData.dividendPayments),
    annualAmount: findData(preparedData.annualAmount),
    eps: findData(preparedData.eps),
  } as FinancialData
})

// Data
const data: ChartData = {
  currency: 'US$',
  financialUnit: '',
  financialData: financialDataArray,
}

const { dividendYield, dividendPayments, annualAmount, eps } =
  data.financialData.reduce((acc, curr) => {
    Object.keys(curr).forEach((key) => {
      if (!acc[key as keyof FinancialObject]) {
        acc[key as keyof FinancialObject] = []
      }
      acc[key as keyof FinancialObject].push(curr[key as keyof FinancialObject])
    })
    return acc
  }, {} as FinancialObject)

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
    case 'dividendYield':
      return dividendYield
    case 'dividendPayments':
      return dividendPayments
    case 'annualAmount':
      return annualAmount
    case 'eps':
      return eps
    default:
      return []
  }
}

const options = computed<Options>(
  () =>
    ({
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
              text: t('companyDetail.dividend.stabilityAndGrowth.past'),
              align: 'right',
              style: {
                color: '#606060',
                opacity: 1,
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
              text: t(
                'companyDetail.dividend.stabilityAndGrowth.analystsForecasts'
              ),
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
      yAxis: [
        {
          title: { text: '' },
          gridLineWidth: 1,
          gridLineColor: 'rgba(var(--v-theme-on-surface), 0.1)',
          lineWidth: 0,
          labels: {
            formatter: function () {
              return this.isFirst ? `0%` : this.isLast ? `2.0%` : ''
            },
            style: {
              color: 'rgb(var(--v-theme-on-surface))',
            },
          },
          min: 0,
          max: 0.02,
        },
        {
          visible: false,
          min: 0,
          max: 0.05,
        },
        {
          visible: false,
          min: 0,
          max: 3,
        },
      ],
      series: legendOptions.value.map((series) => ({
        connectNulls: ['spline', 'areaspline'].includes(series.type)
          ? true
          : undefined,
        pointWidth: 7,
        borderRadius: 0,
        type: series.type,
        name: series.value,
        data: getSeriesData(series.value),
        color: series.color,
        fillColor: series.fillColor,
        yAxis: series.yAxis,
        lineWidth: 3,
        visible: activeLegends.value.includes(series.value),
      })) as SeriesOptionsType[],
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
    }) satisfies Options
)

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
  <div class="stability-growth-payments-chart">
    <div class="stability-growth-payments-chart__tooltip-box">
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

          <template v-if="activeLegends.includes('dividendPayments')">
            <v-divider />

            <v-row no-gutters>
              <v-col>{{
                t(
                  'companyDetail.dividend.stabilityAndGrowth.tooltip.dividendPayments'
                )
              }}</v-col>
              <v-col>
                <div class="text-hc-series1-color">
                  {{ tooltipData.dividendPayments }}
                  <span class="text-disabled"
                    >/{{
                      t(
                        'companyDetail.dividend.stabilityAndGrowth.tooltip.quarterly'
                      )
                    }}</span
                  >
                </div>
              </v-col>
            </v-row>
          </template>
          <template v-if="activeLegends.includes('annualAmount')">
            <v-divider />

            <v-row no-gutters>
              <v-col>{{
                t(
                  'companyDetail.dividend.stabilityAndGrowth.tooltip.annualAmount'
                )
              }}</v-col>
              <v-col>
                <div class="text-hc-series3-color">
                  {{ tooltipData.annualAmount }}
                  <span class="text-disabled"
                    >/{{
                      t(
                        'companyDetail.dividend.stabilityAndGrowth.tooltip.year'
                      )
                    }}</span
                  >
                </div>
              </v-col>
            </v-row>
          </template>
          <template v-if="activeLegends.includes('eps')">
            <v-divider />

            <v-row no-gutters>
              <v-col>{{
                t('companyDetail.dividend.stabilityAndGrowth.tooltip.eps')
              }}</v-col>
              <v-col>
                <div class="text-hc-series4-color">
                  {{ tooltipData.eps }}
                  <span class="text-disabled"
                    >/{{
                      t(
                        'companyDetail.dividend.stabilityAndGrowth.tooltip.year'
                      )
                    }}</span
                  >
                </div>
              </v-col>
            </v-row>
          </template>
          <template v-if="activeLegends.includes('dividendYield')">
            <v-divider />

            <v-row no-gutters>
              <v-col>{{
                t(
                  'companyDetail.dividend.stabilityAndGrowth.tooltip.dividendYield'
                )
              }}</v-col>
              <v-col>
                <div class="text-hc-series2-color">
                  {{ tooltipData.dividendYield }}
                  <span class="text-disabled"
                    >/{{
                      t(
                        'companyDetail.dividend.stabilityAndGrowth.tooltip.year'
                      )
                    }}</span
                  >
                </div>
              </v-col>
            </v-row>
          </template>
        </v-card-item>
      </v-card>
    </div>

    <charts
      ref="chartRef"
      class="stability-growth-payments-chart__chart"
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
        class="stability-growth-payments-chart__legend-button"
        :value="item.value"
        size="small"
        :text="item.text"
        variant="elevated"
      >
        <template #prepend>
          <span
            class="stability-growth-payments-chart__circle-indicator"
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

.stability-growth-payments-chart {
  &__tooltip-box {
    height: 140px;
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
