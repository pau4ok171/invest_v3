<script setup lang="ts">
// Utilities
import { computed, nextTick, ref, watch } from 'vue'
import { DateTime } from 'ts-luxon'

// Types
import type { Options, Point, SVGPathArray, SVGElement, Series } from 'highcharts'

// Constants
const CHART_HEIGHT = 356
const TOOLTIP_WIDTH = 380
const EARNINGS_COLOR = 'rgb(35, 148, 223)'
const REVENU_COLOR = 'rgb(113, 231, 214)'
const FCF_COLOR = 'rgb(187, 71, 134)'
const CFO_COLOR = 'rgb(229, 176, 97)'
const MAIN_TEXT_COLOR = 'rgb(var(--v-theme-on-surface))'

// Interfaces
interface FinancialData {
  date: number
  revenue: number
  earnings: number
  freeCashFlow: number
  cashFromOp: number
  analysts: number
}
interface ChartData {
  currency: string
  financialUnit: '' | 't' | 'm' | 'b' | 'T'
  financialData: FinancialData[]
}

// Reactive states
const currentDate = DateTime.now()
const currentPoint = ref<Point | null>(null)
const chartElements = {
  toolbarConnector: null as SVGElement | null,
  revenueMarker: null as SVGElement | null,
  earningsMarker: null as SVGElement | null,
  fcfMarker: null as SVGElement | null,
  cfoMarker: null as SVGElement | null,
  oneYearZone: null as SVGElement | null,
}
const activeLegends = ref<string[]>(['revenue', 'earnings'])
const legends = [
  { text: 'Revenue', value: 'revenue' },
  { text: 'Earnings', value: 'earnings' },
  { text: 'Free Cash Flow', value: 'fcf' },
  { text: 'Cash From Op', value: 'cfo' },
]

const tooltipData = computed(() => {
  if (!currentPoint.value) return null

  const point = currentPoint.value
  const dataKey = point.category
  const dataInstance = data.financialData.find((f) => f.date === dataKey)

  if (!dataInstance) return null

  const tooltipPos =
    (point.plotX || 0) + point.series.chart.plotLeft - TOOLTIP_WIDTH <= 0
      ? (point.plotX || 0) + point.series.chart.plotLeft
      : (point.plotX || 0) + point.series.chart.plotLeft - TOOLTIP_WIDTH

  return {
    date: DateTime.fromMillis(point.category as number).toFormat('LLL dd yyyy'),
    revenue: {
      value: `${data.currency}${dataInstance.revenue / 1000}b`,
      analysts: 50,
      lastUpdated: DateTime.fromMillis(1745193600000).toFormat('LLL dd yyyy'),
    },
    earnings: {
      value: `${data.currency}${dataInstance.earnings / 1000}b`,
      analysts: 40,
      lastUpdated: DateTime.fromMillis(1745193600000).toFormat('LLL dd yyyy'),
    },
    fcf: {
      value: `${data.currency}${dataInstance.freeCashFlow / 1000}b`,
      analysts: 30,
      lastUpdated: DateTime.fromMillis(1745193600000).toFormat('LLL dd yyyy'),
    },
    cfo: {
      value: `${data.currency}${dataInstance.cashFromOp / 1000}b`,
      analysts: 20,
      lastUpdated: DateTime.fromMillis(1745193600000).toFormat('LLL dd yyyy'),
    },
    tooltipStyle: {
      transform: `translateX(${tooltipPos}px)`,
    },
  }
})

