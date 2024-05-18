<script lang="ts">
import {defineComponent} from 'vue'
import DetailAnalysisTitle from "@/components/UI/text/DetailAnalysisTitle.vue";
import DetailAnalysisDesc from "@/components/UI/text/DetailAnalysisDesc.vue";
import KeyValuationMetricTabList from "@/components/company_detail/valuation/KeyValuationMetricTabList.vue";
import KeyValuationMetricChart from "@/components/charts/KeyValuationMetricChart.vue";
import KeyValuationMetricTable from "@/components/company_detail/valuation/KeyValuationMetricTable.vue";

export default defineComponent({
  name: "KeyValuationMetric",
  components: {
    KeyValuationMetricTable,
    KeyValuationMetricChart,
    KeyValuationMetricTabList,
    DetailAnalysisDesc,
    DetailAnalysisTitle,
  }
})
</script>

<template>
<section>
  <DetailAnalysisTitle>
    <span>1.2</span>Key Valuation Metric
  </DetailAnalysisTitle>
  <DetailAnalysisDesc>
    Which metric is best to use when looking at relative valuation for SBER?
  </DetailAnalysisDesc>

  <div class="detail__content">
    <div class="detail__content-item detail-key-valuation-metric">

      <KeyValuationMetricTabList/>

      <div class="detail-key-valuation-metric__chart-box">

        <KeyValuationMetricChart/>

        <KeyValuationMetricTable/>

      </div>

    </div>
  </div>
</section>
</template>

<style scoped>
.detail-key-valuation-metric {
  display: grid;
  grid-template-columns: 35% auto;
  gap: 20px;
}
.detail-key-valuation-metric__chart-box {
  display: grid;
}
</style>