<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/keyValuationMetricChart";
import type {PropType} from "vue";
import type {Tab} from "@/components/company_detail/content_list/valuation/KeyValuationMetric.vue";
import {mapGetters} from "vuex";

interface ChartData {
  name: string,
  value: number,
  unit: string,
  currency_iso: string,
  mult?: number,
}

export default defineComponent({
  name: "KeyValuationMetricChart",
  data() {
    return {
      chartOpts: chartOpts,
      chartData: {} as {[p: string]: ChartData},
      dataIsAvailable: true,
    }
  },
  props: {
    tabs: {
      type: Object as PropType<{[p: string]: Tab}>,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      company: 'companyDetail/getCompany',
    }),
    get_active_tab() {
      return Object.values(this.tabs).find(t => t.active)
    },
    get_multiplier_value() {
      if (this.tabs.pe.active) return this.chartData.earnings.mult
      if (this.tabs.pb.active) return this.chartData.book.mult
      if (this.tabs.ps.active) return this.chartData.sales.mult
    },
    get_multiplier_name() {
      if (this.tabs.pe.active) return 'PE'
      if (this.tabs.pb.active) return 'PB'
      if (this.tabs.ps.active) return 'PS'
    },
  },
  beforeMount() {
    this.chartData = this.get_data()

    this.chartOpts.series = this.get_series() as any
    this.chartOpts.yAxis = this.get_y_axis() as any
    this.chartOpts.chart.events = {load: this.drawLines}
  },
  watch: {
    tabs: {
      handler() {
        const chart = (this.$refs.keyValuationMetricChart as any).chart
        chart.series[1].visible = false
        chart.series[2].visible = false
        chart.series[3].visible = false

        if (!this.get_active_tab) return null
        chart.series[this.get_active_tab.value].visible = true

        chart.renderSeries()
      },
      deep: true
    }
  },
  methods: {
    get_data(): {[p: string]: ChartData} {
      if (!this.company.reports.length) {
        this.dataIsAvailable = false
        return {}
      } else {
        this.dataIsAvailable = true
      }

      const report = this.company.reports[0]
      const earnings = report.income_net || 0
      const equity = report.equity || 0
      const revenue = report.sales || 0
      const reportUnit = report.scale
      const marketCap = this.get_finance_format_by_unit(this.company.price_data.capitalisation, reportUnit) || 0
      const currency_symbol = this.company.formatting.primaryCurrencySymbol

      return {
        sales: {
          name: 'Sales',
          value: revenue,
          unit: reportUnit,
          currency_iso: currency_symbol,
          mult: Number((revenue/marketCap).toFixed(1)),
        },
        book: {
          name: 'Book',
          value: equity,
          unit: reportUnit,
          currency_iso: currency_symbol,
          mult: Number((equity/marketCap).toFixed(1)),
        },
        earnings: {
          name: 'Earnings',
          value: earnings,
          unit: reportUnit,
          currency_iso: currency_symbol,
          mult: Number((earnings/marketCap).toFixed(1)),
        },
        marketCap: {
          name: 'Market Cap',
          value: marketCap,
          unit: reportUnit,
          currency_iso: currency_symbol
        }
      }
    },
    get_finance_format_by_unit(value: number, unitFormat: string) {
      for (const unit of ["", "t", "M", "B", "T"]) {
        if (Math.abs(value) < 1000 || unit === unitFormat) return Number(value.toFixed(2))
        value /= 1000
      }
      return Number(value.toFixed(2))
    },
    get_series() {
      const data = this.chartData
      if (!data) return null

      return [{
        name: 'Market Cap',
        data: [{
          name: 'Market Cap',
          y: data.marketCap.value,
          color: 'rgb(62, 72, 85)',
          radius: '65%',
          innerRadius: '100%',
          label: `${data.marketCap.currency_iso}${data.marketCap.value}${data.marketCap.unit}`,
          dataLabels: {
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format: '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 36,
          },
        }]
      }, {
        name: 'Earnings',
        visible: true,
        data: [{
          name: 'Earnings',
          y: data.earnings.value,
          color: 'rgb(35, 148, 223)',
          radius: '65%',
          innerRadius: '100%',
          label: `${data.earnings.currency_iso}${data.earnings.value}${data.earnings.unit}`,
          dataLabels: {
            allowOverlap: true,
            // crop: true,
            overflow: 'allow',
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format: '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 0, // 153.5
            y: -184 / 2 - 64
          },
        }]
      }, {
        name: 'Book',
        visible: false,
        data: [{
          name: 'Book',
          y: data.book.value,
          color: 'rgb(35, 148, 223)',
          radius: '65%',
          innerRadius: '100%',
          label: `${data.book.currency_iso}${data.book.value}${data.book.unit}`,
          dataLabels: {
            allowOverlap: true,
            // crop: true,
            overflow: 'allow',
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format: '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 0, // 153.5
            y: -184 / 2 - 64
          },
        }]
      }, {
        name: 'Sales',
        visible: false,
        data: [{
          name: 'Sales',
          y: data.sales.value,
          color: 'rgb(35, 148, 223)',
          radius: '65%',
          innerRadius: '100%',
          label: `${data.sales.currency_iso}${data.sales.value}${data.sales.unit}`,
          dataLabels: {
            allowOverlap: true,
            // crop: true,
            overflow: 'allow',
            align: 'center',
            verticalAlign: 'middle',
            position: 'center',
            borderWidth: 0,
            format: '<tspan class="fundamental-summary-chart__middle-label">{point.name}</tspan><br><tspan class="fundamental-summary-chart__middle-value">{point.label}</tspan>',
            style: {
              fontSize: '12px',
              textAnchor: 'middle',
            },
            x: 0, // 153.5
            y: -184 / 2 - 64
          },
        }]
      }]
    },
    get_y_axis() {
      const data = this.chartData
      if (!data) return  {}

      return {
        min: 0,
        max: data.marketCap.value,
        lineWidth: 0,
        tickPositions: []
      }
    },
    drawLines(event: Event) {
      const chart = event.target as any

      const plotOffsetX = chart.plotBox.x
      const plotOffsetY = chart.plotBox.y
      const lineH = 64
      const lineX = plotOffsetX + chart.series[0].data[0].graphic.pathArray[0][1]
      const lineY = plotOffsetY + chart.series[0].data[0].graphic.pathArray[0][2] - lineH
      const lineW = .5

      chart.renderer.rect(lineX, lineY, lineW, lineH)
        .attr({
          fill: '#2394df',
          zIndex: 10,
        })
        .add()

      chart.renderer.circle()
        .attr({
          cx: lineX,
          cy: lineY,
          fill: '#2394df',
          r: 2.5,
          zIndex: 10,
        })
        .add()
    }
  },
})
</script>

