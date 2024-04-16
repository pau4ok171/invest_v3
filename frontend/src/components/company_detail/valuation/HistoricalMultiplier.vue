<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import HistoricalMultiplierChart from "@/components/charts/HistoricalMultiplierChart.vue";
import HistoricalMultiplierTabList from "@/components/company_detail/valuation/HistoricalMultiplierTabList.vue";

export default defineComponent({
  name: "HistoricalMultiplier",
  components: {HistoricalMultiplierTabList, HistoricalMultiplierChart, DetailAnalysisDesc, DetailAnalysisTitle}
})
</script>

<template>
  <section>
    <DetailAnalysisTitle>
      <span>1.4</span>Historical Price to Earnings Ratio
    </DetailAnalysisTitle>

    <DetailAnalysisDesc>
      Historical Price to Earnings Ratio compares a stock's price to its earnings over time. Higher ratios indicate that investors are willing to pay more for the stock.
    </DetailAnalysisDesc>

    <div class="detail__content">
      <div class="detail__content-item detail-historical-multiplier-chart__wrapper">

        <HistoricalMultiplierTabList/>

        <HistoricalMultiplierChart/>

      </div>
    </div>
  </section>
</template>

<style scoped>
  .detail-historical-multiplier-chart__wrapper {
    height: 454px;
  }
</style>