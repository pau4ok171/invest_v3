<script setup lang="ts">
// Utilities
import { computed, ref } from 'vue'

// Types
import type {Chart, Options, SVGElement, SVGPathArray} from 'highcharts'

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

  const getPathByPosition = (startX: number, startY: number, align: 'top' | 'bottom', side: 'left' | 'right'): SVGPathArray => {
  // Варианты для разных положений
  const paths = {
    'top-right': [
      'M', startX, startY,
      'L', startX + 3.951, startY - 3.065,
      'C',
      startX + 7.902, startY - 6.129,
      startX + 15.803, startY - 12.258,
      startX + 19.754, startY - 19.818,
      'C',
      startX + 23.705, startY - 27.377,
      startX + 23.705, startY - 36.366,
      startX + 23.705, startY - 40.86,
      'L',
      startX + 23.705, startY - 45.355
    ] as unknown as SVGPathArray,
    'top-left': [
      'M', startX, startY,
      'L', startX - 3.951, startY - 3.065,
      'C',
      startX - 7.902, startY - 6.129,
      startX - 15.803, startY - 12.258,
      startX - 19.754, startY - 19.818,
      'C',
      startX - 23.705, startY - 27.377,
      startX - 23.705, startY - 36.366,
      startX - 23.705, startY - 40.86,
      'L',
      startX - 23.705, startY - 45.355
    ]  as unknown as SVGPathArray,
    'bottom-right': [
      'M', startX, startY,
      'L', startX + 3.951, startY + 3.065,
      'C',
      startX + 7.902, startY + 6.129,
      startX + 15.803, startY + 12.258,
      startX + 19.754, startY + 19.818,
      'C',
      startX + 23.705, startY + 27.377,
      startX + 23.705, startY + 36.366,
      startX + 23.705, startY + 40.86,
      'L',
      startX + 23.705, startY + 45.355
    ]  as unknown as SVGPathArray,
    'bottom-left': [
      'M', startX, startY,
      'L', startX - 3.951, startY + 3.065,
      'C',
      startX - 7.902, startY + 6.129,
      startX - 15.803, startY + 12.258,
      startX - 19.754, startY + 19.818,
      'C',
      startX - 23.705, startY + 27.377,
      startX - 23.705, startY + 36.366,
      startX - 23.705, startY + 40.86,
      'L',
      startX - 23.705, startY + 45.355
    ] as unknown as SVGPathArray,
  };

  const position = `${align}-${side}` as keyof typeof paths;
  return paths[position] || paths['top-right'] // По умолчанию top-right
};

// Обновленная функция createFormattedLine
const createFormattedLine = (
  angle: number,
  text: string,
  color: string,
  isFilled: boolean
) => {
  const startAngle = angle - 90;
  const [align, side] = [
    angle > 90 && angle < 270 ? 'bottom' : 'top',
    angle > 0 && angle < 180 ? 'right' : 'left',
  ];

  const startRad = (startAngle * Math.PI) / 180;
  const start = {
    x: centerX + radius * Math.cos(startRad),
    y: centerY + radius * Math.sin(startRad),
  };

  // Получаем путь
  const path = getPathByPosition(start.x, start.y, align, side);

  // Получаем последнюю точку пути (конец линии)
  const pathPoints = path.filter(p => typeof p === 'number');
  const endX = pathPoints[pathPoints.length - 2] as number;
  const endY = pathPoints[pathPoints.length - 1] as number;

  // Создаем линию
  const line = chart.renderer
    .path(path)
    .attr({
      stroke: color,
      'stroke-width': 1,
      fill: 'none',
      zIndex: 5,
    })
    .add();

  // Создаем подпись с выравниванием по центру
  const label = chart.renderer
    .text(text, 0, 0) // Временная позиция
    .attr({
      align: 'center',
      zIndex: 5,
    })
    .css({
      color: isFilled ? 'rgb(var(--v-theme-on-surface))' : 'rgba(var(--v-theme-on-surface), 0.5)',
      fontSize: '0.75rem',
    })
    .add();

  // Позиционируем текст так, чтобы его центр совпадал с концом линии
  label.translate(
    endX, // Центрируем по горизонтали
    align === 'top' ? endY - 5 : endY + 15 // Вертикальное позиционирование
  );

  chartElements.value.push(line, label);
};

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

<style lang="scss">
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
