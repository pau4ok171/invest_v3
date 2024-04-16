<template>
  <div>
    <div class="price-history-chart">
      <charts
        :constructorType="'stockChart'"
        :options="this.chartOpts"
      />
    </div>
  </div>
</template>

<script lang="ts">
  import chartOpts from "@/components/charts/smallPriceChartOpts";
  import store from "@/store";

  export default {
    data() {
      return {
        chartOpts: chartOpts
      }
    },
    mounted() {
      this.chartOpts.series[0].data = store.getters["companyDetail/companyPriceData"]
    },
  }
</script>

<style>
  .price-history-chart {
    display: flex;
    width: 300px;
    max-width: 100%;
    height: 40px;
    line-height: 1.5;
  }
  .price-history-chart svg {
    width: 100%;
    height: 100%;
    fill: none;
  }
</style>