<script lang="ts">
import chartOpts from "@/components/charts/smallPriceChartOpts";
import {defineComponent} from "vue";
import {mapGetters} from "vuex";

export default defineComponent({
  data() {
    return {
      chartOpts: chartOpts
    }
  },
  computed: {
    ...mapGetters({
      companyPriceData: 'companyDetail/companyPriceData',
    }),
  },
  watch: {
    companyPriceData() {
      this.chartOpts.series[0].data = this.companyPriceData
    },
  },
  mounted() {
    this.chartOpts.series[0].data = this.companyPriceData
  },
})
</script>

<template>
<div>
  <div class="price-history-chart">
    <charts
      :constructorType="'stockChart'"
      :options="chartOpts"
    />
  </div>
</div>
</template>

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