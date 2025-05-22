<script setup lang="ts">
// Components
import FetchingData from '@/components/charts/FetchingData.vue'

// Composables
import { useCompanyDetailStore } from '@/store/companyDetail'

// Utilities
import { computed, ref, watch } from 'vue'

// Types
import type { PropType } from 'vue'
import type { MultiplierTab } from '@/components/company_detail/content_list/valuation/CompanyDetailValuation.vue'
import type {
  Chart,
  Options,
  AxisLabelsFormatterContextObject,
  SVGElement,
  SeriesBarOptions,
  SVGPathArray,
} from 'highcharts'
import { useI18n } from 'vue-i18n'

type SeriesKey = 'pe' | 'pb' | 'ps'

const props = defineProps({
  tabs: {
    required: true,
    type: Array as PropType<MultiplierTab[]>,
  },
  activeTab: {
    required: true,
    type: Object as PropType<MultiplierTab>,
  },
})

const store = useCompanyDetailStore()
const chartElements = ref<SVGElement[]>([])
const chartRef = ref<{ chart: Chart }>()
const { t, locale } = useI18n()

// Mock data
const peersData = [
  {
    name: 'ROSBANK',
    selected: false,
    pe: 9.8,
    pb: 0.9,
    ps: 3,
    earningsGrowth: 'n/a',
    salesGrowth: 'n/a',
  },
  {
    name: 'Credit Bank of Moscow',
    selected: false,
    pe: 6.3,
    pb: 0.6,
    ps: 2.6,
    earningsGrowth: '26.9%',
    salesGrowth: '28.3%',
  },
  {
    name: 'Sberbank of Russia',
    selected: true,
    pe: 9.8,
    pb: 0.5,
    ps: 1.2,
    earningsGrowth: '8.2%',
    salesGrowth: '12.5%',
  },
  {
    name: 'Gazprom',
    selected: false,
    pe: 2.2,
    pb: 0.3,
    ps: 0.5,
    earningsGrowth: 'n/a',
    salesGrowth: 'n/a',
  },
  {
    name: 'VTB Bank',
    selected: false,
    pe: 9.8,
    pb: 0.1,
    ps: 0.3,
    earningsGrowth: '-2.1%',
    salesGrowth: '10.2%',
  },
]

const averagesData = {
  pe: {
    averageValue: 4.8,
    maxValue: 9.8,
    max: 10,
  },
  ps: {
    averageValue: 1.6,
    maxValue: 3,
    max: 3.2,
  },
  pb: {
    averageValue: 0.5,
    maxValue: 0.9,
    max: 1.2,
  },
}

function getDataLabelFormat(pointIndex: number, isSelected: boolean) {
  const selectedClass = isSelected
    ? 'multiple-vs-peers-chart__data-label-name--selected text-high-emphasis'
    : 'text-medium-emphasis'
  const value = peersData[pointIndex][activeTabData.value?.id as SeriesKey]
  const name = peersData[pointIndex].name
  return `
    <div class="d-flex flex-column text-caption on-surface-light" style="width: 150px">
      <div class="font-weight-medium">${value}x</div>
      <div class="${selectedClass}">${name}</div>
    </div>
  `
}

const activeTabData = computed(() => {
  if (!props.activeTab) return null

  return {
    ...props.activeTab,
    ...averagesData[props.activeTab.id as SeriesKey],
  }
})

const chartOptions = computed<Options>(
  () =>
    ({
      chart: {
        type: 'bar',
        height: 362,
        style: {
          fontFamily: 'inherit',
        },
        events: {
          load: drawChartElements,
          redraw: drawChartElements,
        },
        backgroundColor: 'transparent',
        spacingTop: 45,
        spacingRight: 45,
        plotBackgroundColor: 'url(#Chart_Fail_Pattern)',
        plotBorderWidth: 0,
      },
      plotOptions: {
        bar: {
          enableMouseTracking: false,
          groupPadding: 0.1,
          borderWidth: 0,
          borderRadius: 0,
          pointWidth: 50,
        },
      },
      series: ['pe', 'ps', 'pb'].map(
        (key) =>
          ({
            name: key.toUpperCase(),
            type: 'bar',
            id: key,
            visible: activeTabData.value?.id === key,
            color: 'url(#BarGradient)',
            dataLabels: {
              useHTML: true,
              enabled: true,
              inside: true,
              align: 'left',
              x: 10,
              formatter: function () {
                return getDataLabelFormat(this.index, this.index === 2)
              },
            },
            data: peersData.map((item) => ({
              y: item[key as SeriesKey],
              color: item.selected
                ? 'rgb(var(--v-theme-surface-light))'
                : undefined,
            })),
          }) as SeriesBarOptions
      ),
      // Горизонтальная ось
      yAxis: getYAxisOptions(),
      xAxis: getXAxisOptions(),
      title: {
        text: '',
      },
      credits: {
        enabled: false,
      },
      legend: {
        enabled: false,
      },
    }) satisfies Options
)