// Data
const data: ChartData = {
  currency: 'US$',
  financialUnit: 'm',
  financialData: [
    {
      date: 1835568000000,
      revenue: 287928,
      earnings: 158511,
      freeCashFlow: 144364,
      cashFromOp: 155550,
      analysts: 21,
    },
    {
      date: 1803830400000,
      revenue: 248214,
      earnings: 133079,
      freeCashFlow: 126857,
      cashFromOp: 131939,
      analysts: 50,
    },
    {
      date: 1772006400000,
      revenue: 201633,
      earnings: 104904,
      freeCashFlow: 95759,
      cashFromOp: 101337,
      analysts: 55,
    },
    {
      date: 1737763200000,
      revenue: 130497,
      earnings: 72880,
      freeCashFlow: 60853,
      cashFromOp: 64089,
      analysts: null,
    },
    {
      date: 1729987200000,
      revenue: 113269,
      earnings: 63074,
      freeCashFlow: 56546,
      cashFromOp: 58959,
      analysts: null,
    },
    {
      date: 1722124800000,
      revenue: 96307,
      earnings: 53008,
      freeCashFlow: 46786,
      cashFromOp: 48664,
      analysts: null,
    },
    {
      date: 1714262400000,
      revenue: 79774,
      earnings: 42598,
      freeCashFlow: 39334,
      cashFromOp: 40524,
      analysts: null,
    },
    {
      date: 1706400000000,
      revenue: 60922,
      earnings: 29760,
      freeCashFlow: 27021,
      cashFromOp: 28090,
      analysts: null,
    },
    {
      date: 1698537600000,
      revenue: 44870,
      earnings: 18889,
      freeCashFlow: 17515,
      cashFromOp: 18839,
      analysts: null,
    },
    {
      date: 1690675200000,
      revenue: 32681,
      earnings: 10326,
      freeCashFlow: 10323,
      cashFromOp: 11899,
      analysts: null,
    },
    {
      date: 1682812800000,
      revenue: 25878,
      earnings: 4793,
      freeCashFlow: 5101,
      cashFromOp: 6821,
      analysts: null,
    },
    {
      date: 1674950400000,
      revenue: 26974,
      earnings: 4368,
      freeCashFlow: 3808,
      cashFromOp: 5641,
      analysts: null,
    },
    {
      date: 1667088000000,
      revenue: 28566,
      earnings: 5957,
      freeCashFlow: 4829,
      cashFromOp: 6426,
      analysts: null,
    },
    {
      date: 1659225600000,
      revenue: 29738,
      earnings: 7741,
      freeCashFlow: 6264,
      cashFromOp: 7553,
      analysts: null,
    },
    {
      date: 1651363200000,
      revenue: 29541,
      earnings: 9458,
      freeCashFlow: 7926,
      cashFromOp: 8965,
      analysts: null,
    },
    {
      date: 1643500800000,
      revenue: 26914,
      earnings: 9752,
      freeCashFlow: 8132,
      cashFromOp: 9108,
      analysts: null,
    },
    {
      date: 1635638400000,
      revenue: 24274,
      earnings: 8206,
      freeCashFlow: 7156,
      cashFromOp: 8142,
      analysts: null,
    },
    {
      date: 1627776000000,
      revenue: 21897,
      earnings: 7078,
      freeCashFlow: 6665,
      cashFromOp: 7902,
      analysts: null,
    },
    {
      date: 1619913600000,
      revenue: 19256,
      earnings: 5327,
      freeCashFlow: 5516,
      cashFromOp: 6787,
      analysts: null,
    },
    {
      date: 1612051200000,
      revenue: 16675,
      earnings: 4332,
      freeCashFlow: 4694,
      cashFromOp: 5822,
      analysts: null,
    },
    {
      date: 1604188800000,
      revenue: 14777,
      earnings: 3826,
      freeCashFlow: 4230,
      cashFromOp: 5220,
      analysts: null,
    },
    {
      date: 1596326400000,
      revenue: 13065,
      earnings: 3388,
      freeCashFlow: 4961,
      cashFromOp: 5581,
      analysts: null,
    },
    {
      date: 1588464000000,
      revenue: 11778,
      earnings: 3319,
      freeCashFlow: 4434,
      cashFromOp: 4950,
      analysts: null,
    },
    {
      date: 1580601600000,
      revenue: 10918,
      earnings: 2796,
      freeCashFlow: 4272,
      cashFromOp: 4761,
      analysts: null,
    },
    {
      date: 1572739200000,
      revenue: 10018,
      earnings: 2411,
      freeCashFlow: 3647,
      cashFromOp: 4194,
      analysts: null,
    },
    {
      date: 1564876800000,
      revenue: 10185,
      earnings: 2743,
      freeCashFlow: 2447,
      cashFromOp: 3041,
      analysts: null,
    },
    {
      date: 1557014400000,
      revenue: 10729,
      earnings: 3291,
      freeCashFlow: 2408,
      cashFromOp: 3018,
      analysts: null,
    },
    {
      date: 1549152000000,
      revenue: 11716,
      earnings: 4141,
      freeCashFlow: 3143,
      cashFromOp: 3743,
      analysts: null,
    },
    {
      date: 1541289600000,
      revenue: 12422,
      earnings: 4694,
      freeCashFlow: null,
      cashFromOp: 4203,
      analysts: null,
    },
    {
      date: 1533427200000,
      revenue: 11877,
      earnings: 4301,
      freeCashFlow: null,
      cashFromOp: 4873,
      analysts: null,
    },
    {
      date: 1525564800000,
      revenue: 10984,
      earnings: 3784,
      freeCashFlow: null,
      cashFromOp: 4665,
      analysts: null,
    },
    {
      date: 1517702400000,
      revenue: 9714,
      earnings: 3047,
      freeCashFlow: null,
      cashFromOp: 3502,
      analysts: null,
    },
    {
      date: 1509840000000,
      revenue: 8976,
      earnings: 2582,
      freeCashFlow: null,
      cashFromOp: 2865,
      analysts: null,
    },
    {
      date: 1501977600000,
      revenue: 8344,
      earnings: 2288,
      freeCashFlow: null,
      cashFromOp: 2140,
      analysts: null,
    },
    {
      date: 1494115200000,
      revenue: 7542,
      earnings: 1965,
      freeCashFlow: null,
      cashFromOp: 1635,
      analysts: null,
    },
    {
      date: 1486252800000,
      revenue: 6910,
      earnings: 1666,
      freeCashFlow: null,
      cashFromOp: 1672,
      analysts: null,
    },
    {
      date: 1478390400000,
      revenue: 6138,
      earnings: 1220,
      freeCashFlow: null,
      cashFromOp: 1462,
      analysts: null,
    },
    {
      date: 1470528000000,
      revenue: 5439,
      earnings: 923,
      freeCashFlow: null,
      cashFromOp: 1285,
      analysts: null,
    },
    {
      date: 1462665600000,
      revenue: 5164,
      earnings: 688,
      freeCashFlow: null,
      cashFromOp: 1248,
      analysts: null,
    },
    {
      date: 1454803200000,
      revenue: 5010,
      earnings: 614,
      freeCashFlow: null,
      cashFromOp: 1175,
      analysts: null,
    },
    {
      date: 1446940800000,
      revenue: 4860,
      earnings: 600,
      freeCashFlow: null,
      cashFromOp: 1107,
      analysts: null,
    },
    {
      date: 1439078400000,
      revenue: 4780,
      earnings: 526,
      freeCashFlow: null,
      cashFromOp: 1068,
      analysts: null,
    },
    {
      date: 1431216000000,
      revenue: 4730,
      earnings: 628,
      freeCashFlow: null,
      cashFromOp: 1001,
      analysts: null,
    },
    {
      date: 1423353600000,
      revenue: 4682,
      earnings: 631,
      freeCashFlow: null,
      cashFromOp: 906,
      analysts: null,
    },
    {
      date: 1415491200000,
      revenue: 4575,
      earnings: 584,
      freeCashFlow: null,
      cashFromOp: 864,
      analysts: null,
    },
    {
      date: 1407628800000,
      revenue: 4404,
      earnings: 531,
      freeCashFlow: null,
      cashFromOp: 810,
      analysts: null,
    },
    {
      date: 1399766400000,
      revenue: 4278,
      earnings: 499,
      freeCashFlow: null,
      cashFromOp: 810,
      analysts: null,
    },
  ] as FinancialData[],
}

