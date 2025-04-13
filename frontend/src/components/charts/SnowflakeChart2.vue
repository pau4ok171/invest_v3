<script setup lang="ts">
// Utilities
import { reactive } from 'vue'

// Types
import type { PropType } from 'vue'
import type { Options } from 'highcharts'

// Colors
const seriesColor5 = '#6bc51a'
const seriesBorderColor5 = '#79ee04'

const seriesColor4 = '#b2c319'
const seriesBorderColor4 = '#def30b'

const seriesColor3 = '#c7a028'
const seriesBorderColor3 = '#ffc413'

const seriesColor2 = '#c75633'
const seriesBorderColor2 = '#ff5a23'

const seriesColor1 = '#c74a35'
const seriesBorderColor1 = '#fb4a27'

const props = defineProps({
  data: {
    type: Object as PropType<number[]>,
    required: true,
  },
  size: Number,
  String,
})

const options = reactive<Options>({
  chart: {
    polar: true,
    type: 'column',
    backgroundColor: 'transparent',
  },
  accessibility: {
    enabled: false,
  },
  title: {
    text: undefined,
  },
  legend: {
    enabled: false,
  },
  credits: {
    enabled: false,
  },
  xAxis: {
    categories: ['Value', 'Future', 'Past', 'Health', 'Dividend'],
    tickmarkPlacement: 'on',
    gridLineColor: 'rgb(var(--v-theme-hc-snowflake-bg-light))',
    gridLineWidth: 3,
    lineWidth: 0,
    labels: {
      style: {
        color: 'rgb(var(--v-theme-on-surface-light))',
      },
    },
  },
  yAxis: {
    min: 0,
    max: 6,
    tickInterval: 1,
    labels: {
      enabled: false,
    },
    gridLineWidth: 0,
  },
  series: [
    {
      name: 'Tests',
      type: 'areaspline',
      data: [5, 4, 3, 6, 2],
      pointPlacement: 'on',
      fillColor: seriesColor5,
      lineColor: seriesBorderColor5,
      lineWidth: 2,
      opacity: 0.75,
      zIndex: 1,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
    {
      name: 'Hover',
      animation: {
        duration: 300,
      },
      data: [6, 6, 6, 6, 6], // Максимальное значение
      type: 'column',
      pointPlacement: 'on',
      color: 'transparent',
      enableMouseTracking: true,
      states: {
        hover: {
          color: 'rgba(255, 255, 255, 0.4)', // Подсветка сектора
          halo: {
            enabled: false,
          },
          lineWidth: 0,
        },
      },
      zIndex: 2,
    },
    // ---- Фоновые кольца (чередующиеся) ----
    {
      name: 'Background 1',
      type: 'areasplinerange',
      pointPlacement: 'on',
      data: [
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 1],
      ],
      fillColor: 'rgb(var(--v-theme-hc-snowflake-bg-light))',
      fillOpacity: 1,
      lineWidth: 0,
      zIndex: -3,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
    {
      name: 'Background 3',
      type: 'areasplinerange',
      pointPlacement: 'on',
      data: [
        [2, 3],
        [2, 3],
        [2, 3],
        [2, 3],
        [2, 3],
      ],
      fillColor: 'rgb(var(--v-theme-hc-snowflake-bg-light))',
      fillOpacity: 1,
      lineWidth: 0,
      zIndex: 0,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
    {
      name: 'Background 5',
      type: 'areasplinerange',
      pointPlacement: 'on',
      data: [
        [4, 5],
        [4, 5],
        [4, 5],
        [4, 5],
        [4, 5],
      ],
      fillColor: 'rgb(var(--v-theme-hc-snowflake-bg-light))',
      fillOpacity: 1,
      lineWidth: 0,
      zIndex: 0,
      marker: {
        enabled: false,
        states: {
          hover: {
            enabled: false,
          },
        },
      },
    },
  ],
  tooltip: {
    shared: true,
    headerFormat: '<b>{point.key}</b><br>',
    pointFormat: '<b>{point.y}</b> из 6',
  },
  plotOptions: {
    column: {
      // Убираем промежутки между столбцами
      grouping: false,
      pointPadding: 0,
      groupPadding: 0,
      borderWidth: 0,
    },
  },
  pane: [
    {
      background: [
        {
          backgroundColor: 'rgb(var(--v-theme-hc-snowflake-bg-dark))',
          borderWidth: 0,
          outerRadius: '100%',
        }
      ]
    },
  ],
})
</script>

<template>
  <div class="snowflake-chart">
    <charts :constructorType="'chart'" :options="options" />
  </div>
</template>

