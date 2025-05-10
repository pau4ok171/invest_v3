<script setup lang="ts">
// Utilities
import { computed, ref } from 'vue'

// Types
import type { Chart, Options, SVGElement, SVGPathArray } from 'highcharts'

// Types
interface GaugeProps {
  value?: number | string
  prefix?: string
  suffix?: string
  title?: string
  seriesText?: string
  restText?: string
}

type PositionAlign = 'top' | 'bottom'
type PositionSide = 'left' | 'right'
type PositionKey = `${PositionAlign}-${PositionSide}`

// Props
const props = withDefaults(defineProps<GaugeProps>(), {
  value: 0,
  prefix: '',
  suffix: '',
  title: '',
  seriesText: '',
  restText: '',
})

// Computed
const numericValue = computed(() => Number(props.value) || 0)
const displayText = computed(() => ({
  prefix: props.prefix,
  suffix: props.suffix,
  title: props.title,
  seriesText: props.seriesText,
  restText: props.restText,
}))

// Chart elements ref
const chartElements = ref<SVGElement[]>([])

// Path definitions
const pathTemplates: Record<PositionKey, SVGPathArray> = {
  'top-right': [
    'M',
    0,
    0,
    'L',
    3.951,
    -3.065,
    'C',
    7.902,
    -6.129,
    15.803,
    -12.258,
    19.754,
    -19.818,
    'C',
    23.705,
    -27.377,
    23.705,
    -36.366,
    23.705,
    -40.86,
    'L',
    23.705,
    -45.355,
  ] as unknown as SVGPathArray,
  'top-left': [
    'M',
    0,
    0,
    'L',
    -3.951,
    -3.065,
    'C',
    -7.902,
    -6.129,
    -15.803,
    -12.258,
    -19.754,
    -19.818,
    'C',
    -23.705,
    -27.377,
    -23.705,
    -36.366,
    -23.705,
    -40.86,
    'L',
    -23.705,
    -45.355,
  ] as unknown as SVGPathArray,
  'bottom-right': [
    'M',
    0,
    0,
    'L',
    3.951,
    3.065,
    'C',
    7.902,
    6.129,
    15.803,
    12.258,
    19.754,
    19.818,
    'C',
    23.705,
    27.377,
    23.705,
    36.366,
    23.705,
    40.86,
    'L',
    23.705,
    45.355,
  ] as unknown as SVGPathArray,
  'bottom-left': [
    'M',
    0,
    0,
    'L',
    -3.951,
    3.065,
    'C',
    -7.902,
    6.129,
    -15.803,
    12.258,
    -19.754,
    19.818,
    'C',
    -23.705,
    27.377,
    -23.705,
    36.366,
    -23.705,
    40.86,
    'L',
    -23.705,
    45.355,
  ] as unknown as SVGPathArray,
}

// Helper functions
const getPosition = (angle: number): [PositionAlign, PositionSide] => [
  angle > 90 && angle < 270 ? 'bottom' : 'top',
  angle > 0 && angle < 180 ? 'right' : 'left',
]

const createPath = (
  startX: number,
  startY: number,
  align: PositionAlign,
  side: PositionSide
) => {
  const template = pathTemplates[`${align}-${side}`]
  const path = [...template] as unknown as Array<number | string>

  let counter = 0
  // Apply offset to path coordinates
  for (let i = 0; i < path.length; i++) {
    if (typeof path[i] === 'number') {
      path[i] = (path[i] as number) + (counter % 2 === 0 ? startX : startY)
      counter++
    }
  }

  return path
}

const createAnnotation = (
  chart: Chart,
  angle: number,
  text: string,
  color: string,
  isFilled: boolean
) => {
  const [align, side] = getPosition(angle)
  const startAngle = angle - 90
  const rad = (startAngle * Math.PI) / 180

  const pane = (chart as any).pane[0]
  const [paneWidth, paneHeight, diameter] = pane.center
  const centerX = paneWidth + chart.plotLeft
  const centerY = paneHeight + chart.plotTop
  const radius = diameter / 2

  const start = {
    x: centerX + radius * Math.cos(rad),
    y: centerY + radius * Math.sin(rad),
  }

  const path = createPath(start.x, start.y, align, side)
  const pathPoints = path.filter((p) => typeof p === 'number')
  const endX = pathPoints[pathPoints.length - 2] as number
  const endY = pathPoints[pathPoints.length - 1] as number

  // Create line
  const line = chart.renderer
    .path(path as unknown as SVGPathArray)
    .attr({
      stroke: color,
      'stroke-width': 1,
      fill: 'none',
      zIndex: 5,
    })
    .add()

  // Create label
  const label = chart.renderer
    .text(text, endX, endY + (align === 'top' ? -5 : 15))
    .attr({
      align: 'center',
      zIndex: 5,
    })
    .css({
      color: isFilled
        ? 'rgb(var(--v-theme-on-surface))'
        : 'rgba(var(--v-theme-on-surface), 0.5)',
      fontSize: '0.75rem',
    })
    .add()

  return { line, label }
}

const drawAnnotations = (chart: Chart) => {
  // Clear previous elements
  chartElements.value.forEach((el) => el.destroy())
  chartElements.value = []

  // Calculate angles
  const filledAngle = 360 * (numericValue.value / 100)
  const filledMidAngle = filledAngle / 2
  const emptyMidAngle = filledAngle + (360 - filledAngle) / 2

  // Create annotations
  const filled = createAnnotation(
    chart,
    filledMidAngle,
    displayText.value.seriesText,
    'rgb(var(--v-theme-hc-series1-color))',
    true
  )

  const empty = createAnnotation(
    chart,
    emptyMidAngle,
    displayText.value.restText,
    'rgb(95, 104, 117)',
    false
  )

  chartElements.value.push(filled.line, filled.label, empty.line, empty.label)
}

// Chart options
const chartOptions = computed<Options>(() => ({
  chart: {
    type: 'solidgauge',
    backgroundColor: 'transparent',
    plotBorderWidth: 0,
    plotBackgroundColor: undefined,
    plotBackgroundImage: undefined,
    plotShadow: false,
    height: '200px',
    events: {
      load: function () {
        drawAnnotations(this)
      },
      redraw: function () {
        drawAnnotations(this)
      },
    },
  },
  accessibility: { enabled: false },
  title: { text: undefined },
  credits: { enabled: false },
  legend: { enabled: false },
  tooltip: { enabled: false },
  series: [
    {
      type: 'solidgauge',
      name: 'main',
      data: [numericValue.value],
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
              ${displayText.value.prefix}${numericValue.value}${displayText.value.suffix}
            </div>
            <div class="text-caption">
              ${displayText.value.title}
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
    labels: { enabled: false },
  },
  pane: [
    {
      startAngle: 0,
      endAngle: 360,
      center: ['50%', '50%'],
      size: '60%',
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
}))
</script>

<template>
  <div class="round-gauge-chart">
    <charts
      class="round-gauge-chart__chart"
      constructor-type="chart"
      :options="chartOptions"
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