<template>
<div class="detail-key-valuation-metric__chart-wrapper">
  <div class="detail-key-valuation-metric__chart">

    <charts
      :options="chartOpts"
      :constructorType="'chart'"
      ref="keyValuationMetricChart"
    />

    <div class="detail-key-valuation-metric__chart-metric">
      <h4 class="detail-key-valuation-metric__chart-metric-value">{{ get_multiplier_value }}x</h4>
      <span class="detail-key-valuation-metric__chart-metric-text">{{ get_multiplier_name }} Ratio</span>
    </div>

  </div>
</div>
</template>

<style>
.detail-key-valuation-metric__chart-wrapper {
    display: grid;
    height: 280px;
}
.detail-key-valuation-metric__chart {
    display: grid;
    grid-template-columns: auto 200px;
    grid-template-rows: auto;
}
.detail-key-valuation-metric__chart svg {
  width: auto;
  height: auto;
}
.detail-key-valuation-metric__chart-metric {
    display: grid;
    place-content: center start;
}
.detail-key-valuation-metric__chart-metric-value {
    line-height: 1.25;
    font-size: 3.6rem;
    font-weight: normal;
}
.detail-key-valuation-metric__chart-metric-text {
    font-size: 1.6rem;
    font-weight: 500;
    line-height: 1.5;
    color: rgba(255, 255, 255, .7);
}
</style>