<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/DCFChart";
import FailPattern from "@/components/patterns/FailPattern.vue";
import BarGradient from "@/components/lineair_gradient/BarGradient.vue";
import DataNotAvailable from "@/components/charts/DataNotAvailable.vue";
import {mapGetters} from "vuex";

interface DiffMode {
  type: string,
  class: string,
  color: string,
}

export default defineComponent({
  name: "DCFChart",
  components: {
    DataNotAvailable,
    BarGradient,
    FailPattern
  },
  data() {
    return {
      chartOpts: chartOpts,
      dataIsAvailable: true,
      diff: 0,
      highest: 0,
      diffMode: {
        undervalued: {
          type: 'Undervalued',
          class: 'dcf-chart__data-label-diff--undervalued',
          color: '#2dc97e',
        },
        overvalued: {
          type: 'Overvalued',
          class: 'dcf-chart__data-label-diff--overvalued',
          color: '#e64141',
        },
        about_right: {
          type: 'About Right',
          class: 'dcf-chart__data-label-diff--about-right',
          color: '#eeb219',
        },
      },
      currentDiffMode: {} as DiffMode,
    }
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
  },
  beforeMount() {
    this.get_series()
    this.chartOpts.chart.events = {load: this.drawMultipleBgC}
  },
  methods: {
    get_series() {
      const currency_symbol = this.company.formatting.primaryCurrencySymbol
      if (!currency_symbol) {
        this.dataIsAvailable = false
        return null
      } else {
        this.dataIsAvailable = true
      }
      const dataLabelFormat = `` +
        `<tspan class='dcf-chart__data-label-name'>{series.name}</tspan>` +
        `<br>` +
        `<tspan class='dcf-chart__data-label-value'>{series.yData}${currency_symbol}</tspan>`

      const currentValue = this.company.price_data?.last_price
      if (!currentValue) {
        this.dataIsAvailable = false
        return null
      } else {
        this.dataIsAvailable = true
      }
      const fairValue = Number((currentValue * 1.2).toFixed(2))
      this.diff = +((fairValue - currentValue) / currentValue * 100).toFixed(2)
      this.highest = Math.max(currentValue, fairValue)

      if (this.diff >= 20) {
        this.currentDiffMode = this.diffMode['undervalued']
      } else if (this.diff <= -20) {
        this.currentDiffMode = this.diffMode['overvalued']
      } else {
        this.currentDiffMode = this.diffMode['about_right']
      }

      this.chartOpts.yAxis = {
        visible: false,
        max: this.highest * 1.5 // Максимальное значение по ширине [ЗАВИСИТ ОТ МАКСИМАЛЬНОГО ЗНАЧЕНИЯ СТОИМОСТИ]
      }

      this.chartOpts.series = [{
        name: 'Current Price',
        data: [currentValue],
        enableMouseTracking: false,
        dataLabels: {
          align: 'right',
          enabled: true,
          format: dataLabelFormat,
        }
      }, {
        name: 'Fair Price',
        data: [fairValue],
        enableMouseTracking: false,
        dataLabels: {
          align: 'right',
          enabled: true,
          format: dataLabelFormat
        }
      }] as any
    },
    drawMultipleBgC(event: Event) {
      const chart = event.target as any
      // BACKGROUND
      const plotBox = chart.plotBox
      const x1 = plotBox.x
      const y1 = plotBox.y
      const w = chart.series[1].data[0].tooltipPos[2]
      const h = plotBox.height
      chart.renderer.rect(x1, y1, w*1.2, h)
        .attr({
          fill: '#eeb219'
        })
        .add()

      chart.renderer.rect(x1, y1, w*0.8, h)
        .attr({
          fill: '#2dc97e'
        })
        .add()

      // LINES
      const OUTLINE_OFFSET = 24
      const point2XOffset = chart.series[0].pointXOffset
      const client2X = chart.series[0].points[0].clientX

      const line1X = chart.series[1].data[0].tooltipPos[2] + plotBox.x -1
      const line1Y = plotBox.y + 0.5 - OUTLINE_OFFSET
      const line1H = plotBox.height - 1 + OUTLINE_OFFSET

      const line2X = chart.series[0].data[0].tooltipPos[2] + plotBox.x - 1
      const line2Y = plotBox.y + 0.5 - OUTLINE_OFFSET
      const line2H = plotBox.height - 1 + OUTLINE_OFFSET - client2X - point2XOffset

      const line3X = line2X < line1X ? line2X + 0.5 : line1X + 0.5
      const line3Y = plotBox.y + 0.5 - OUTLINE_OFFSET
      const line3W = Math.abs(line2X - line1X) - 0.5

      const dataDiffLabelFormat = `` +
        `<tspan class=\"dcf-chart__data-label-diff-value\">${this.diff}%</tspan>` +
        `<br>` +
        `<tspan class=\"dcf-chart__data-label-diff-type\">${this.currentDiffMode.type}</tspan>`

      // FAIR PRICE LINE
      chart.renderer.rect(line1X, line1Y, .5, line1H)
        .attr({
          fill: '#fff',
          opacity: .7,
          zIndex: 10,
        })
        .add()

      // CURRENT PRICE LINE
      chart.renderer.rect(line2X, line2Y, .5, line2H)
        .attr({
          fill: '#fff',
          opacity: .7,
        })
        .add()

      // CONNECTING LINE
      chart.renderer.rect(line3X, line3Y, line3W, 2)
        .attr({
          fill: this.currentDiffMode.color, // [ЗАВИСИТ ОТ ОТНОШЕНИЯ СПРАВЕДЛИВОЙ ОЦЕНКИ: ПЕРЕОЦЕНЕН, НЕДООЦЕНЕН]
        })
        .add()

      // CONNECTING LINE LABEL
      chart.renderer.text(
        dataDiffLabelFormat,
        line3X,
        line3Y-22
      )
        .attr({
            class: this.currentDiffMode.class
        })
        .add()

      // TEXT
      const textY = plotBox.y + plotBox.height
      const textYOffset = 12
      const textXOffset = 12
      chart.renderer.text(
        "<tspan class='dcf-chart__label-level-name'>20% Undervalued</tspan>",
        w * 0.8 + textXOffset,
        textY + textYOffset
      )
        .attr({
            rotation: -35,
            class: 'dcf-chart__data-label-diff--undervalued'
        })
        .add()

      chart.renderer.text(
        "<tspan class='dcf-chart__label-level-name'>About Right</tspan>",
        w + textXOffset,
        textY + textYOffset
      )
        .attr({
          rotation: -35,
          class: 'dcf-chart__data-label-diff--about-right'
        })
        .add()

      chart.renderer.text(
        "<tspan class='dcf-chart__label-level-name'>20% Overvalued</tspan>",
        w * 1.2 + textXOffset,
        textY + textYOffset
      )
        .attr({
          rotation: -35,
          class: 'dcf-chart__data-label-diff--overvalued'
        })
        .add()
    },
  },
})
</script>