const [date, revenue, earnings, fcf, cfo] = [
  data.financialData
    .map((p) => p.date)
    .slice(0, 16)
    .reverse(),
  data.financialData
    .map((p) => [p.date, p.revenue])
    .slice(0, 16)
    .reverse(),
  data.financialData
    .map((p) => [p.date, p.earnings])
    .slice(0, 16)
    .reverse(),
  data.financialData
    .map((p) => [p.date, p.freeCashFlow])
    .slice(0, 16)
    .reverse(),
  data.financialData
    .map((p) => [p.date, p.cashFromOp])
    .slice(0, 16)
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

function findPointOneYearAgo(series: Series, datetimeInMills: number): Point | null {
  // Ищем ближайшую точку
  let closestPoint = null;
  let minDiff = Infinity;
  const yearAgo = DateTime.fromMillis(datetimeInMills).minus({ year: 1 }).toMillis()

  series.points.forEach(point => {
    const diff = Math.abs(point.x - yearAgo);
    if (diff < minDiff) {
      minDiff = diff;
      closestPoint = point;
    }
  });

  return closestPoint;
}

const options = computed<Options>(
  () =>
    ({
      chart: {
        type: 'areaspline',
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
            color: MAIN_TEXT_COLOR,
          },
        },
        plotBands: [
          {
            from: 0,
            to: currentDate.toMillis(),
            color: 'url(#Actual_Background_Gradient)',
            label: {
              text: 'Past',
              align: 'right',
              style: {
                color: MAIN_TEXT_COLOR,
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
            return this.isFirst ? `US$0` : this.isLast ? `US$300b` : ''
          },
          style: {
            color: 'rgb(var(--v-theme-on-surface))',
          },
        },
        min: 0,
        max: 300000,
      },
      series: [
        {
          type: 'areaspline',
          name: 'revenue',
          data: revenue,
          color: EARNINGS_COLOR,
          fillColor: 'url(#Chart_01_Gradient_02)',
          lineWidth: 3,
          visible: activeLegends.value.includes('revenue'),
        },
        {
          type: 'areaspline',
          name: 'earnings',
          data: earnings,
          color: REVENU_COLOR,
          fillColor: 'url(#Chart_02_Gradient_02)',
          lineWidth: 3,
          visible: activeLegends.value.includes('earnings'),
        },
        {
          type: 'areaspline',
          name: 'fcf',
          data: fcf,
          color: FCF_COLOR,
          fillColor: 'url(#Chart_03_Gradient_02)',
          lineWidth: 3,
          visible: activeLegends.value.includes('fcf'),
        },
        {
          type: 'areaspline',
          name: 'cfo',
          data: cfo,
          color: CFO_COLOR,
          fillColor: 'url(#Chart_04_Gradient_02)',
          lineWidth: 3,
          visible: activeLegends.value.includes('cfo'),
        },
      ],
    }) satisfies Options
)

// Core functions
const updatePointElements = (point: Point) => {
  destroyChartElements()

  const chart = point.series?.chart

  if (!chart) return

  const dataInstance = data.financialData.find((f) => f.date === point.category)

  if (!dataInstance) return

  // Draw main elements
  chartElements.toolbarConnector = drawConnector(point)

  const pointX = (point.plotX || 0) + chart.plotLeft

  // Find series points Y position
  const revenuePoint = chart.series.find((s) => s.name === 'revenue')?.points?.[
    point.index
  ]
  const earningsPoint = chart.series.find((s) => s.name === 'earnings')
    ?.points?.[point.index]
  const fcfPoint = chart.series.find((s) => s.name === 'fcf')?.points?.[
    point.index
  ]
  const cfoPoint = chart.series.find((s) => s.name === 'cfo')?.points?.[
    point.index
  ]

  const revenueY = revenuePoint
    ? (revenuePoint.plotY || 0) + chart.plotTop
    : null
  const earningsY = earningsPoint
    ? (earningsPoint.plotY || 0) + chart.plotTop
    : null
  const fcfY = fcfPoint ? (fcfPoint.plotY || 0) + chart.plotTop : null
  const cfoY = cfoPoint ? (cfoPoint.plotY || 0) + chart.plotTop : null

  // Draw markers
  chartElements.revenueMarker =
    revenueY && activeLegends.value.includes('revenue')
      ? chart.renderer
          .circle(pointX, revenueY, 5)
          .attr({
            fill: 'rgb(var(--v-theme-hc-series1-color))',
            stroke: 'white',
            'stroke-width': 2,
            zIndex: 5,
          })
          .add()
      : null

  chartElements.earningsMarker =
    earningsY && activeLegends.value.includes('earnings')
      ? chart.renderer
          .circle(pointX, earningsY, 5)
          .attr({
            fill: 'rgb(var(--v-theme-hc-series2-color))',
            stroke: 'white',
            'stroke-width': 2,
            zIndex: 5,
          })
          .add()
      : null
  chartElements.fcfMarker =
    fcfY && activeLegends.value.includes('fcf')
      ? chart.renderer
          .circle(pointX, fcfY, 5)
          .attr({
            fill: 'rgb(var(--v-theme-hc-series3-color))',
            stroke: 'white',
            'stroke-width': 2,
            zIndex: 5,
          })
          .add()
      : null

  chartElements.cfoMarker =
    cfoY && activeLegends.value.includes('cfo')
      ? chart.renderer
          .circle(pointX, cfoY, 5)
          .attr({
            fill: 'rgb(var(--v-theme-hc-series4-color))',
            stroke: 'white',
            'stroke-width': 2,
            zIndex: 5,
          })
          .add()
      : null

  // Draw year zone
  const activeLegend = activeLegends.value[0]
  const activeSeries = chart.series.find(s => s.name === activeLegend)
  if (!activeSeries) return;

  const pointOneYAgo = findPointOneYearAgo(activeSeries, activeSeries.points[point.index].category as number)

  chartElements.oneYearZone = pointOneYAgo
    ? chart.renderer
      .rect((pointOneYAgo.plotX || 0) + chart.plotLeft, chart.plotTop, pointX - ((pointOneYAgo.plotX || 0) + chart.plotLeft), chart.plotHeight)
      .attr({
        fill: 'url(#YearMarkerGradient)',
        stroke: 'rgba(35, 148, 223, 0.1)',
        'stroke-width': 1,
        zIndex: -1,
      })
      .add()
    : null
}

const updateTooltip = (point: Point, force: boolean = false) => {
  if (currentPoint.value && point.index === currentPoint.value.index && !force)
    return

  updatePointElements(point)
  currentPoint.value = point
}

watch(
  () => activeLegends,
  () => {
    if (currentPoint.value) {
      nextTick(() => updateTooltip(currentPoint.value, true))
    }
  },
  { deep: true }
)
</script>

<template>
  <div class="earnings-and-revenue-growth-forecast-chart">
    <div class="earnings-and-revenue-growth-forecast-chart__tooltip-box">
      <v-card
        v-if="tooltipData"
        :width="TOOLTIP_WIDTH"
        :style="tooltipData.tooltipStyle"
        class="text-disabled"
      >
        <v-card-item>
          <v-row no-gutters>
            <v-col class="text-high-emphasis">{{ tooltipData.date }}</v-col>
            <v-col></v-col>
            <v-col><div class="text-center">Analysts</div></v-col>
            <v-col>Last Updated</v-col>
          </v-row>

          <template v-if="activeLegends.includes('revenue')">
            <v-divider />

            <v-row no-gutters>
              <v-col>Revenue</v-col>
              <v-col>
                <div class="text-hc-series1-color">
                  {{ tooltipData.revenue.value
                  }}<span class="text-disabled">/yr</span>
                </div>
              </v-col>
              <v-col class="text-high-emphasis">
                <div class="text-center">
                  {{ tooltipData.revenue.analysts }}
                </div>
              </v-col>
              <v-col class="text-high-emphasis">
                {{ tooltipData.revenue.lastUpdated }}
              </v-col>
            </v-row>
          </template>

          <template v-if="activeLegends.includes('earnings')">
            <v-divider />

            <v-row no-gutters>
              <v-col>Earnings</v-col>
              <v-col>
                <div class="text-hc-series2-color">
                  {{ tooltipData.earnings.value
                  }}<span class="text-disabled">/yr</span>
                </div>
              </v-col>
              <v-col class="text-high-emphasis">
                <div class="text-center">
                  {{ tooltipData.earnings.analysts }}
                </div>
              </v-col>
              <v-col class="text-high-emphasis">
                {{ tooltipData.earnings.lastUpdated }}
              </v-col>
            </v-row>
          </template>

          <template v-if="activeLegends.includes('fcf')">
            <v-divider />

            <v-row no-gutters>
              <v-col>Free Cash Flow</v-col>
              <v-col>
                <div class="text-hc-series3-color">
                  {{ tooltipData.fcf.value
                  }}<span class="text-disabled">/yr</span>
                </div>
              </v-col>
              <v-col class="text-high-emphasis">
                <div class="text-center">
                  {{ tooltipData.fcf.analysts }}
                </div>
              </v-col>
              <v-col class="text-high-emphasis">
                {{ tooltipData.fcf.lastUpdated }}
              </v-col>
            </v-row>
          </template>

          <template v-if="activeLegends.includes('cfo')">
            <v-divider />

            <v-row no-gutters>
              <v-col>Cash From Op</v-col>
              <v-col>
                <div class="text-hc-series4-color">
                  {{ tooltipData.cfo.value
                  }}<span class="text-disabled">/yr</span>
                </div>
              </v-col>
              <v-col class="text-high-emphasis">
                <div class="text-center">
                  {{ tooltipData.cfo.analysts }}
                </div>
              </v-col>
              <v-col class="text-high-emphasis">
                {{ tooltipData.cfo.lastUpdated }}
              </v-col>
            </v-row>
          </template>
        </v-card-item>
      </v-card>
    </div>
    <charts
      class="earnings-and-revenue-growth-forecast-chart__chart"
      constructorType="chart"
      :options="options"
    />
    <v-btn-toggle multiple mandatory variant="outlined" v-model="activeLegends">
      <v-btn
        v-for="item in legends"
        :key="`legend-${item.value}`"
        class="earnings-and-revenue-growth-forecast-chart__legend-button"
        :value="item.value"
        size="small"
        :text="item.text"
      >
        <template #prepend>
          <span
            :class="[
              'earnings-and-revenue-growth-forecast-chart__circle-indicator',
              `earnings-and-revenue-growth-forecast-chart__circle-indicator--${item.value}`,
              {
                [`earnings-and-revenue-growth-forecast-chart__circle-indicator--${item.value}-active`]:
                  activeLegends.includes(item.value),
              },
            ]"
          />
        </template>
      </v-btn>
    </v-btn-toggle>
  </div>
</template>

<style scoped lang="scss">
.earnings-and-revenue-growth-forecast-chart {
  &__tooltip-box {
    height: 190px;
    position: relative;
    display: flex;
    align-items: end;
    font-weight: 400;
    font-size: 0.75rem;
    line-height: 1.125rem;
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
    border: 1px solid transparent;
    background-color: transparent;
    transition: background-color 0.3s;

    &--revenue {
      border-color: rgb(35, 148, 223);
      &-active {
        background-color: rgb(35, 148, 223);
      }
    }
    &--earnings {
      border-color: rgb(113, 231, 214);

      &-active {
        background-color: rgb(113, 231, 214);
      }
    }
    &--fcf {
      border-color: rgb(187, 71, 134);

      &-active {
        background-color: rgb(187, 71, 134);
      }
    }
    &--cfo {
      border-color: rgb(229, 176, 97);

      &-active {
        background-color: rgb(229, 176, 97);
      }
    }
  }
}
</style>
