<script setup lang="ts">
// Components
import BackgroundGradient from '@/components/lineair_gradient/BackgroundGradient.vue'
import ChartGradient from '@/components/lineair_gradient/ChartGradient.vue'

// Composables
import { useI18n } from 'vue-i18n'

// Utilities
import { computed, ref, watch } from 'vue'
import { debounce } from 'lodash'
import Highcharts from 'highcharts'

// Types
import type { Chart, Options } from 'highcharts'

const HMdataPE = [
  [1703980800000, 36],
  [1696032000000, 30.4],
  [1688083200000, 35],
  [1680220800000, 31.1],
  [1672444800000, 26.5],
  [1664496000000, 24.9],
  [1656547200000, 26.4],
  [1648684800000, 31.9],
  [1640908800000, 35.5],
  [1632960000000, 31.2],
  [1625011200000, 33.3],
  [1617148800000, 31.7],
  [1609372800000, 32.8],
  [1601424000000, 33.5],
  [1593475200000, 34.9],
  [1585612800000, 25.9],
  [1577750400000, 27.1],
  [1569801600000, 25.8],
  [1561852800000, 26.2],
  [1553990400000, 25.9],
]
const HMdataPS = [
  [1703980800000, 12.6],
  [1696032000000, 10.4],
  [1688083200000, 11.9],
  [1680220800000, 10.3],
  [1672444800000, 8.8],
  [1664496000000, 8.6],
  [1656547200000, 9.7],
  [1648684800000, 12.0],
  [1640908800000, 13.7],
  [1632960000000, 12.0],
  [1625011200000, 12.1],
  [1617148800000, 11.1],
  [1609372800000, 11.0],
  [1601424000000, 10.8],
  [1593475200000, 10.8],
  [1585612800000, 8.6],
  [1577750400000, 9.0],
  [1569801600000, 8.2],
  [1561852800000, 7.4],
  [1553990400000, 6.6],
]
const HMdataPB = [
  [1703980800000, 12.5],
  [1696032000000, 10.6],
  [1688083200000, 12.3],
  [1680220800000, 11.0],
  [1672444800000, 9.8],
  [1664496000000, 10],
  [1656547200000, 11.5],
  [1648684800000, 14.2],
  [1640908800000, 15.8],
  [1632960000000, 14.2],
  [1625011200000, 15.8],
  [1617148800000, 13.9],
  [1609372800000, 14.4],
  [1601424000000, 13.2],
  [1593475200000, 12.9],
  [1585612800000, 12.9],
  [1577750400000, 13.0],
  [1569801600000, 10.5],
  [1561852800000, 10.9],
  [1553990400000, 10],
]

const tooltipFormat =
  '' +
  '<div class="historical-metrics-chart__tooltip">' +
  '<table class="historical-metrics-chart__tooltip-table">' +
  '<thead><tr><th colspan="2">{point.key}</th></tr></thead>' +
  '<tbody>' +
  '<tr>' +
  '<td class="historical-metrics-chart__tooltip-title">SBER</td>' +
  '<td class="historical-metrics-chart__tooltip-value">{point.y}x</td>' +
  '</tr>' +
  '</tbody>' +
  '</table>' +
  '</div>'

const chartRef = ref<{ chart: Chart }>()
const { locale } = useI18n()

