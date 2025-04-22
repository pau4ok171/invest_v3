<script setup lang="ts">
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
  analysts: number
  lastUpdated: number
}
interface ChartData {
  currency: string
  financialData: FinancialData[]
}

// Reactive states
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
    text: 'Analysts\' EPS Range',
    value: 'epsRange',
  }
]

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
    lastUpdated: 1745280000,
  },
  {
    date: 1682812800000,
    eps: 0.19,
    epsHigh: 0.19,
    epsLow: 0.19,
    analysts: null,
    lastUpdated: 1745280000,
  },
  {
    date: 1690675200000,
    eps: 0.42,
    epsHigh: 0.42,
    epsLow: 0.42,
    analysts: null,
    lastUpdated: 1745280000,
  },
  {
    date: 1698537600000,
    eps: 0.77,
    epsHigh: 0.77,
    epsLow: 0.77,
    analysts: null,
    lastUpdated: 1745280000,
  },
  {
    date: 1706400000000,
    eps: 1.21,
    epsHigh: 1.21,
    epsLow: 1.21,
    analysts: null,
    lastUpdated: 1745280000,
  },
  {
    date: 1714262400000,
    eps: 1.73,
    epsHigh: 1.73,
    epsLow: 1.73,
    analysts: null,
    lastUpdated: 1745280000,
  },
  {
    date: 1722124800000,
    eps: 2.15,
    epsHigh: 2.15,
    epsLow: 2.15,
    analysts: null,
    lastUpdated: 1745280000,
  },
  {
    date: 1729987200000,
    eps: 2.56,
    epsHigh: 2.56,
    epsLow: 2.56,
    analysts: null,
    lastUpdated: 1745280000,
  },
  {
    date: 1737763200000,
    eps: 2.97,
    epsHigh: 2.97,
    epsLow: 2.97,
    analysts: null,
    lastUpdated: 1745280000,
  },
  {
    date: 1769817600000,
    eps: 4.26,
    epsHigh: 5.33,
    epsLow: 3.56,
    analysts: 29,
    lastUpdated: 1745280000,
  },
  {
    date: 1801353600000,
    eps: 5.44,
    epsHigh: 7.55,
    epsLow: 4.61,
    analysts: 26,
    lastUpdated: 1745280000,
  },
  {
    date: 1832889600000,
    eps: 6.39,
    epsHigh: 9.73,
    epsLow: 5.33,
    analysts: 13,
    lastUpdated: 1745280000,
  }
  ]
}

const [eps, epsRange] = [
  data.financialData.map(p => [p.date, p.eps]),
  data.financialData.filter(p => p.epsHigh != null && p.epsLow != null).map(p => [p.date, p.epsLow, p.epsHigh]),
]

const options = computed<Options>(() => ({
  chart: {
    type: 'spline',
    height: CHART_HEIGHT,
    backgroundColor: 'transparent',
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
  series: [{
    type: 'spline',
    name: 'eps',
    data: eps,
    lineWidth: 3,
    visible: activeLegends.value.includes('eps'),
    zoneAxis: 'x',
    zones: [{
      value: currentDate.toMillis(),
      color: 'rgb(var(--v-theme-hc-series1-color))',
    }, {
      color: 'rgb(var(--v-theme-hc-series2-color))',
    }],
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
    zones: [{
      value: currentDate.toMillis(),
      color: 'url(#Chart_01_Gradient_02)',
    }, {
      color: 'url(#Chart_02_Gradient_02)',
    }],
  }],
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
    },
  },
}))
</script>

<template>
  <div class="eps-growth-forecast-chart">
    <div class="earnings-and-revenue-growth-forecast-chart__tooltip-box">

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
  .eps-growth-forecast-chart {
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
      border: 1px solid;
      transition: background-color 0.3s;
    }
  }
</style>