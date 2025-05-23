<script setup lang="ts">
// Utilities
import { computed } from 'vue'

// Types
import type { PropType } from 'vue'
import type { Options } from 'highcharts'

// Constants
const CHART_HEIGHT = 280

// Interfaces
interface DataItem {
  name: string
  value: number
}

const props = defineProps({
  data: {
    type: Object as PropType<[DataItem, DataItem]>,
    required: true,
  },
  title: String,
  max: {
    type: [String, Number],
    default: '100',
  },
})

// Helper functions
const calculateGaugeValues = (values: [DataItem, DataItem]) => {
  // Определяем максимальное и минимальное значение на основе входных данных
  const maxValue = Math.max(values[0].value, values[1].value)
  const minValue = Math.min(values[0].value, values[1].value)

  // Устанавливаем границы шкалы
  const maxScaleValue = Math.round(maxValue / 5) * 5
  const minScaleValue = Math.min(Math.round(minValue / 5) * 5, -10)

  // Рассчитываем шаг
  const rawStep = (maxScaleValue - minScaleValue) / 5
  const step = Math.round(rawStep / 5) * 5

  // Генерация меток для делений
  const tickLabels = [-1, 0, 1, 2, 3, 4, 5].map((n) => n * step + '%')

  // Позиции делений (фиксированные значения)
  const tickPositions = [-135, -90, -45, 0, 45, 90, 135]

  // Ограничение значений
  const clampedValues = values.map((item) =>
    Math.min(Math.max(item.value, minScaleValue), maxScaleValue)
  )

  // Расчет позиций стрелок
  const seriesPositions = clampedValues.map((value) => {
    return (
      -135 + ((value - minScaleValue) / (maxScaleValue - minScaleValue)) * 270
    )
  })

  return {
    tickPositions,
    tickLabels,
    seriesPositions,
    maxScaleValue,
    minScaleValue,
  }
}

const options = computed<Options>(() => {
  const { tickLabels, tickPositions, seriesPositions } = calculateGaugeValues(
    props.data
  )
  return {
    chart: {
      type: 'gauge',
      height: CHART_HEIGHT,
      backgroundColor: 'transparent',
      plotBorderWidth: 0,
      plotBackgroundColor: undefined,
      plotBackgroundImage: undefined,
      plotShadow: false,
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
    pane: [
      {
        size: '95%',
        center: ['50%', '70%'],
        startAngle: -135,
        endAngle: 135,
        background: [
          {
            outerRadius: '100%',
            innerRadius: '90%',
            shape: 'arc',
            backgroundColor: 'transparent',
            borderWidth: 0,
          },
        ],
      },
    ],
    yAxis: {
      min: -135,
      max: 135,
      lineWidth: 0,
      minorTickWidth: 0,
      tickPixelInterval: 90,
      tickWidth: 2,
      tickPosition: 'inside',
      tickPositions: tickPositions,
      tickLength: 12,
      tickColor: 'rgba(21, 27, 36, 0.5)',
      labels: {
        align: 'center',
        distance: '120%',
        formatter: function () {
          const index = tickPositions.indexOf(this.value as number)
          return index >= 0
            ? !this.isFirst && !this.isLast
              ? `${tickLabels[index]}`
              : ''
            : ''
        },
        style: {
          color: 'rgb(var(--v-theme-on-surface))',
          fontSize: '0.75rem',
          fontWeight: '500',
        },
      },
      plotBands: [
        {
          from: -135,
          to: -90,
          color: '#803137',
          thickness: 12,
        },
        {
          from: -90,
          to: 90,
          color: {
            linearGradient: { x1: 0, y1: 0, x2: 1, y2: 0 },
            stops: [
              [0, '#e64440'],
              [0.5, '#eeb219'],
              [1, '#2dc97e'],
            ],
          },
          thickness: 12,
        },
        {
          from: 90,
          to: 135,
          color: '#247555',
          thickness: 12,
        },
      ],
    },
    series: [
      {
        type: 'solidgauge',
        name: `${props.data[0].name}Line`,
        data: [
          {
            color: '#1c2d3f',
            radius: '85%',
            innerRadius: '75%',
            y: seriesPositions[0],
          },
        ],
      },
      {
        type: 'solidgauge',
        name: `${props.data[0].name}Line`,
        data: [
          {
            color: '#23363d',
            radius: '70%',
            innerRadius: '60%',
            y: seriesPositions[1],
          },
        ],
      },
      {
        type: 'gauge',
        name: props.data[0].name,
        data: [seriesPositions[0]],
        dial: {
          radius: '85%',
          backgroundColor: '#2394df',
          baseWidth: 8,
          topWidth: 4,
          baseLength: '10%',
          rearLength: '0%',
        },
        pivot: {
          radius: 0,
        },
      },
      {
        type: 'gauge',
        name: props.data[1].name,
        data: [seriesPositions[1]],
        dial: {
          radius: '70%',
          backgroundColor: '#71e7d6',
          baseWidth: 8,
          topWidth: 4,
          baseLength: '10%',
          rearLength: '0%',
        },
        pivot: {
          radius: 0,
        },
      },
      {
        type: 'gauge',
        name: 'pivot',
        data: [0],
        dial: {
          baseWidth: 0,
          topWidth: 0,
        },
        pivot: {
          backgroundColor: '#494e57',
          radius: 12,
        },
        zIndex: 1,
      },
    ],
    plotOptions: {
      series: {
        dataLabels: {
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
      },
    },
  } satisfies Options
})
</script>

<template>
  <div class="gauge-chart">
    <charts
      class="gauge-chart__chart"
      constructor-type="chart"
      :options="options"
    />
    <v-card width="144" class="gauge-chart__caption" flat>
      <v-row no-gutters class="justify-center align-center text-center">
        <v-col cols="12" class="text-subtitle-1 text-center">
          {{ title || 'Gauge' }}
        </v-col>
      </v-row>
      <v-row
        no-gutters
        class="justify-center align-center text-center text-subtitle-1 text-hc-series1-color"
      >
        <v-col>
          {{ props.data[0].name }}
        </v-col>
        <v-col class="text-end"> {{ props.data[0].value }}% </v-col>
      </v-row>
      <v-divider />
      <v-row
        no-gutters
        class="justify-center align-center text-center text-caption text-hc-series2-color"
      >
        <v-col>
          {{ props.data[1].name }}
        </v-col>
        <v-col class="text-end"> {{ props.data[1].value }}% </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<style scoped lang="scss">
.gauge-chart {
  display: flex;
  flex-direction: column;
  align-items: center;

  &__caption {
    background-color: transparent;
    margin-top: -24px;
  }
}
</style>
