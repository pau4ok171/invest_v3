<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/priceChartOpts";
import { DateTime } from 'luxon';
import {mapActions, mapGetters} from "vuex";
import FetchingData from "@/components/charts/FetchingData.vue";
import BaseButton from "@/components/UI/base/components/BaseButton/BaseButton.vue";

interface Tab {
  value: string,
  min: DateTime,
}

export default defineComponent({
  name: "PriceChart",
  components: {BaseButton, FetchingData},
  data() {
    return {
      chartOpts: chartOpts,
      currentPeriod: "1Y",
      tablist: {
        M1: {value: '1M', min: DateTime.now().minus({months: 1})},
        M3: {value: '3M', min: DateTime.now().minus({months: 3})},
        Y1: {value: '1Y', min: DateTime.now().minus({years: 1})},
        Y3: {value: '3Y', min: DateTime.now().minus({years: 3})},
        Y5: {value: '5Y', min: DateTime.now().minus({years: 5})},
        MAX: {value: 'Max', min: DateTime.now().minus({years: 50})},
      },
      chartDataUpdateInterval: 0,
    }
  },
  watch: {
    priceData() {
      this.chartOpts.series[0].data = this.priceData
    },
  },
  methods: {
    ...mapActions({
      fetchPriceData: 'companyDetail/fetchPriceData',
    }),
    changeZoom(tab: Tab) {
      this.currentPeriod = tab.value
      const priceChart = this.$refs.priceChart as any
      const chart = priceChart.chart
      const  chartMax = chart.xAxis[1].max || DateTime.now().ts
      chart.xAxis[0].setExtremes(tab.min.ts, chartMax)
    },
    afterCreate(chart: any) {
      this.chartOpts.series[0].data = this.priceData
      const  chartMax = chart.xAxis[1].max || DateTime.now().ts
      chart.xAxis[0].setExtremes(this.tablist['Y1'].min.ts, chartMax)
      this.setChartDataUpdateInterval()
    },
    setChartDataUpdateInterval() {
      const company_slug = this.$route.params.company_slug as String
      this.chartDataUpdateInterval = setInterval(() => this.fetchPriceData(company_slug), 1000*60*5) // 5min
    }
  },
  computed: {
    ...mapGetters({
      priceData: 'companyDetail/companyPriceData',
      pageIsReady: 'companyDetail/getPageIsReady',
    }),
  },
  unmounted() {
    if (this.chartDataUpdateInterval){
      window.clearInterval(this.chartDataUpdateInterval)
    }
  },
})
</script>

<template>
<div class="detail-price-chart__wrapper">
  <FetchingData v-if="!pageIsReady"/>
  <template v-else>
    <div role="tablist" class="detail-price-chart__tablist">
      <base-button
        v-for="tab in tablist"
        :key="tab.value"
        :text="tab.value"
        variant="text"
        :disabled="tab.value === currentPeriod"
        @click="changeZoom(tab)"
      />
    </div>
    <div class="detail-price-chart">
      <charts
        ref="priceChart"
        :constructorType="'stockChart'"
        :options="chartOpts"
        :callback="afterCreate"
      />
    </div>
  </template>
</div>
</template>

<style>
.detail-price-chart__wrapper {
  height: 430px;
}
.detail-price-chart__tablist {
  display: grid;
  grid-template-columns: repeat(6, auto);
}
.detail-price-chart svg {
  width: 100%;
  height: 100%;
  fill: none;
}
.detail-price-chart .highcharts-button-box {
  overflow: visible;
  font: inherit;
  -webkit-font-smoothing: inherit;
  letter-spacing: inherit;
  background-color: transparent;
  cursor: pointer;
  position: relative;
  display: block;
  width: 100%;
  height: auto;
  border-top: 1px solid transparent;
  border-left: 1px solid transparent;
  border-right: 1px solid transparent;
  padding: 4px;

  border-radius: 4px;
}
.detail-price-chart .highcharts-button > text, #price-history-chart .highcharts-label > text, #price-history-chart .highcharts-tooltip-box > text {
  font-size: 1.3rem!important;
  line-height: 1.5!important;
  font-weight: 500!important;
  fill: rgba(255, 255, 255, 0.3)!important;
}
.detail-price-chart .highcharts-button-pressed > text {
  fill: var(--blue)!important;
}
.detail-price-chart .highcharts-button-hover > text {
  fill: var(--blue)!important;
}
.detail-price-chart .price-history-chart-point-box__date {
  fill: rgba(255, 255, 255, 0.7);
  line-height: 1.4;
}
.detail-price-chart .price-history-chart-point-box__price {
  fill: #fff;
  font-weight: 900;
}
.detail-price-chart .highcharts-navigator-mask-inside {
  cursor: grab!important;
  rx: 4;
  ry: 4;
  stroke-width: 1;
  stroke: rgb(35, 148, 223);
}
.detail-price-chart .highcharts-navigator-mask-outside {
  fill: rgba(21, 27, 36, .3);
  rx: 4;
  ry: 4;
}
</style>