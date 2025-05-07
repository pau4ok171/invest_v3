<script setup lang="ts">
// Utilities
import { computed, ref } from 'vue'

// Types
import type { Chart, Options, SVGElement } from 'highcharts'

const props = defineProps({
  value: [Number, String],
  prefix: String,
  suffix: String,
  title: String,
  seriesText: String,
  restText: String,
})

const value = computed<number>(() => Number(props.value as string) || 0)
const prefix = computed<string>(() => props.prefix || '')
const suffix = computed<string>(() => props.suffix || '')
const title = computed<string>(() => props.title || '')
const seriesText = computed<string>(() => props.seriesText || '')
const restText = computed<string>(() => props.restText || '')

const chartElements = ref<SVGElement[]>([])

const drawAnnotations = (chart: Chart) => {
  // Удаляем предыдущие элементы
  chartElements.value.forEach((el) => el.destroy())
  chartElements.value = []

  const pane = (chart as any).pane[0]
  const [paneWidth, paneHeight, diameter] = pane.center
  const centerX = paneWidth + chart.plotLeft
  const centerY = paneHeight + chart.plotTop
  const radius = diameter / 2

  // Угол заполненной зоны (в градусах)
  const filledAngle = 360 * (value.value / 100)

  // Угол для середины заполненной зоны
  const filledMidAngle = filledAngle / 2
  // Угол для середины пустой зоны
  const emptyMidAngle = filledAngle + (360 - filledAngle) / 2

  // Функция для создания линии в точном формате
  const createFormattedLine = (
    angle: number,
    text: string,
    color: string,
    isFilled: boolean
  ) => {
    // Начальная точка на окружности (смещение -90° чтобы 0° был вверху)
    const startAngle = angle - 90
    const [align, side] = [
      angle > 90 && angle < 270 ? 'bottom' : ('top' as 'top' | 'bottom'),
      angle > 0 && angle < 180 ? 'right' : ('left' as 'right' | 'left'),
    ]
    console.log('start ', align, side)
    const startRad = (startAngle * Math.PI) / 180
    const start = {
      x: centerX + radius * Math.cos(startRad),
      y: centerY + radius * Math.sin(startRad),
    }
    const end = {
      x: centerX + radius * 1.4 * Math.cos(startRad),
      y: centerY + radius * 1.4 * Math.sin(startRad),
    }

    const path = ['M', start.x, start.y, 'L', end.x, end.y]

    // Создаем линию
    const line = chart.renderer
      .path(path)
      .attr({
        stroke: color,
        'stroke-width': 1,
        fill: 'none',
        zIndex: 5,
      })
      .add()

    // Создаем подпись
    const label = chart.renderer
      .text(
        text,
        side === 'left' ? end.x - 10 : end.x + 10,
        align === 'top' ? end.y - 10 : end.y + 15
      )
      .attr({
        align: 'center',
        zIndex: 5,
      })
      .css({
        color: isFilled ? '#fff' : 'rgba(255,255,255,0.5)',
        fontSize: '12px',
      })
      .add()

    chartElements.value.push(line, label)
  }

  // Создаем линии и подписи в точном соответствии с вашим примером
  createFormattedLine(
    filledMidAngle,
    seriesText.value,
    'rgb(var(--v-theme-hc-series1-color))',
    true
  )
  createFormattedLine(emptyMidAngle, restText.value, 'rgb(95, 104, 117)', false)
}

const options = computed<Options>(() => {
  return {
    chart: {
      type: 'solidgauge',
      backgroundColor: 'transparent',
      plotBorderWidth: 0,
      plotBackgroundColor: undefined,
      plotBackgroundImage: undefined,
      plotShadow: false,
      height: '45%',
      events: {
        load: function () {
          drawAnnotations(this)
        },
        redraw: function () {
          drawAnnotations(this)
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
    series: [
      {
        type: 'solidgauge',
        name: 'main',
        data: [value.value],
        color: 'rgb(var(--v-theme-hc-series1-color))',
        dataLabels: {
          borderWidth: 0,
          verticalAlign: 'center',
          align: 'center',
          useHTML: true,
          formatter: function () {
            return `
            <div class="d-flex flex-column on-surface font-weight-medium">
              <div class="text-h5">
                ${prefix.value}${value.value}${suffix.value}
              </div>
              <div class="text-caption">
                ${title.value}
              </div>
            </div>
          `
          },
        },
      },
    ],
    yAxis: {
      min: 0,
      max: 100,
      lineWidth: 0,
      minorTickWidth: 0,
      tickWidth: 0,
      labels: {
        enabled: false,
      },
    },
    pane: [
      {
        startAngle: 0,
        endAngle: 360,
        center: ['50%', '55%'],
        background: [
          {
            backgroundColor: 'rgb(95, 104, 117)',
            borderWidth: 0,
            innerRadius: '60%',
            outerRadius: '100%',
          },
        ],
      },
    ],
  } satisfies Options
})
</script>

<template>
  <div class="round-gauge-chart">
    <charts
      class="round-gauge-chart__chart"
      constructorType="chart"
      :options="options"
    />
  </div>
</template>

<style scoped lang="scss">
.round-gauge-chart {
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;

  &__chart {
    width: 100%;
    height: 100%;
  }
}
</style>