<template>
  <div class="dcf-chart">
    <DataNotAvailable v-if="!dataIsAvailable" chart-name="DCF Chart"/>
    <charts
      v-else
      :constructorType="'chart'"
      :options="chartOpts"
    />
    <FailPattern/>
    <BarGradient/>
  </div>
</template>

<style>
  .dcf-chart svg {
    height: auto;
    width: auto;
  }
  .dcf-chart .highcharts-visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    white-space: nowrap;
    clip: rect(1px, 1px, 1px, 1px);
    margin-top: -3px;
    opacity: 0.01;
  }
  .dcf-chart .highcharts-container {
    position: relative;
    overflow: hidden;
    width: 100%;
    height: 100%;
    text-align: left;
    line-height: normal;
    z-index: 0;
    font-size: 1rem;
    user-select: none;
    touch-action: manipulation;
    outline: none;
  }
  .dcf-chart .highcharts-plot-border, .dcf-chart .highcharts-plot-background {
    fill: none;
  }
  .dcf-chart g.highcharts-series, .dcf-chart .highcharts-point, .dcf-chart .highcharts-markers, .dcf-chart .highcharts-data-labels {
    transition: opacity 250ms;
  }
  .dcf-chart .highcharts-data-label-box {
    fill: none;
    stroke-width: 0;
  }
  .dcf-chart {
    height: 380px;
    width: 100%;
  }
  .dcf-chart__container {
    font-family: inherit;
  }
  .dcf-chart .highcharts-background {
    fill: #1b222d;
  }
  .dcf-chart .highcharts-plot-background {
    fill: url(#Chart_Fail_Pattern);
  }
  .dcf-chart .highcharts-color-0 {
    outline: none;
    stroke-width: 0;
    fill: #1b222d;
  }
  .dcf-chart .highcharts-color-1 {
    outline: none;
    stroke-width: 0;
    fill: url(#BarGradient);
  }
  .dcf-chart__data-label-value {
    fill: #fff;
    font-size: 2.4rem;
    line-height: 1.25;
    font-weight: 500;
  }
  .dcf-chart__data-label-name {
    fill: #fff;
    font-size: 1.6rem;
    line-height: 1.5;
    font-weight: 500;
  }
  .dcf-chart__data-label-diff--undervalued {
    fill: #2dc97e;
  }
  .dcf-chart__data-label-diff--about-right {
    fill: #eeb219;
  }
  .dcf-chart__data-label-diff--overvalued {
    fill: #e64141;
  }
  .dcf-chart__data-label-diff-value {
    line-height: 1.25;
    font-weight: 500;
    font-size: 2.4rem;
  }
  .dcf-chart__data-label-diff-type {
    line-height: 1.5;
    font-weight: 500;
    font-size: 1.4rem;
  }
  .dcf-chart__label-level-name {
    line-height: 1.5;
    font-weight: 500;
    font-size: 1.4rem;
    text-anchor: end;
  }
</style>