<script lang="ts">
import {defineComponent} from 'vue'
import {chartOpts} from "@/components/charts/priceChartOpts";
import store from "@/store";

export default defineComponent({
  name: "PriceChart",
  data() {
    return {
      chartOpts: chartOpts
    }
  },
  mounted() {
    this.chartOpts.series[0].data = store.getters["companyDetail/companyPriceData"]
  }
})
</script>

<template>
  <div class="detail-price-chart">
    <charts
      :constructorType="'stockChart'"
      :options="chartOpts"
    />
  </div>
</template>

<style>
  .detail-price-chart {
    margin-bottom: 24px;
    margin-top: 24px;
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
</style>