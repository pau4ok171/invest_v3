<script setup lang="ts">
// Components
import Chart05Gradient01 from '@/components/lineair_gradient/Chart05Gradient01.vue'
import Chart05Gradient02 from '@/components/lineair_gradient/Chart05Gradient02.vue'

// Utilities
import { computed } from 'vue'

// Types
import type { Options } from 'highcharts'

interface ChartData {
  datetime: number | 'current'
  sharePrice: number
  average1YPrice: number
  dispersion: number
}

const currentDare = Date.now()

const data: ChartData[] = [
  {
    datetime: 1774990800,
    sharePrice: 110.15,
    average1YPrice: 171.89,
    dispersion: 0.122,
  },
  {
    datetime: 1772312400,
    sharePrice: 124.92,
    average1YPrice: 173.62,
    dispersion: 0.109,
  },
  {
    datetime: 1769893200,
    sharePrice: 120.07,
    average1YPrice: 174.25,
    dispersion: 0.108,
  },
  {
    datetime: 1767214800,
    sharePrice: 134.29,
    average1YPrice: 172.95,
    dispersion: 0.102,
  },
  {
    datetime: 1764536400,
    sharePrice: 138.25,
    average1YPrice: 171.19,
    dispersion: 0.104,
  },
  {
    datetime: 1761944400,
    sharePrice: 135.4,
    average1YPrice: 150.43,
    dispersion: 0.131,
  },
  {
    datetime: 1759266000,
    sharePrice: 117.0,
    average1YPrice: 149.8,
    dispersion: 0.127,
  },
  {
    datetime: 1756674000,
    sharePrice: 119.37,
    average1YPrice: 148.68,
    dispersion: 0.138,
  },
  {
    datetime: 1753995600,
    sharePrice: 109.21,
    average1YPrice: 139.23,
    dispersion: 0.173,
  },
  {
    datetime: 1751317200,
    sharePrice: 124.3,
    average1YPrice: 132.34,
    dispersion: 0.166,
  },
  {
    datetime: 1748725200,
    sharePrice: 109.63,
    average1YPrice: 119.29,
    dispersion: 0.118,
  },
  {
    datetime: 1746046800,
    sharePrice: 83.04,
    average1YPrice: 99.9,
    dispersion: 0.142,
  },
  {
    datetime: 1743454800,
    sharePrice: 90.36,
    average1YPrice: 96.39,
    dispersion: 0.157,
  },
  {
    datetime: 1740776400,
    sharePrice: 82.28,
    average1YPrice: 88.04,
    dispersion: 0.18,
  },
  {
    datetime: 1738357200,
    sharePrice: 63.03,
    average1YPrice: 66.63,
    dispersion: 0.199,
  },
  {
    datetime: 1735678800,
    sharePrice: 49.52,
    average1YPrice: 65.63,
    dispersion: 0.19,
  },
  {
    datetime: 1733000400,
    sharePrice: 46.77,
    average1YPrice: 65.29,
    dispersion: 0.194,
  },
  {
    datetime: 1730408400,
    sharePrice: 42.33,
    average1YPrice: 63.91,
    dispersion: 0.197,
  },
  {
    datetime: 1727730000,
    sharePrice: 43.5,
    average1YPrice: 63.87,
    dispersion: 0.2,
  },
  {
    datetime: 1725138000,
    sharePrice: 48.51,
    average1YPrice: 62.97,
    dispersion: 0.214,
  },
  {
    datetime: 1722459600,
    sharePrice: 46.51,
    average1YPrice: 49.26,
    dispersion: 0.17,
  },
  {
    datetime: 1719781200,
    sharePrice: 42.3,
    average1YPrice: 46.0,
    dispersion: 0.169,
  },
  {
    datetime: 1717189200,
    sharePrice: 39.77,
    average1YPrice: 43.02,
    dispersion: 0.211,
  },
  {
    datetime: 1714510800,
    sharePrice: 28.91,
    average1YPrice: 28.15,
    dispersion: 0.147,
  },
  {
    datetime: 1711918800,
    sharePrice: 27.78,
    average1YPrice: 27.51,
    dispersion: 0.15,
  },
]