function getYAxisOptions() {
  const tickInterval = Number(((activeTabData.value?.max || 0) / 2).toFixed(2))
  return {
    gridLineWidth: 0,
    lineWidth: 1,
    lineColor: 'rgba(var(--v-theme-on-surface-light), .2)',
    tickInterval: tickInterval, // Расстояние между чертами
    tickColor: 'rgba(var(--v-theme-on-surface-light), .2)',
    tickWidth: 1,
    title: { text: undefined },
    labels: {
      style: {
        fontSize: '.75rem',
        color: 'rgb(var(--v-theme-on-surface-light))',
      },
      formatter: function (this: AxisLabelsFormatterContextObject) {
        return this.isFirst
          ? activeTabData.value?.shortName || ''
          : String(this.value)
      },
    },
    max: activeTabData.value?.max,
    plotLines: [
      {
        value: activeTabData.value?.averageValue || 0,
        color: '#eeb219',
        zIndex: 2,
        width: 3,
      },
    ],
    plotBands: [
      {
        from: 0,
        to: activeTabData.value?.averageValue || 0,
        color: '#2dc97e',
      },
    ],
  }
}

function getXAxisOptions() {
  return {
    opposite: true,
    lineWidth: 0,
    tickWidth: 0,
    labels: {
      style: {
        fontSize: '.75rem',
        color: 'rgb(var(--v-theme-on-surface-light))',
      },
      formatter: function (this: AxisLabelsFormatterContextObject) {
        const index = Number(this.value)
        return index === 1
          ? peersData[index].salesGrowth
          : peersData[index].earningsGrowth
      },
    },
  }
}

function drawChartElements(this: Chart) {
  chartElements.value.forEach((el) => el?.destroy())
  chartElements.value = []

  drawVAxisElements(this)
  drawMiddleElements(this)
}

function drawVAxisElements(chart: Chart) {
  const plotBox = {
    x: chart.plotLeft,
    y: chart.plotTop,
    height: chart.plotHeight,
    width: chart.plotWidth,
  }
  const offsetX = 8
  const boxW = 60

  chartElements.value.push(
    chart.renderer
      .rect(
        plotBox.x + plotBox.width + offsetX,
        plotBox.y,
        boxW,
        plotBox.height
      )
      .attr({
        fill: 'rgb(var(--v-theme-surface-bright))',
        rx: 4,
      })
      .add()
  )

  // X-axis label
  const textOffsetX = 8
  const textOffsetY = 18
  const textValueType = t(
    `companyDetail.valuation.peVsPeers.${activeTabData.value?.id === 'ps' ? 'salesGrowth' : 'earningsGrowth'}`
  ).split(' ')
  const textFormat = `
    <div class="d-flex flex-column text-caption text-medium-emphasis mt-n4">
      <div class='multiple-vs-peers-chart__v-axis-name'>${textValueType[0]}</div>
      <div class='multiple-vs-peers-chart__v-axis-name'>${textValueType[1]}</div>
    </div>
  `

  chartElements.value.push(
    chart.renderer
      .text(
        textFormat,
        plotBox.x + plotBox.width + textOffsetX,
        plotBox.y - textOffsetY,
        true
      )
      .add()
  )
}

function drawMiddleElements(chart: Chart) {
  if (!activeTabData.value) return

  const plotBox = {
    x: chart.plotLeft,
    y: chart.plotTop,
    height: chart.plotHeight,
    width: chart.plotWidth,
  }

  const { averageValue, max } = activeTabData.value
  const pointWidth = plotBox.width / max
  const averagePosX = pointWidth * averageValue

  const labelGroup = chart.renderer
    .g()
    .attr({
      class: 'average-label-group',
      zIndex: 5,
    })
    .add()

  // Middle polygon
  const polygonH = 19
  const labelPosY = plotBox.y - polygonH

  chart.renderer
    .path([
      'M',
      0,
      0,
      11,
      0,
      11,
      19,
      9,
      19,
      0,
      0,
      'Z',
    ] as unknown as SVGPathArray)
    .attr({
      transform: `translate(${averagePosX + 1}, ${labelPosY})`,
      fill: '#eeb219',
    })
    .add(labelGroup)

  // Middle label
  const labelW = 140
  const labelH = 25
  const labelX = averagePosX + 1 - labelW + 11

  chart.renderer
    .rect(labelX, plotBox.y - labelH - polygonH + 1, labelW, labelH)
    .attr({
      fill: '#eeb219',
      rx: 2,
    })
    .add(labelGroup)

  // Middle text
  const textX = averagePosX - labelW / 2 - 40
  const textY = plotBox.y - polygonH - labelH / 2 + 5

  chart.renderer
    .text(
      `<tspan class='text-caption'>${t('companyDetail.valuation.peVsPeers.peerAvg')} ${averageValue}x</tspan>`,
      textX,
      textY
    )
    .add(labelGroup)

  chartElements.value.push(labelGroup)
}

watch(locale, () => {
  chartRef.value?.chart.redraw()
})
</script>

<template>
  <div class="detail-multiplier-vs-peers-chart">
    <fetching-data v-if="store.fetchingCompany" />
    <charts
      v-else
      ref="chartRef"
      :options="chartOptions"
      constructorType="chart"
    />
  </div>
</template>

<style lang="scss">
.detail-multiplier-vs-peers-chart svg {
  height: auto;
  width: auto;
}
.multiple-vs-peers-chart__v-axis-name {
  border-bottom: 1px dotted rgb(35, 148, 223);
}
.multiple-vs-peers-chart__middle-label-name {
  fill: rgb(var(--v-theme-surface-light));
  font-size: 0.75rem;
}
.multiple-vs-peers-chart__data-label-name--selected {
  background: linear-gradient(
    270deg,
    rgb(35, 148, 223) 0%,
    rgb(2, 189, 8) 100%
  );
  padding: 0 6px;
  border-radius: 4px;
  margin-top: 2px;
  width: fit-content;
}
</style>