const chartOptions = computed<Options>(
  () =>
    ({
      lang: {
        locale: locale.value,
      },
      chart: {
        type: 'areaspline',
        spacingTop: 60,
        backgroundColor: 'rgb(var(--v-theme-surface-light))',
        plotBackgroundColor: 'url(#ActualBackgroundGradient)',
        style: {
          fontFamily: 'inherit',
          fontSize: '1rem',
          fontWeight: 'normal',
        },
        zooming: {
          mouseWheel: {
            enabled: false,
          },
        },
      },
      title: {
        text: undefined,
      },
      scrollbar: {
        enabled: false,
      },
      credits: {
        enabled: false,
      },
      navigator: {
        enabled: false,
      },
      rangeSelector: {
        enabled: false,
      },
      plotOptions: {
        series: {
          threshold: null,
          fillColor: 'url(#Chart_01_Gradient_01)',
          fillOpacity: 0.4,
          lineWidth: 3,
          color: '#2394df',
          marker: {
            symbol: 'circle',
          },
        },
      },
      series: [
        {
          type: 'areaspline',
          visible: true,
          name: 'PE',
          data: HMdataPE.reverse(),
        },
        {
          type: 'areaspline',
          visible: false,
          name: 'PS',
          data: HMdataPS.reverse(),
        },
        {
          type: 'areaspline',
          visible: false,
          name: 'PB',
          data: HMdataPB.reverse(),
        },
      ],
      tooltip: {
        outside: true,
        backgroundColor: undefined,
        borderWidth: 0,
        shadow: false,
        style: {
          padding: '0',
        },
        xDateFormat: '%b %e %Y',
        useHTML: true,
        headerFormat: '',
        footerFormat: '',
        pointFormat: tooltipFormat,
      },
      xAxis: {
        ordinal: false,
        units: [['year', [1, 3, 5]]],
        labels: {
          style: {
            color: 'rgb(var(--v-theme-on-surface-light))',
          },
        },
        crosshair: {
          color: '#2394df',
        },
      },
      yAxis: [
        {
          opposite: false,
          tickColor: 'rgba(var(--v-theme-on-surface-light), .1)',
          gridLineColor: 'rgba(var(--v-theme-on-surface-light), .1)',
          gridLineWidth: 1,
          tickLength: 30,
          tickWidth: 1,
          tickInterval: 10,
          min: 0,
          max: 40,
          showLastLabel: true,
          labels: {
            allowOverlap: true,
            overflow: 'allow',
            step: 4,
            x: -20,
            style: {
              color: 'rgb(var(--v-theme-on-surface-light))',
            },
          },
        },
        {
          tickColor: 'rgba(var(--v-theme-on-surface-light), .1)',
          tickLength: 30,
          gridLineWidth: 0,
          tickWidth: 1,
          tickInterval: 10,
          linkedTo: 0,
          labels: {
            enabled: false,
          },
        },
      ],
    }) satisfies Options
)

const reinitChart = () => {
  if (!chartRef.value?.chart) return

  const chart = chartRef.value.chart
  const renderTo = chart.renderTo

  chart.destroy()
  const newChart = new Highcharts.StockChart(renderTo, chartOptions.value)

  chartRef.value.chart = newChart
}

watch(locale, debounce(reinitChart, 100))
</script>

<template>
  <div class="detail-historical-metrics-chart">
    <charts
      constructorType="stockChart"
      ref="chartRef"
      :options="chartOptions"
    />
    <background-gradient />
    <chart-gradient />
  </div>
</template>

<style lang="scss">
@use 'vuetify/settings' as vuetify;

.detail-historical-metrics-chart svg {
  height: auto;
  width: auto;
}
.historical-metrics-chart__tooltip {
  background: rgb(var(--v-theme-surface-bright));
  padding: 8px;
  margin: 0;
  width: 340px;
  max-width: 340px;

  @media #{map-get(vuetify.$display-breakpoints, 'md-and-down')} {
    width: 180px;
  }
}
.historical-metrics-chart__tooltip-table {
  width: 100%;
  table-layout: auto;
  margin: 0 auto;
  border-spacing: 0;
  color: rgb(var(--v-theme-on-surface-light));
  background-color: rgb(var(--v-theme-surface-bright));
  user-select: none;
}
.historical-metrics-chart__tooltip-table thead tr th {
  line-height: 1.5;
  text-align: left;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.2);
  text-transform: capitalize;
  font-size: 0.75rem;
}
.historical-metrics-chart__tooltip-title {
  line-height: 1.5;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.2);
  vertical-align: top;
  font-size: 0.75rem;
  color: rgba(var(--v-theme-on-surface-light), 0.5);
}
.historical-metrics-chart__tooltip-value {
  color: rgba(var(--v-theme-on-surface-light), 0.5);
  line-height: 1.5;
  border-bottom: 1px solid rgba(var(--v-theme-on-surface-light), 0.2);
  vertical-align: top;
  font-size: 0.75rem;
  width: 100%;
  padding-left: 16px;
  font-weight: 500;
  color: rgb(35, 148, 223);
}
</style>