const sharePrices = data.map((p) => p.sharePrice).reverse()
const averages = data.map((p) => p.average1YPrice).reverse()
const averagesRange = data
  .map((p) => [
    p.average1YPrice * (1 - p.dispersion),
    p.average1YPrice * (1 + p.dispersion),
  ])
  .reverse()

const options = computed<Options>(() => ({
  chart: {
    type: 'spline',
    height: 356,
    width: null,
    backgroundColor: 'transparent',
    events: {
      load: function () {
        const chart = this
        // Блокируем стандартное скрытие
        chart.tooltip.hide = function () {}
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
    plotLines: [
      {
        color: '#666',
        width: 2,
        value: currentDare,
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
        return this.isFirst ? `US$20` : this.isLast ? `US$${this.value}` : ''
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
      data: sharePrices,
      color: 'rgb(var(--v-theme-info))',
      lineWidth: 3,
      pointStart: Date.parse('2023-04-01'),
      enableMouseTracking: false,
    },
    {
      name: 'Average 1Y Target',
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
      color: '#A54CEC',
      fillOpacity: 0.5,
      fill: 'url(#Chart_05_Gradient_02)',
      lineWidth: 0,
      linkedTo: ':previous',
      zIndex: 0,
      pointStart: Date.parse('2024-04-01'),
      enableMouseTracking: false,
    },
  ],
  tooltip: {
    useHTML: true,
    outside: true,
    stickOnContact: true,
    // Критически важные дополнения:
    style: {
      pointerEvents: 'none', // Позволяет курсору "проходить сквозь" tooltip
      zIndex: 1000, // Гарантирует поверх других элементов
    },
    positioner: function (boxWidth, boxHeight, point) {
      return {
        x: point.plotX + this.chart.plotLeft - boxWidth,
        y: this.chart.plotTop - boxHeight - 20,
      }
    },
    formatter: function () {
      console.log(this)
      return `
      <div class="analyst-price-targets-chart-tooltip">
        <div class="analyst-price-targets-chart-tooltip__header">
          <div class="text-info">Apr 18 2025</div>
          <div>54 Analysts</div>
        </div>
        <div class="analyst-price-targets-chart-tooltip__divider"></div>
        <div class="analyst-price-targets-chart-tooltip__grid">
           <div>Share Price</div>
           <div class="analyst-price-targets-chart-tooltip__share-price">US$101.49</div>
        </div>
        <div class="analyst-price-targets-chart-tooltip__divider"></div>
        <div class="analyst-price-targets-chart-tooltip__grid">
            <div>Average 1Y Price Target</div>
            <div class="analyst-price-targets-chart-tooltip__average">US$165.66 <span class="text-success ml-4">+63.2%</span></div>
        </div>
        <div class="analyst-price-targets-chart-tooltip__divider"></div>
        <div class="analyst-price-targets-chart-tooltip__grid">
          <div>Agreement</div>
          <div class="d-flex flex-column">
            <div class="text-success">Good</div>
            <div>Analysts agreement range is spread less than 15% from the average</div>
          </div>
        </div>
      </div>
      `
    },
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
  annotations: [
    {
      labels: [
        {
          point: {
            x: currentDare - 3 * 30 * 24 * 3600 * 1000,
            y: 50,
            xAxis: 0,
            yAxis: 0,
          },
          text: 'Past',
          style: {
            color: '#666',
          },
        },
        {
          point: {
            x: currentDare + 3 * 30 * 24 * 3600 * 1000,
            y: 50,
            xAxis: 0,
            yAxis: 0,
          },
          text: '12M Forecast',
          style: {
            color: '#666',
          },
        },
      ],
    },
  ],
}))
</script>

<template>
  <div class="analyst-price-targets-chart">
    <div class="analyst-price-targets-chart__tooltip-box"></div>
    <charts
      class="analyst-price-targets-chart__chart"
      constructorType="chart"
      :options="options"
    />
    <chart05-gradient01 />
    <chart05-gradient02 />
  </div>
</template>

<style lang="scss">
.analyst-price-targets-chart__tooltip-box {
  height: 190px;
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
  border-radius: 8px;
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
