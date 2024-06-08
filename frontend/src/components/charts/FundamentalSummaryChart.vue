<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/fundamentalSummaryChart";
import {mapGetters} from "vuex";

export default defineComponent({
  name: "FundamentalSummaryChart",
  data() {
    return {
      chartOpts: chartOpts,
    }
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
  },
  beforeMount() {
    this.chartOpts.series = this.get_chart_series()
    this.chartOpts.chart.events = {load: this.draw_labels}
  },
  methods: {
    get_chart_data() {
      const currency_symbol = this.company.formatting.primaryCurrencySymbol
      const report = this.company.reports[0]
      const scale = report.scale
      const market_cap = this.company.price_data.capitalisation / 1000000000
      const revenue = report.sales
      const earnings = report.income_net
      return {
        market_cap: {
          value: market_cap.toFixed(0),
          unit: scale,
          currency_iso: currency_symbol,
          ratio: market_cap/market_cap*100
        },
        revenue: {
          value: revenue.toFixed(0),
          unit: scale,
          currency_iso: currency_symbol,
          ratio: revenue/market_cap*100
        },
        earnings: {
          value: earnings.toFixed(0),
          unit: scale,
          currency_iso: currency_symbol,
          ratio: earnings/market_cap*100
        },
      }
    },
    get_chart_series(): any {
      const chartData = this.get_chart_data()
      return [
        {
          name: 'Market Cap',
          enableMouseTracking: false,
          data: [{
            color: 'rgb(62, 72, 85)',
            radius: '65%',
            innerRadius: '100%',
            y: chartData.market_cap.ratio,
            label: `${chartData.earnings.currency_iso}${chartData.market_cap.value}${chartData.earnings.unit}`,
            dataLabels: {
              align: 'center',
              verticalAlign: 'middle',
              position: 'center',
              borderWidth: 0,
              format: '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
              style: {
                fontSize: '12px',
                textAnchor: 'middle',
              },
              x: 36,
            },
          }]
        },
        {
          name: 'Revenue',
          enableMouseTracking: false,
          data: [{
            color: 'rgb(35, 148, 223)',
            radius: '85%',
            innerRadius: '100%',
            y: chartData.revenue.ratio,
            label: `${chartData.earnings.currency_iso}${chartData.revenue.value}${chartData.earnings.unit}`,
            dataLabels: {
              allowOverlap: true,
              crop: false,
              overflow: 'allow',
              align: 'center',
              verticalAlign: 'middle',
              position: 'center',
              borderWidth: 0,
              format: '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
              style: {
                fontSize: '12px',
                textAnchor: 'middle',
              },
              x: 130,
              y: -110
            },
          }]
        },
        {
          name: 'Earnings',
          enableMouseTracking: false,
          data: [{
            color: 'rgb(113, 231, 214)',
            radius: '65%',
            innerRadius: '85%',
            y: chartData.earnings.ratio,
            label: `${chartData.earnings.currency_iso}${chartData.earnings.value}${chartData.earnings.unit}`,
            dataLabels: {
              allowOverlap: true,
              crop: false,
              overflow: 'allow',
              align: 'center',
              verticalAlign: 'middle',
              position: 'center',
              borderWidth: 0,
              format: '<tspan class="fundamental-summary-chart__middle-label">{series.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
              style: {
                fontSize: '12px',
                textAnchor: 'middle',
              },
              x: 30,
              y: -160
            },
          }]
        }
      ]
    },
    draw_labels(event: Event) {
      const chart = event.target as any
      const rDiffX = 10
      const rDiffY = 17
      const rOffsetY = -67
      const rData = chart.series[1].data

      const rStartX = rData[0].plotX+rDiffX
      const rStartY = rData[0].plotY+rDiffY
      const rFinishX = rStartX
      const rFinishY = rStartY+rOffsetY

      chart.renderer.path(['M', rStartX, rStartY, 'L', rFinishX, rFinishY]).attr({'stroke-width': 1, stroke: '#71E7D6', fill:'transparent', zIndex: 6}).add()
      chart.renderer.circle().attr({cx:rFinishX, cy:rFinishY, fill: '#71E7D6', r: 2.5}).add()

      const eData = chart.series[2].data
      const eStartX = eData[0].plotX + 15
      const eStartY = eData[0].plotY - 15
      const eMiddleX = eStartX + 18
      const eMiddleY = eStartY - 18

      const eFinishX = eMiddleX + 27
      const eFinishY = eMiddleY

      chart.renderer.path(['M', eStartX, eStartY, 'L', eMiddleX, eMiddleY, 'L', eFinishX, eFinishY]).attr({'stroke-width': 1, stroke: '#2394DF', fill:'transparent', zIndex: 6}).add()
      chart.renderer.circle().attr({cx:eFinishX, cy:eFinishY, fill: '#2394DF', r: 2.5}).add()
    }
  },
})
</script>

<template>
<div class="fundamental-summary-chart">
  <charts
    ref="fundamentalSummaryChart"
    :constructorType="'chart'"
    :options="chartOpts"
  />
</div>
</template>

<style>
.fundamental-summary-chart svg {
  width: auto;
  height: auto;
}
.fundamental-summary-chart__middle-label {
  line-height: 1.7;
  fill: rgba(255, 255, 255, .7);
}
</style>